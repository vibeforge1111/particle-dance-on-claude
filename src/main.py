"""
GestureFlow: Hand-Controlled ASMR Particle Simulator
Main application entry point.
"""
import pygame
import sys
import time

from particle import ParticleSystem
from gesture import GestureDetector, MouseGestureDetector, Gesture, GestureState, MEDIAPIPE_AVAILABLE, create_gesture_detector
from audio import AudioSystem
from renderer import ParticleRenderer

# Only import cv2 if mediapipe is available
if MEDIAPIPE_AVAILABLE:
    import cv2


class GestureFlow:
    """Main application class."""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Get display info for fullscreen
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h

        # Start FULLSCREEN by default (per PRD)
        self.fullscreen = True
        self.window_width = 1280
        self.window_height = 720

        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height),
                pygame.FULLSCREEN
            )
            current_width, current_height = self.screen_width, self.screen_height
        else:
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.RESIZABLE
            )
            current_width, current_height = self.window_width, self.window_height

        pygame.display.set_caption("GestureFlow - ASMR Particle Simulator")

        # Initialize clock
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        self.running = True

        # Initialize systems
        self.particle_system = ParticleSystem(
            max_particles=2000,
            width=current_width,
            height=current_height
        )

        # Create gesture detector (MediaPipe or Mouse fallback)
        self.gesture_detector, self.using_camera = create_gesture_detector(use_camera=True)
        self.gesture_detector.set_screen_size(current_width, current_height)

        # Multi-hand gesture state
        self.gesture_state = GestureState()

        self.audio_system = AudioSystem()
        self.renderer = ParticleRenderer(self.screen)

        # Initialize webcam if using camera mode
        self.camera = None
        if self.using_camera:
            self._init_camera()

        # UI State
        self.show_help = False
        self.show_settings = False
        self.settings = {
            'volume': 0.7,
            'particle_count': 500,
            'glow': True,
            'trails': True,
            'audio': True,
            'binaural': False,
        }

        # Interaction state
        self.last_spawn_time = 0
        self.spawn_cooldown = 0.3  # seconds
        self.last_gesture_sounds = {}
        self.last_gravity_change = 0
        self.last_two_hands_sound = 0

        # Performance
        self.frame_times = []
        self.fps = 60

        # Key states for mouse mode
        self.keys_pressed = {}

        # Print mode info
        if self.using_camera:
            print("Running in CAMERA mode - use hand gestures to control particles")
        else:
            print("Running in MOUSE mode - use mouse buttons to control particles")
            print("  Left click: Attract | Right click: Repel | Middle click: Spawn")
            print("  Left+Right: Explode | Q/E: Vortex | W/S: Gravity Up/Down")

    def _init_camera(self):
        """Initialize webcam."""
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("Warning: Could not open webcam. Falling back to mouse mode.")
            self.camera = None
            self.gesture_detector = MouseGestureDetector()
            self.using_camera = False
        else:
            # Set camera resolution
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height),
                pygame.FULLSCREEN
            )
            width, height = self.screen_width, self.screen_height
        else:
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.RESIZABLE
            )
            width, height = self.window_width, self.window_height

        # Update systems for new size
        self.particle_system.resize(width, height)
        self.gesture_detector.set_screen_size(width, height)
        self.renderer = ParticleRenderer(self.screen)

    def _handle_resize(self, width, height):
        """Handle window resize."""
        self.window_width = width
        self.window_height = height
        self.particle_system.resize(width, height)
        self.gesture_detector.set_screen_size(width, height)
        self.renderer.resize(width, height)

    def _process_gestures(self, hands):
        """Process detected gestures and apply to particle system."""
        gesture_names = []
        current_time = time.time()

        # Update multi-hand gesture state
        self.gesture_state.update(hands)

        # Check for exit gesture (both fists for 3 seconds)
        if self.gesture_state.should_exit():
            print("\nExit gesture detected (both fists held)")
            self.running = False
            return gesture_names

        # Process two-hands-close gesture (merge particles between hands)
        if self.gesture_state.two_hands_close and len(hands) >= 2:
            h1, h2 = hands[0], hands[1]
            center = self.gesture_state.get_hands_center(hands)
            if center:
                # Attract particles between hands
                affected = self.particle_system.attract_between_points(
                    h1.palm_center[0], h1.palm_center[1],
                    h2.palm_center[0], h2.palm_center[1],
                    self.gesture_state.hands_distance * 0.8,
                    1.5
                )
                if affected > 0 and current_time - self.last_two_hands_sound > 1.0:
                    self.audio_system.play_resonant_tone()
                    self.last_two_hands_sound = current_time
                gesture_names.append("TWO_HANDS_MERGE")

        for hand in hands:
            if not hand.is_active:
                continue

            x, y = hand.palm_center
            gesture = hand.gesture
            gesture_names.append(gesture.name)

            # Gesture-specific interactions
            if gesture == Gesture.OPEN_PALM:
                # Attract particles toward hand
                affected, touching = self.particle_system.apply_force(x, y, 200, 0.8, repel=False)
                if touching > 0 and self._should_play_sound('touch', 0.1):
                    self.audio_system.play_touch_pop(touching // 10 + 1)
                if affected > 0 and self._should_play_sound('attract', 0.5):
                    if affected > 50:
                        self.audio_system.play_pop(0.3)

            elif gesture == Gesture.FIST:
                # Repel particles away from hand
                affected, touching = self.particle_system.apply_force(x, y, 250, 1.2, repel=True)
                if touching > 0 and self._should_play_sound('touch', 0.1):
                    self.audio_system.play_touch_pop(touching // 10 + 1)
                if affected > 0 and self._should_play_sound('repel', 0.3):
                    self.audio_system.play_whoosh(min(1.0, affected / 100))

            elif gesture == Gesture.PINCH:
                # Spawn new particle cluster
                if current_time - self.last_spawn_time > self.spawn_cooldown:
                    spawned = self.particle_system.spawn_cluster(x, y, count=15, spread=20)
                    if spawned > 0:
                        self.audio_system.play_spawn()
                        self.last_spawn_time = current_time

            elif gesture == Gesture.SPREAD:
                # Explode particles outward
                affected = self.particle_system.explode_from_point(x, y, 300, 3.0)
                if affected > 0 and self._should_play_sound('explode', 0.5):
                    self.audio_system.play_whoosh(1.0)
                    self.audio_system.play_pop(0.8)

            elif gesture == Gesture.WAVE:
                # Apply directional flow
                vx, vy = hand.palm_velocity
                self.particle_system.apply_directional_flow(vx * 0.1, vy * 0.1, 0.5)
                if self._should_play_sound('wave', 0.3):
                    self.audio_system.play_whoosh(0.5)

            elif gesture == Gesture.PALM_UP:
                # Change gravity to up
                if current_time - self.last_gravity_change > 0.5:
                    self.particle_system.set_gravity_direction(-1)
                    self.audio_system.play_gravity_shift()
                    self.last_gravity_change = current_time

            elif gesture == Gesture.PALM_DOWN:
                # Change gravity to down
                if current_time - self.last_gravity_change > 0.5:
                    self.particle_system.set_gravity_direction(1)
                    self.audio_system.play_gravity_shift()
                    self.last_gravity_change = current_time

            # Check for rotation/vortex
            if abs(hand.rotation_angle) > 0.1:
                affected = self.particle_system.apply_vortex(x, y, 180, hand.rotation_angle * 2)
                if affected > 0 and self._should_play_sound('vortex', 1.0):
                    self.audio_system.play_swirl()

        # Check for particle merges and play sound
        merge_count = self.particle_system.get_merge_count()
        if merge_count > 0 and self._should_play_sound('merge', 0.3):
            self.audio_system.play_merge()

        return gesture_names

    def _should_play_sound(self, sound_type, cooldown):
        """Check if enough time has passed to play a sound again."""
        current_time = time.time()
        last_time = self.last_gesture_sounds.get(sound_type, 0)
        if current_time - last_time > cooldown:
            self.last_gesture_sounds[sound_type] = current_time
            return True
        return False

    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self._handle_resize(event.w, event.h)

            elif event.type == pygame.KEYDOWN:
                self.keys_pressed[event.key] = True
                self._handle_keydown(event.key)

            elif event.type == pygame.KEYUP:
                self.keys_pressed[event.key] = False

    def _handle_keydown(self, key):
        """Handle keyboard input."""
        if key == pygame.K_ESCAPE:
            self.running = False

        elif key == pygame.K_f:
            self._toggle_fullscreen()

        elif key == pygame.K_h:
            self.show_help = not self.show_help
            self.show_settings = False

        elif key == pygame.K_s and not self.keys_pressed.get(pygame.K_LCTRL, False):
            self.show_settings = not self.show_settings
            self.show_help = False

        elif key == pygame.K_g:
            self.settings['glow'] = not self.settings['glow']

        elif key == pygame.K_t:
            self.settings['trails'] = not self.settings['trails']

        elif key == pygame.K_a:
            self.settings['audio'] = not self.settings['audio']
            if self.settings['audio']:
                self.audio_system.start_ambient()
            else:
                self.audio_system.stop_ambient()

        elif key == pygame.K_b:
            # Toggle binaural beats
            self.settings['binaural'] = self.audio_system.toggle_binaural()

        elif key == pygame.K_EQUALS or key == pygame.K_PLUS:
            # Spawn more particles
            import random
            for _ in range(50):
                self.particle_system.spawn_particle(
                    random.uniform(100, self.screen.get_width() - 100),
                    random.uniform(100, self.screen.get_height() - 100)
                )

        elif key == pygame.K_MINUS:
            # Reduce particles (just stop spawning, they'll naturally decay)
            pass

        # Volume controls (1-9)
        elif pygame.K_1 <= key <= pygame.K_9:
            volume = (key - pygame.K_1 + 1) / 9.0
            self.settings['volume'] = volume
            self.audio_system.set_master_volume(volume)

    def _update_fps(self, dt):
        """Track FPS."""
        self.frame_times.append(dt)
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 60

    def run(self):
        """Main application loop."""
        print("\nStarting GestureFlow...")
        print("Controls: H=Help, F=Fullscreen, S=Settings, B=Binaural, ESC=Exit")
        print("Exit: Hold both fists for 3 seconds\n")

        # Start ambient audio
        if self.settings['audio']:
            self.audio_system.start_ambient()

        while self.running:
            dt = self.clock.tick(self.target_fps) / 1000.0
            self._update_fps(dt)

            # Handle events
            self._handle_events()

            # Get gesture input
            gesture_names = []
            hands = []

            if self.using_camera and self.camera is not None:
                # Camera mode - process video frame
                ret, frame = self.camera.read()
                if ret:
                    hands = self.gesture_detector.process_frame(frame)
                    gesture_names = self._process_gestures(hands)
            else:
                # Mouse mode
                mouse_pos = pygame.mouse.get_pos()
                mouse_buttons = pygame.mouse.get_pressed()
                hands = self.gesture_detector.update_from_mouse(mouse_pos, mouse_buttons, self.keys_pressed)
                gesture_names = self._process_gestures(hands)

            # Update particle physics
            self.particle_system.update(dt * 60)  # Normalize to 60fps

            # Render
            self.renderer.render_background()

            if self.settings['trails']:
                self.renderer.render_trails()

            # Get particle data and render
            positions, colors, sizes, alphas, is_bubble = self.particle_system.get_particle_data()
            self.renderer.render_particles(positions, colors, sizes, alphas)

            # Render hand indicators
            for hand in hands:
                self.renderer.render_hand_indicator(hand, hand.gesture.name if hand.is_active else "")

            # Render UI
            if self.show_settings:
                self.renderer.render_settings(self.settings)
            else:
                self.renderer.render_ui_overlay(
                    self.show_help,
                    self.particle_system.count,
                    self.fps,
                    gesture_names
                )

            # Update display
            pygame.display.flip()

        # Cleanup
        self._cleanup()

    def _cleanup(self):
        """Clean up resources."""
        print("\nShutting down...")

        if self.camera is not None:
            self.camera.release()

        self.gesture_detector.release()
        self.audio_system.cleanup()
        pygame.quit()


def main():
    """Entry point."""
    app = GestureFlow()
    app.run()


if __name__ == "__main__":
    main()

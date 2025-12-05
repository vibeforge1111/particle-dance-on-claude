"""
Particle renderer with glow/bloom effects.
"""
import pygame
import numpy as np
import math
import colorsys


class ParticleRenderer:
    """Renders particles with glow effects and trails."""

    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Background colors from PRD
        self.bg_colors = [
            (13, 2, 33),    # Deep Purple-Black #0D0221
            (10, 22, 40),   # Deep Blue-Black #0A1628
        ]
        self.bg_index = 0
        self.bg_transition = 0.0
        self.bg_direction = 1

        # Create surfaces for effects
        self.glow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.trail_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Pre-render glow textures for different sizes
        self.glow_textures = {}
        self._create_glow_textures()

        # Trail fade
        self.trail_fade = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.trail_fade.fill((0, 0, 0, 15))  # Slight fade per frame

    def _create_glow_textures(self):
        """Pre-render glow textures for performance."""
        for size in range(4, 25, 2):
            glow_size = size * 4
            texture = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)

            center = glow_size
            for r in range(glow_size, 0, -1):
                alpha = int(255 * (1 - r / glow_size) ** 2 * 0.5)
                pygame.draw.circle(texture, (255, 255, 255, alpha), (center, center), r)

            self.glow_textures[size] = texture

    def resize(self, width, height):
        """Handle window resize."""
        self.width = width
        self.height = height
        self.glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.trail_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.trail_fade = pygame.Surface((width, height), pygame.SRCALPHA)
        self.trail_fade.fill((0, 0, 0, 15))

    def _hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB."""
        r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))

    def _interpolate_color(self, c1, c2, t):
        """Interpolate between two colors."""
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    def render_background(self):
        """Render breathing background."""
        # Slowly transition between background colors
        self.bg_transition += 0.001 * self.bg_direction
        if self.bg_transition >= 1.0:
            self.bg_transition = 1.0
            self.bg_direction = -1
        elif self.bg_transition <= 0.0:
            self.bg_transition = 0.0
            self.bg_direction = 1

        color = self._interpolate_color(self.bg_colors[0], self.bg_colors[1], self.bg_transition)
        self.screen.fill(color)

    def render_trails(self):
        """Render fading trails."""
        # Apply fade to trail surface
        self.trail_surface.blit(self.trail_fade, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.screen.blit(self.trail_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    def render_particles(self, positions, colors, sizes, alphas):
        """Render particles with glow effect."""
        if len(positions) == 0:
            return

        # Clear glow surface
        self.glow_surface.fill((0, 0, 0, 0))

        for i in range(len(positions)):
            x, y = int(positions[i][0]), int(positions[i][1])
            h, s, v = colors[i]
            size = max(4, int(sizes[i]))
            alpha = alphas[i]

            # Convert HSV to RGB
            rgb = self._hsv_to_rgb(h, s, v)

            # Draw to trail surface (small dot)
            trail_alpha = int(alpha * 100)
            trail_color = (*rgb, trail_alpha)
            pygame.draw.circle(self.trail_surface, trail_color, (x, y), max(2, size // 3))

            # Get closest pre-rendered glow texture
            texture_size = min(24, max(4, (size // 2) * 2))
            if texture_size in self.glow_textures:
                glow = self.glow_textures[texture_size].copy()

                # Tint the glow with particle color
                glow_colored = pygame.Surface(glow.get_size(), pygame.SRCALPHA)
                glow_colored.fill((*rgb, 0))
                glow_colored.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                # Scale alpha
                glow_colored.set_alpha(int(alpha * 200))

                # Blit to glow surface
                glow_rect = glow_colored.get_rect(center=(x, y))
                self.glow_surface.blit(glow_colored, glow_rect, special_flags=pygame.BLEND_ADD)

            # Draw core particle
            pygame.draw.circle(self.screen, rgb, (x, y), size)

            # Draw bright center
            bright_rgb = tuple(min(255, c + 50) for c in rgb)
            pygame.draw.circle(self.screen, bright_rgb, (x, y), max(1, size // 2))

        # Apply glow layer
        self.screen.blit(self.glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    def render_hand_indicator(self, hand, gesture_name):
        """Render subtle hand position indicator."""
        if not hand.is_active:
            return

        x, y = int(hand.palm_center[0]), int(hand.palm_center[1])

        # Outer glow ring
        for r in range(60, 20, -10):
            alpha = int((60 - r) * 2)
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, alpha), (r, r), r, 2)
            self.screen.blit(s, (x - r, y - r))

        # Inner dot
        pygame.draw.circle(self.screen, (255, 255, 255, 100), (x, y), 5)

    def render_ui_overlay(self, show_help, particle_count, fps, gesture_names):
        """Render minimal UI overlay."""
        if not show_help:
            # Just show FPS and particle count in corner
            font = pygame.font.Font(None, 24)
            text = f"Particles: {particle_count} | FPS: {int(fps)}"
            text_surface = font.render(text, True, (100, 100, 100))
            self.screen.blit(text_surface, (10, 10))
            return

        # Full help overlay
        font = pygame.font.Font(None, 28)
        font_large = pygame.font.Font(None, 36)

        # Semi-transparent overlay
        overlay = pygame.Surface((400, 350), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (self.width // 2 - 200, self.height // 2 - 175))

        # Title
        title = font_large.render("GestureFlow Controls", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 2 - 155))

        # Gesture list
        gestures = [
            ("Open Palm", "Attract particles"),
            ("Closed Fist", "Repel particles"),
            ("Pinch", "Spawn new particles"),
            ("Spread Fingers", "Explode particles"),
            ("Wave Hand", "Create flow current"),
        ]

        y_offset = self.height // 2 - 100
        for gesture, action in gestures:
            text = font.render(f"{gesture}: {action}", True, (200, 200, 200))
            self.screen.blit(text, (self.width // 2 - 180, y_offset))
            y_offset += 35

        # Keyboard controls
        y_offset += 20
        keys = [
            ("H", "Toggle help"),
            ("F", "Toggle fullscreen"),
            ("S", "Settings"),
            ("ESC", "Exit"),
        ]

        for key, action in keys:
            text = font.render(f"[{key}] {action}", True, (150, 150, 150))
            self.screen.blit(text, (self.width // 2 - 180, y_offset))
            y_offset += 30

        # Current gestures
        if gesture_names:
            gesture_text = " | ".join(gesture_names)
            text = font.render(f"Detected: {gesture_text}", True, (100, 255, 100))
            self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 + 150))

    def render_settings(self, settings):
        """Render settings panel."""
        font = pygame.font.Font(None, 28)
        font_large = pygame.font.Font(None, 36)

        # Semi-transparent overlay
        overlay = pygame.Surface((400, 350), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (self.width // 2 - 200, self.height // 2 - 175))

        # Title
        title = font_large.render("Settings", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 2 - 155))

        y_offset = self.height // 2 - 100

        # Settings items
        items = [
            ("Volume", f"{int(settings.get('volume', 0.7) * 100)}%", "[1-9]"),
            ("Particles", f"{settings.get('particle_count', 500)}", "[+/-]"),
            ("Glow", "On" if settings.get('glow', True) else "Off", "[G]"),
            ("Trails", "On" if settings.get('trails', True) else "Off", "[T]"),
            ("Audio", "On" if settings.get('audio', True) else "Off", "[A]"),
            ("Binaural", "On" if settings.get('binaural', False) else "Off", "[B]"),
        ]

        for label, value, key in items:
            text = font.render(f"{label}: {value}  {key}", True, (200, 200, 200))
            self.screen.blit(text, (self.width // 2 - 150, y_offset))
            y_offset += 35

        # Close hint
        hint = font.render("Press [S] to close", True, (100, 100, 100))
        self.screen.blit(hint, (self.width // 2 - hint.get_width() // 2, self.height // 2 + 140))

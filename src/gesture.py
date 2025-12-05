"""
Hand gesture detection using MediaPipe (with fallback to mouse control).
"""
import numpy as np
from enum import Enum, auto
from collections import deque
import math

# Try to import MediaPipe, fall back to mouse mode if unavailable
MEDIAPIPE_AVAILABLE = False
try:
    import cv2
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    print("MediaPipe not available. Running in mouse control mode.")
    print("For hand tracking, install with: pip install mediapipe opencv-python")
    print("Note: MediaPipe requires Python 3.8-3.11")


class Gesture(Enum):
    """Gesture types from PRD."""
    NONE = auto()
    OPEN_PALM = auto()      # Attract particles
    FIST = auto()           # Repel particles
    PINCH = auto()          # Spawn particles
    SPREAD = auto()         # Explode particles
    WAVE = auto()           # Create flow current
    ROTATION = auto()       # Vortex swirl


class Hand:
    """Represents a tracked hand with gesture state."""

    def __init__(self):
        self.landmarks = None
        self.gesture = Gesture.NONE
        self.palm_center = (0, 0)
        self.palm_velocity = (0, 0)
        self.gesture_confidence = 0.0
        self.rotation_angle = 0.0
        self.is_active = False

        # Smoothing
        self.position_history = deque(maxlen=5)
        self.gesture_history = deque(maxlen=8)


class MouseGestureDetector:
    """Fallback gesture detector using mouse input."""

    def __init__(self):
        self.hand = Hand()
        self.screen_width = 1920
        self.screen_height = 1080
        self.prev_pos = (0, 0)

    def set_screen_size(self, width, height):
        """Set screen size for coordinate mapping."""
        self.screen_width = width
        self.screen_height = height

    def update_from_mouse(self, mouse_pos, mouse_buttons, keys_pressed):
        """
        Update gesture based on mouse input.

        Controls:
        - Move mouse: hand position
        - Left click: attract (open palm)
        - Right click: repel (fist)
        - Middle click: spawn (pinch)
        - Left + Right: explode (spread)
        - Scroll or fast movement: wave
        """
        import pygame

        self.hand.is_active = True
        self.hand.palm_center = mouse_pos

        # Calculate velocity
        self.hand.position_history.append(mouse_pos)
        if len(self.hand.position_history) >= 2:
            prev = self.hand.position_history[-2]
            curr = self.hand.position_history[-1]
            self.hand.palm_velocity = (curr[0] - prev[0], curr[1] - prev[1])

        # Check velocity for wave
        speed = math.sqrt(self.hand.palm_velocity[0]**2 + self.hand.palm_velocity[1]**2)

        # Determine gesture from mouse buttons
        left, middle, right = mouse_buttons

        if left and right:
            self.hand.gesture = Gesture.SPREAD
        elif middle:
            self.hand.gesture = Gesture.PINCH
        elif right:
            self.hand.gesture = Gesture.FIST
        elif left:
            self.hand.gesture = Gesture.OPEN_PALM
        elif speed > 20:
            self.hand.gesture = Gesture.WAVE
        else:
            self.hand.gesture = Gesture.NONE

        # Check for rotation (using Q/E keys)
        if keys_pressed.get(pygame.K_q, False):
            self.hand.rotation_angle = 0.15
        elif keys_pressed.get(pygame.K_e, False):
            self.hand.rotation_angle = -0.15
        else:
            self.hand.rotation_angle = 0

        return [self.hand] if self.hand.gesture != Gesture.NONE or any(mouse_buttons) else []

    def release(self):
        """Clean up (no-op for mouse mode)."""
        pass


class GestureDetector:
    """Detects hand gestures using MediaPipe."""

    # Thresholds
    PINCH_THRESHOLD = 0.06
    SPREAD_THRESHOLD = 0.25
    FIST_THRESHOLD = 0.08
    WAVE_VELOCITY_THRESHOLD = 15
    ROTATION_THRESHOLD = 0.3

    def __init__(self, max_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError("MediaPipe not available")

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

        self.tracked_hands = [Hand(), Hand()]
        self.frame_width = 640
        self.frame_height = 480
        self.screen_width = 1920
        self.screen_height = 1080

        # Previous frame landmarks for velocity calculation
        self.prev_landmarks = [None, None]
        self.prev_rotation = [0.0, 0.0]

    def set_screen_size(self, width, height):
        """Set the target screen size for coordinate mapping."""
        self.screen_width = width
        self.screen_height = height

    def process_frame(self, frame):
        """Process a camera frame and detect gestures."""
        if frame is None:
            return []

        self.frame_height, self.frame_width = frame.shape[:2]

        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        # Reset hand activity
        for hand in self.tracked_hands:
            hand.is_active = False

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                if idx >= 2:
                    break

                hand = self.tracked_hands[idx]
                hand.is_active = True
                hand.landmarks = hand_landmarks.landmark

                # Calculate palm center (landmark 9 - middle finger base)
                palm_landmark = hand_landmarks.landmark[9]
                raw_x = palm_landmark.x * self.frame_width
                raw_y = palm_landmark.y * self.frame_height

                # Mirror the x-coordinate (webcam is mirrored)
                raw_x = self.frame_width - raw_x

                # Map to screen coordinates
                screen_x = (raw_x / self.frame_width) * self.screen_width
                screen_y = (raw_y / self.frame_height) * self.screen_height

                # Smooth position
                hand.position_history.append((screen_x, screen_y))
                if len(hand.position_history) > 0:
                    avg_x = sum(p[0] for p in hand.position_history) / len(hand.position_history)
                    avg_y = sum(p[1] for p in hand.position_history) / len(hand.position_history)
                    hand.palm_center = (avg_x, avg_y)

                # Calculate velocity
                if len(hand.position_history) >= 2:
                    prev = hand.position_history[-2]
                    curr = hand.position_history[-1]
                    hand.palm_velocity = (curr[0] - prev[0], curr[1] - prev[1])

                # Detect gesture
                gesture = self._detect_gesture(hand_landmarks.landmark, idx)
                hand.gesture_history.append(gesture)

                # Use most common recent gesture for stability
                if len(hand.gesture_history) > 0:
                    gesture_counts = {}
                    for g in hand.gesture_history:
                        gesture_counts[g] = gesture_counts.get(g, 0) + 1
                    hand.gesture = max(gesture_counts.keys(), key=lambda g: gesture_counts[g])

                # Calculate rotation angle for vortex
                hand.rotation_angle = self._calculate_rotation(hand_landmarks.landmark, idx)

        return [h for h in self.tracked_hands if h.is_active]

    def _detect_gesture(self, landmarks, hand_idx):
        """Detect gesture from hand landmarks."""
        # Key landmark indices
        THUMB_TIP = 4
        INDEX_TIP = 8
        MIDDLE_TIP = 12
        RING_TIP = 16
        PINKY_TIP = 20
        WRIST = 0
        INDEX_MCP = 5
        MIDDLE_MCP = 9
        RING_MCP = 13
        PINKY_MCP = 17

        # Get landmark positions
        thumb_tip = landmarks[THUMB_TIP]
        index_tip = landmarks[INDEX_TIP]
        middle_tip = landmarks[MIDDLE_TIP]
        ring_tip = landmarks[RING_TIP]
        pinky_tip = landmarks[PINKY_TIP]
        wrist = landmarks[WRIST]
        palm = landmarks[MIDDLE_MCP]

        # Calculate hand scale (wrist to middle finger base)
        hand_scale = self._distance(wrist, palm)
        if hand_scale < 0.01:
            return Gesture.NONE

        # Pinch detection (thumb tip to index tip)
        pinch_dist = self._distance(thumb_tip, index_tip) / hand_scale
        if pinch_dist < self.PINCH_THRESHOLD:
            return Gesture.PINCH

        # Count extended fingers
        fingers_extended = self._count_extended_fingers(landmarks)

        # Fist detection (no fingers extended)
        if fingers_extended == 0:
            return Gesture.FIST

        # Spread fingers detection (all extended and wide apart)
        if fingers_extended >= 4:
            spread = self._finger_spread(landmarks) / hand_scale
            if spread > self.SPREAD_THRESHOLD:
                return Gesture.SPREAD
            return Gesture.OPEN_PALM

        # Wave detection (based on velocity, handled separately)
        if self.tracked_hands[hand_idx].is_active:
            vel = self.tracked_hands[hand_idx].palm_velocity
            speed = math.sqrt(vel[0]**2 + vel[1]**2)
            if speed > self.WAVE_VELOCITY_THRESHOLD:
                return Gesture.WAVE

        return Gesture.OPEN_PALM if fingers_extended >= 3 else Gesture.NONE

    def _count_extended_fingers(self, landmarks):
        """Count how many fingers are extended."""
        count = 0

        # Finger tip and pip (proximal interphalangeal) indices
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]

        for tip_idx, pip_idx in zip(finger_tips, finger_pips):
            # Finger is extended if tip is higher (lower y) than pip
            if landmarks[tip_idx].y < landmarks[pip_idx].y:
                count += 1

        # Thumb: check if tip is to the side of the ip joint
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]

        # Check thumb extension based on x distance from mcp
        if abs(thumb_tip.x - thumb_mcp.x) > abs(thumb_ip.x - thumb_mcp.x):
            count += 1

        return count

    def _finger_spread(self, landmarks):
        """Calculate how spread apart the fingers are."""
        # Distance between index and pinky tips
        index_tip = landmarks[8]
        pinky_tip = landmarks[20]
        return self._distance(index_tip, pinky_tip)

    def _distance(self, p1, p2):
        """Calculate Euclidean distance between two landmarks."""
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

    def _calculate_rotation(self, landmarks, hand_idx):
        """Calculate hand rotation angle for vortex gesture."""
        # Use wrist to middle finger direction
        wrist = landmarks[0]
        middle_mcp = landmarks[9]

        angle = math.atan2(middle_mcp.y - wrist.y, middle_mcp.x - wrist.x)

        # Calculate rotation delta
        prev_angle = self.prev_rotation[hand_idx]
        self.prev_rotation[hand_idx] = angle

        delta = angle - prev_angle
        # Normalize to [-pi, pi]
        while delta > math.pi:
            delta -= 2 * math.pi
        while delta < -math.pi:
            delta += 2 * math.pi

        return delta

    def release(self):
        """Release MediaPipe resources."""
        self.hands.close()


def create_gesture_detector(use_camera=True):
    """Factory function to create appropriate gesture detector."""
    if use_camera and MEDIAPIPE_AVAILABLE:
        try:
            return GestureDetector(), True
        except Exception as e:
            print(f"Failed to initialize MediaPipe: {e}")

    return MouseGestureDetector(), False

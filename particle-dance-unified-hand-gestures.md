# Particle Dance
## Unified Experience Spec — Hand Gestures First

---

## Core Concept (Restated)

**Particle Dance is a hand-controlled particle experience.**

Your hands—via webcam—control hundreds of glowing particles. Open palm attracts. Closed fist repels. Pinch spawns new particles. Every gesture has a satisfying ASMR sound response.

**Cursor is the fallback, not the feature.**

---

## Experience Modes

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   PRIMARY: Hand Tracking (Webcam)                           │
│   ═══════════════════════════════                           │
│   • MediaPipe Hands for 21-landmark tracking                │
│   • 1-2 hands supported                                     │
│   • 8 distinct gestures                                     │
│   • Full ASMR audio feedback                                │
│   • "Magic" feeling—no device between you and particles     │
│                                                             │
│   ───────────────────────────────────────                   │
│                                                             │
│   FALLBACK: Cursor/Touch                                    │
│   ════════════════════════                                  │
│   • For users without webcam                                │
│   • For quick "try it" before enabling camera               │
│   • Mobile touch support                                    │
│   • Reduced gesture set (3 modes vs 8)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Hand Gesture System

### Full Gesture Set

| Gesture | Detection | Particle Behavior | Sound | Feel |
|---------|-----------|-------------------|-------|------|
| **Open Palm** | 5 fingers extended | Attract toward palm center | Warm magnetic hum | Gathering energy |
| **Closed Fist** | 0 fingers extended | Repel/push away | Soft whoosh | Releasing force |
| **Pinch** | Thumb + index close | Spawn particle cluster | Bubble plop | Creating life |
| **Spread** | 5 fingers, wide apart | Explode outward | Scatter shimmer | Joyful release |
| **Wave** | Hand moving laterally | Create flow current | Water swoosh | Guiding stream |
| **Rotation** | Wrist rotating | Swirl vortex | Spiral wind | Stirring magic |
| **Two Hands Close** | Palms approaching | Merge particles between | Resonant tone | Connection |
| **Palm Up/Down** | Hand orientation | Shift gravity | Deep bass shift | Changing world |

### Gesture Detection Logic

```javascript
// Landmark indices
const THUMB_TIP = 4;
const INDEX_TIP = 8;
const MIDDLE_TIP = 12;
const RING_TIP = 16;
const PINKY_TIP = 20;
const PALM_BASE = 0;
const PALM_CENTER = 9;

function detectGesture(landmarks) {
  const fingersExtended = countExtendedFingers(landmarks);
  const pinchDistance = distance(landmarks[THUMB_TIP], landmarks[INDEX_TIP]);
  const fingerSpread = calculateFingerSpread(landmarks);
  const palmOrientation = getPalmOrientation(landmarks);
  const handVelocity = getHandVelocity(landmarks);
  
  // Pinch (highest priority)
  if (pinchDistance < PINCH_THRESHOLD && fingersExtended <= 2) {
    return { gesture: 'PINCH', confidence: 0.9 };
  }
  
  // Fist
  if (fingersExtended === 0) {
    return { gesture: 'FIST', confidence: 0.95 };
  }
  
  // Spread (open + wide)
  if (fingersExtended === 5 && fingerSpread > SPREAD_THRESHOLD) {
    return { gesture: 'SPREAD', confidence: 0.85 };
  }
  
  // Open palm
  if (fingersExtended >= 4) {
    return { gesture: 'OPEN_PALM', confidence: 0.9 };
  }
  
  // Wave (movement-based)
  if (handVelocity.x > WAVE_THRESHOLD) {
    return { gesture: 'WAVE', confidence: 0.7 };
  }
  
  return { gesture: 'NEUTRAL', confidence: 0.5 };
}
```

### Two-Hand Interactions

```javascript
function detectTwoHandGesture(leftHand, rightHand) {
  const palmDistance = distance(
    leftHand[PALM_CENTER], 
    rightHand[PALM_CENTER]
  );
  
  // Hands coming together = merge
  if (palmDistance < MERGE_THRESHOLD) {
    return { gesture: 'MERGE', strength: 1 - (palmDistance / MERGE_THRESHOLD) };
  }
  
  // Hands moving apart = expand
  if (palmDistance > EXPAND_THRESHOLD && handsMovingApart(leftHand, rightHand)) {
    return { gesture: 'EXPAND', strength: palmDistance / MAX_DISTANCE };
  }
  
  return null; // Process hands individually
}
```

---

## Visual Hand Feedback

### Hand Presence Indicator

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   OPTION A: Minimal Glow                                    │
│   ══════════════════════                                    │
│   • Soft glow at palm center position                       │
│   • Color indicates current gesture mode                    │
│   • No hand outline—keeps it abstract                       │
│                                                             │
│           ◉ ← Glow follows palm center                      │
│                                                             │
│   ───────────────────────────────────────                   │
│                                                             │
│   OPTION B: Particle Cloud                                  │
│   ═════════════════════════                                 │
│   • Small particle cluster follows hand                     │
│   • Particles orbit palm, extend to fingertips              │
│   • Your hand "becomes" particles                           │
│                                                             │
│           °°°°°                                             │
│          °°◉°°° ← Particles trace hand shape                │
│           °°°°°                                             │
│                                                             │
│   ───────────────────────────────────────                   │
│                                                             │
│   OPTION C: Ghost Hand (Optional Toggle)                    │
│   ═══════════════════════════════════════                   │
│   • Faint hand silhouette                                   │
│   • Helps users learn positioning                           │
│   • Can be disabled once comfortable                        │
│                                                             │
│           🖐 ← Semi-transparent hand overlay                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Gesture State Visualization

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Gesture         Visual Indicator                          │
│   ───────         ────────────────                          │
│                                                             │
│   Open Palm       ◉ with inward-flowing particle streams    │
│   Fist            ◉ with outward-exploding particles        │
│   Pinch           ✦ sparkle burst at pinch point            │
│   Spread          ◉ → ○ expanding ring                      │
│   Wave            ～～～ wave trail behind hand              │
│   Swirl           ◎ spiral forming around hand              │
│   Merge           ◉←──→◉ particles bridging hands           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Onboarding Flow (Hand Tracking)

### First Visit Experience

```
STEP 1: Landing
═══════════════

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    [particles floating]                     │
│                                                             │
│                                                             │
│                  Move your cursor to start                  │
│                                                             │
│                         — or —                              │
│                                                             │
│              [ Enable Camera for Hand Control ]             │
│                                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

• Particles active immediately (cursor mode)
• Camera prompt is prominent but not blocking
• Users can try cursor first, upgrade to hands later


STEP 2: Camera Permission
═════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│        ┌─────────────────────────────────────────┐          │
│        │                                         │          │
│        │   🎥  Particle Dance wants to use       │          │
│        │       your camera                       │          │
│        │                                         │          │
│        │   Your camera stays on your device.    │          │
│        │   We never record or upload video.      │          │
│        │                                         │          │
│        │   ┌──────────┐  ┌──────────────────┐   │          │
│        │   │  Allow   │  │  Use Cursor Only │   │          │
│        │   └──────────┘  └──────────────────┘   │          │
│        │                                         │          │
│        └─────────────────────────────────────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘


STEP 3: Hand Calibration (5 seconds)
════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                                                             │
│                      ┌─────────┐                            │
│                      │  🖐     │                            │
│                      │  You    │                            │
│                      └─────────┘                            │
│                                                             │
│              Hold your hand up so we can see it             │
│                                                             │
│                    ████████░░░░ 60%                         │
│                                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

• Small webcam preview in corner (optional)
• Progress bar as hand is detected
• Particles start responding once detected


STEP 4: Gesture Tutorial (Optional, Skippable)
══════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                                                             │
│                      Try this: Open Palm                    │
│                                                             │
│                           🖐                                │
│                                                             │
│                   Watch particles gather                    │
│                                                             │
│                                                             │
│                    [Skip Tutorial →]                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

• Teach one gesture at a time
• User does gesture → particles respond → next gesture
• Can skip anytime
• Takes ~30 seconds total
```

---

## Website Copy (Hand-Gesture Focused)

### Headlines

```
Primary:
"Touch light with your hands"

Alternatives:
"Your hands control the particles"
"Dance with light—no controller needed"
"What if particles could feel your touch?"
"Move your hands. Watch the magic."
```

### Subheadlines

```
"Open palm attracts. Fist repels. Pinch creates. 
Every gesture has a sound. Every moment is shareable."

"An ASMR particle experience controlled by your hands.
No mouse. No keyboard. Just you and the light."
```

### Feature Callouts

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🖐  HAND TRACKING                                         │
│       Your webcam sees your hands.                          │
│       Particles respond to every gesture.                   │
│                                                             │
│   🎵  ASMR AUDIO                                            │
│       Every touch has a sound.                              │
│       Soft pops. Gentle whooshes. Warm drones.              │
│                                                             │
│   📹  RECORD & SHARE                                        │
│       Capture your dance in seconds.                        │
│       Share the magic with friends.                         │
│                                                             │
│   ✨  NO SIGNUP NEEDED                                      │
│       Just open the page and start.                         │
│       Your camera stays on your device.                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Privacy Messaging

```
"Your camera never leaves your device.
We don't record. We don't upload. We don't track.
The particles see your hands. We don't."
```

---

## Technical Architecture (Hand Tracking)

### MediaPipe Integration

```javascript
import { Hands } from '@mediapipe/hands';
import { Camera } from '@mediapipe/camera_utils';

const hands = new Hands({
  locateFile: (file) => {
    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
  }
});

hands.setOptions({
  maxNumHands: 2,
  modelComplexity: 1,        // 0=lite, 1=full
  minDetectionConfidence: 0.7,
  minTrackingConfidence: 0.5
});

hands.onResults((results) => {
  if (results.multiHandLandmarks) {
    for (const landmarks of results.multiHandLandmarks) {
      const gesture = detectGesture(landmarks);
      applyGestureToParticles(gesture, landmarks);
      triggerGestureSound(gesture);
    }
  }
});

// Camera feed
const camera = new Camera(videoElement, {
  onFrame: async () => {
    await hands.send({ image: videoElement });
  },
  width: 640,
  height: 480
});
camera.start();
```

### Performance Optimization

```javascript
// Throttle hand processing for performance
let lastProcessTime = 0;
const PROCESS_INTERVAL = 33; // ~30fps for hand tracking

function onFrame() {
  const now = performance.now();
  if (now - lastProcessTime >= PROCESS_INTERVAL) {
    hands.send({ image: videoElement });
    lastProcessTime = now;
  }
  // Particles still update at 60fps
  updateParticles();
  render();
  requestAnimationFrame(onFrame);
}
```

### Gesture Smoothing

```javascript
// Prevent jittery gesture detection
class GestureSmoothing {
  constructor(bufferSize = 5) {
    this.buffer = [];
    this.bufferSize = bufferSize;
  }
  
  update(gesture) {
    this.buffer.push(gesture);
    if (this.buffer.length > this.bufferSize) {
      this.buffer.shift();
    }
    
    // Return most common gesture in buffer
    const counts = {};
    for (const g of this.buffer) {
      counts[g] = (counts[g] || 0) + 1;
    }
    return Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
  }
}
```

---

## Fallback Strategy

### When to Fallback to Cursor

```javascript
const useCursorFallback = () => {
  // No camera available
  if (!navigator.mediaDevices?.getUserMedia) return true;
  
  // User denied camera permission
  if (cameraPermissionDenied) return true;
  
  // User explicitly chose cursor mode
  if (userPrefersCursor) return true;
  
  // Low-end device detected
  if (isLowEndDevice()) return true;
  
  return false;
};
```

### Cursor Mode Gestures (Simplified)

| Input | Behavior | Maps to Hand Gesture |
|-------|----------|---------------------|
| Mouse move | Attract | Open Palm |
| Left click + move | Repel | Closed Fist |
| Right click | Spawn cluster | Pinch |
| Scroll wheel | Adjust force strength | — |
| Middle click | Toggle swirl | Rotation |

### Mobile Touch Gestures

| Input | Behavior | Maps to Hand Gesture |
|-------|----------|---------------------|
| One finger drag | Attract | Open Palm |
| Two finger drag | Repel | Closed Fist |
| Tap | Spawn cluster | Pinch |
| Pinch out | Explode | Spread |
| Rotate gesture | Swirl | Rotation |

---

## MVP Adjustment (Hand Tracking First)

### 4-Hour MVP — Now With Hands

```
Hour 1: Core
════════════
• Canvas + particle system
• MediaPipe Hands setup
• Basic palm position tracking
• Particles follow palm center

Hour 2: Gestures
════════════════
• Open palm = attract
• Closed fist = repel
• Basic gesture detection
• Cursor fallback if no camera

Hour 3: Polish
══════════════
• Gesture smoothing
• Glow effects
• Sound triggers
• Mobile fallback

Hour 4: Share + Deploy
══════════════════════
• Recording (canvas capture)
• Download
• Deploy
• Test both modes (hands + cursor)
```

### Minimum Hand Features for MVP

```
✓ Palm position tracking (both hands)
✓ Open palm gesture (attract)
✓ Closed fist gesture (repel)
✓ Smooth gesture transitions
✓ Visual feedback at palm center
✓ Fallback to cursor if no camera

Save for v1.1:
• Pinch to spawn
• Spread to explode  
• Wave for flow
• Rotation for swirl
• Two-hand merge
```

---

## UI Updates (Hand-Focused)

### Main Interface

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🖐 Hand Tracking ON          ⛶ Fullscreen   🔊   ❓       │
│                                                             │
│                                                             │
│                                                             │
│                     [particles + hands]                     │
│                                                             │
│                                                             │
│                                                             │
│                                                             │
│─────────────────────────────────────────────────────────────│
│   Open Palm = Attract  ·  Fist = Repel  ·  SPACE = Record   │
└─────────────────────────────────────────────────────────────┘
```

### Mode Toggle

```
┌──────────────────────────────────┐
│  🖐 Hands  ·  🖱️ Cursor  ·  📱   │
└──────────────────────────────────┘

Active mode is highlighted
Click to switch
Remembers preference
```

### Hand Status Indicator

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   HAND DETECTED                  HAND LOST                  │
│                                                             │
│   🖐 ✓                          🖐 ✗                        │
│   ────                          ────                        │
│   Green glow                    Fades out                   │
│   "Tracking"                    "Show your hand"            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Marketing Angle (Updated)

### Primary Message

```
"Control particles with your bare hands"
```

### Differentiation

```
Other particle toys:      Particle Dance:
• Mouse/cursor control    • Hand gesture control
• Silent                  • ASMR audio feedback
• No sharing              • One-click share
• Tech demos              • Designed experience
```

### Demo Video Shot List (Updated)

```
1. Open on particles floating (2 sec)
2. Hand enters frame (real hand, not cursor)
3. Open palm—particles rush toward hand (3 sec)
4. Close fist—particles explode away (3 sec)
5. Pinch—new particles spawn (3 sec)
6. Both hands—particles merge between (3 sec)
7. Pull back to show full experience (2 sec)
8. "Particle Dance" title card
9. URL: particledance.app
```

### Social Proof Headlines

```
"Wait, it's tracking my actual hands??"

"This is the coolest thing I've seen all week"

"I've been playing with this for 20 minutes"

"No way this works this well in a browser"
```

---

## Updated Document Summary

| Document | Key Update |
|----------|------------|
| **PRD** | ✓ Already hand-gesture focused |
| **Website Spec** | Updated: Lead with hand control, cursor as fallback |
| **Brand Guide** | ✓ Already includes gesture icons |
| **MVP Spec** | Updated: MediaPipe in hour 1, gestures in hour 2 |
| **Launch Playbook** | Updated: Demo videos show hands, not cursor |
| **Roadmap** | Adjusted: Hand tracking is v1.0, not v2.0 |

---

## One-Line Pitch (Final)

**"Particle Dance: control glowing particles with your bare hands, hear them respond, share the magic."**

---

*"The cursor is training wheels. The hands are the ride."*

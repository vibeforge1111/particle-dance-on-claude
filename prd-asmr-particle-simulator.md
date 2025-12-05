# Product Requirements Document
## GestureFlow: Hand-Controlled ASMR Particle Simulator

**Version:** 1.0  
**Author:** Cem  
**Date:** December 2024

---

## 1. Executive Summary

GestureFlow is a mesmerizing, gesture-controlled particle simulator that combines the hypnotic qualities of a digital lava lamp with satisfying ASMR audio feedback. Users interact with flowing particles using hand gestures captured via webcam, creating a deeply relaxing and immersive sensory experience.

---

## 2. Problem Statement

Existing particle simulators are typically mouse-controlled, creating a disconnect between the user and the visual experience. There's an opportunity to create a more embodied, tactile-feeling interaction using hand gestures while layering satisfying audio feedback to engage multiple senses simultaneously.

---

## 3. Target Audience

- **Primary:** Relaxation seekers, ASMR enthusiasts, people looking for digital stress relief
- **Secondary:** Creative coders, installation artists, streamers wanting ambient visuals
- **Tertiary:** Accessibility-focused users who prefer gesture over mouse/keyboard

---

## 4. Core Experience Vision

Imagine dipping your hands into a warm pool of glowing particles. As you move, particles flow around your fingers like liquid light. Each interaction produces soft, satisfying sounds—gentle pops, whooshes, and crystalline tones. The experience is meditative, hypnotic, and deeply satisfying.

---

## 5. Feature Requirements

### 5.1 Visual System (Pygame)

| Feature | Priority | Description |
|---------|----------|-------------|
| Particle Physics | P0 | Soft-body fluid dynamics with gravity, buoyancy, and viscosity |
| Color Gradients | P0 | Smooth HSV transitions creating lava lamp color blobs |
| Glow Effects | P0 | Bloom/glow shader effect on particles for dreamy aesthetic |
| Trail Persistence | P1 | Particles leave fading trails for flowing motion blur |
| Particle Morphing | P1 | Particles merge and split organically when close |
| Background Breathing | P2 | Subtle dark background color shifts (deep blues, purples, blacks) |
| Bubble Formation | P2 | Particles occasionally cluster into larger "bubbles" that float up |

**Visual Style Direction:**
- Color palette: Deep jewel tones (magenta, cyan, amber, violet) against dark backgrounds
- Particle shapes: Soft circles with gaussian blur edges
- Motion: Slow, languid, organic—nothing jarring or sudden
- Density: 500-2000 particles depending on performance

### 5.2 Hand Gesture Control (MediaPipe)

| Gesture | Action | ASMR Feedback |
|---------|--------|---------------|
| **Open Palm** | Attract particles toward hand center | Gentle magnetic hum |
| **Closed Fist** | Repel/push particles away | Soft whoosh/wind |
| **Pinch (thumb + index)** | Spawn new particle cluster | Bubble pop/plop sound |
| **Spread Fingers** | Explode nearby particles outward | Satisfying scatter sound |
| **Slow Wave** | Create current/flow in wave direction | Water/flowing sound |
| **Two Hands Close** | Merge particles between hands | Warm resonant tone |
| **Hand Rotation** | Swirl particles in vortex | Spiral wind sound |
| **Palm Up/Down** | Adjust gravity direction | Deep bass shift |

**Technical Requirements:**
- MediaPipe Hands for 21-landmark hand tracking
- Minimum 30 FPS hand tracking performance
- Support for 1-2 hands simultaneously
- Gesture smoothing to prevent jitter
- Configurable gesture sensitivity

### 5.3 ASMR Audio System

| Sound Category | Triggers | Characteristics |
|----------------|----------|-----------------|
| **Ambient Drone** | Always playing | Low, warm sine wave pad; binaural optional |
| **Interaction Pops** | Particle collision with hand hitbox | Soft bubble pops, varied pitch |
| **Flow Sounds** | Hand movement speed | Gentle water/wind whoosh |
| **Spawn Sounds** | New particles created | Crystalline chime, water drop |
| **Merge Sounds** | Particles combining | Soft thud, satisfying "click" |
| **Swirl Sounds** | Vortex gesture | Spiral wind, rising tone |

**Audio Design Principles:**
- All sounds soft, warm, lo-fi aesthetic
- No harsh frequencies (roll off above 8kHz)
- Gentle reverb on all sounds (cathedral/hall)
- Sounds are reactive but never overwhelming
- Volume scales with interaction intensity
- Optional: Binaural beats in ambient layer (theta waves for relaxation)

### 5.4 Particle Behaviors

```
┌─────────────────────────────────────────────────────────┐
│                    PARTICLE STATES                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [Floating] ──attract──> [Orbiting Hand]               │
│       │                        │                        │
│       │                        │ release                │
│       ▼                        ▼                        │
│   [Rising] <──buoyancy─── [Falling]                     │
│       │                        │                        │
│       │                        │                        │
│       └────> [Merging] <───────┘                        │
│                 │                                       │
│                 ▼                                       │
│           [Blob/Bubble]                                 │
│                 │                                       │
│                 │ split                                 │
│                 ▼                                       │
│           [Scatter] ───────> [Floating]                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Physics Parameters:**
- Gravity: 0.02 (very gentle downward pull)
- Buoyancy: Temperature-based (warm particles rise)
- Viscosity: 0.95 (thick, honey-like movement)
- Particle mass: Variable (affects interaction response)
- Collision softness: High (particles overlap and blend)

### 5.5 User Interface

**Minimal UI Philosophy:** The experience should feel like a portal, not software.

| Element | Behavior |
|---------|----------|
| **Controls** | Hidden by default, press `H` to show overlay |
| **Settings** | Press `S` for settings panel (particle count, colors, audio) |
| **Fullscreen** | `F` to toggle, fullscreen by default |
| **Calibration** | On first launch, brief hand calibration (5 sec) |
| **Exit** | `ESC` or hold both fists for 3 seconds |

---

## 6. Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN LOOP                                │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   CAPTURE    │───>│   GESTURE    │───>│   PHYSICS    │      │
│  │   (OpenCV)   │    │  (MediaPipe) │    │   ENGINE     │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                   │               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   WEBCAM     │    │   GESTURE    │    │   PARTICLE   │      │
│  │   OVERLAY    │    │   EVENTS     │    │   STATE      │      │
│  │  (optional)  │    │              │    │              │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                             │                   │               │
│                             ▼                   ▼               │
│                      ┌──────────────┐    ┌──────────────┐      │
│                      │    AUDIO     │    │   RENDERER   │      │
│                      │   (Pygame)   │    │   (Pygame)   │      │
│                      └──────────────┘    └──────────────┘      │
│                             │                   │               │
│                             └─────────┬─────────┘               │
│                                       ▼                         │
│                              ┌──────────────┐                   │
│                              │   DISPLAY    │                   │
│                              └──────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

**Dependencies:**
- Python 3.10+
- Pygame 2.5+
- MediaPipe 0.10+
- OpenCV 4.8+
- NumPy (particle physics optimization)
- Optional: PyOpenGL (for advanced glow effects)

---

## 7. ASMR Design Deep Dive

### 7.1 Sound Layering Architecture

```
Layer 0 (Base):     [═══════════════════════════════════════]
                    Ambient drone - always present, breathing

Layer 1 (Motion):   [    ~~~    ~~~       ~~~    ~~~       ]
                    Flow sounds - triggered by hand movement

Layer 2 (Touch):    [  •   •  •    •  • •    •      •  •   ]
                    Pop sounds - particle interactions

Layer 3 (Events):   [      ◆           ◆              ◆    ]
                    Special sounds - gestures, merges, spawns
```

### 7.2 Satisfying Feedback Moments

| Moment | Visual | Audio | Feel |
|--------|--------|-------|------|
| **First touch** | Particles gently scatter from hand | Soft "pff" with reverb | Like touching water surface |
| **Gathering** | Particles spiral into palm | Rising warm hum | Magnetic, powerful |
| **Release** | Particles drift away slowly | Fading chime | Letting go, peaceful |
| **Big merge** | Two blobs combine into one | Deep satisfying "thonk" | Completion, wholeness |
| **Explosion** | Particles scatter like dandelion | Crisp scatter + shimmer | Release, joy |

### 7.3 Audio File Requirements

| Sound | Duration | Format | Notes |
|-------|----------|--------|-------|
| ambient_drone.wav | Loop (30s) | 48kHz stereo | Seamless loop, binaural option |
| pop_01-05.wav | 0.1-0.3s | 48kHz mono | 5 variations, soft transients |
| whoosh_01-03.wav | 0.5-1.0s | 48kHz mono | 3 variations, velocity-layered |
| chime_spawn.wav | 1.0s | 48kHz stereo | Crystal bowl sound |
| merge_thonk.wav | 0.3s | 48kHz mono | Satisfying low "click" |
| swirl_wind.wav | Loop (2s) | 48kHz mono | Crossfade loop |

---

## 8. Visual Reference / Mood Board

**Color Palette:**
```
Primary:    ██████  #FF006E (Magenta)
            ██████  #00D4FF (Cyan)
            ██████  #FFB800 (Amber)
            
Accent:     ██████  #8338EC (Violet)
            ██████  #06FFA5 (Mint)
            
Background: ██████  #0D0221 (Deep Purple-Black)
            ██████  #0A1628 (Deep Blue-Black)
```

**Visual Inspirations:**
- Lava lamps (organic blob movement)
- Bioluminescent ocean waves
- Northern lights (color gradients)
- Soap bubbles (iridescence, merging)
- Ferrofluid (magnetic response to hand)

---

## 9. Performance Requirements

| Metric | Target | Minimum |
|--------|--------|---------|
| Frame Rate | 60 FPS | 30 FPS |
| Particle Count | 1500 | 500 |
| Hand Tracking Latency | <50ms | <100ms |
| Audio Latency | <20ms | <50ms |
| Memory Usage | <500MB | <1GB |
| CPU Usage | <40% | <70% |

**Optimization Strategies:**
- Spatial partitioning for particle collision (quadtree)
- NumPy vectorized physics calculations
- Particle LOD (reduce detail for distant/small particles)
- Frame skip for hand tracking if needed
- Audio sample pooling

---

## 10. Future Enhancements (v2.0+)

| Feature | Description | Priority |
|---------|-------------|----------|
| **Multiplayer** | Two people, two webcams, shared particle space | P2 |
| **Music Reactivity** | Particles respond to external music input | P2 |
| **Particle Personalities** | Different particle types with unique behaviors | P3 |
| **Recording/Playback** | Record sessions as video with audio | P2 |
| **VR Support** | Hand tracking via Quest/Index controllers | P3 |
| **Custom Skins** | User-created color themes and particle shapes | P3 |
| **Twitch Integration** | Chat commands spawn particles | P3 |

---

## 11. Success Metrics

| Metric | Target |
|--------|--------|
| Average session length | >10 minutes |
| User return rate (7-day) | >40% |
| "Relaxation" survey score | >8/10 |
| Social shares | Track viral clips |
| Crash rate | <1% of sessions |

---

## 12. Development Phases

### Phase 1: Core Loop (Week 1-2)
- [ ] Basic Pygame particle system
- [ ] MediaPipe hand tracking integration
- [ ] Simple attract/repel gestures
- [ ] Basic collision sounds

### Phase 2: Polish Visuals (Week 3)
- [ ] Glow/bloom effects
- [ ] Color gradient system
- [ ] Particle trails
- [ ] Blob merging behavior

### Phase 3: ASMR Audio (Week 4)
- [ ] Ambient drone layer
- [ ] Interaction sound triggers
- [ ] Audio mixing and spatialization
- [ ] Sound variation system

### Phase 4: Refinement (Week 5)
- [ ] Performance optimization
- [ ] Gesture smoothing
- [ ] Settings UI
- [ ] User testing and iteration

---

## 13. Open Questions

1. **Webcam overlay?** Show faint hand silhouette in corner, or keep fully abstract?
2. **Binaural audio?** Include theta wave option for deeper relaxation, or keep simple?
3. **Calibration UX?** Auto-detect hand or require explicit calibration step?
4. **Particle cap behavior?** Hard limit or graceful degradation when spawning too many?

---

## Appendix A: Gesture Detection Pseudocode

```python
def detect_gesture(hand_landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    palm_center = landmarks[9]
    
    # Pinch detection
    pinch_distance = distance(thumb_tip, index_tip)
    if pinch_distance < PINCH_THRESHOLD:
        return Gesture.PINCH
    
    # Fist detection (all fingers curled)
    fingers_extended = count_extended_fingers(landmarks)
    if fingers_extended == 0:
        return Gesture.FIST
    
    # Open palm (all fingers extended)
    if fingers_extended == 5:
        return Gesture.OPEN_PALM
    
    # Spread fingers (extended + wide apart)
    if fingers_extended == 5 and finger_spread(landmarks) > SPREAD_THRESHOLD:
        return Gesture.SPREAD
    
    return Gesture.NEUTRAL
```

---

*"The best interface is no interface—just you and the particles."*

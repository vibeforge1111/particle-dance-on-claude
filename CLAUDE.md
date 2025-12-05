# CLAUDE.md - Particle Dance

## Project Overview

**Particle Dance** is an interactive ASMR particle experience controlled by your hands (webcam) or cursor (fallback). The core loop: Play → Create → Capture → Share → Friend clicks → Repeat.

**Domain:** particledance.app
**Tagline:** "Touch light. Make magic."

## Brand Essence

Lives in the space between:
- Playful ←→ Calming (center)
- Retro ←→ Futuristic (center)
- Simple ←→ Magical (center)

**Core Values:** Wonder, Calm, Play, Connection, Beauty

## Technical Architecture

### Current: Desktop Python App (`/src`)
- `main.py` - Application entry point, event loop
- `particle.py` - Particle system with physics, merging, bubbles, spatial hashing
- `gesture.py` - MediaPipe hand tracking + mouse fallback
- `audio.py` - Procedural ASMR audio, binaural beats
- `renderer.py` - Pygame rendering with glow effects
- `quadtree.py` - Spatial partitioning for collision optimization
- `settings.py` - Persistent settings manager

**Stack:** Python 3.11, Pygame, MediaPipe, NumPy

### Target: Web MVP (`/web`)
- Vanilla JS + Canvas 2D (no frameworks for MVP)
- MediaRecorder API for video capture
- Web Audio API for sounds
- Deploy to Vercel/Netlify

**Stack:** HTML, CSS, Vanilla JS, Canvas 2D

## Key Features

### MVP (Web - Ship in Hours)
- [x] Particle playground with cursor interaction
- [x] 3 modes: Attract (A), Repel (R), Swirl (S)
- [x] Sound toggle (ambient drone + pops)
- [x] 5-second recording + download as video
- [x] Fullscreen mode (F)
- [x] Mobile touch support
- [ ] Copy link to share (stretch goal)

### v1.1 (Week 1)
- Share links (URL-encoded or backend)
- OG image/Twitter card previews
- More particle themes
- Bug fixes from launch

### v2.0 (Month 2) - The Real Vision
- Webcam hand tracking (MediaPipe in browser)
- Full 8-gesture system
- Desktop app (Electron/Tauri)

### v3.0 (Month 3+)
- Live multiplayer rooms
- Dance battles
- Remix culture
- Daily prompts

## Design System

### Colors
```
VOID (bg):     #0D0221 - Deep purple-black
MAGENTA:       #FF006E - Touch/warm
CYAN:          #00D4FF - Flow/cool
AMBER:         #FFB800 - Warmth/golden
VIOLET:        #8338EC - Dream/mystical
MINT:          #06FFA5 - Fresh/alive
```

### Typography
- **Headlines:** Space Grotesk (Bold)
- **Body:** Inter (Regular)
- **Quotes:** Instrument Serif (Italic)

### UI Principles
- Glassmorphism cards (frosted glass)
- Gradient borders on primary buttons
- Soft glows, never harsh
- Everything slow, everything gentle

## Gesture Mapping

### Hand Gestures (v2.0)
| Gesture | Behavior | Sound |
|---------|----------|-------|
| Open Palm | Attract | Warm hum |
| Closed Fist | Repel | Soft whoosh |
| Pinch | Spawn cluster | Bubble plop |
| Spread | Explode | Scatter shimmer |
| Wave | Create flow | Water swoosh |
| Rotation | Swirl vortex | Spiral wind |
| Two Hands Close | Merge | Resonant tone |
| Palm Up/Down | Shift gravity | Deep bass |

### Cursor/Touch (MVP)
| Input | Behavior |
|-------|----------|
| Move cursor | Attract |
| A key | Attract mode |
| R key | Repel mode |
| S key | Swirl mode |
| Click (mobile) | Tap to cycle modes |

## Audio Design

- **Ambient:** C2 sine wave pad (65 Hz), warm and womb-like
- **Pops:** Soft attack, 200-600 Hz, heavy reverb
- **Whoosh:** Filtered noise sweep, 300ms
- **All sounds:** Soft transients, roll off above 8kHz, 2-4s reverb tail

## Commands

### Desktop App
```bash
# Activate venv
.\venv\Scripts\activate

# Run app
python run.py

# Or directly
"C:\Users\USER\Desktop\Particle Dance\venv\Scripts\python.exe" run.py
```

### Web MVP
```bash
# From /web directory
npx serve .
# Or
python -m http.server 8000
```

## File Structure

```
/Particle Dance
├── /src                    # Desktop Python app
│   ├── main.py
│   ├── particle.py
│   ├── gesture.py
│   ├── audio.py
│   ├── renderer.py
│   ├── quadtree.py
│   └── settings.py
├── /web                    # Web MVP (to build)
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   ├── particles.js
│   └── /audio
│       ├── ambient.mp3
│       └── pop.mp3
├── /docs                   # Product docs
│   ├── prd-asmr-particle-simulator.md
│   ├── particle-dance-mvp-spec.md
│   ├── particle-dance-brand-guide.md
│   ├── particle-dance-launch-roadmap.md
│   ├── particle-dance-website-sharing-spec.md
│   └── particle-dance-unified-hand-gestures.md
├── CLAUDE.md               # This file
├── tasks.md                # Current tasks
├── requirements.txt
└── run.py
```

## Success Metrics (MVP)

- Loads fast (< 2 seconds)
- Particles respond immediately
- Mode switching feels snappy
- Someone says "this is cool" within 10 seconds
- Recording actually works
- Works on phone (basic but functional)

## Key Philosophy

> "Cut ruthlessly. Ship magic."
> "Done is better than perfect."
> "The cursor is training wheels. The hands are the ride."

## GitHub

Repository: https://github.com/vibeforge1111/particle-dance-on-claude

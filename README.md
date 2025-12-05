# GestureFlow: Hand-Controlled ASMR Particle Simulator

A mesmerizing, gesture-controlled particle simulator that combines the hypnotic qualities of a digital lava lamp with satisfying ASMR audio feedback. Control flowing particles using hand gestures captured via webcam for a deeply relaxing sensory experience.

![GestureFlow Demo](https://img.shields.io/badge/Python-3.11-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.6-green) ![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)

## Features

- **Hand Gesture Control**: Use natural hand gestures via webcam to interact with particles
- **Fluid Particle Physics**: Soft-body dynamics with gravity, buoyancy, and viscosity
- **Glow Effects**: Beautiful bloom/glow rendering for a dreamy aesthetic
- **ASMR Audio**: Procedurally generated ambient sounds and interaction feedback
- **Color Palette**: Jewel tones (magenta, cyan, amber, violet, mint) against dark backgrounds
- **Mouse Fallback**: Works without a webcam using mouse controls

## Hand Gestures

| Gesture | Action | Sound |
|---------|--------|-------|
| **Open Palm** | Attract particles toward hand | Gentle magnetic hum |
| **Closed Fist** | Repel/push particles away | Soft whoosh |
| **Pinch** (thumb + index) | Spawn new particle cluster | Bubble pop |
| **Spread Fingers** | Explode particles outward | Scatter sound |
| **Wave Hand** | Create flow current | Flowing sound |
| **Rotate Hand** | Swirl particles in vortex | Spiral wind |

## Installation

### Requirements
- Python 3.11 (MediaPipe requires Python 3.8-3.11)
- Webcam (optional, falls back to mouse control)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/vibeforge1111/particle-dance-on-claude.git
cd particle-dance-on-claude
```

2. Create a virtual environment with Python 3.11:
```bash
py -3.11 -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Windows
Double-click `run.bat` or run:
```bash
venv\Scripts\python.exe run.py
```

### macOS/Linux
```bash
python run.py
```

## Keyboard Controls

| Key | Action |
|-----|--------|
| **H** | Toggle help overlay |
| **F** | Toggle fullscreen |
| **S** | Settings panel |
| **G** | Toggle glow effects |
| **T** | Toggle particle trails |
| **A** | Toggle audio |
| **1-9** | Adjust volume |
| **+/-** | Add/reduce particles |
| **ESC** | Exit |

## Mouse Controls (Fallback Mode)

If MediaPipe is unavailable or no webcam is detected:

| Input | Action |
|-------|--------|
| **Left Click** | Attract particles |
| **Right Click** | Repel particles |
| **Middle Click** | Spawn particles |
| **Left + Right** | Explode particles |
| **Q/E Keys** | Vortex swirl |

## Project Structure

```
particle-dance-on-claude/
├── run.py              # Entry point
├── run.bat             # Windows launcher
├── requirements.txt    # Dependencies
└── src/
    ├── main.py         # Main application loop
    ├── particle.py     # Particle physics system
    ├── gesture.py      # Hand tracking & gesture detection
    ├── audio.py        # ASMR audio system
    └── renderer.py     # Visual rendering with glow effects
```

## Technical Details

- **Particle System**: NumPy-vectorized physics for performance (500-2000 particles)
- **Hand Tracking**: MediaPipe Hands with 21-landmark detection
- **Audio**: Procedurally generated sounds using pygame mixer
- **Rendering**: Pygame with pre-rendered glow textures and alpha blending

## Credits

Built with Claude Code by Anthropic.

## License

MIT License

# Particle Dance MVP
## Launch in Hours, Not Weeks

---

## MVP Philosophy

**Cut ruthlessly. Ship magic.**

The goal: Someone visits → plays with particles → thinks "this is cool" → shares with a friend.

That's it. Everything else is v2.

---

## What's IN the MVP

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ✅ IN                           ❌ OUT                    │
│   ════                            ════                      │
│                                                             │
│   • Particle playground           • User accounts           │
│   • Cursor interaction            • Live rooms              │
│   • 2-3 gesture modes             • Dance battles           │
│   • Sound on/off                  • Remix trees             │
│   • Download as GIF/video         • Achievements            │
│   • Copy link to share            • Daily prompts           │
│   • Mobile touch support          • Trending feed           │
│   • Basic landing text            • Analytics dashboard     │
│   • Fullscreen mode               • Multiple themes         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## The MVP Experience

### Single Page, Three States

```
STATE 1: LANDING (0-3 seconds)
═══════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                     [particles floating]                    │
│                                                             │
│                                                             │
│                                                             │
│                   Move your cursor                          │
│                                                             │
│                                                             │
│                                                             │
│                                                 🔊 Sound    │
└─────────────────────────────────────────────────────────────┘

• Particles already moving (no loading state needed)
• Hint text fades in after 2 seconds
• Sound toggle in corner (off by default)
• That's it. No nav, no logo yet.


STATE 2: PLAYING (main experience)
═══════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   [A] Attract  [R] Repel  [S] Swirl          ⛶  🔊  [?]    │
│                                                             │
│                                                             │
│                                                             │
│                     [particles + cursor]                    │
│                                                             │
│                                                             │
│                                                             │
│                                                             │
│───────────────────────────────────────────────────────────  │
│   Hold [SPACE] to record  ·  [F] Fullscreen                 │
└─────────────────────────────────────────────────────────────┘

• Minimal UI, appears after first interaction
• Keyboard shortcuts for power users
• Bottom hint bar (dismissable)


STATE 3: SHARE (after recording)
════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│        ┌─────────────────────────────────────┐              │
│        │                                     │              │
│        │       [5-sec loop preview]          │              │
│        │                                     │              │
│        └─────────────────────────────────────┘              │
│                                                             │
│                   Your dance is ready!                      │
│                                                             │
│        ┌──────────────┐  ┌──────────────┐                   │
│        │  Download    │  │  Copy Link   │                   │
│        │    .mp4      │  │      🔗      │                   │
│        └──────────────┘  └──────────────┘                   │
│                                                             │
│                    [✕ Keep dancing]                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘

• Auto-records last 5 seconds (not 15, simpler)
• Download gives MP4 with watermark
• "Copy Link" → generates shareable URL
• Can dismiss and keep playing
```

---

## Gesture Modes (MVP: Just 3)

| Key | Mode | Behavior | Cursor |
|-----|------|----------|--------|
| A | **Attract** (default) | Particles pull toward cursor | ○ with inward arrows |
| R | **Repel** | Particles push away from cursor | ○ with outward arrows |
| S | **Swirl** | Particles orbit cursor | ○ with circular arrow |

That's it. Pinch, spread, wave—all v2.

**Mobile:** Tap toggles through modes. Touch point = cursor.

---

## Sharing (MVP Version)

### Option A: Client-Side Only (Fastest)
```
• MediaRecorder API captures canvas
• Saves as WebM (Chrome) or MP4 (Safari)
• User downloads file, shares manually
• No server needed
```

### Option B: Simple Share Links (2-3 hours extra)
```
• Record canvas → encode as base64
• Store in URL hash: particledance.app/#[encoded-data]
• Anyone with link sees replay
• Limit: ~10 seconds of data fits in URL
• No database needed
```

### Option C: Basic Backend (If you have it ready)
```
• Upload WebM to S3/R2
• Generate short ID
• particledance.app/d/abc123
• Simple redirect, video plays
```

**Recommendation:** Start with Option A. Add Option B if time permits.

---

## Technical Stack (Minimal)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   FRONTEND ONLY (No backend needed for MVP)                 │
│                                                             │
│   Framework:     Vanilla JS or single React component       │
│   Particles:     Canvas 2D (not WebGL—faster to build)      │
│   Recording:     MediaRecorder API                          │
│   Audio:         Howler.js (or just <audio> elements)       │
│   Hosting:       Vercel / Netlify / GitHub Pages            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### File Structure
```
/particle-dance
  ├── index.html
  ├── style.css
  ├── app.js
  ├── particles.js
  └── /audio
      ├── ambient.mp3
      ├── pop.mp3
      └── whoosh.mp3
```

One HTML file. One JS file for particles. Done.

---

## Particle System (Simplified)

### Core Properties
```javascript
const CONFIG = {
  particleCount: 300,        // Start low, performant
  maxSpeed: 2,
  friction: 0.98,
  attractStrength: 0.5,
  repelStrength: 0.8,
  colors: ['#FF006E', '#00D4FF', '#FFB800', '#8338EC', '#06FFA5']
};
```

### Particle Class (Minimal)
```javascript
class Particle {
  constructor() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.vx = 0;
    this.vy = 0;
    this.radius = 3 + Math.random() * 4;
    this.color = CONFIG.colors[Math.floor(Math.random() * CONFIG.colors.length)];
  }
  
  update(mouseX, mouseY, mode) {
    const dx = mouseX - this.x;
    const dy = mouseY - this.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    
    if (mode === 'attract' && dist < 200) {
      this.vx += (dx / dist) * CONFIG.attractStrength;
      this.vy += (dy / dist) * CONFIG.attractStrength;
    }
    // ... repel, swirl logic
    
    this.vx *= CONFIG.friction;
    this.vy *= CONFIG.friction;
    this.x += this.vx;
    this.y += this.vy;
  }
  
  draw(ctx) {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
  }
}
```

### Glow Effect (Simple Version)
```javascript
// Instead of shaders, use shadowBlur
ctx.shadowBlur = 15;
ctx.shadowColor = particle.color;
particle.draw(ctx);
ctx.shadowBlur = 0;
```

---

## Sound (MVP: 3 Files)

| File | Trigger | Notes |
|------|---------|-------|
| ambient.mp3 | Toggle on | Loops forever, low volume |
| pop.mp3 | Particle near cursor | Play with random pitch shift |
| whoosh.mp3 | Mode change | Quick feedback |

```javascript
// Dead simple audio
const sounds = {
  ambient: new Audio('audio/ambient.mp3'),
  pop: new Audio('audio/pop.mp3'),
  whoosh: new Audio('audio/whoosh.mp3')
};

sounds.ambient.loop = true;
sounds.ambient.volume = 0.3;

function playPop() {
  const s = sounds.pop.cloneNode();
  s.playbackRate = 0.8 + Math.random() * 0.4; // Pitch variation
  s.volume = 0.2;
  s.play();
}
```

---

## Recording (Client-Side)

```javascript
let mediaRecorder;
let chunks = [];

function startRecording() {
  const stream = canvas.captureStream(30);
  mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
  
  mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
  mediaRecorder.onstop = () => {
    const blob = new Blob(chunks, { type: 'video/webm' });
    showShareModal(blob);
    chunks = [];
  };
  
  mediaRecorder.start();
  setTimeout(() => mediaRecorder.stop(), 5000); // 5 sec recording
}

function showShareModal(blob) {
  const url = URL.createObjectURL(blob);
  // Show modal with download link
}
```

---

## Mobile Support (Minimal)

```javascript
// Touch = mouse
canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  mouseX = touch.clientX;
  mouseY = touch.clientY;
});

// Tap to cycle modes
canvas.addEventListener('touchstart', (e) => {
  if (e.touches.length === 2) {
    // Two-finger tap = cycle mode
    cycleMode();
  }
});
```

**Mobile UI adjustment:**
- Mode buttons visible (no keyboard)
- Larger touch targets
- Hide "hold SPACE to record" → show record button

---

## Checklist: Launch in 4 Hours

### Hour 1: Core
- [ ] HTML/CSS scaffold (dark bg, fullscreen canvas)
- [ ] Basic particle system (spawn, draw, float)
- [ ] Mouse tracking

### Hour 2: Interaction  
- [ ] Attract mode working
- [ ] Repel mode working
- [ ] Swirl mode working
- [ ] Mode switching (keyboard + buttons)

### Hour 3: Polish
- [ ] Glow effect on particles
- [ ] Sound integration (ambient + pops)
- [ ] Fullscreen toggle
- [ ] Mobile touch support

### Hour 4: Share + Deploy
- [ ] Record button + 5-sec capture
- [ ] Download functionality
- [ ] Watermark on export
- [ ] Deploy to Vercel/Netlify
- [ ] Test share on Twitter/Discord

---

## What Good Looks Like (MVP)

```
✓ Loads fast (< 2 seconds)
✓ Particles respond to cursor immediately
✓ Switching modes feels snappy
✓ Sound enhances, doesn't annoy
✓ Recording actually works
✓ Downloaded video looks good enough to share
✓ Works on phone (basic but functional)
✓ Someone says "this is cool" within 10 seconds
```

---

## Post-Launch (v1.1, next week)

- [ ] Share links (URL-encoded replays)
- [ ] More particle colors/themes
- [ ] Better mobile gestures
- [ ] Smoother recording
- [ ] OG image for link previews
- [ ] Basic analytics (how many visits, recordings)

---

## Copy for MVP

### Landing hint
```
Move your cursor
```

### Mode labels
```
[A] Attract    [R] Repel    [S] Swirl
```

### Bottom bar
```
Hold SPACE to record  ·  F fullscreen  ·  ? help
```

### Share modal
```
Your dance is ready!

[Download .mp4]    [Keep dancing]

particledance.app
```

### Help modal (if they press ?)
```
Particle Dance

Move your cursor to interact with particles.

A — Attract particles
R — Repel particles  
S — Swirl particles
SPACE — Record 5 seconds
F — Fullscreen

Made by @cem
```

---

## Deploy Checklist

- [ ] Domain pointing (particledance.app or temp domain)
- [ ] HTTPS working
- [ ] OG meta tags (even if just text, no image yet)
- [ ] Test on Chrome, Safari, Firefox
- [ ] Test on iPhone, Android
- [ ] Test recording + download
- [ ] Tweet it 🚀

---

*"Done is better than perfect. Ship the magic, polish later."*

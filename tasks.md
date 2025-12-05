# Particle Dance - Tasks & Roadmap

## Current Sprint: Web MVP Launch

### Phase 1: Web MVP (4-hour build) - COMPLETE

#### Hour 1: Foundation
- [x] Create web/ directory structure
- [x] HTML scaffold with fullscreen canvas
- [x] CSS: dark background (#0D0221), responsive layout
- [x] Basic particle class with position, velocity, color
- [x] Render loop with 300 particles
- [x] Mouse tracking for cursor position

#### Hour 2: Core Mechanics
- [x] Attract mode (A key) - particles flow toward cursor
- [x] Repel mode (R key) - particles push away from cursor
- [x] Swirl mode (S key) - orbital vortex effect
- [x] Smooth easing for natural movement
- [x] Mode indicator UI

#### Hour 3: Polish
- [x] Glow/bloom effect on particles
- [x] Ambient drone sound (Web Audio API)
- [x] Pop sounds on particle spawns
- [x] Sound toggle button
- [x] Fullscreen button (F key)
- [x] Touch support for mobile

#### Hour 4: Viral Features
- [x] MediaRecorder for 5-second capture
- [x] Download as WebM/MP4
- [x] Recording indicator UI
- [x] Vercel/Netlify config ready
- [ ] Deploy live
- [ ] Test on mobile devices

---

## Completed Tasks

### Desktop App (Python/Pygame) - DONE
- [x] MediaPipe hand tracking integration
- [x] 5 gesture recognition (palm, fist, pinch, spread, wave)
- [x] Particle physics with forces
- [x] Glow/bloom rendering
- [x] Trail effects
- [x] Color palettes (default, sunset, ocean, aurora, monochrome)
- [x] Spatial audio panning
- [x] Settings persistence (~/.gestureflow/settings.json)
- [x] Webcam overlay option
- [x] First-launch calibration UX
- [x] Screensaver idle mode
- [x] Performance auto-scaling
- [x] High contrast accessibility mode
- [x] Particle LOD (level of detail)
- [x] Quadtree/spatial hashing optimization

---

## Future Roadmap

### v1.1 Polish (Post-MVP)
- [ ] Particle trails toggle
- [ ] 3 color themes UI
- [ ] Keyboard shortcuts overlay
- [ ] Performance optimizations
- [ ] Bug fixes from user feedback

### v1.5 Social Features
- [ ] Share to Twitter/TikTok integration
- [ ] Unique shareable URLs
- [ ] View counter
- [ ] "Made with Particle Dance" watermark option

### v2.0 Hand Tracking Web
- [ ] MediaPipe Hands JavaScript integration
- [ ] Webcam permission flow
- [ ] Full gesture support in browser
- [ ] Cursor fallback for non-webcam users

### v3.0 Platform
- [ ] User accounts
- [ ] Gallery of creations
- [ ] Multiplayer sessions (WebRTC)
- [ ] Custom particle skins
- [ ] API for developers

---

## Technical Debt
- [ ] Add unit tests for particle physics
- [ ] Document API for future integrations
- [ ] Set up CI/CD pipeline
- [ ] Performance profiling on low-end devices

---

## Ideas Backlog
- Audio visualizer mode (react to music)
- VR/AR version
- Procedural music generation
- AI-generated particle behaviors
- Collaborative art mode
- NFT minting (if requested)

# Particle Dance
## Launch Playbook, Roadmap & Competitive Landscape

---

# Part 1: Launch Playbook

## Launch Day Strategy

### The Goal
Get 1,000 people to play with Particle Dance in the first 24 hours.

### Pre-Launch (1-2 Hours Before)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   PREP CHECKLIST                                            │
│                                                             │
│   [ ] Site is live and tested                               │
│   [ ] Recording/download works                              │
│   [ ] Mobile tested (iPhone + Android)                      │
│   [ ] Create 3-5 demo recordings yourself                   │
│   [ ] Screen record a 30-sec demo video                     │
│   [ ] Write all tweets/posts in advance                     │
│   [ ] Have links ready to paste                             │
│   [ ] Tell 5 friends to be ready to retweet                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Launch Sequence

```
T-0:00  Post on Twitter/X (your main account)
T-0:05  Post on LinkedIn (if relevant audience)
T-0:10  Submit to Hacker News (Show HN: Particle Dance)
T-0:15  Post in Discord servers you're part of
T-0:30  Submit to Product Hunt (if timing works)
T-1:00  Post to Reddit (r/InternetIsBeautiful, r/web_design)
T-2:00  Follow up in replies, engage with comments
```

---

## Platform-Specific Tactics

### Twitter/X (Primary)

**Thread structure:**
```
Tweet 1 (Hook + Video):
I built Particle Dance—touch light with your cursor ✨

[30-sec screen recording showing the magic]

Tweet 2 (What it is):
It's an interactive particle experience. 
Move your cursor, watch them dance.
3 modes: attract, repel, swirl.

Weirdly relaxing.

Tweet 3 (Try it):
Try it: particledance.app

Works on mobile too 📱

Tweet 4 (Tech callout):
Built with vanilla JS + Canvas 2D.
No frameworks, no WebGL.
Just particles and vibes.

Tweet 5 (CTA):
Record your own dance and share it!
Show me what you make 👇
```

**Best times to post:**
- Weekday: 9-10am EST or 1-2pm EST
- Avoid Friday afternoon, weekends

**Hashtags (sparingly):**
#creativecoding #generativeart #webdev #asmr

---

### Hacker News

**Title options:**
```
Show HN: Particle Dance – An interactive ASMR particle experience
Show HN: I made a cursor-controlled particle simulator
Show HN: Particle Dance – Touch light with your cursor
```

**First comment (post immediately after):**
```
Hey HN! I built this over a weekend.

It's a simple idea: particles that respond to your cursor. 
Three modes (attract, repel, swirl), optional ambient sound, 
and you can record/download your creations.

Tech: Vanilla JS, Canvas 2D, MediaRecorder API. No frameworks.
About 500 lines of code total.

I'm planning to add hand gesture control (via webcam) 
and multiplayer rooms next.

Would love feedback on the particle physics—currently using 
simple attraction/repulsion forces. Any suggestions for 
making the motion feel more organic?

Try it: particledance.app
```

---

### Reddit

**Best subreddits:**
| Subreddit | Approach |
|-----------|----------|
| r/InternetIsBeautiful | "Particle Dance - an interactive particle experience" |
| r/web_design | Focus on the UI/UX, minimal interface |
| r/creativecoding | Technical angle, share the approach |
| r/oddlysatisfying | Video of particles (don't oversell) |
| r/webdev | "I built this with vanilla JS" |
| r/asmr | If the sound design is good |

**Reddit rules:**
- Don't spam multiple subs at once (stagger by hours)
- Engage genuinely in comments
- Never be defensive about criticism

---

### Discord Servers

**Good communities:**
- Creative coding discords
- Indie hacker communities
- Web dev communities
- ASMR communities
- Any servers you're already active in

**How to share:**
```
Hey everyone! Just launched something I've been working on—

Particle Dance: an interactive particle experience 
where your cursor controls hundreds of glowing particles.

It's strangely relaxing. You can record and download 
your creations too.

particledance.app

Would love to know what you think! 🎨
```

---

### Product Hunt

**Best for:** Getting on the radar of tech-savvy early adopters

**Timing:** Launch at 12:01 AM PST (their new day)

**Tagline options:**
```
"Touch light with your cursor"
"An ASMR particle playground"
"Interactive particles that dance with you"
```

**Maker comment:**
```
Hi Product Hunt! 👋

I built Particle Dance because I wanted something 
beautiful and calming to play with during work breaks.

Move your cursor → particles respond
Switch modes → attract, repel, or swirl
Record → share your creation

It's intentionally simple. No signup, no features 
getting in the way. Just you and the particles.

Coming soon: hand gesture control via webcam 
and multiplayer rooms.

Try it and let me know what you think!
```

---

## Content to Prepare

### Demo Videos (Make Before Launch)

| Video | Length | Purpose |
|-------|--------|---------|
| Hero demo | 30 sec | Main share video, show all 3 modes |
| Attract mode | 10 sec | Focused loop, satisfying |
| Swirl mode | 10 sec | Hypnotic spiral |
| Mobile demo | 15 sec | Show touch working |
| "How relaxing" | 20 sec | Slow, ambient, ASMR vibes |

### Screenshots
- Full-screen particle view (dark, glowy)
- UI visible (shows it's interactive)
- Mobile view
- Recording in progress

### GIFs
- Short loop of particles responding to cursor
- Mode switching
- Satisfying moment (particles converging)

---

## Engagement Strategy

### Reply to Every Comment
Especially in first 2-4 hours. Algorithms reward engagement.

### Prompt Discussion
Ask questions in your posts:
- "What mode is your favorite?"
- "What feature should I add next?"
- "Anyone else find this weirdly relaxing?"

### Retweet/Share User Creations
When someone shares their recording, amplify it. This encourages others.

### Handle Criticism Gracefully
```
❌ "Actually, you're wrong because..."
✅ "Good point! I'll consider that for v2"
✅ "Fair feedback—what would make it better for you?"
```

---

## Post-Launch (First Week)

### Day 1-2: Ride the Wave
- Keep engaging with comments
- Share interesting user creations
- Fix any critical bugs immediately
- Note all feature requests

### Day 3-4: Follow-Up Content
- "Thank you" post with stats
- "Most requested features" post
- Behind-the-scenes technical post

### Day 5-7: Build on Momentum
- Start working on most-requested feature
- Tease what's coming next
- Reach out to anyone who covered/shared it

---

## Tracking Success

### Metrics to Watch

| Metric | Tool | Target Day 1 |
|--------|------|--------------|
| Unique visitors | Vercel Analytics / Plausible | 1,000+ |
| Avg. session time | Analytics | > 2 minutes |
| Recordings created | Custom counter | 100+ |
| Social shares | Manual tracking | 50+ |
| HN points | Hacker News | Top 30 |
| Tweets mentioning | Twitter search | 20+ |

### Simple Analytics Setup
```html
<!-- Plausible (privacy-friendly, simple) -->
<script defer data-domain="particledance.app" 
  src="https://plausible.io/js/script.js"></script>
```

Or just use Vercel Analytics if hosting there.

---

# Part 2: Roadmap

## Version Timeline

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   NOW ──────────────────────────────────────────────> FUTURE│
│                                                             │
│   v1.0        v1.1        v1.5        v2.0        v3.0     │
│   MVP         Polish      Social      Gestures    Platform │
│   ────        ──────      ──────      ────────    ──────── │
│   Hours       Week 1      Week 2-3    Month 2     Month 3+ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## v1.0 — MVP (Launch Day)
*Ship in hours*

### Features
- [x] Particle playground
- [x] 3 gesture modes (attract, repel, swirl)
- [x] Cursor/touch interaction
- [x] Sound toggle (ambient + pops)
- [x] 5-second recording
- [x] Download as video
- [x] Fullscreen mode
- [x] Mobile support (basic)

### Success = People say "this is cool"

---

## v1.1 — Polish (Week 1)
*Based on launch feedback*

### Features
- [ ] Share links (URL-encoded replay OR simple backend)
- [ ] OG image / Twitter card preview
- [ ] Smoother particle physics
- [ ] More particle colors (3 themes)
- [ ] Better mobile gestures
- [ ] Keyboard shortcuts help modal
- [ ] Bug fixes from launch

### Technical Debt
- [ ] Refactor particle system for performance
- [ ] Add proper error handling
- [ ] Optimize for low-end devices

### Success = Return visitors, shares working

---

## v1.5 — Social (Week 2-3)
*Make sharing viral*

### Features
- [ ] Persistent share links (database)
- [ ] Animated link previews (GIF/video in OG)
- [ ] "Remix" button on shared dances
- [ ] View count on dances
- [ ] Gallery of recent/popular dances
- [ ] Like/heart button
- [ ] Basic profile (optional, claim your dances)
- [ ] Watermark on exports

### Infrastructure
- [ ] Simple database (Supabase or Planetscale)
- [ ] Video storage (Cloudflare R2 or S3)
- [ ] CDN for fast playback

### Success = Viral coefficient > 0.5 (every 2 shares = 1 new user)

---

## v2.0 — Hand Gestures (Month 2)
*The real vision*

### Features
- [ ] Webcam hand tracking (MediaPipe)
- [ ] Open palm = attract
- [ ] Closed fist = repel
- [ ] Pinch = spawn particles
- [ ] Spread = explode
- [ ] Wave = create flow
- [ ] Rotation = swirl
- [ ] Calibration flow
- [ ] Hand visualization (optional)

### Desktop App
- [ ] Electron wrapper (or Tauri)
- [ ] Better webcam access
- [ ] Local recording (higher quality)
- [ ] Offline support

### Success = "This feels like magic" reactions

---

## v2.5 — ASMR Audio (Month 2-3)
*Complete the sensory experience*

### Features
- [ ] Layered audio system
- [ ] Binaural beats option
- [ ] Sound per gesture type
- [ ] Spatial audio (particles have position)
- [ ] Volume mixer
- [ ] Import your own music (react to beat)

### Success = People use it for relaxation/focus

---

## v3.0 — Multiplayer Platform (Month 3+)
*Social becomes core*

### Features
- [ ] Live rooms (up to 8 people)
- [ ] Real-time cursor sync
- [ ] Collaborative recording
- [ ] Voice chat (optional)
- [ ] Dance battles (async)
- [ ] Daily prompts / challenges
- [ ] Leaderboards
- [ ] Achievements / badges
- [ ] Invite rewards (unlock colors)
- [ ] Custom themes (user-created)

### Monetization (Optional)
- [ ] Premium themes
- [ ] Extended recording time
- [ ] Private rooms
- [ ] Remove watermark

### Success = Community forming, daily active users

---

## Backlog (Ideas for Later)

### Visual Enhancements
- [ ] WebGL renderer (more particles, better glow)
- [ ] Particle trails
- [ ] Blob/metaball merging
- [ ] Multiple particle types
- [ ] Background themes (space, underwater, forest)

### Interaction
- [ ] Physics toys (gravity wells, black holes)
- [ ] Drawing mode (particles follow path)
- [ ] Text made of particles
- [ ] Image import (particles form image)

### Platform
- [ ] iOS/Android native app
- [ ] VR support (hand tracking)
- [ ] Twitch integration
- [ ] Screensaver mode
- [ ] API for developers

---

## Prioritization Framework

When deciding what to build next, score features:

| Factor | Weight | Questions |
|--------|--------|-----------|
| User demand | 30% | Are people asking for this? |
| Virality | 25% | Will this help the app spread? |
| Effort | 20% | Can we ship in < 1 week? |
| Delight | 15% | Will this make people smile? |
| Revenue | 10% | Does this enable monetization? |

---

# Part 3: Competitive Landscape

## Direct Competitors

### Silk Interactive
**URL:** weavesilk.com

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   WHAT IT IS                                                │
│   Generative art canvas with flowing, symmetrical lines     │
│                                                             │
│   STRENGTHS                          WEAKNESSES             │
│   • Beautiful, unique aesthetic      • No particle physics  │
│   • Very polished                    • No sound             │
│   • Mobile apps                      • No sharing built-in  │
│   • Been around forever              • Feels "finished"     │
│                                                             │
│   OUR ANGLE                                                 │
│   More playful, physics-based, social sharing native        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Staggering Beauty
**URL:** staggeringbeauty.com

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   WHAT IT IS                                                │
│   Weird worm that goes crazy when you shake it              │
│                                                             │
│   STRENGTHS                          WEAKNESSES             │
│   • Extremely viral                  • One-note joke        │
│   • Memorable                        • No depth             │
│   • Surprising                       • Flashing lights      │
│                                                             │
│   OUR ANGLE                                                 │
│   Sustained experience vs. quick gag                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Fluid Simulation
**URL:** paveldogreat.github.io/WebGL-Fluid-Simulation

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   WHAT IT IS                                                │
│   WebGL fluid dynamics simulation                           │
│                                                             │
│   STRENGTHS                          WEAKNESSES             │
│   • Technically impressive           • Dev/tech focused     │
│   • Satisfying physics               • No sound             │
│   • Open source                      • No sharing           │
│   • Mobile works well                • Just a demo          │
│                                                             │
│   OUR ANGLE                                                 │
│   Product vs. demo, audio, sharing, hand gestures           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Ball Pool
**URL:** ball-pool.com (or similar)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   WHAT IT IS                                                │
│   Simple ball physics sandbox                               │
│                                                             │
│   STRENGTHS                          WEAKNESSES             │
│   • Kid-friendly                     • Dated visuals        │
│   • Simple concept                   • No aesthetic focus   │
│   • Addictive                        • No audio             │
│                                                             │
│   OUR ANGLE                                                 │
│   Elevated aesthetics, audio, adult-friendly relaxation     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Indirect Competitors / Inspiration

### Looom (App)
```
Animation tool with playful interface
LEARN: Gesture-based interaction done well
```

### Calm / Headspace
```
Meditation apps with ambient visuals
LEARN: How they create calming environments
```

### Noisli / Coffitivity
```
Ambient sound generators
LEARN: Audio layering, user preferences
```

### Theremix by Google
```
Hand-tracked musical instrument
LEARN: MediaPipe implementation, gesture UX
```

### Blob Opera by Google
```
Playful, shareable music creation
LEARN: Viral sharing, delight-focused design
```

---

## Competitive Advantages

### What We Do That Others Don't

| Feature | Silk | Fluid Sim | Ball Pool | **Us** |
|---------|------|-----------|-----------|--------|
| Particle physics | ❌ | ✓ | ✓ | ✓ |
| Beautiful aesthetic | ✓ | ❌ | ❌ | ✓ |
| Sound/ASMR | ❌ | ❌ | ❌ | ✓ |
| Native sharing | ❌ | ❌ | ❌ | ✓ |
| Hand gestures | ❌ | ❌ | ❌ | ✓ (v2) |
| Multiplayer | ❌ | ❌ | ❌ | ✓ (v3) |
| Mobile-first | ❌ | ✓ | ❌ | ✓ |

### Our Moat (What's Hard to Copy)

1. **Sound Design** — The ASMR layer is unique and creates stickiness
2. **Sharing Infrastructure** — Once we have viral loops, hard to replicate
3. **Hand Gesture Vision** — Technical complexity + design polish
4. **Community** — If we build multiplayer, network effects kick in

---

## Positioning Statement

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   FOR        people who want a moment of calm               │
│   WHO        are tired of doomscrolling                     │
│   PARTICLE   is an interactive particle experience          │
│   DANCE                                                     │
│   THAT       responds to your movement                      │
│   UNLIKE     other toys that are just tech demos            │
│   WE         focus on beauty, sound, and sharing            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

### From Competitors
1. **Polish matters** — Silk is old but still shared because it's beautiful
2. **Sharing is everything** — None of them do it well; huge opportunity
3. **Sound is underused** — Audio makes experiences 10x more memorable
4. **Keep it simple** — The best ones do ONE thing really well

### For Us
1. Launch simple, iterate fast
2. Nail the core interaction before adding features
3. Make sharing dead-simple (it's our growth engine)
4. Sound is a differentiator—invest in it
5. Hand gestures are the "wow" factor for v2

---

# Document Summary

You now have:

| Document | Purpose |
|----------|---------|
| **PRD** | Full product vision for gesture-controlled ASMR experience |
| **Website Spec** | Detailed interactive website design |
| **Brand Guide** | Visual identity, colors, typography, motion |
| **MVP Spec** | What to build to launch in hours |
| **Launch Playbook** | How to get users on day 1 |
| **Roadmap** | What to build after MVP |
| **Competitive Analysis** | Where we fit, how we win |

---

*"Know where you're going, but focus on the next step."*

**Now go ship it.** 🚀

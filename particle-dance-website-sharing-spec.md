# Particle Dance
## Website & Sharing Experience Spec

---

## The Name

**Particle Dance** — Playful. Active. Invites participation. Works as both noun and verb.

*"Come do the Particle Dance"*
*"I made this on Particle Dance"*
*"Let's Particle Dance together"*

**Domain ideas:**
- particledance.app ✨ (primary)
- particle.dance
- particledance.io

**Tagline options:**
- "Touch light. Make magic."
- "Your hands. Infinite particles."
- "Dance with light."

---

## Core Concept

**"Create → Capture → Share → Compete"**

The website isn't just a demo—it's a creation tool. Every session can become shareable content. Every share brings new dancers.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    THE VIRAL LOOP                           │
│                                                             │
│         ┌──────────┐                                        │
│         │  PLAY    │ ←───────────────────────┐              │
│         └────┬─────┘                         │              │
│              │                               │              │
│              ▼                               │              │
│         ┌──────────┐                         │              │
│         │ CREATE   │                         │              │
│         └────┬─────┘                         │              │
│              │                               │              │
│              ▼                               │              │
│         ┌──────────┐                         │              │
│         │ CAPTURE  │  (auto-record loops)    │              │
│         └────┬─────┘                         │              │
│              │                               │              │
│              ▼                               │              │
│         ┌──────────┐      ┌──────────┐       │              │
│         │  SHARE   │ ───> │  FRIEND  │ ──────┘              │
│         └──────────┘      │  CLICKS  │                      │
│                           └──────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Sharing Features

### 1. Instant Replay Links

Every playground session auto-records the last 15 seconds. One click to share.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Your creation is ready!                                   │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                                                     │   │
│   │              [15-sec loop preview]                  │   │
│   │                                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   particledance.app/d/7xK2m                                 │
│                                                             │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│   │  Copy   │ │ Twitter │ │  Insta  │ │ TikTok  │          │
│   │  Link   │ │    𝕏    │ │   IG    │ │   ♪     │          │
│   └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
│                                                             │
│   ┌─────────┐ ┌─────────┐                                   │
│   │Download │ │ Try     │                                   │
│   │  .mp4   │ │ Again   │                                   │
│   └─────────┘ └─────────┘                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**URL Structure:**
```
particledance.app/d/[id]        → View someone's dance
particledance.app/d/[id]/remix  → Start from their creation
particledance.app/d/[id]/vs     → Side-by-side comparison
```

### 2. Dance Battles (Async Multiplayer)

Challenge friends to create something better with the same starting conditions.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🎯 CHALLENGE MODE                                         │
│                                                             │
│   @cem challenged you!                                      │
│   Theme: "Ocean Waves"                                      │
│   Time: 30 seconds                                          │
│   Colors: Blues only                                        │
│                                                             │
│   ┌─────────────────────┐  ┌─────────────────────┐         │
│   │                     │  │                     │         │
│   │   Cem's Dance       │  │   Your Turn         │         │
│   │   Score: 2.4k ❤️    │  │   [ Accept ]        │         │
│   │                     │  │                     │         │
│   └─────────────────────┘  └─────────────────────┘         │
│                                                             │
│   Winner = Most ❤️ in 24 hours                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. Remix Culture

Every shared dance can be "remixed"—start where they left off.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Original by @maya                                         │
│     └── Remixed by @cem                                     │
│           └── Remixed by @alex                              │
│                 └── Remixed by @jordan                      │
│                                                             │
│   [View remix tree]                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. Live Rooms (Real-time Multiplayer)

Dance together in the same particle space.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🟢 LIVE ROOM: Chill Vibes                                 │
│   3 dancers online                                          │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                                                     │   │
│   │    🔴 cem         🔵 maya        🟢 alex           │   │
│   │      ↓              ↓              ↓               │   │
│   │   [particles interact with all three cursors]      │   │
│   │                                                     │   │
│   │         ○    ○         ○                           │   │
│   │      ○     ○    ○           ○    ○                 │   │
│   │         ○         ○    ○         ○                 │   │
│   │                                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   [Invite friend]  [Share room link]  [Start recording]    │
│                                                             │
│   Room link: particledance.app/room/chillvibes             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Room Features:**
- Up to 8 dancers per room
- Each person gets a unique cursor color
- Combined creations can be saved
- Voice chat optional (spatial audio!)
- "Sync mode" where everyone's gestures mirror

### 5. Social Embeds

Shared links render beautifully everywhere:

**Twitter/X Card:**
```
┌─────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                                                         │ │
│ │              [Animated preview GIF]                     │ │
│ │                                                         │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Particle Dance                                              │
│ @cem made something beautiful ✨                            │
│ particledance.app/d/7xK2m                                   │
│                                                             │
│ [▶ Play]                                                    │
└─────────────────────────────────────────────────────────────┘
```

**iMessage/WhatsApp:**
```
┌─────────────────────────────────────┐
│ ┌─────────────────────────────────┐ │
│ │      [Animated thumbnail]       │ │
│ └─────────────────────────────────┘ │
│ Particle Dance                      │
│ Watch my dance! 💫                  │
└─────────────────────────────────────┘
```

### 6. QR Code Generation

For IRL sharing—show at parties, events, installations.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              ┌───────────────┐                              │
│              │ ▄▄▄▄▄ █ ▄▄▄▄▄│                              │
│              │ █   █ █ █   █│                              │
│              │ █▄▄▄█ █ █▄▄▄█│                              │
│              │ ▄▄▄▄▄▄▄▄▄▄▄▄▄│                              │
│              │ █ ▄ █ ▄ █ ▄ █│                              │
│              │ ▄▄▄▄▄ █ ▄▄▄▄▄│                              │
│              └───────────────┘                              │
│                                                             │
│              Scan to dance with me                          │
│                                                             │
│              [ Download QR ]                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Share-Optimized UI

### Persistent Share Bar

Always visible, never intrusive:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                                                             │
│                    [ PLAYGROUND ]                           │
│                                                             │
│                                                             │
│                                                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  ● REC          00:12 / 00:15         [Share ↗] [New 🔄]   │
└─────────────────────────────────────────────────────────────┘
```

- Red dot pulses when recording
- Timer shows loop progress
- "Share" becomes highlighted when you've made something cool
- Auto-detects "interesting" moments (lots of movement, merges, etc.)

### One-Tap Sharing Flow

```
Step 1: Tap "Share"
        ↓
Step 2: Preview your 15-sec loop (auto-trimmed to best moment)
        ↓  
Step 3: Add optional caption
        ↓
Step 4: Choose destination OR copy link
        ↓
Step 5: Done! Link is live instantly.
```

**No sign-up required to share.** Creations are anonymous by default. Optional account to claim your dances.

---

## Viral Mechanics

### 1. "Made with Particle Dance" Watermark

Subtle, aesthetic watermark on all exports:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                                                             │
│                    [ Video content ]                        │
│                                                             │
│                                                             │
│                                                             │
│                                    particledance.app    ✨  │
└─────────────────────────────────────────────────────────────┘
```

- Small, bottom-right
- Matches the aesthetic (glowing, particle-like)
- Clicking watermark in shared video goes to site

### 2. Daily Prompts

Give people a reason to create and share:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ✨ Today's Prompt                                         │
│                                                             │
│   "Northern Lights"                                         │
│                                                             │
│   Create something that captures the aurora.                │
│   Best dances featured on our page!                         │
│                                                             │
│   #ParticleDance #NorthernLights                            │
│                                                             │
│   [Start Dancing]                                           │
│                                                             │
│   142 dances submitted today                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. Trending Dances

Homepage showcases viral creations:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🔥 Trending Now                                           │
│                                                             │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│   │         │  │         │  │         │  │         │       │
│   │  12.4k  │  │   8.2k  │  │   6.1k  │  │   4.8k  │       │
│   │   ❤️    │  │    ❤️   │  │    ❤️   │  │    ❤️   │       │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│    @maya       @alex        @jordan      @sam              │
│                                                             │
│   [See all]                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. Achievement Badges

Gamification for repeat engagement:

| Badge | Requirement |
|-------|-------------|
| 🌟 First Dance | Create your first shareable |
| 🔥 Viral | Get 1,000 views on a dance |
| 🎨 Artist | Create 10 dances |
| 👯 Social | Have 5 friends join via your link |
| 🏆 Champion | Win a dance battle |
| 🌊 Trendsetter | Get featured in trending |
| 🔄 Remix Master | Have your dance remixed 10 times |
| 🎭 Collaborator | Complete a live room session |

### 5. Invite Rewards

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Invite friends, unlock colors!                            │
│                                                             │
│   🔓 1 friend  → Unlock "Sunset" palette                    │
│   🔓 3 friends → Unlock "Neon" palette                      │
│   🔓 5 friends → Unlock "Galaxy" palette                    │
│   🔒 10 friends → Unlock "Custom" color picker              │
│                                                             │
│   Your invite link:                                         │
│   particledance.app/join/cem                                │
│                                                             │
│   [ Copy ] [ Share ]                                        │
│                                                             │
│   2/5 friends joined                                        │
│   ████████░░░░░░░░░░░░                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Share Analytics (For Creators)

Optional dashboard for people who create accounts:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Your Dances                                     [Create]  │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                                                     │   │
│   │  This Week                                          │   │
│   │                                                     │   │
│   │  👁️ 2,847 views    ❤️ 342 likes    🔄 28 remixes    │   │
│   │                                                     │   │
│   │  ████████████████████░░░░░░                         │   │
│   │  Mon Tue Wed Thu Fri Sat Sun                        │   │
│   │                                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   Top Performing:                                           │
│   1. "Ocean sunset" — 1.2k views                           │
│   2. "Galaxy swirl" — 892 views                            │
│   3. "Fireflies" — 453 views                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Requirements for Sharing

### Video Generation

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Client-Side Recording:                                    │
│   • MediaRecorder API for canvas capture                    │
│   • WebM format (Chrome) / MP4 (Safari)                     │
│   • 720p default, 1080p for downloads                       │
│   • 15-second loops (configurable 5-30s)                    │
│   • Audio included (ASMR sounds!)                           │
│                                                             │
│   Server-Side Processing:                                   │
│   • FFmpeg for format conversion                            │
│   • GIF generation for previews                             │
│   • Thumbnail extraction                                    │
│   • Watermark overlay                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Real-Time Multiplayer Stack

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   WebSocket Server:                                         │
│   • Socket.io or PartyKit                                   │
│   • Cursor position sync (60 updates/sec)                   │
│   • Gesture state sync                                      │
│   • Room management                                         │
│                                                             │
│   State Sync:                                               │
│   • CRDT for conflict-free particle state                   │
│   • Delta compression for bandwidth                         │
│   • Interpolation for smooth remote cursors                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Storage & CDN

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Dance Storage:                                            │
│   • Cloudflare R2 or AWS S3 for videos                      │
│   • Edge caching for popular dances                         │
│   • Auto-delete after 30 days (unless saved)                │
│   • Claimed dances persist indefinitely                     │
│                                                             │
│   Database:                                                 │
│   • Planetscale or Supabase                                 │
│   • Dance metadata, view counts, likes                      │
│   • User accounts (optional)                                │
│   • Remix relationships                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Share URL Spec

### URL Patterns

```
particledance.app                     → Homepage
particledance.app/play                → Start creating
particledance.app/d/[id]              → View a dance
particledance.app/d/[id]/remix        → Remix a dance
particledance.app/d/[id]/download     → Direct download
particledance.app/room/[slug]         → Join live room
particledance.app/room/new            → Create live room
particledance.app/u/[username]        → User profile
particledance.app/join/[code]         → Invite link
particledance.app/battle/[id]         → Dance battle
particledance.app/trending            → Trending dances
particledance.app/prompt              → Today's prompt
```

### Short Links

```
prtcl.dance/[id]                      → Ultra-short share link
```

### Deep Links (Mobile)

```
particledance://d/[id]                → Open in app (future)
particledance://room/[slug]           → Join room in app
```

---

## Open Graph & Social Cards

```html
<!-- Dynamic per-dance -->
<meta property="og:title" content="@cem's Particle Dance">
<meta property="og:description" content="Watch this mesmerizing creation ✨">
<meta property="og:image" content="https://particledance.app/d/7xK2m/thumb.gif">
<meta property="og:video" content="https://particledance.app/d/7xK2m/preview.mp4">
<meta property="og:type" content="video.other">

<!-- Twitter Player Card -->
<meta name="twitter:card" content="player">
<meta name="twitter:player" content="https://particledance.app/d/7xK2m/embed">
<meta name="twitter:player:width" content="480">
<meta name="twitter:player:height" content="480">

<!-- Discord Embed -->
<meta property="og:site_name" content="Particle Dance">
```

---

## Privacy & Moderation

### Content Policy

```
✓ All dances are abstract particles—no harmful content possible
✓ Usernames checked against blocklist
✓ Optional content reporting (rare edge cases)
✓ No personal data in dance files
```

### Data Handling

```
Anonymous dances:
• Stored 30 days, then deleted
• No tracking, no cookies required
• IP addresses not logged

Claimed dances (with account):
• Stored indefinitely
• Email only (no personal info required)
• Full GDPR compliance
• One-click data export/delete
```

---

## Launch Sharing Strategy

### Phase 1: Soft Launch
- Share with creative coding communities
- r/creativecoding, Hacker News, Twitter tech community
- Focus on "look what I made" organic sharing

### Phase 2: Creator Outreach
- ASMR YouTubers / TikTokers
- Digital artists
- Meditation/relaxation influencers
- "Made this for you" personalized outreach

### Phase 3: Viral Push
- Daily prompts with prizes
- Featured creator program
- TikTok sound integration
- Twitter Spaces live dance sessions

---

## Success Metrics

| Metric | Week 1 | Month 1 | Month 3 |
|--------|--------|---------|---------|
| Total dances created | 1,000 | 25,000 | 200,000 |
| Dances shared | 200 | 5,000 | 50,000 |
| Share-to-visit conversion | 15% | 20% | 25% |
| Viral coefficient (K) | 0.5 | 0.8 | 1.2+ |
| Live room sessions | 50 | 500 | 5,000 |
| Avg. session length | 3 min | 5 min | 7 min |

---

*"The best content is content people want to share."*

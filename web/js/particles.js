/**
 * Particle Dance - Particle System
 * Optimized for 60fps with hundreds of particles
 */

// Pre-computed constants
const TWO_PI = Math.PI * 2;
const DEG_TO_RAD = Math.PI / 180;

class Particle {
    constructor(x, y, options = {}) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 2;
        this.vy = (Math.random() - 0.5) * 2;

        // Size with slight variation
        this.baseSize = options.size || 3 + Math.random() * 3;
        this.size = this.baseSize;

        // Color (HSL for easy manipulation)
        this.hue = options.hue || Math.random() * 360;
        this.saturation = 80 + Math.random() * 20;
        this.lightness = 50 + Math.random() * 20;
        this.alpha = 0.8 + Math.random() * 0.2;

        // Physics
        this.friction = 0.98;
        this.maxSpeed = 15;
        this.maxSpeedSq = 225; // Pre-computed squared value

        // Glow intensity
        this.glowIntensity = 0.5 + Math.random() * 0.5;

        // For color cycling
        this.hueSpeed = 0.1 + Math.random() * 0.2;

        // Pre-cache color strings (updated periodically, not every frame)
        this._colorCache = '';
        this._colorCacheAlpha = -1;
        this._updateColorCache();
    }

    _updateColorCache() {
        // Round values for better string caching
        const h = Math.round(this.hue);
        const s = Math.round(this.saturation);
        const l = Math.round(this.lightness);
        this._colorBase = `${h},${s}%,${l}%`;
    }

    update(width, height) {
        // Apply velocity
        this.x += this.vx;
        this.y += this.vy;

        // Apply friction
        this.vx *= this.friction;
        this.vy *= this.friction;

        // Speed limit using squared distance (avoid sqrt)
        const speedSq = this.vx * this.vx + this.vy * this.vy;
        if (speedSq > this.maxSpeedSq) {
            const scale = this.maxSpeed / Math.sqrt(speedSq);
            this.vx *= scale;
            this.vy *= scale;
        }

        // Boundary wrapping (seamless)
        if (this.x < -20) this.x = width + 20;
        else if (this.x > width + 20) this.x = -20;
        if (this.y < -20) this.y = height + 20;
        else if (this.y > height + 20) this.y = -20;

        // Slowly cycle hue for shimmer effect
        this.hue = (this.hue + this.hueSpeed) % 360;

        // Size pulse based on speed (use squared speed approximation)
        this.size = this.baseSize + Math.sqrt(speedSq) * 0.3;

        // Update color cache occasionally (every ~10 frames worth of hue change)
        if (Math.random() < 0.1) {
            this._updateColorCache();
        }
    }

    applyForce(fx, fy) {
        this.vx += fx;
        this.vy += fy;
    }

    getColor(alpha) {
        if (alpha === undefined) alpha = this.alpha;
        return `hsla(${this._colorBase},${alpha})`;
    }
}

class ParticleSystem {
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d', { alpha: false });
        this.particles = [];

        // Options
        this.particleCount = options.particleCount || 300;
        this.glowEnabled = options.glow !== false;

        // Interaction state
        this.mouseX = canvas.width / 2;
        this.mouseY = canvas.height / 2;
        this.mouseActive = false;
        this.mode = 'attract';

        // Force settings
        this.forceRadius = 200;
        this.forceRadiusSq = 40000; // Pre-computed
        this.forceStrength = 0.5;

        // Background
        this.bgHue = 270;
        this.bgBrightness = 0;
        this.bgDirection = 1;

        // Performance
        this.lastTime = performance.now();
        this.fps = 60;
        this.performanceMode = false;
        this.cursorVisible = true;

        // Pre-computed values for cursor colors
        this._cursorColors = {
            attract: 'rgba(0,217,255,',
            repel: 'rgba(255,0,255,',
            swirl: 'rgba(255,215,0,'
        };

        // Background color cache
        this._bgColorCache = '';
        this._lastBgBrightness = -1;

        this.init();
    }

    init() {
        this.particles = [];
        const w = this.canvas.width;
        const h = this.canvas.height;
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push(new Particle(
                Math.random() * w,
                Math.random() * h,
                { hue: (i / this.particleCount) * 360 }
            ));
        }
    }

    resize(width, height) {
        const scaleX = width / this.canvas.width;
        const scaleY = height / this.canvas.height;
        const particles = this.particles;
        for (let i = 0, len = particles.length; i < len; i++) {
            particles[i].x *= scaleX;
            particles[i].y *= scaleY;
        }
    }

    setMode(mode) {
        this.mode = mode;
    }

    setMousePosition(x, y, active = true) {
        this.mouseX = x;
        this.mouseY = y;
        this.mouseActive = active;
    }

    update() {
        const width = this.canvas.width;
        const height = this.canvas.height;
        const particles = this.particles;
        const len = particles.length;

        // Update background breathing
        this.bgBrightness += 0.1 * this.bgDirection;
        if (this.bgBrightness > 3) this.bgDirection = -1;
        else if (this.bgBrightness < 0) this.bgDirection = 1;

        // Cache mouse state
        const mouseActive = this.mouseActive;
        const mouseX = this.mouseX;
        const mouseY = this.mouseY;
        const forceRadiusSq = this.forceRadiusSq;
        const forceRadius = this.forceRadius;
        const forceStrength = this.forceStrength;
        const mode = this.mode;

        // Update particles
        for (let i = 0; i < len; i++) {
            const particle = particles[i];

            // Apply interaction forces
            if (mouseActive) {
                const dx = mouseX - particle.x;
                const dy = mouseY - particle.y;
                const distSq = dx * dx + dy * dy;

                if (distSq < forceRadiusSq && distSq > 1) {
                    const dist = Math.sqrt(distSq);
                    const force = (1 - dist / forceRadius) * forceStrength;
                    const invDist = 1 / dist;
                    const nx = dx * invDist; // Normalized
                    const ny = dy * invDist;

                    if (mode === 'attract') {
                        particle.vx += nx * force;
                        particle.vy += ny * force;
                    } else if (mode === 'repel') {
                        const f = force * 1.5;
                        particle.vx -= nx * f;
                        particle.vy -= ny * f;
                    } else { // swirl
                        const pullForce = force * 0.3;
                        const swirlForce = force * 0.8;
                        particle.vx += -ny * swirlForce + nx * pullForce;
                        particle.vy += nx * swirlForce + ny * pullForce;
                    }
                }
            }

            particle.update(width, height);
        }
    }

    render() {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;
        const particles = this.particles;
        const len = particles.length;
        const performanceMode = this.performanceMode;

        // Clear with background
        if (performanceMode) {
            ctx.fillStyle = '#0D0214';
            ctx.fillRect(0, 0, width, height);
        } else {
            // Only recreate gradient if brightness changed significantly
            const brightRounded = Math.round(this.bgBrightness);
            if (brightRounded !== this._lastBgBrightness) {
                this._lastBgBrightness = brightRounded;
                const gradient = ctx.createRadialGradient(
                    width / 2, height / 2, 0,
                    width / 2, height / 2, Math.max(width, height)
                );
                gradient.addColorStop(0, `hsl(270,50%,${2 + brightRounded}%)`);
                gradient.addColorStop(1, 'hsl(290,60%,1%)');
                this._bgGradient = gradient;
            }
            ctx.fillStyle = this._bgGradient;
            ctx.fillRect(0, 0, width, height);
        }

        // Batch render particles
        if (performanceMode) {
            // Simple circles only - maximum performance
            for (let i = 0; i < len; i++) {
                const p = particles[i];
                ctx.fillStyle = p.getColor();
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, TWO_PI);
                ctx.fill();
            }
        } else {
            // Glow mode - render glow layer first, then cores
            ctx.globalCompositeOperation = 'lighter';

            // Glow pass - simplified gradient (only 2 stops)
            for (let i = 0; i < len; i++) {
                const p = particles[i];
                const glowSize = p.size * 3;
                const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, glowSize);
                gradient.addColorStop(0, p.getColor(0.25 * p.glowIntensity));
                gradient.addColorStop(1, p.getColor(0));
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(p.x, p.y, glowSize, 0, TWO_PI);
                ctx.fill();
            }

            // Core pass
            ctx.globalCompositeOperation = 'source-over';
            for (let i = 0; i < len; i++) {
                const p = particles[i];
                ctx.fillStyle = p.getColor();
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, TWO_PI);
                ctx.fill();
            }

            // Bright center pass
            for (let i = 0; i < len; i++) {
                const p = particles[i];
                ctx.fillStyle = p.getColor(1);
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * 0.5, 0, TWO_PI);
                ctx.fill();
            }
        }

        ctx.globalCompositeOperation = 'source-over';

        // Render cursor
        if (this.mouseActive && this.cursorVisible) {
            this.renderCursor(ctx);
        }
    }

    renderCursor(ctx) {
        const x = this.mouseX;
        const y = this.mouseY;
        const color = this._cursorColors[this.mode];

        // Simplified cursor - just ring and dot
        ctx.strokeStyle = color + '0.5)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(x, y, 20, 0, TWO_PI);
        ctx.stroke();

        ctx.fillStyle = color + '0.8)';
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, TWO_PI);
        ctx.fill();
    }

    animate() {
        const now = performance.now();
        const dt = Math.min((now - this.lastTime) / 1000, 0.1);
        this.lastTime = now;
        this.fps = 1 / dt;

        this.update();
        this.render();

        requestAnimationFrame(() => this.animate());
    }

    start() {
        this.lastTime = performance.now();
        this.animate();
    }

    spawnBurst(x, y, count = 10) {
        const particles = this.particles;
        const maxLen = this.particleCount * 1.2;

        for (let i = 0; i < count; i++) {
            const angle = (i / count) * TWO_PI;
            const speed = 2 + Math.random() * 3;

            const particle = new Particle(x, y, { hue: Math.random() * 360 });
            particle.vx = Math.cos(angle) * speed;
            particle.vy = Math.sin(angle) * speed;

            if (particles.length >= maxLen) {
                particles.shift();
            }
            particles.push(particle);
        }
        return true;
    }

    waveEffect(x, y) {
        const time = performance.now() * 0.003;
        const particles = this.particles;
        const len = particles.length;

        for (let i = 0; i < len; i++) {
            const p = particles[i];
            const dx = p.x - x;
            const dy = p.y - y;
            const distSq = dx * dx + dy * dy;

            if (distSq < 90000 && distSq > 100) { // 300^2 and 10^2
                const dist = Math.sqrt(distSq);
                const wave = Math.sin(dist * 0.02 - time) * 0.3;
                const invDist = 1 / dist;
                p.vx += dx * invDist * wave;
                p.vy += dy * invDist * wave;
            }
        }
    }

    energyBoost() {
        const particles = this.particles;
        const len = particles.length;
        for (let i = 0; i < len; i++) {
            const p = particles[i];
            p.vx += (Math.random() - 0.5) * 4;
            p.vy += (Math.random() - 0.5) * 4;
            p.lightness = Math.min(80, p.lightness + 10);
        }
    }

    chaosMode(x, y) {
        const particles = this.particles;
        const len = particles.length;

        for (let i = 0; i < len; i++) {
            const p = particles[i];
            const dx = p.x - x;
            const dy = p.y - y;
            const distSq = dx * dx + dy * dy;

            if (distSq < 62500) { // 250^2
                p.vx += (Math.random() - 0.5) * 2;
                p.vy += (Math.random() - 0.5) * 2;
                p.hue = (p.hue + 5) % 360;
            }
        }
    }
}

window.ParticleSystem = ParticleSystem;

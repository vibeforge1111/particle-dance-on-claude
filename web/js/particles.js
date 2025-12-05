/**
 * Particle Dance - Particle System
 * Beautiful, performant particle physics with Canvas 2D
 */

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

        // Glow intensity
        this.glowIntensity = 0.5 + Math.random() * 0.5;

        // For color cycling
        this.hueOffset = Math.random() * 30;
        this.hueSpeed = 0.1 + Math.random() * 0.2;
    }

    update(dt, width, height) {
        // Apply velocity
        this.x += this.vx;
        this.y += this.vy;

        // Apply friction
        this.vx *= this.friction;
        this.vy *= this.friction;

        // Speed limit
        const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
        if (speed > this.maxSpeed) {
            this.vx = (this.vx / speed) * this.maxSpeed;
            this.vy = (this.vy / speed) * this.maxSpeed;
        }

        // Boundary wrapping (seamless)
        if (this.x < -20) this.x = width + 20;
        if (this.x > width + 20) this.x = -20;
        if (this.y < -20) this.y = height + 20;
        if (this.y > height + 20) this.y = -20;

        // Slowly cycle hue for shimmer effect
        this.hue = (this.hue + this.hueSpeed) % 360;

        // Size pulse based on speed
        this.size = this.baseSize + speed * 0.3;
    }

    applyForce(fx, fy) {
        this.vx += fx;
        this.vy += fy;
    }

    getColor(alpha = this.alpha) {
        return `hsla(${this.hue}, ${this.saturation}%, ${this.lightness}%, ${alpha})`;
    }
}

class ParticleSystem {
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];

        // Options
        this.particleCount = options.particleCount || 300;
        this.glowEnabled = options.glow !== false;

        // Interaction state
        this.mouseX = canvas.width / 2;
        this.mouseY = canvas.height / 2;
        this.mouseActive = false;
        this.mode = 'attract'; // attract, repel, swirl

        // Force settings
        this.forceRadius = 200;
        this.forceStrength = 0.5;

        // Background breathing
        this.bgHue = 270; // Deep purple
        this.bgBrightness = 0;
        this.bgDirection = 1;

        // Performance
        this.lastTime = performance.now();
        this.fps = 60;

        // Performance mode (reduces glow during recording)
        this.performanceMode = false;

        // Initialize particles
        this.init();
    }

    init() {
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push(new Particle(
                Math.random() * this.canvas.width,
                Math.random() * this.canvas.height,
                { hue: (i / this.particleCount) * 360 } // Spectrum distribution
            ));
        }
    }

    resize(width, height) {
        // Scale particle positions
        const scaleX = width / this.canvas.width;
        const scaleY = height / this.canvas.height;

        this.particles.forEach(p => {
            p.x *= scaleX;
            p.y *= scaleY;
        });
    }

    setMode(mode) {
        this.mode = mode;
    }

    setMousePosition(x, y, active = true) {
        this.mouseX = x;
        this.mouseY = y;
        this.mouseActive = active;
    }

    update(dt) {
        const width = this.canvas.width;
        const height = this.canvas.height;

        // Update background breathing
        this.bgBrightness += 0.1 * this.bgDirection;
        if (this.bgBrightness > 3) this.bgDirection = -1;
        if (this.bgBrightness < 0) this.bgDirection = 1;

        // Update particles
        for (const particle of this.particles) {
            // Apply interaction forces
            if (this.mouseActive) {
                const dx = this.mouseX - particle.x;
                const dy = this.mouseY - particle.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < this.forceRadius && dist > 1) {
                    const force = (1 - dist / this.forceRadius) * this.forceStrength;
                    const angle = Math.atan2(dy, dx);

                    switch (this.mode) {
                        case 'attract':
                            // Pull toward cursor
                            particle.applyForce(
                                Math.cos(angle) * force,
                                Math.sin(angle) * force
                            );
                            break;

                        case 'repel':
                            // Push away from cursor
                            particle.applyForce(
                                -Math.cos(angle) * force * 1.5,
                                -Math.sin(angle) * force * 1.5
                            );
                            break;

                        case 'swirl':
                            // Orbital motion around cursor
                            const perpAngle = angle + Math.PI / 2;
                            const pullForce = force * 0.3;
                            const swirlForce = force * 0.8;
                            particle.applyForce(
                                Math.cos(perpAngle) * swirlForce + Math.cos(angle) * pullForce,
                                Math.sin(perpAngle) * swirlForce + Math.sin(angle) * pullForce
                            );
                            break;
                    }
                }
            }

            particle.update(dt, width, height);
        }
    }

    render() {
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;
        const useGlow = this.glowEnabled && !this.performanceMode;

        // Clear with solid background (faster than gradient in performance mode)
        if (this.performanceMode) {
            ctx.fillStyle = `hsl(${this.bgHue}, 50%, 2%)`;
            ctx.fillRect(0, 0, width, height);
        } else {
            const gradient = ctx.createRadialGradient(
                width / 2, height / 2, 0,
                width / 2, height / 2, Math.max(width, height)
            );
            gradient.addColorStop(0, `hsl(${this.bgHue}, 50%, ${2 + this.bgBrightness}%)`);
            gradient.addColorStop(1, `hsl(${this.bgHue + 20}, 60%, ${1}%)`);

            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, width, height);
        }

        // Enable compositing for glow
        if (useGlow) {
            ctx.globalCompositeOperation = 'lighter';
        }

        // Render particles
        for (const particle of this.particles) {
            const x = particle.x;
            const y = particle.y;
            const size = particle.size;

            // Glow effect (outer soft circle) - skip in performance mode
            if (useGlow) {
                const glowSize = size * 4;
                const glowGradient = ctx.createRadialGradient(x, y, 0, x, y, glowSize);
                glowGradient.addColorStop(0, particle.getColor(0.3 * particle.glowIntensity));
                glowGradient.addColorStop(0.5, particle.getColor(0.1 * particle.glowIntensity));
                glowGradient.addColorStop(1, particle.getColor(0));

                ctx.fillStyle = glowGradient;
                ctx.beginPath();
                ctx.arc(x, y, glowSize, 0, Math.PI * 2);
                ctx.fill();
            }

            // Core particle
            ctx.globalCompositeOperation = 'source-over';
            ctx.fillStyle = particle.getColor();
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();

            // Bright center (skip in performance mode for speed)
            if (!this.performanceMode) {
                ctx.fillStyle = particle.getColor(1);
                ctx.beginPath();
                ctx.arc(x, y, size * 0.5, 0, Math.PI * 2);
                ctx.fill();
            }

            if (useGlow) {
                ctx.globalCompositeOperation = 'lighter';
            }
        }

        // Reset compositing
        ctx.globalCompositeOperation = 'source-over';

        // Render cursor glow indicator
        if (this.mouseActive) {
            this.renderCursor(ctx);
        }
    }

    renderCursor(ctx) {
        const x = this.mouseX;
        const y = this.mouseY;

        // Mode-specific colors
        let color;
        switch (this.mode) {
            case 'attract':
                color = 'rgba(0, 217, 255, '; // Cyan
                break;
            case 'repel':
                color = 'rgba(255, 0, 255, '; // Magenta
                break;
            case 'swirl':
                color = 'rgba(255, 215, 0, '; // Gold
                break;
        }

        // Outer glow
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, 60);
        gradient.addColorStop(0, color + '0.3)');
        gradient.addColorStop(0.5, color + '0.1)');
        gradient.addColorStop(1, color + '0)');

        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, 60, 0, Math.PI * 2);
        ctx.fill();

        // Inner ring
        ctx.strokeStyle = color + '0.5)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(x, y, 20, 0, Math.PI * 2);
        ctx.stroke();

        // Center dot
        ctx.fillStyle = color + '0.8)';
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();
    }

    // Animation loop
    animate() {
        const now = performance.now();
        const dt = Math.min((now - this.lastTime) / 1000, 0.1); // Cap delta time
        this.lastTime = now;

        // Calculate FPS
        this.fps = 1 / dt;

        this.update(dt);
        this.render();

        requestAnimationFrame(() => this.animate());
    }

    start() {
        this.lastTime = performance.now();
        this.animate();
    }

    // Spawn burst of particles at position
    spawnBurst(x, y, count = 10) {
        for (let i = 0; i < count; i++) {
            const angle = (i / count) * Math.PI * 2;
            const speed = 2 + Math.random() * 3;

            const particle = new Particle(x, y, {
                hue: Math.random() * 360
            });
            particle.vx = Math.cos(angle) * speed;
            particle.vy = Math.sin(angle) * speed;

            // Replace oldest particle if at limit
            if (this.particles.length >= this.particleCount * 1.2) {
                this.particles.shift();
            }
            this.particles.push(particle);
        }

        return true; // Signal that burst happened (for sound)
    }

    // Wave effect - particles ripple outward in a calming pattern
    waveEffect(x, y) {
        const time = performance.now() * 0.003;
        for (const particle of this.particles) {
            const dx = particle.x - x;
            const dy = particle.y - y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 300 && dist > 10) {
                // Sine wave pushes particles in and out
                const wave = Math.sin(dist * 0.02 - time) * 0.3;
                const angle = Math.atan2(dy, dx);
                particle.applyForce(
                    Math.cos(angle) * wave,
                    Math.sin(angle) * wave
                );
            }
        }
    }

    // Energy boost - all particles get excited and speed up
    energyBoost() {
        for (const particle of this.particles) {
            // Add random velocity
            particle.vx += (Math.random() - 0.5) * 4;
            particle.vy += (Math.random() - 0.5) * 4;
            // Brighten
            particle.lightness = Math.min(80, particle.lightness + 10);
        }
    }

    // Chaos mode - particles go wild with random forces
    chaosMode(x, y) {
        for (const particle of this.particles) {
            const dx = particle.x - x;
            const dy = particle.y - y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 250) {
                // Random jittery forces
                particle.applyForce(
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2
                );
                // Cycle colors faster
                particle.hue = (particle.hue + 5) % 360;
            }
        }
    }
}

// Export for use in app.js
window.ParticleSystem = ParticleSystem;

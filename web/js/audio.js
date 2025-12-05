/**
 * Particle Dance - Audio System
 * Web Audio API for ambient sounds and particle pops
 */

class AudioSystem {
    constructor() {
        this.context = null;
        this.enabled = true;
        this.initialized = false;
        this.masterGain = null;
        this.ambientGain = null;
        this.effectsGain = null;

        // Ambient oscillators
        this.ambientOscs = [];

        // Pop sound pool for performance
        this.popPool = [];
        this.popPoolSize = 10;
        this.nextPop = 0;

        // Volume settings
        this.masterVolume = 0.5;
        this.ambientVolume = 0.3;
        this.effectsVolume = 0.7;
    }

    async init() {
        if (this.initialized) return;

        try {
            // Create audio context (requires user interaction)
            this.context = new (window.AudioContext || window.webkitAudioContext)();

            // Master gain
            this.masterGain = this.context.createGain();
            this.masterGain.gain.value = this.masterVolume;
            this.masterGain.connect(this.context.destination);

            // Ambient gain
            this.ambientGain = this.context.createGain();
            this.ambientGain.gain.value = this.ambientVolume;
            this.ambientGain.connect(this.masterGain);

            // Effects gain
            this.effectsGain = this.context.createGain();
            this.effectsGain.gain.value = this.effectsVolume;
            this.effectsGain.connect(this.masterGain);

            // Pre-create pop sound pool
            this.createPopPool();

            this.initialized = true;
            console.log('Audio system initialized');

            return true;
        } catch (e) {
            console.warn('Audio initialization failed:', e);
            return false;
        }
    }

    resume() {
        if (this.context && this.context.state === 'suspended') {
            this.context.resume();
        }
    }

    createPopPool() {
        // Pre-create oscillators for pop sounds
        for (let i = 0; i < this.popPoolSize; i++) {
            this.popPool.push({
                osc: null,
                gain: null,
                inUse: false
            });
        }
    }

    startAmbient() {
        if (!this.initialized || !this.enabled) return;

        // Stop any existing ambient
        this.stopAmbient();

        // Create layered ambient drone
        // Base frequency - deep hum
        const baseFreq = 55; // A1

        // Layer 1: Sub bass
        const osc1 = this.context.createOscillator();
        const gain1 = this.context.createGain();
        osc1.type = 'sine';
        osc1.frequency.value = baseFreq;
        gain1.gain.value = 0.15;
        osc1.connect(gain1);
        gain1.connect(this.ambientGain);
        osc1.start();
        this.ambientOscs.push({ osc: osc1, gain: gain1 });

        // Layer 2: Fifth harmonic
        const osc2 = this.context.createOscillator();
        const gain2 = this.context.createGain();
        osc2.type = 'sine';
        osc2.frequency.value = baseFreq * 1.5; // Perfect fifth
        gain2.gain.value = 0.08;
        osc2.connect(gain2);
        gain2.connect(this.ambientGain);
        osc2.start();
        this.ambientOscs.push({ osc: osc2, gain: gain2 });

        // Layer 3: Octave with slight detune for warmth
        const osc3 = this.context.createOscillator();
        const gain3 = this.context.createGain();
        osc3.type = 'triangle';
        osc3.frequency.value = baseFreq * 2.01; // Slight detune
        gain3.gain.value = 0.05;
        osc3.connect(gain3);
        gain3.connect(this.ambientGain);
        osc3.start();
        this.ambientOscs.push({ osc: osc3, gain: gain3 });

        // Layer 4: High shimmer (slowly modulated)
        const osc4 = this.context.createOscillator();
        const gain4 = this.context.createGain();
        osc4.type = 'sine';
        osc4.frequency.value = baseFreq * 4;
        gain4.gain.value = 0.02;

        // LFO for shimmer
        const lfo = this.context.createOscillator();
        const lfoGain = this.context.createGain();
        lfo.type = 'sine';
        lfo.frequency.value = 0.1; // Very slow modulation
        lfoGain.gain.value = 0.01;
        lfo.connect(lfoGain);
        lfoGain.connect(gain4.gain);
        lfo.start();

        osc4.connect(gain4);
        gain4.connect(this.ambientGain);
        osc4.start();
        this.ambientOscs.push({ osc: osc4, gain: gain4, lfo });

        // Fade in
        this.ambientGain.gain.setValueAtTime(0, this.context.currentTime);
        this.ambientGain.gain.linearRampToValueAtTime(
            this.ambientVolume,
            this.context.currentTime + 2
        );
    }

    stopAmbient() {
        // Fade out and stop
        if (this.ambientGain && this.context) {
            this.ambientGain.gain.linearRampToValueAtTime(
                0,
                this.context.currentTime + 0.5
            );
        }

        // Stop oscillators after fade
        setTimeout(() => {
            for (const layer of this.ambientOscs) {
                try {
                    layer.osc.stop();
                    layer.osc.disconnect();
                    if (layer.lfo) {
                        layer.lfo.stop();
                        layer.lfo.disconnect();
                    }
                } catch (e) { }
            }
            this.ambientOscs = [];
        }, 600);
    }

    playPop(x, y, canvasWidth, canvasHeight) {
        if (!this.initialized || !this.enabled) return;

        // Get available pop from pool
        let pop = this.popPool[this.nextPop];
        this.nextPop = (this.nextPop + 1) % this.popPoolSize;

        // Create new oscillator for this pop
        const osc = this.context.createOscillator();
        const gain = this.context.createGain();

        // Frequency based on Y position (higher = higher pitch)
        const baseFreq = 200 + (1 - y / canvasHeight) * 600;
        osc.type = 'sine';
        osc.frequency.value = baseFreq;

        // Pan based on X position
        let panner = null;
        if (this.context.createStereoPanner) {
            panner = this.context.createStereoPanner();
            panner.pan.value = (x / canvasWidth) * 2 - 1; // -1 to 1
            osc.connect(gain);
            gain.connect(panner);
            panner.connect(this.effectsGain);
        } else {
            osc.connect(gain);
            gain.connect(this.effectsGain);
        }

        // Quick attack, medium decay envelope
        const now = this.context.currentTime;
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.3, now + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);

        // Pitch drop for "plop" feel
        osc.frequency.setValueAtTime(baseFreq * 1.5, now);
        osc.frequency.exponentialRampToValueAtTime(baseFreq * 0.5, now + 0.1);

        osc.start(now);
        osc.stop(now + 0.2);

        // Cleanup
        osc.onended = () => {
            osc.disconnect();
            gain.disconnect();
            if (panner) panner.disconnect();
        };
    }

    // Play a softer pop for particle movement
    playSoftPop(intensity = 0.5) {
        if (!this.initialized || !this.enabled) return;

        const osc = this.context.createOscillator();
        const gain = this.context.createGain();

        osc.type = 'sine';
        osc.frequency.value = 300 + Math.random() * 200;

        osc.connect(gain);
        gain.connect(this.effectsGain);

        const now = this.context.currentTime;
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.1 * intensity, now + 0.005);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);

        osc.start(now);
        osc.stop(now + 0.1);

        osc.onended = () => {
            osc.disconnect();
            gain.disconnect();
        };
    }

    setEnabled(enabled) {
        this.enabled = enabled;
        if (enabled) {
            this.startAmbient();
        } else {
            this.stopAmbient();
        }
    }

    toggle() {
        this.setEnabled(!this.enabled);
        return this.enabled;
    }

    setMasterVolume(volume) {
        this.masterVolume = Math.max(0, Math.min(1, volume));
        if (this.masterGain) {
            this.masterGain.gain.value = this.masterVolume;
        }
    }
}

// Export
window.AudioSystem = AudioSystem;

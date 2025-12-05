/**
 * Particle Dance - Main Application
 * Orchestrates particles, audio, recording, and UI
 */

class ParticleDanceApp {
    constructor() {
        // Canvas setup
        this.canvas = document.getElementById('particleCanvas');
        this.ctx = this.canvas.getContext('2d');

        // Systems (initialized after user interaction)
        this.particles = null;
        this.audio = null;
        this.recorder = null;

        // State
        this.mode = 'attract';
        this.soundEnabled = true;
        this.isRecording = false;
        this.hasInteracted = false;

        // UI elements
        this.ui = {
            modeIndicator: document.getElementById('mode-indicator'),
            modeText: document.getElementById('mode-text'),
            btnAttract: document.getElementById('btn-attract'),
            btnRepel: document.getElementById('btn-repel'),
            btnSwirl: document.getElementById('btn-swirl'),
            btnSound: document.getElementById('btn-sound'),
            btnFullscreen: document.getElementById('btn-fullscreen'),
            btnRecord: document.getElementById('btn-record'),
            recordingIndicator: document.getElementById('recording-indicator'),
            recTimer: document.getElementById('rec-timer'),
            helpText: document.getElementById('help-text'),
            helpModal: document.getElementById('help-modal'),
            closeHelp: document.getElementById('close-help'),
            soundOn: document.getElementById('sound-on'),
            soundOff: document.getElementById('sound-off')
        };

        // Initialize
        this.init();
    }

    init() {
        this.setupCanvas();
        this.setupEventListeners();
        this.createSystems();

        // Start render loop
        this.particles.start();

        // Fade out help text after 5 seconds
        setTimeout(() => {
            this.ui.helpText.classList.add('fade-out');
        }, 5000);
    }

    setupCanvas() {
        // Set canvas to full window size
        const resize = () => {
            const dpr = window.devicePixelRatio || 1;
            const width = window.innerWidth;
            const height = window.innerHeight;

            // Store old dimensions for scaling
            const oldWidth = this.canvas.width;
            const oldHeight = this.canvas.height;

            // Set display size
            this.canvas.style.width = width + 'px';
            this.canvas.style.height = height + 'px';

            // Set actual size (accounting for DPR for sharpness)
            this.canvas.width = width * dpr;
            this.canvas.height = height * dpr;

            // Scale context for DPR
            this.ctx.scale(dpr, dpr);

            // Update particle system if it exists
            if (this.particles && oldWidth > 0) {
                this.particles.resize(width, height);
            }
        };

        resize();
        window.addEventListener('resize', resize);
    }

    createSystems() {
        // Particle system
        this.particles = new ParticleSystem(this.canvas, {
            particleCount: 300,
            glow: true
        });

        // Audio system
        this.audio = new AudioSystem();

        // Recorder
        this.recorder = new ScreenRecorder(this.canvas, {
            duration: 5000,
            onStart: () => this.onRecordStart(),
            onStop: () => this.onRecordStop(),
            onProgress: (remaining, progress) => this.onRecordProgress(remaining),
            onComplete: (data) => this.onRecordComplete(data),
            onError: (error) => console.error('Record error:', error)
        });
    }

    setupEventListeners() {
        // Mouse events
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseenter', () => this.handleMouseEnter());
        this.canvas.addEventListener('mouseleave', () => this.handleMouseLeave());
        this.canvas.addEventListener('click', (e) => this.handleClick(e));

        // Touch events
        this.canvas.addEventListener('touchstart', (e) => this.handleTouchStart(e), { passive: false });
        this.canvas.addEventListener('touchmove', (e) => this.handleTouchMove(e), { passive: false });
        this.canvas.addEventListener('touchend', () => this.handleTouchEnd());

        // Keyboard events
        document.addEventListener('keydown', (e) => this.handleKeydown(e));

        // Button events
        this.ui.btnAttract.addEventListener('click', () => this.setMode('attract'));
        this.ui.btnRepel.addEventListener('click', () => this.setMode('repel'));
        this.ui.btnSwirl.addEventListener('click', () => this.setMode('swirl'));
        this.ui.btnSound.addEventListener('click', () => this.toggleSound());
        this.ui.btnFullscreen.addEventListener('click', () => this.toggleFullscreen());
        this.ui.btnRecord.addEventListener('click', () => this.toggleRecording());
        this.ui.closeHelp.addEventListener('click', () => this.hideHelp());

        // Close help on click outside
        this.ui.helpModal.addEventListener('click', (e) => {
            if (e.target === this.ui.helpModal) {
                this.hideHelp();
            }
        });
    }

    // First interaction - initialize audio
    async ensureAudioInit() {
        if (!this.hasInteracted) {
            this.hasInteracted = true;
            await this.audio.init();
            if (this.soundEnabled) {
                this.audio.startAmbient();
            }
        }
        this.audio.resume();
    }

    // Mouse handlers
    handleMouseMove(e) {
        this.ensureAudioInit();
        this.particles.setMousePosition(e.clientX, e.clientY, true);
    }

    handleMouseEnter() {
        this.particles.mouseActive = true;
    }

    handleMouseLeave() {
        this.particles.mouseActive = false;
    }

    handleClick(e) {
        this.ensureAudioInit();
        // Spawn particle burst on click
        const spawned = this.particles.spawnBurst(e.clientX, e.clientY, 15);
        if (spawned && this.soundEnabled) {
            this.audio.playPop(e.clientX, e.clientY, this.canvas.width, this.canvas.height);
        }
    }

    // Touch handlers
    handleTouchStart(e) {
        e.preventDefault();
        this.ensureAudioInit();
        const touch = e.touches[0];
        this.particles.setMousePosition(touch.clientX, touch.clientY, true);
    }

    handleTouchMove(e) {
        e.preventDefault();
        const touch = e.touches[0];
        this.particles.setMousePosition(touch.clientX, touch.clientY, true);

        // Occasional soft pops while dragging
        if (Math.random() < 0.1 && this.soundEnabled) {
            this.audio.playSoftPop(0.3);
        }
    }

    handleTouchEnd() {
        this.particles.mouseActive = false;
    }

    // Keyboard handler
    handleKeydown(e) {
        // Ignore if typing in input
        if (e.target.tagName === 'INPUT') return;

        this.ensureAudioInit();

        switch (e.key.toLowerCase()) {
            case 'a':
                this.setMode('attract');
                break;
            case 'r':
                this.setMode('repel');
                break;
            case 's':
                this.setMode('swirl');
                break;
            case 'm':
                this.toggleSound();
                break;
            case 'f':
                this.toggleFullscreen();
                break;
            case ' ':
                e.preventDefault();
                this.toggleRecording();
                break;
            case 'h':
                this.toggleHelp();
                break;
            case 'escape':
                this.hideHelp();
                break;
        }
    }

    // Mode switching
    setMode(mode) {
        this.mode = mode;
        this.particles.setMode(mode);

        // Update UI
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        switch (mode) {
            case 'attract':
                this.ui.btnAttract.classList.add('active');
                this.ui.modeText.textContent = 'ATTRACT';
                break;
            case 'repel':
                this.ui.btnRepel.classList.add('active');
                this.ui.modeText.textContent = 'REPEL';
                break;
            case 'swirl':
                this.ui.btnSwirl.classList.add('active');
                this.ui.modeText.textContent = 'SWIRL';
                break;
        }

        // Show mode indicator briefly
        this.ui.modeIndicator.classList.add('visible');
        clearTimeout(this.modeTimeout);
        this.modeTimeout = setTimeout(() => {
            this.ui.modeIndicator.classList.remove('visible');
        }, 1500);

        // Sound feedback
        if (this.soundEnabled && this.hasInteracted) {
            this.audio.playSoftPop(0.5);
        }
    }

    // Sound toggle
    toggleSound() {
        this.soundEnabled = !this.soundEnabled;
        this.audio.setEnabled(this.soundEnabled);

        // Update UI
        this.ui.soundOn.classList.toggle('hidden', !this.soundEnabled);
        this.ui.soundOff.classList.toggle('hidden', this.soundEnabled);
    }

    // Fullscreen toggle
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(() => {});
        } else {
            document.exitFullscreen();
        }
    }

    // Recording
    toggleRecording() {
        if (this.isRecording) {
            this.recorder.stop();
        } else {
            this.recorder.start();
        }
    }

    onRecordStart() {
        this.isRecording = true;
        this.ui.btnRecord.classList.add('recording');
        this.ui.recordingIndicator.classList.remove('hidden');
        this.ui.recTimer.textContent = '5';
    }

    onRecordStop() {
        this.isRecording = false;
        this.ui.btnRecord.classList.remove('recording');
        this.ui.recordingIndicator.classList.add('hidden');
    }

    onRecordProgress(remaining) {
        this.ui.recTimer.textContent = remaining;
    }

    onRecordComplete(data) {
        // Auto-download
        data.download();

        // Could also show a preview/share modal here
        console.log('Recording complete:', data.filename);
    }

    // Help modal
    toggleHelp() {
        this.ui.helpModal.classList.toggle('hidden');
    }

    hideHelp() {
        this.ui.helpModal.classList.add('hidden');
    }
}

// Start the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ParticleDanceApp();
});

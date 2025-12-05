/**
 * Particle Dance - Main Application
 * Orchestrates particles, audio, hand tracking, and recording
 */

class ParticleDanceApp {
    constructor() {
        // Canvas setup
        this.canvas = document.getElementById('particleCanvas');
        this.ctx = this.canvas.getContext('2d');

        // Systems (initialized after user interaction)
        this.particles = null;
        this.audio = null;
        this.handTracker = null;
        this.recorder = null;

        // State
        this.mode = 'attract';
        this.soundEnabled = true;
        this.handTrackingEnabled = false;
        this.isRecording = false;
        this.hasInteracted = false;
        this.showCameraPrompt = true;

        // Hand tracking state
        this.hands = [];
        this.lastGesture = null;

        // Tutorial state
        this.tutorialActive = false;
        this.tutorialStep = 1;
        this.handDetectedTime = 0;
        this.gestureCompleted = {};

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
            btnHands: document.getElementById('btn-hands'),
            recordingIndicator: document.getElementById('recording-indicator'),
            recTimer: document.getElementById('rec-timer'),
            helpText: document.getElementById('help-text'),
            helpModal: document.getElementById('help-modal'),
            closeHelp: document.getElementById('close-help'),
            soundOn: document.getElementById('sound-on'),
            soundOff: document.getElementById('sound-off'),
            cameraPrompt: document.getElementById('camera-prompt'),
            btnEnableCamera: document.getElementById('btn-enable-camera'),
            btnSkipCamera: document.getElementById('btn-skip-camera'),
            handStatus: document.getElementById('hand-status'),
            handIcon: document.getElementById('hand-icon'),
            handStatusText: document.getElementById('hand-status-text'),
            tutorial: document.getElementById('tutorial'),
            tutorialDone: document.getElementById('tutorial-done'),
            skipTutorial: document.getElementById('skip-tutorial')
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

        // Show camera prompt after short delay (let particles load first)
        setTimeout(() => {
            if (this.showCameraPrompt && !this.isMobile()) {
                this.ui.cameraPrompt.classList.remove('hidden');
            }
        }, 1500);

        // Fade out help text after 5 seconds
        setTimeout(() => {
            this.ui.helpText.classList.add('fade-out');
        }, 5000);
    }

    isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
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

        // Hand tracker
        this.handTracker = new HandTracker({
            onHandsDetected: (hands) => this.onHandsDetected(hands),
            onGesture: (gesture, hand) => this.onGesture(gesture, hand),
            onTrackingLost: () => this.onTrackingLost(),
            onReady: () => this.onHandTrackingReady(),
            onError: (error) => this.onHandTrackingError(error)
        });

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
        this.ui.btnHands.addEventListener('click', () => this.toggleHandTracking());
        this.ui.closeHelp.addEventListener('click', () => this.hideHelp());

        // Camera prompt buttons
        this.ui.btnEnableCamera.addEventListener('click', () => this.enableCamera());
        this.ui.btnSkipCamera.addEventListener('click', () => this.skipCamera());

        // Tutorial buttons
        if (this.ui.tutorialDone) {
            this.ui.tutorialDone.addEventListener('click', () => this.endTutorial());
        }
        if (this.ui.skipTutorial) {
            this.ui.skipTutorial.addEventListener('click', () => this.endTutorial());
        }

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

    // Camera prompt handlers
    async enableCamera() {
        this.ui.cameraPrompt.classList.add('hidden');
        this.showCameraPrompt = false;
        await this.ensureAudioInit();
        await this.startHandTracking();

        // Start tutorial
        this.startTutorial();
    }

    // Tutorial system
    startTutorial() {
        this.tutorialActive = true;
        this.tutorialStep = 1;
        this.gestureCompleted = {};
        this.ui.tutorial.classList.remove('hidden');
        this.showTutorialStep(1);
    }

    showTutorialStep(step) {
        // Hide all steps
        document.querySelectorAll('.tutorial-step').forEach(el => {
            el.classList.add('hidden');
        });

        // Show current step
        const currentStep = document.querySelector(`.tutorial-step[data-step="${step}"]`);
        if (currentStep) {
            currentStep.classList.remove('hidden');
        }

        this.tutorialStep = step;
    }

    advanceTutorial() {
        if (this.tutorialStep < 5) {
            this.tutorialStep++;
            this.showTutorialStep(this.tutorialStep);
        }
    }

    updateTutorialProgress(progress) {
        const progressBar = document.querySelector('.tutorial-progress .progress-bar');
        if (progressBar) {
            progressBar.style.width = `${progress * 100}%`;
        }
    }

    checkTutorialGesture(gestureType) {
        if (!this.tutorialActive) return;

        // Step 1: Waiting for hand detection (handled separately)
        // Step 2: Palm gesture
        if (this.tutorialStep === 2 && gestureType === 'PALM') {
            if (!this.gestureCompleted.palm) {
                this.gestureCompleted.palm = true;
                setTimeout(() => this.advanceTutorial(), 1500);
            }
        }
        // Step 3: Fist gesture
        else if (this.tutorialStep === 3 && gestureType === 'FIST') {
            if (!this.gestureCompleted.fist) {
                this.gestureCompleted.fist = true;
                setTimeout(() => this.advanceTutorial(), 1500);
            }
        }
        // Step 4: Point gesture
        else if (this.tutorialStep === 4 && gestureType === 'POINT') {
            if (!this.gestureCompleted.point) {
                this.gestureCompleted.point = true;
                setTimeout(() => this.advanceTutorial(), 1500);
            }
        }
    }

    endTutorial() {
        this.tutorialActive = false;
        this.ui.tutorial.classList.add('hidden');
    }

    skipCamera() {
        this.ui.cameraPrompt.classList.add('hidden');
        this.showCameraPrompt = false;
    }

    // Hand tracking
    async startHandTracking() {
        const success = await this.handTracker.start();
        if (success) {
            this.handTrackingEnabled = true;
            this.ui.btnHands.classList.add('active');
            this.ui.handStatus.classList.remove('hidden');
        }
    }

    stopHandTracking() {
        this.handTracker.stop();
        this.handTrackingEnabled = false;
        this.ui.btnHands.classList.remove('active');
        this.ui.handStatus.classList.add('hidden');
        this.particles.mouseActive = false;
    }

    async toggleHandTracking() {
        await this.ensureAudioInit();
        if (this.handTrackingEnabled) {
            this.stopHandTracking();
        } else {
            await this.startHandTracking();
        }
    }

    onHandTrackingReady() {
        console.log('Hand tracking ready');
        this.ui.handStatus.classList.add('tracking');
        this.ui.handStatusText.textContent = 'Ready';
    }

    onHandTrackingError(error) {
        console.error('Hand tracking error:', error);
        this.ui.handStatus.classList.add('hidden');
        this.handTrackingEnabled = false;
        this.ui.btnHands.classList.remove('active');
    }

    onHandsDetected(handsData) {
        this.hands = handsData;

        // Update status
        this.ui.handStatus.classList.remove('lost');
        this.ui.handStatus.classList.add('tracking');
        this.ui.handStatusText.textContent = `${handsData.length} hand${handsData.length > 1 ? 's' : ''}`;

        // Tutorial step 1: Track hand detection progress
        if (this.tutorialActive && this.tutorialStep === 1) {
            if (this.handDetectedTime === 0) {
                this.handDetectedTime = Date.now();
            }
            const elapsed = Date.now() - this.handDetectedTime;
            const progress = Math.min(elapsed / 2000, 1); // 2 seconds to complete
            this.updateTutorialProgress(progress);

            if (progress >= 1) {
                this.advanceTutorial();
                this.handDetectedTime = 0;
            }
        }

        // Process each hand
        for (const hand of handsData) {
            // Convert normalized coords to screen coords
            const screenPos = this.handTracker.toScreenCoords(
                hand.palmCenter,
                window.innerWidth,
                window.innerHeight
            );

            // Update particle system with hand position
            this.particles.setMousePosition(screenPos.x, screenPos.y, true);

            // Set mode based on gesture
            this.handleGestureMode(hand.gesture);
        }

        // Two-hand gesture
        if (handsData.twoHandGesture) {
            this.handleTwoHandGesture(handsData.twoHandGesture);
        }
    }

    onGesture(gesture, hand) {
        // Only play sound if gesture changed
        if (gesture.type !== this.lastGesture) {
            this.lastGesture = gesture.type;
            this.playGestureSound(gesture.type);

            // Check tutorial progress
            this.checkTutorialGesture(gesture.type);
        }
    }

    handleGestureMode(gesture) {
        switch (gesture.type) {
            case 'PALM':
                if (this.mode !== 'attract') this.setMode('attract', true);
                break;
            case 'FIST':
                if (this.mode !== 'repel') this.setMode('repel', true);
                break;
            case 'SPREAD':
                // Explosion effect
                this.particles.spawnBurst(
                    this.particles.mouseX,
                    this.particles.mouseY,
                    20
                );
                break;
            case 'PINCH':
                // Spawn particles at pinch point
                this.particles.spawnBurst(
                    this.particles.mouseX,
                    this.particles.mouseY,
                    5
                );
                break;
            case 'POINT':
                if (this.mode !== 'swirl') this.setMode('swirl', true);
                break;
        }
    }

    handleTwoHandGesture(gesture) {
        if (gesture.type === 'MERGE') {
            // Pull all particles toward center
            const centerX = gesture.center.x * window.innerWidth;
            const centerY = gesture.center.y * window.innerHeight;
            this.particles.setMousePosition(centerX, centerY, true);
            this.particles.forceStrength = 0.8 * gesture.strength;
        } else if (gesture.type === 'EXPAND') {
            // Push particles outward
            this.particles.forceStrength = -0.5 * gesture.strength;
        }
    }

    playGestureSound(gestureType) {
        if (!this.soundEnabled || !this.hasInteracted) return;

        switch (gestureType) {
            case 'PALM':
                this.audio.playSoftPop(0.3);
                break;
            case 'FIST':
                this.audio.playPop(
                    this.particles.mouseX,
                    this.particles.mouseY,
                    window.innerWidth,
                    window.innerHeight
                );
                break;
            case 'PINCH':
                this.audio.playPop(
                    this.particles.mouseX,
                    this.particles.mouseY,
                    window.innerWidth,
                    window.innerHeight
                );
                break;
            case 'SPREAD':
                // Multiple pops for explosion
                for (let i = 0; i < 3; i++) {
                    setTimeout(() => this.audio.playSoftPop(0.5), i * 50);
                }
                break;
        }
    }

    onTrackingLost() {
        this.ui.handStatus.classList.remove('tracking');
        this.ui.handStatus.classList.add('lost');
        this.ui.handStatusText.textContent = 'Show hand';
        this.particles.mouseActive = false;

        // Reset tutorial hand detection timer
        if (this.tutorialActive && this.tutorialStep === 1) {
            this.handDetectedTime = 0;
            this.updateTutorialProgress(0);
        }
    }

    // Mouse handlers
    handleMouseMove(e) {
        if (this.handTrackingEnabled) return; // Hand tracking takes priority

        this.ensureAudioInit();
        this.particles.setMousePosition(e.clientX, e.clientY, true);
    }

    handleMouseEnter() {
        if (!this.handTrackingEnabled) {
            this.particles.mouseActive = true;
        }
    }

    handleMouseLeave() {
        if (!this.handTrackingEnabled) {
            this.particles.mouseActive = false;
        }
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
            case 'w':
                this.toggleHandTracking();
                break;
            case 'escape':
                this.hideHelp();
                if (this.ui.cameraPrompt) {
                    this.ui.cameraPrompt.classList.add('hidden');
                }
                break;
        }
    }

    // Mode switching
    setMode(mode, silent = false) {
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

        // Sound feedback (unless silent mode for hand gestures)
        if (!silent && this.soundEnabled && this.hasInteracted) {
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

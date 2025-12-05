/**
 * Particle Dance - Hand Tracking System
 * MediaPipe Hands integration for gesture control
 */

class HandTracker {
    constructor(options = {}) {
        this.enabled = false;
        this.initialized = false;
        this.hands = null;
        this.camera = null;
        this.videoElement = null;

        // Callbacks
        this.onHandsDetected = options.onHandsDetected || (() => {});
        this.onGesture = options.onGesture || (() => {});
        this.onTrackingLost = options.onTrackingLost || (() => {});
        this.onError = options.onError || (() => {});
        this.onReady = options.onReady || (() => {});

        // Landmark indices
        this.THUMB_TIP = 4;
        this.INDEX_TIP = 8;
        this.MIDDLE_TIP = 12;
        this.RING_TIP = 16;
        this.PINKY_TIP = 20;
        this.WRIST = 0;
        this.PALM_BASE = 9;

        // Thresholds
        this.PINCH_THRESHOLD = 0.08;
        this.SPREAD_THRESHOLD = 0.25;
        this.WAVE_THRESHOLD = 0.02;

        // Gesture smoothing
        this.gestureBuffer = [];
        this.bufferSize = 5;

        // Hand state
        this.leftHand = null;
        this.rightHand = null;
        this.lastHandPositions = {};

        // Detection state
        this.handsDetected = false;
        this.lastDetectionTime = 0;
    }

    async init() {
        if (this.initialized) return true;

        try {
            // Check if MediaPipe is available
            if (typeof Hands === 'undefined') {
                throw new Error('MediaPipe Hands not loaded');
            }

            // Create video element for camera
            this.videoElement = document.createElement('video');
            this.videoElement.style.display = 'none';
            this.videoElement.setAttribute('playsinline', '');
            document.body.appendChild(this.videoElement);

            // Initialize MediaPipe Hands
            this.hands = new Hands({
                locateFile: (file) => {
                    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
                }
            });

            this.hands.setOptions({
                maxNumHands: 2,
                modelComplexity: 1,
                minDetectionConfidence: 0.7,
                minTrackingConfidence: 0.5
            });

            this.hands.onResults((results) => this.processResults(results));

            this.initialized = true;
            console.log('Hand tracking initialized');
            return true;

        } catch (e) {
            console.error('Hand tracking init failed:', e);
            this.onError('Hand tracking not available');
            return false;
        }
    }

    async start() {
        if (!this.initialized) {
            const success = await this.init();
            if (!success) return false;
        }

        try {
            // Request camera permission
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: 640,
                    height: 480,
                    facingMode: 'user'
                }
            });

            this.videoElement.srcObject = stream;
            await this.videoElement.play();

            // Start camera processing
            this.camera = new Camera(this.videoElement, {
                onFrame: async () => {
                    if (this.enabled) {
                        await this.hands.send({ image: this.videoElement });
                    }
                },
                width: 640,
                height: 480
            });

            await this.camera.start();
            this.enabled = true;
            this.onReady();

            console.log('Hand tracking started');
            return true;

        } catch (e) {
            console.error('Camera access failed:', e);
            if (e.name === 'NotAllowedError') {
                this.onError('Camera permission denied');
            } else {
                this.onError('Camera not available');
            }
            return false;
        }
    }

    stop() {
        this.enabled = false;
        if (this.camera) {
            this.camera.stop();
        }
        if (this.videoElement && this.videoElement.srcObject) {
            this.videoElement.srcObject.getTracks().forEach(track => track.stop());
        }
    }

    processResults(results) {
        if (!results.multiHandLandmarks || results.multiHandLandmarks.length === 0) {
            // No hands detected
            if (this.handsDetected) {
                this.handsDetected = false;
                this.onTrackingLost();
            }
            return;
        }

        this.handsDetected = true;
        this.lastDetectionTime = performance.now();

        const handsData = [];

        for (let i = 0; i < results.multiHandLandmarks.length; i++) {
            const landmarks = results.multiHandLandmarks[i];
            const handedness = results.multiHandedness[i];
            const isLeft = handedness.label === 'Left';

            // Get palm center (average of key points)
            const palmCenter = this.getPalmCenter(landmarks);

            // Detect gesture
            const gesture = this.detectGesture(landmarks);

            // Smooth gesture
            const smoothedGesture = this.smoothGesture(gesture, isLeft ? 'left' : 'right');

            const handData = {
                landmarks,
                palmCenter,
                gesture: smoothedGesture,
                isLeft,
                handedness: handedness.label
            };

            handsData.push(handData);

            // Store for two-hand detection
            if (isLeft) {
                this.leftHand = handData;
            } else {
                this.rightHand = handData;
            }
        }

        // Check for two-hand gestures
        if (this.leftHand && this.rightHand) {
            const twoHandGesture = this.detectTwoHandGesture();
            if (twoHandGesture) {
                handsData.twoHandGesture = twoHandGesture;
            }
        }

        this.onHandsDetected(handsData);

        // Trigger gesture callbacks
        for (const hand of handsData) {
            this.onGesture(hand.gesture, hand);
        }
    }

    getPalmCenter(landmarks) {
        // Use wrist and middle finger base for stable palm center
        const wrist = landmarks[this.WRIST];
        const palmBase = landmarks[this.PALM_BASE];

        return {
            x: (wrist.x + palmBase.x) / 2,
            y: (wrist.y + palmBase.y) / 2,
            z: (wrist.z + palmBase.z) / 2
        };
    }

    detectGesture(landmarks) {
        const fingersExtended = this.countExtendedFingers(landmarks);
        const pinchDistance = this.distance(landmarks[this.THUMB_TIP], landmarks[this.INDEX_TIP]);
        const fingerSpread = this.calculateFingerSpread(landmarks);

        // Pinch (highest priority)
        if (pinchDistance < this.PINCH_THRESHOLD && fingersExtended <= 2) {
            return { type: 'PINCH', confidence: 0.9, pinchDistance };
        }

        // Fist
        if (fingersExtended === 0) {
            return { type: 'FIST', confidence: 0.95 };
        }

        // Spread (open + wide apart)
        if (fingersExtended === 5 && fingerSpread > this.SPREAD_THRESHOLD) {
            return { type: 'SPREAD', confidence: 0.85, spread: fingerSpread };
        }

        // Open palm
        if (fingersExtended >= 4) {
            return { type: 'PALM', confidence: 0.9, fingersExtended };
        }

        // Pointing (index only)
        if (fingersExtended === 1 && this.isFingerExtended(landmarks, this.INDEX_TIP)) {
            return { type: 'POINT', confidence: 0.8 };
        }

        return { type: 'NEUTRAL', confidence: 0.5 };
    }

    countExtendedFingers(landmarks) {
        let count = 0;

        // Thumb (check x distance from palm)
        const thumbExtended = landmarks[this.THUMB_TIP].x < landmarks[this.THUMB_TIP - 2].x - 0.02;
        if (thumbExtended) count++;

        // Other fingers (check y position relative to knuckle)
        const fingerTips = [this.INDEX_TIP, this.MIDDLE_TIP, this.RING_TIP, this.PINKY_TIP];
        for (const tip of fingerTips) {
            if (this.isFingerExtended(landmarks, tip)) {
                count++;
            }
        }

        return count;
    }

    isFingerExtended(landmarks, tipIndex) {
        const tip = landmarks[tipIndex];
        const pip = landmarks[tipIndex - 2]; // Middle joint
        return tip.y < pip.y - 0.02; // Tip is above middle joint
    }

    calculateFingerSpread(landmarks) {
        // Distance between index and pinky tips
        return this.distance(landmarks[this.INDEX_TIP], landmarks[this.PINKY_TIP]);
    }

    distance(p1, p2) {
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const dz = (p1.z || 0) - (p2.z || 0);
        return Math.sqrt(dx * dx + dy * dy + dz * dz);
    }

    smoothGesture(gesture, handId) {
        if (!this.gestureBuffer[handId]) {
            this.gestureBuffer[handId] = [];
        }

        const buffer = this.gestureBuffer[handId];
        buffer.push(gesture.type);

        if (buffer.length > this.bufferSize) {
            buffer.shift();
        }

        // Return most common gesture in buffer
        const counts = {};
        for (const g of buffer) {
            counts[g] = (counts[g] || 0) + 1;
        }

        let maxCount = 0;
        let smoothedType = gesture.type;
        for (const [type, count] of Object.entries(counts)) {
            if (count > maxCount) {
                maxCount = count;
                smoothedType = type;
            }
        }

        return { ...gesture, type: smoothedType, raw: gesture.type };
    }

    detectTwoHandGesture() {
        if (!this.leftHand || !this.rightHand) return null;

        const leftPalm = this.leftHand.palmCenter;
        const rightPalm = this.rightHand.palmCenter;
        const palmDistance = this.distance(leftPalm, rightPalm);

        // Hands coming together = merge
        if (palmDistance < 0.15) {
            return {
                type: 'MERGE',
                strength: 1 - (palmDistance / 0.15),
                center: {
                    x: (leftPalm.x + rightPalm.x) / 2,
                    y: (leftPalm.y + rightPalm.y) / 2
                }
            };
        }

        // Hands far apart = expand
        if (palmDistance > 0.5) {
            return {
                type: 'EXPAND',
                strength: Math.min(1, (palmDistance - 0.5) / 0.3)
            };
        }

        return null;
    }

    // Convert normalized coordinates to screen coordinates
    toScreenCoords(normalized, canvasWidth, canvasHeight) {
        return {
            x: (1 - normalized.x) * canvasWidth, // Mirror horizontally
            y: normalized.y * canvasHeight
        };
    }
}

// Export
window.HandTracker = HandTracker;

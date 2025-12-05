/**
 * Particle Dance - Hand Tracking System
 * MediaPipe Hands integration for gesture control
 */

class HandTracker {
    constructor(options = {}) {
        this.enabled = false;
        this.initialized = false;
        this.hands = null;
        this.videoElement = null;
        this.animationId = null;

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

        // Gesture smoothing
        this.gestureBuffer = {};
        this.bufferSize = 5;

        // Hand state
        this.leftHand = null;
        this.rightHand = null;

        // Detection state
        this.handsDetected = false;
    }

    async init() {
        if (this.initialized) return true;

        try {
            // Check if MediaPipe is available
            if (typeof Hands === 'undefined') {
                console.error('MediaPipe Hands not loaded');
                throw new Error('MediaPipe Hands not loaded');
            }

            console.log('Initializing MediaPipe Hands...');

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
            console.log('MediaPipe Hands initialized');
            return true;

        } catch (e) {
            console.error('Hand tracking init failed:', e);
            this.onError('Hand tracking not available: ' + e.message);
            return false;
        }
    }

    async start() {
        if (!this.initialized) {
            const success = await this.init();
            if (!success) return false;
        }

        try {
            console.log('Requesting camera access...');

            // Request camera permission
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            });

            console.log('Camera access granted');

            // Create video element
            this.videoElement = document.createElement('video');
            this.videoElement.srcObject = stream;
            this.videoElement.setAttribute('playsinline', '');
            this.videoElement.style.display = 'none';
            document.body.appendChild(this.videoElement);

            // Wait for video to be ready
            await new Promise((resolve) => {
                this.videoElement.onloadedmetadata = () => {
                    this.videoElement.play();
                    resolve();
                };
            });

            console.log('Video ready, starting hand detection loop...');

            this.enabled = true;
            this.onReady();

            // Start processing loop
            this.processFrame();

            return true;

        } catch (e) {
            console.error('Camera access failed:', e);
            if (e.name === 'NotAllowedError') {
                this.onError('Camera permission denied');
            } else {
                this.onError('Camera not available: ' + e.message);
            }
            return false;
        }
    }

    async processFrame() {
        if (!this.enabled || !this.videoElement) return;

        try {
            await this.hands.send({ image: this.videoElement });
        } catch (e) {
            console.error('Error processing frame:', e);
        }

        // Continue loop
        this.animationId = requestAnimationFrame(() => this.processFrame());
    }

    stop() {
        this.enabled = false;

        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }

        if (this.videoElement && this.videoElement.srcObject) {
            this.videoElement.srcObject.getTracks().forEach(track => track.stop());
            this.videoElement.remove();
            this.videoElement = null;
        }
    }

    processResults(results) {
        if (!results.multiHandLandmarks || results.multiHandLandmarks.length === 0) {
            if (this.handsDetected) {
                this.handsDetected = false;
                this.onTrackingLost();
            }
            return;
        }

        this.handsDetected = true;
        const handsData = [];

        for (let i = 0; i < results.multiHandLandmarks.length; i++) {
            const landmarks = results.multiHandLandmarks[i];
            const handedness = results.multiHandedness[i];
            const isLeft = handedness.label === 'Left';

            // Get palm center
            const palmCenter = this.getPalmCenter(landmarks);

            // Detect gesture
            const gesture = this.detectGesture(landmarks);

            // Smooth gesture
            const handId = isLeft ? 'left' : 'right';
            const smoothedGesture = this.smoothGesture(gesture, handId);

            const handData = {
                landmarks,
                palmCenter,
                gesture: smoothedGesture,
                isLeft,
                handedness: handedness.label
            };

            handsData.push(handData);

            if (isLeft) {
                this.leftHand = handData;
            } else {
                this.rightHand = handData;
            }
        }

        // Check for two-hand gestures
        if (this.leftHand && this.rightHand && results.multiHandLandmarks.length === 2) {
            const twoHandGesture = this.detectTwoHandGesture();
            if (twoHandGesture) {
                handsData.twoHandGesture = twoHandGesture;
            }
        }

        this.onHandsDetected(handsData);

        for (const hand of handsData) {
            this.onGesture(hand.gesture, hand);
        }
    }

    getPalmCenter(landmarks) {
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

        // Thumb
        const thumbExtended = Math.abs(landmarks[this.THUMB_TIP].x - landmarks[this.WRIST].x) > 0.1;
        if (thumbExtended) count++;

        // Other fingers
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
        const pip = landmarks[tipIndex - 2];
        return tip.y < pip.y - 0.02;
    }

    calculateFingerSpread(landmarks) {
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

        if (palmDistance > 0.5) {
            return {
                type: 'EXPAND',
                strength: Math.min(1, (palmDistance - 0.5) / 0.3)
            };
        }

        return null;
    }

    toScreenCoords(normalized, canvasWidth, canvasHeight) {
        return {
            x: (1 - normalized.x) * canvasWidth,
            y: normalized.y * canvasHeight
        };
    }
}

// Export
window.HandTracker = HandTracker;

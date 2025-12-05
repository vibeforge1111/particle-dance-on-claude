/**
 * Particle Dance - Screen Recorder
 * MediaRecorder API for capturing 5-second clips
 */

class ScreenRecorder {
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.duration = options.duration || 5000; // 5 seconds
        this.frameRate = options.frameRate || 30;

        this.mediaRecorder = null;
        this.chunks = [];
        this.isRecording = false;
        this.recordingTimeout = null;

        // Callbacks
        this.onStart = options.onStart || (() => {});
        this.onStop = options.onStop || (() => {});
        this.onProgress = options.onProgress || (() => {});
        this.onComplete = options.onComplete || (() => {});
        this.onError = options.onError || (() => {});

        // Check support
        this.supported = this.checkSupport();
    }

    checkSupport() {
        return !!(
            this.canvas.captureStream &&
            window.MediaRecorder &&
            MediaRecorder.isTypeSupported('video/webm')
        );
    }

    start() {
        if (!this.supported) {
            this.onError('Recording not supported in this browser');
            return false;
        }

        if (this.isRecording) {
            return false;
        }

        try {
            // Get stream from canvas
            const stream = this.canvas.captureStream(this.frameRate);

            // Determine best codec
            let mimeType = 'video/webm;codecs=vp9';
            if (!MediaRecorder.isTypeSupported(mimeType)) {
                mimeType = 'video/webm;codecs=vp8';
            }
            if (!MediaRecorder.isTypeSupported(mimeType)) {
                mimeType = 'video/webm';
            }

            // Create recorder
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType,
                videoBitsPerSecond: 5000000 // 5 Mbps for quality
            });

            this.chunks = [];

            this.mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    this.chunks.push(e.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                this.finalizeRecording();
            };

            this.mediaRecorder.onerror = (e) => {
                console.error('MediaRecorder error:', e);
                this.onError('Recording failed');
                this.isRecording = false;
            };

            // Start recording
            this.mediaRecorder.start(100); // Collect data every 100ms
            this.isRecording = true;
            this.onStart();

            // Progress updates
            let elapsed = 0;
            const progressInterval = setInterval(() => {
                elapsed += 100;
                const remaining = Math.ceil((this.duration - elapsed) / 1000);
                this.onProgress(remaining, elapsed / this.duration);

                if (!this.isRecording) {
                    clearInterval(progressInterval);
                }
            }, 100);

            // Auto-stop after duration
            this.recordingTimeout = setTimeout(() => {
                this.stop();
            }, this.duration);

            return true;

        } catch (e) {
            console.error('Failed to start recording:', e);
            this.onError('Failed to start recording');
            return false;
        }
    }

    stop() {
        if (!this.isRecording || !this.mediaRecorder) {
            return;
        }

        clearTimeout(this.recordingTimeout);
        this.isRecording = false;

        try {
            this.mediaRecorder.stop();
        } catch (e) {
            console.error('Error stopping recorder:', e);
        }

        this.onStop();
    }

    finalizeRecording() {
        if (this.chunks.length === 0) {
            this.onError('No recording data');
            return;
        }

        // Create blob from chunks
        const blob = new Blob(this.chunks, { type: 'video/webm' });
        this.chunks = [];

        // Generate filename with timestamp
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        const filename = `particle-dance-${timestamp}.webm`;

        // Create download
        const url = URL.createObjectURL(blob);

        this.onComplete({
            blob,
            url,
            filename,
            download: () => this.downloadBlob(url, filename)
        });
    }

    downloadBlob(url, filename) {
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // Revoke URL after download
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    }
}

// Export
window.ScreenRecorder = ScreenRecorder;

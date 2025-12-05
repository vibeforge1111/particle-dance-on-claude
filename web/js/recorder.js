/**
 * Particle Dance - Screen Recorder
 * Performance-optimized MediaRecorder for smooth 5-second clips
 */

class ScreenRecorder {
    constructor(canvas, options = {}) {
        this.canvas = canvas;
        this.duration = options.duration || 5000; // 5 seconds
        // Lower frame rate for better performance - 30fps is plenty for sharing
        this.frameRate = options.frameRate || 30;

        this.mediaRecorder = null;
        this.chunks = [];
        this.isRecording = false;
        this.recordingTimeout = null;
        this.progressInterval = null;

        // Callbacks
        this.onStart = options.onStart || (() => {});
        this.onStop = options.onStop || (() => {});
        this.onProgress = options.onProgress || (() => {});
        this.onComplete = options.onComplete || (() => {});
        this.onError = options.onError || (() => {});

        // Check support and best codec
        this.supported = this.checkSupport();
        this.mimeType = this.getBestMimeType();
    }

    checkSupport() {
        return !!(
            this.canvas.captureStream &&
            window.MediaRecorder
        );
    }

    getBestMimeType() {
        // Prefer VP8 over VP9 for better performance (VP9 encoding is CPU-heavy)
        const codecs = [
            'video/webm;codecs=vp8',
            'video/webm',
            'video/mp4'
        ];

        for (const codec of codecs) {
            if (MediaRecorder.isTypeSupported(codec)) {
                console.log('Using codec:', codec);
                return codec;
            }
        }
        return 'video/webm';
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
            // Get stream from canvas - lower frame rate for performance
            const stream = this.canvas.captureStream(this.frameRate);

            // Create recorder with performance-optimized settings
            const options = {
                mimeType: this.mimeType,
                // Lower bitrate for better performance (2.5 Mbps is good for web sharing)
                videoBitsPerSecond: 2500000
            };

            this.mediaRecorder = new MediaRecorder(stream, options);
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
                this.cleanup();
            };

            // Start recording - collect data less frequently for better performance
            this.mediaRecorder.start(500); // Every 500ms (less CPU overhead)
            this.isRecording = true;
            this.onStart();

            // Progress updates
            const startTime = Date.now();
            this.progressInterval = setInterval(() => {
                const elapsed = Date.now() - startTime;
                const remaining = Math.ceil((this.duration - elapsed) / 1000);
                this.onProgress(remaining, elapsed / this.duration);

                if (!this.isRecording) {
                    clearInterval(this.progressInterval);
                }
            }, 100);

            // Auto-stop after duration
            this.recordingTimeout = setTimeout(() => {
                this.stop();
            }, this.duration);

            return true;

        } catch (e) {
            console.error('Failed to start recording:', e);
            this.onError('Failed to start recording: ' + e.message);
            return false;
        }
    }

    stop() {
        if (!this.isRecording || !this.mediaRecorder) {
            return;
        }

        this.cleanup();

        try {
            if (this.mediaRecorder.state !== 'inactive') {
                this.mediaRecorder.stop();
            }
        } catch (e) {
            console.error('Error stopping recorder:', e);
        }

        this.onStop();
    }

    cleanup() {
        this.isRecording = false;
        if (this.recordingTimeout) {
            clearTimeout(this.recordingTimeout);
            this.recordingTimeout = null;
        }
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    finalizeRecording() {
        if (this.chunks.length === 0) {
            this.onError('No recording data');
            return;
        }

        // Create blob from chunks
        const blob = new Blob(this.chunks, { type: this.mimeType });
        this.chunks = [];

        // Generate filename with timestamp
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        const extension = this.mimeType.includes('mp4') ? 'mp4' : 'webm';
        const filename = `particle-dance-${timestamp}.${extension}`;

        // Create download URL
        const url = URL.createObjectURL(blob);

        console.log(`Recording complete: ${(blob.size / 1024 / 1024).toFixed(2)} MB`);

        this.onComplete({
            blob,
            url,
            filename,
            size: blob.size,
            download: () => this.downloadBlob(url, filename)
        });
    }

    downloadBlob(url, filename) {
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // Revoke URL after download
        setTimeout(() => URL.revokeObjectURL(url), 5000);
    }
}

// Export
window.ScreenRecorder = ScreenRecorder;

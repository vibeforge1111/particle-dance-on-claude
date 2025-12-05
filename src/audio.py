"""
ASMR Audio system with layered sounds and binaural beats.
"""
import pygame
import math
import random
import numpy as np


class AudioSystem:
    """Manages layered ASMR audio feedback."""

    def __init__(self):
        # Initialize pygame mixer with good audio quality
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)  # Allow many simultaneous sounds

        self.master_volume = 0.7
        self.ambient_volume = 0.3
        self.interaction_volume = 0.5

        # Sound pools for variation
        self.pop_sounds = []
        self.whoosh_sounds = []
        self.chime_sounds = []
        self.touch_pops = []  # Light pops for particle collision

        # Ambient state
        self.ambient_channel = None
        self.binaural_channel = None
        self.ambient_playing = False
        self.binaural_enabled = False

        # Gravity shift sound
        self.gravity_shift_sound = None

        # Generate procedural sounds
        self._generate_sounds()

    def _generate_sounds(self):
        """Generate procedural ASMR sounds."""
        sample_rate = 44100

        # Generate soft pop sounds (5 variations)
        for i in range(5):
            duration = 0.1 + random.uniform(0, 0.1)
            pop = self._create_pop_sound(sample_rate, duration, 200 + i * 50)
            self.pop_sounds.append(pop)

        # Generate very light touch pops (for particle collisions)
        for i in range(8):
            duration = 0.05 + random.uniform(0, 0.05)
            pitch = 300 + i * 80 + random.uniform(-20, 20)
            pop = self._create_touch_pop(sample_rate, duration, pitch)
            self.touch_pops.append(pop)

        # Generate whoosh sounds (3 variations)
        for i in range(3):
            duration = 0.4 + random.uniform(0, 0.3)
            whoosh = self._create_whoosh_sound(sample_rate, duration)
            self.whoosh_sounds.append(whoosh)

        # Generate chime/spawn sound
        chime = self._create_chime_sound(sample_rate, 0.8)
        self.chime_sounds.append(chime)

        # Generate ambient drone
        self.ambient_drone = self._create_ambient_drone(sample_rate, 10.0)

        # Generate binaural beat drone (theta waves ~6Hz for relaxation)
        self.binaural_drone = self._create_binaural_drone(sample_rate, 10.0, 6.0)

        # Generate merge thonk sound
        self.merge_sound = self._create_merge_sound(sample_rate, 0.25)

        # Generate swirl sound
        self.swirl_sound = self._create_swirl_sound(sample_rate, 1.5)

        # Generate gravity shift sound (deep bass)
        self.gravity_shift_sound = self._create_gravity_shift_sound(sample_rate, 0.5)

        # Generate resonant tone for two-hands merge
        self.resonant_tone = self._create_resonant_tone(sample_rate, 1.0)

    def _create_touch_pop(self, sample_rate, duration, base_freq):
        """Create a very light touch pop for particle collision."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Very quick, soft pop
        freq = base_freq * np.exp(-t * 50)
        wave = np.sin(2 * np.pi * freq * t)

        # Very quick envelope
        envelope = np.exp(-t * 40) * (1 - np.exp(-t * 500))
        wave *= envelope * 0.15

        # Slight noise texture
        noise = np.random.uniform(-0.02, 0.02, samples)
        noise *= np.exp(-t * 50)
        wave += noise

        return self._array_to_sound(wave, sample_rate)

    def _create_pop_sound(self, sample_rate, duration, base_freq):
        """Create a soft bubble pop sound."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Quick frequency drop (like a bubble popping)
        freq = base_freq * np.exp(-t * 30)

        # Generate waveform
        wave = np.sin(2 * np.pi * freq * t)

        # Apply envelope (quick attack, medium decay)
        envelope = np.exp(-t * 15) * (1 - np.exp(-t * 200))
        wave *= envelope * 0.3

        # Add some noise for texture
        noise = np.random.uniform(-0.05, 0.05, samples)
        noise *= np.exp(-t * 20)
        wave += noise

        # Low pass filter effect (simple moving average)
        wave = np.convolve(wave, np.ones(5)/5, mode='same')

        return self._array_to_sound(wave, sample_rate)

    def _create_whoosh_sound(self, sample_rate, duration):
        """Create a soft wind whoosh sound."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Filtered noise
        noise = np.random.uniform(-1, 1, samples)

        # Bandpass envelope (rises and falls)
        envelope = np.sin(np.pi * t / duration) ** 2 * 0.2

        # Simple lowpass (moving average)
        kernel_size = 50
        wave = np.convolve(noise, np.ones(kernel_size)/kernel_size, mode='same')
        wave *= envelope

        return self._array_to_sound(wave, sample_rate)

    def _create_chime_sound(self, sample_rate, duration):
        """Create a crystalline chime sound."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Multiple harmonics for bell-like tone
        freqs = [800, 1200, 1600, 2400]
        wave = np.zeros(samples)

        for i, freq in enumerate(freqs):
            amp = 0.3 / (i + 1)
            decay = 3 + i * 0.5
            harmonic = np.sin(2 * np.pi * freq * t) * amp * np.exp(-t * decay)
            wave += harmonic

        # Gentle attack
        attack = 1 - np.exp(-t * 50)
        wave *= attack

        return self._array_to_sound(wave, sample_rate)

    def _create_ambient_drone(self, sample_rate, duration):
        """Create a warm ambient drone loop."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Base frequencies for warm pad
        freqs = [55, 82.5, 110, 165]  # A1, E2, A2, E3 - perfect fifths
        wave = np.zeros(samples)

        for freq in freqs:
            # Slight detuning for warmth
            detune = random.uniform(-0.5, 0.5)
            # Slow amplitude modulation
            mod = 1 + 0.1 * np.sin(2 * np.pi * 0.1 * t + random.uniform(0, 2*np.pi))
            harmonic = np.sin(2 * np.pi * (freq + detune) * t) * mod
            wave += harmonic * 0.15

        # Smooth the loop endpoints
        fade_samples = int(sample_rate * 0.5)
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        wave[:fade_samples] *= fade_in
        wave[-fade_samples:] *= fade_out

        return self._array_to_sound(wave, sample_rate)

    def _create_binaural_drone(self, sample_rate, duration, beat_freq=6.0):
        """Create a binaural beat drone for relaxation (theta waves)."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Base frequency
        base_freq = 100  # Hz

        # Left ear frequency
        left_freq = base_freq
        # Right ear frequency (slightly different to create beat)
        right_freq = base_freq + beat_freq

        # Generate separate channels
        left_wave = np.sin(2 * np.pi * left_freq * t) * 0.2
        right_wave = np.sin(2 * np.pi * right_freq * t) * 0.2

        # Add some harmonics for warmth
        left_wave += np.sin(2 * np.pi * left_freq * 2 * t) * 0.05
        right_wave += np.sin(2 * np.pi * right_freq * 2 * t) * 0.05

        # Smooth loop endpoints
        fade_samples = int(sample_rate * 0.5)
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        left_wave[:fade_samples] *= fade_in
        left_wave[-fade_samples:] *= fade_out
        right_wave[:fade_samples] *= fade_in
        right_wave[-fade_samples:] *= fade_out

        return self._array_to_sound_stereo(left_wave, right_wave, sample_rate)

    def _create_merge_sound(self, sample_rate, duration):
        """Create a satisfying merge/thonk sound."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Low thud with quick pitch drop
        freq = 150 * np.exp(-t * 20)
        wave = np.sin(2 * np.pi * freq * t)

        # Quick punch envelope
        envelope = np.exp(-t * 8) * (1 - np.exp(-t * 100))
        wave *= envelope * 0.5

        # Add subtle click
        click = np.zeros(samples)
        click[:int(sample_rate * 0.01)] = np.random.uniform(-0.3, 0.3, int(sample_rate * 0.01))
        click *= np.exp(-t * 100)

        wave += click

        return self._array_to_sound(wave, sample_rate)

    def _create_swirl_sound(self, sample_rate, duration):
        """Create a spiral/swirl wind sound."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Rising pitch noise
        noise = np.random.uniform(-1, 1, samples)

        # Moving bandpass effect
        wave = np.zeros(samples)
        for i in range(0, samples, 100):
            end = min(i + 100, samples)
            kernel_size = max(10, 50 - int(40 * i / samples))
            if end - i > kernel_size:
                segment = np.convolve(noise[i:end], np.ones(kernel_size)/kernel_size, mode='same')
                wave[i:end] = segment

        # Envelope
        envelope = np.sin(np.pi * t / duration) * 0.15
        wave *= envelope

        return self._array_to_sound(wave, sample_rate)

    def _create_gravity_shift_sound(self, sample_rate, duration):
        """Create a deep bass shift sound for gravity change."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Deep bass sweep
        freq_start = 80
        freq_end = 40
        freq = freq_start + (freq_end - freq_start) * t / duration
        wave = np.sin(2 * np.pi * freq * t)

        # Sub-bass layer
        wave += np.sin(2 * np.pi * 30 * t) * 0.3

        # Envelope
        envelope = np.sin(np.pi * t / duration) ** 0.5 * 0.4
        wave *= envelope

        return self._array_to_sound(wave, sample_rate)

    def _create_resonant_tone(self, sample_rate, duration):
        """Create a warm resonant tone for two-hands merge."""
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)

        # Warm chord (major triad)
        freqs = [220, 277.18, 329.63, 440]  # A3, C#4, E4, A4
        wave = np.zeros(samples)

        for i, freq in enumerate(freqs):
            amp = 0.2 / (i + 1)
            harmonic = np.sin(2 * np.pi * freq * t) * amp
            # Slow modulation
            harmonic *= 1 + 0.1 * np.sin(2 * np.pi * 2 * t)
            wave += harmonic

        # Envelope with slow attack
        attack = 1 - np.exp(-t * 3)
        decay = np.exp(-(t - duration * 0.3) * 2)
        decay = np.clip(decay, 0, 1)
        envelope = attack * decay
        wave *= envelope

        return self._array_to_sound(wave, sample_rate)

    def _array_to_sound(self, wave, sample_rate):
        """Convert numpy array to pygame Sound (mono to stereo)."""
        # Normalize and convert to 16-bit
        wave = np.clip(wave, -1, 1)
        wave_int = (wave * 32767).astype(np.int16)

        # Stereo (same on both channels)
        stereo = np.column_stack((wave_int, wave_int))

        return pygame.sndarray.make_sound(stereo)

    def _array_to_sound_stereo(self, left, right, sample_rate):
        """Convert separate L/R arrays to pygame Sound."""
        left = np.clip(left, -1, 1)
        right = np.clip(right, -1, 1)

        left_int = (left * 32767).astype(np.int16)
        right_int = (right * 32767).astype(np.int16)

        stereo = np.column_stack((left_int, right_int))

        return pygame.sndarray.make_sound(stereo)

    def start_ambient(self):
        """Start the ambient drone loop."""
        if not self.ambient_playing:
            self.ambient_channel = pygame.mixer.Channel(0)
            self.ambient_drone.set_volume(self.ambient_volume * self.master_volume)
            self.ambient_channel.play(self.ambient_drone, loops=-1)
            self.ambient_playing = True

    def stop_ambient(self):
        """Stop the ambient drone."""
        if self.ambient_channel:
            self.ambient_channel.stop()
            self.ambient_playing = False

    def toggle_binaural(self):
        """Toggle binaural beats on/off."""
        self.binaural_enabled = not self.binaural_enabled
        if self.binaural_enabled:
            self.binaural_channel = pygame.mixer.Channel(1)
            self.binaural_drone.set_volume(self.ambient_volume * self.master_volume * 0.5)
            self.binaural_channel.play(self.binaural_drone, loops=-1)
        else:
            if self.binaural_channel:
                self.binaural_channel.stop()
        return self.binaural_enabled

    def play_pop(self, intensity=1.0):
        """Play a random pop sound."""
        sound = random.choice(self.pop_sounds)
        volume = self.interaction_volume * self.master_volume * min(intensity, 1.0)
        sound.set_volume(volume)
        sound.play()

    def play_touch_pop(self, count=1):
        """Play light touch pops for particle collisions."""
        # Play multiple quick pops for many collisions
        for _ in range(min(count, 3)):
            sound = random.choice(self.touch_pops)
            volume = self.interaction_volume * self.master_volume * 0.3
            sound.set_volume(volume)
            sound.play()

    def play_whoosh(self, intensity=1.0):
        """Play a whoosh sound."""
        sound = random.choice(self.whoosh_sounds)
        volume = self.interaction_volume * self.master_volume * min(intensity, 1.0)
        sound.set_volume(volume)
        sound.play()

    def play_spawn(self):
        """Play spawn/chime sound."""
        sound = self.chime_sounds[0]
        sound.set_volume(self.interaction_volume * self.master_volume * 0.6)
        sound.play()

    def play_merge(self):
        """Play merge/thonk sound."""
        self.merge_sound.set_volume(self.interaction_volume * self.master_volume * 0.7)
        self.merge_sound.play()

    def play_swirl(self):
        """Play swirl sound."""
        self.swirl_sound.set_volume(self.interaction_volume * self.master_volume * 0.4)
        self.swirl_sound.play()

    def play_gravity_shift(self):
        """Play gravity shift bass sound."""
        if self.gravity_shift_sound:
            self.gravity_shift_sound.set_volume(self.interaction_volume * self.master_volume * 0.6)
            self.gravity_shift_sound.play()

    def play_resonant_tone(self):
        """Play warm resonant tone for two-hands merge."""
        if self.resonant_tone:
            self.resonant_tone.set_volume(self.interaction_volume * self.master_volume * 0.5)
            self.resonant_tone.play()

    def set_master_volume(self, volume):
        """Set master volume (0-1)."""
        self.master_volume = max(0, min(1, volume))
        if self.ambient_playing and self.ambient_channel:
            self.ambient_drone.set_volume(self.ambient_volume * self.master_volume)
        if self.binaural_enabled and self.binaural_channel:
            self.binaural_drone.set_volume(self.ambient_volume * self.master_volume * 0.5)

    def cleanup(self):
        """Clean up audio resources."""
        self.stop_ambient()
        if self.binaural_channel:
            self.binaural_channel.stop()
        pygame.mixer.quit()

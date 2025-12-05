"""
ASMR Audio system with layered sounds.
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

        # Ambient state
        self.ambient_channel = None
        self.ambient_playing = False

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

        # Generate merge thonk sound
        self.merge_sound = self._create_merge_sound(sample_rate, 0.25)

        # Generate swirl sound
        self.swirl_sound = self._create_swirl_sound(sample_rate, 1.5)

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

    def _array_to_sound(self, wave, sample_rate):
        """Convert numpy array to pygame Sound."""
        # Normalize and convert to 16-bit
        wave = np.clip(wave, -1, 1)
        wave_int = (wave * 32767).astype(np.int16)

        # Stereo
        stereo = np.column_stack((wave_int, wave_int))

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

    def play_pop(self, intensity=1.0):
        """Play a random pop sound."""
        sound = random.choice(self.pop_sounds)
        volume = self.interaction_volume * self.master_volume * min(intensity, 1.0)
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

    def set_master_volume(self, volume):
        """Set master volume (0-1)."""
        self.master_volume = max(0, min(1, volume))
        if self.ambient_playing and self.ambient_channel:
            self.ambient_drone.set_volume(self.ambient_volume * self.master_volume)

    def cleanup(self):
        """Clean up audio resources."""
        self.stop_ambient()
        pygame.mixer.quit()

"""
Settings persistence for GestureFlow.
"""
import json
import os


class Settings:
    """Manages application settings with persistence."""

    DEFAULT_SETTINGS = {
        'volume': 0.7,
        'particle_count': 500,
        'glow': True,
        'trails': True,
        'audio': True,
        'binaural': False,
        'palette': 'default',
        'spatial_audio': True,
        'webcam_overlay': False,
        'gesture_sensitivity': 0.7,
        'first_launch': True,
        'high_contrast': False,
    }

    def __init__(self, config_path=None):
        if config_path is None:
            # Store in user's home directory
            home = os.path.expanduser('~')
            config_dir = os.path.join(home, '.gestureflow')
            os.makedirs(config_dir, exist_ok=True)
            self.config_path = os.path.join(config_dir, 'settings.json')
        else:
            self.config_path = config_path

        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        """Load settings from file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    saved = json.load(f)
                    # Merge with defaults (in case new settings were added)
                    for key, value in saved.items():
                        if key in self.DEFAULT_SETTINGS:
                            self.settings[key] = value
                print(f"Settings loaded from {self.config_path}")
        except Exception as e:
            print(f"Could not load settings: {e}")

    def save(self):
        """Save settings to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
            print(f"Settings saved to {self.config_path}")
        except Exception as e:
            print(f"Could not save settings: {e}")

    def get(self, key, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Set a setting value."""
        if key in self.DEFAULT_SETTINGS:
            self.settings[key] = value
            return True
        return False

    def reset(self):
        """Reset all settings to defaults."""
        self.settings = self.DEFAULT_SETTINGS.copy()

    def is_first_launch(self):
        """Check if this is the first launch."""
        return self.settings.get('first_launch', True)

    def mark_launched(self):
        """Mark that the app has been launched before."""
        self.settings['first_launch'] = False
        self.save()

    def to_dict(self):
        """Return settings as dictionary."""
        return self.settings.copy()

import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}

    def load_sound(self, name, filepath, volume=1.0):
        """Load a sound effect by name with safety checks."""
        if not os.path.exists(filepath):
            print(f"⚠️ Missing sound: {filepath}")
            return

        try:
            snd = pygame.mixer.Sound(filepath)
            snd.set_volume(volume)
            self.sounds[name] = snd
        except Exception as e:
            print(f"❌ Failed to load sound '{filepath}': {e}")

    def load_folder(self, folder_path):
        """Bulk load all WAV/OGG/MP3 files in a folder."""
        if not os.path.exists(folder_path):
            print(f"⚠️ Sound folder not found: {folder_path}")
            return

        for file in os.listdir(folder_path):
            if file.lower().endswith((".wav", ".ogg", ".mp3")):
                name = os.path.splitext(file)[0]  # 'pluck_ping.wav' → 'pluck_ping'
                full_path = os.path.join(folder_path, file)
                self.load_sound(name, full_path)

        print(f"🎵 Loaded {len(self.sounds)} sounds from {folder_path}")

    def play(self, name, volume=1.0):
        """Play a sound effect once."""

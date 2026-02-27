import pygame


class AudioHandler:
    """
    Basic handler for sound effects and music
    """
    
    def __init__(self):
        pygame.mixer.init()
        
        # Music settings
        self.music_volume = 0.7
        self.music_muted = False
        
        # SFX settings
        self.sfx_volume = 0.8
        self.sfx_muted = False
        
        # Cache for loaded sounds
        self.sounds = {}

    # Music

    def play_music(self, name, loops=-1, fade_ms=1000):
        """
        Play background music.
        loops=-1 means infinite.
        """
        pygame.mixer.music.load(f"resources/music/{name}.mp3")
        pygame.mixer.music.set_volume(
            0 if self.music_muted else self.music_volume
        )
        pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)

    def stop_music(self, fade_ms=500):
        pygame.mixer.music.fadeout(fade_ms)

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def set_music_volume(self, volume):
        """Volume range: 0.0 - 1.0"""
        self.music_volume = max(0.0, min(1.0, volume))
        if not self.music_muted:
            pygame.mixer.music.set_volume(self.music_volume)

    def toggle_music_mute(self):
        self.music_muted = not self.music_muted
        pygame.mixer.music.set_volume(0 if self.music_muted else self.music_volume)

    # Sounds

    def load_sound(self, name):
        """Preload a sound and cache it."""
        sound = pygame.mixer.Sound(f"resources/sounds/{name}.mp3")
        sound.set_volume(self.sfx_volume)
        self.sounds[name] = sound

    def play_sound(self, name):
        if name in self.sounds and not self.sfx_muted:
            self.sounds[name].play()

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def toggle_sfx_mute(self):
        self.sfx_muted = not self.sfx_muted
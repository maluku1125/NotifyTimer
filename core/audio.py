import tempfile
import pygame
import os
import sys
from gtts import gTTS


def _resource_path(relative_path):
    """Get absolute path to resource (supports PyInstaller bundled environment)."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # In dev, resolve from project root (parent of core/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, 'assets', relative_path)


def play_ding_sound():
    """播放 ding.wav 音效。"""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        ding_path = _resource_path('ding.wav')
        sound = pygame.mixer.Sound(ding_path)
        sound.set_volume(0.2)
        sound.play()
        # 等待播放完畢
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing ding sound: {e}")


def play_text_to_speech(message, lang='zh-tw'):
    try:
        speech = gTTS(text=message, lang=lang, slow=False)
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Save to a temporary file
        temp_fd, temp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(temp_fd) # Close the file descriptor, gTTS will open it again
        
        speech.save(temp_path)
        
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        # Wait for the music to finish playing so we can delete the file
        # We can't delete it while playing on Windows
        # A better approach is to clean up on next run or exit, but for now we wait
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload() # Unload so the file is freed
        
        # Now try to remove
        try:
             os.remove(temp_path)
        except OSError:
             print(f"Failed to remove temp file {temp_path}, it might still be locked.")

    except Exception as e:
        print(f"Error playing TTS: {e}")

# Call init early
pygame.mixer.init()

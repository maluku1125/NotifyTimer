import tempfile
import pygame
import os
from gtts import gTTS

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

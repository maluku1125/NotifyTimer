from winotify import Notification, audio
import os

def send_windows_notification(title, message, icon_path=None):
    try:
        # Default icon could be the python executable or app icon if provided
        toast = Notification(
            app_id="NotifyTimer",
            title=title,
            msg=message,
            duration="short"
        )
        if icon_path and os.path.exists(icon_path):
            toast.set_audio(audio.Default, loop=False)
            toast.icon = icon_path
        
        toast.show()
    except Exception as e:
        print(f"Failed to send Windows notification: {e}")

import tkinter as tk
import ctypes
import sys
from core.ui import TimerApp

VERSION = "2.2.1"

def main():
    # Set AppUserModelID so Windows taskbar shows custom icon instead of Python default
    if sys.platform == 'win32':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('NotifyTimer.App')

    root = tk.Tk()
    app = TimerApp(root, VERSION)
    root.mainloop()

if __name__ == "__main__":
    main()

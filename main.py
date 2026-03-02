import tkinter as tk
import ctypes
import sys
from ui import TimerApp

def main():
    # 設定 AppUserModelID，讓 Windows 工作列顯示自訂圖標而非 Python 預設圖標
    if sys.platform == 'win32':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('NotifyTimer.App')

    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

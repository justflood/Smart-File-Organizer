import customtkinter as ctk
from gui.app import App
import ctypes

# Fix Taskbar Icon (Windows)
try:
    myappid = 'FloodTechLab.SmartFileOrganizer.v0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

if __name__ == "__main__":
    app = App()
    app.mainloop()

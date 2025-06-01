# src/Inspectores.py
import tkinter as tk
from frames.inspectores.menu_frame import MenuInspectorFrame

class AppInspectores(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inspectores - Parqueo Callejero")
        self.geometry("500x500")
        self.current_frame = None
        self.cambiar_frame(MenuInspectorFrame)

    def cambiar_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

    def volver(self):
        self.cambiar_frame(MenuInspectorFrame)

if __name__ == "__main__":
    app = AppInspectores()
    app.mainloop()

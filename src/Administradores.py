# src/Administradores.py

import tkinter as tk
from frames.administradores.menu_frame import MenuFrame

class AppAdmin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Parqueo Callejero - Administración")
        self.geometry("500x500")
        self.resizable(True, True)

        self.current_frame = None
        self.frame_history = []  # Para mantener un historial de frames
        self.cambiar_frame(MenuFrame)

    def cambiar_frame(self, frame_class, *args):
        if self.current_frame:
            self.frame_history.append((self.current_frame.__class__, args))
            self.current_frame.destroy()

        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

    def volver(self):
        """Vuelve al frame anterior en el historial."""
        if self.frame_history:
            frame_class, args = self.frame_history.pop()
            self.cambiar_frame(frame_class, *args)
        else:
            # Si no hay historial, volver al menú principal
            self.cambiar_frame(MenuFrame)

if __name__ == "__main__":
    app = AppAdmin()
    app.mainloop()

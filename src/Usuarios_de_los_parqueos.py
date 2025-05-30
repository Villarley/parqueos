# src/Usuarios_de_los_parqueos.py

import tkinter as tk
from frames.login_frame import LoginFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Parqueo Callejero - Usuario")
        self.geometry("500x500")
        self.resizable(True, True)

        self.current_frame = None
        self.cambiar_frame(LoginFrame)

    def cambiar_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()

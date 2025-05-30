# src/frames/base_frame.py

import tkinter as tk

class BaseFrame(tk.Frame):
    def __init__(self, master, usuario=None):
        super().__init__(master)
        self.master = master
        self.usuario = usuario

    def volver_al_menu(self):
        """Método común para volver al menú principal"""
        from frames.menu_usuario_frame import MenuUsuarioFrame
        self.master.cambiar_frame(MenuUsuarioFrame, self.usuario)

    def crear_boton_volver(self):
        """Método común para crear el botón de volver"""
        tk.Button(self, text="🔙 Volver al menú", command=self.volver_al_menu).pack(pady=10) 
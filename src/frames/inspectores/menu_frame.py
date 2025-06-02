# src/frames/inspectores/menu_frame.py
import tkinter as tk
from frames.inspectores.revision_frame import RevisionParqueoFrame
from frames.inspectores.reportes_frame import ReportesInspectorFrame
from frames.inspectores.acerca_de_frame import AcercaDeFrame
import os
import subprocess
import sys

class MenuInspectorFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Menú del Inspector", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="🔍 Revisar parqueo", command=lambda: master.cambiar_frame(RevisionParqueoFrame)).pack(pady=5)
        tk.Button(self, text="📊 Reportes", command=lambda: master.cambiar_frame(ReportesInspectorFrame)).pack(pady=5)
        tk.Button(self, text="🧠 Acerca de", command=lambda: master.cambiar_frame(AcercaDeFrame)).pack(pady=5)
        tk.Button(self, text="📘 Ayuda", command=self.abrir_ayuda).pack(pady=5)
        tk.Button(self, text="❌ Cerrar Aplicación", command=master.quit).pack(pady=5)

    def abrir_ayuda(self):
        path_pdf = os.path.abspath("docs/manual_ayuda.pdf")
        try:
            if os.name == 'nt':
                os.startfile(path_pdf)
            elif os.name == 'posix':
                subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', path_pdf])
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo abrir el manual de ayuda.\n{e}")

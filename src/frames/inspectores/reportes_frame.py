# src/frames/inspectores/reportes_frame.py
import tkinter as tk

class ReportesInspectorFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="📊 Reportes de Inspector", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="📄 Lista de espacios", command=self.reporte_espacios).pack(pady=5)
        tk.Button(self, text="⚠️ Historial de multas", command=self.reporte_multas).pack(pady=5)
        tk.Button(self, text="🔙 Volver", command=self.master.volver).pack(pady=5)

        self.resultado = tk.Text(self, width=80, height=20)
        self.resultado.pack(pady=10)

    def reporte_espacios(self):
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, "(Lógica pendiente) Aquí se listarán los espacios...")

    def reporte_multas(self):
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, "(Lógica pendiente) Aquí se mostrará el historial de multas...")

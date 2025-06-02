# src/frames/inspectores/reportes_frame.py

import tkinter as tk
from tkinter import messagebox
import modulo_utiles as mu
from datetime import datetime

ESPACIOS_PATH = "data/pc_espacios.json"
MULTAS_PATH = "data/pc_multas.json"

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
        self.resultado.delete("1.0", tk.END)
        espacios = mu.leer_json(ESPACIOS_PATH)

        if not isinstance(espacios, dict):
            self.resultado.insert(tk.END, "Error: No se pudieron leer los datos de los espacios.")
            return

        ahora = datetime.now()
        reporte = "📄 Lista de espacios de parqueo:\n\n"

        for id_esp, datos in sorted(espacios.items()):
            ocupado = False
            try:
                fin_dt = datetime.strptime(datos.get("fin", ""), "%d/%m/%Y %H:%M")
                ocupado = fin_dt >= ahora
            except:
                ocupado = False

            estado = "🟥 Ocupado" if ocupado else "🟩 Libre"
            reporte += f"{id_esp} - {estado} - Habilitado: {datos.get('habilitado', 'N/A')}\n"

        self.resultado.insert(tk.END, reporte)

    def reporte_multas(self):
        self.resultado.delete("1.0", tk.END)
        multas = mu.leer_json(MULTAS_PATH)

        if not isinstance(multas, list):
            self.resultado.insert(tk.END, "Error: No se pudieron leer los datos de las multas.")
            return

        reporte = "⚠️ Historial de multas:\n\n"
        total = 0

        for m in sorted(multas, key=lambda x: x.get("fecha", ""), reverse=True):
            reporte += (
                f"Fecha: {m.get('fecha', '')}\n"
                f"Espacio: {m.get('espacio', '')}\n"
                f"Placa: {m.get('placa', '')}\n"
                f"Motivo: {m.get('detalle', '')}\n"
                f"Monto: ₡{m.get('monto', 0)}\n"
                f"{'-'*40}\n"
            )
            total += int(m.get("monto", 0))

        reporte += f"\nTotal recaudado en multas: ₡{total}"
        self.resultado.insert(tk.END, reporte)

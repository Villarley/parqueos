# src/frames/inspectores/revision_frame.py

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import modulo_utiles as mu
import modulo_multas as mm

ESPACIOS_PATH = "data/pc_espacios.json"

class RevisionParqueoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="🔎 Revisión de Parqueo", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Ingrese número de espacio:").pack()
        self.espacio_entry = tk.Entry(self)
        self.espacio_entry.pack()

        tk.Label(self, text="Ingrese placa observada:").pack()
        self.placa_entry = tk.Entry(self)
        self.placa_entry.pack()

        tk.Button(self, text="✅ Verificar", command=self.verificar_espacio).pack(pady=10)
        tk.Button(self, text="🔙 Volver", command=self.master.volver).pack(pady=5)

        self.resultado = tk.Text(self, width=70, height=12)
        self.resultado.pack(pady=10)

    def verificar_espacio(self):
        espacio = self.espacio_entry.get().strip().upper()
        placa_observada = self.placa_entry.get().strip().upper()
        ahora = datetime.now()
        self.resultado.delete("1.0", tk.END)

        if not espacio or not placa_observada:
            return messagebox.showwarning("Datos faltantes", "Debe ingresar el espacio y la placa.")

        espacios = mu.leer_json(ESPACIOS_PATH)

        if not isinstance(espacios, dict) or espacio not in espacios:
            return messagebox.showerror("Error", "Espacio no encontrado en el sistema.")

        espacio_info = espacios[espacio]
        fin = espacio_info.get("fin")
        placa_registrada = espacio_info.get("placa", "")

        if not fin:
            detalle = "No hay alquiler registrado en este espacio."
            return self.registrar_multa(espacio, placa_observada, detalle)

        try:
            dt_fin = datetime.strptime(fin, "%d/%m/%Y %H:%M")
        except ValueError:
            detalle = "Formato inválido en la fecha de finalización del alquiler."
            return self.registrar_multa(espacio, placa_observada, detalle)

        if ahora > dt_fin:
            detalle = f"Tiempo vencido | Finalizó: {fin} | Observado: {ahora.strftime('%d/%m/%Y %H:%M')}"
            return self.registrar_multa(espacio, placa_observada, detalle)

        if placa_observada != placa_registrada.upper():
            detalle = f"Placa no coincide | Registrada: {placa_registrada or 'N/A'} | Observada: {placa_observada}"
            return self.registrar_multa(espacio, placa_observada, detalle)

        self.resultado.insert(tk.END, "✅ Espacio en regla. No se registra multa.\n")

    def registrar_multa(self, espacio_id, placa, detalle):
        multa, enviado = mm.registrar_multa(espacio_id, placa, detalle)

        mensaje = (
            f"⚠️ MULTA REGISTRADA\n"
            f"Espacio: {espacio_id}\n"
            f"Placa: {placa}\n"
            f"Detalle: {detalle}\n"
            f"Correo enviado: {'Sí' if enviado else 'No'}"
        )
        self.resultado.insert("1.0", mensaje + "\n")
        messagebox.showwarning("Multa registrada", f"Se ha generado una multa.\n{detalle}")

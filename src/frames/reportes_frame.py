import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_utiles as mu
from modulo_reportes import generar_pdf, enviar_reporte_pdf

class ReportesFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.reporte_actual = ""
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="📊 Reportes de Usuario", font=("Arial", 14)).pack(pady=10)

        tk.Button(self, text="🔍 Buscar parqueos disponibles", command=self.mostrar_disponibles).pack(pady=5)
        tk.Button(self, text="📄 Historial de alquileres", command=self.mostrar_historial_alquileres).pack(pady=5)
        tk.Button(self, text="⚠️ Historial de multas", command=self.mostrar_historial_multas).pack(pady=5)

        self.texto = tk.Text(self, width=80, height=20)
        self.texto.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack()

        tk.Button(btn_frame, text="📥 Guardar como PDF", command=self.guardar_pdf).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="📧 Enviar por correo", command=self.enviar_correo).grid(row=0, column=1, padx=10)

        self.crear_boton_volver()

    def mostrar_disponibles(self):
        espacios = mu.leer_json("data/pc_espacios.json")
        libres = [f"{e['id']}: {e['ubicacion']}" for e in espacios if e["estado"] == "libre"]
        contenido = "Espacios disponibles:\n\n" + "\n".join(libres) if libres else "No hay espacios disponibles."

        self.actualizar_reporte(contenido)

    def mostrar_historial_alquileres(self):
        alquileres = mu.leer_json("data/pc_alquileres.json")
        propios = [a for a in alquileres if a["usuario"] == self.usuario["correo"]]

        if not propios:
            return self.actualizar_reporte("No hay alquileres registrados.")

        contenido = ""
        for a in propios:
            contenido += (
                f"Espacio: {a['espacio_id']}\n"
                f"Inicio: {a['inicio']}\n"
                f"Fin: {a['fin']}\n"
                f"Costo: ₡{a['costo_total']}\n"
                f"Estado: {a['estado']}\n"
                + "-" * 40 + "\n"
            )
        self.actualizar_reporte(contenido)

    def mostrar_historial_multas(self):
        multas = mu.leer_json("data/pc_multas.json")
        propios = [m for m in multas if m["correo"] == self.usuario["correo"]]

        if not propios:
            return self.actualizar_reporte("No hay multas registradas.")

        contenido = ""
        for m in propios:
            contenido += (
                f"Fecha: {m['fecha']}\n"
                f"Espacio: {m['espacio']}\n"
                f"Placa: {m['placa']}\n"
                f"Motivo: {m['detalle']}\n"
                + "-" * 40 + "\n"
            )
        self.actualizar_reporte(contenido)

    def actualizar_reporte(self, texto):
        self.reporte_actual = texto
        self.texto.delete(1.0, tk.END)
        self.texto.insert(tk.END, texto)

    def guardar_pdf(self):
        if not self.reporte_actual:
            return messagebox.showerror("Error", "No hay contenido para guardar.")
        path = generar_pdf(self.usuario['correo'], self.reporte_actual)
        messagebox.showinfo("PDF generado", f"Reporte guardado como:\n{path}")

    def enviar_correo(self):
        if not self.reporte_actual:
            return messagebox.showerror("Error", "No hay contenido para enviar.")
        path = generar_pdf(self.usuario['correo'], self.reporte_actual)
        enviado = enviar_reporte_pdf(self.usuario["correo"], path)
        if enviado:
            messagebox.showinfo("Correo enviado", f"Reporte enviado a {self.usuario['correo']}")
        else:
            messagebox.showerror("Error", "No se pudo enviar el correo.")

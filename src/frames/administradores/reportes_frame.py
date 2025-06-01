import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import modulo_utiles as mu

ALQUILERES_PATH = "data/pc_alquileres.json"
MULTAS_PATH = "data/pc_multas.json"
ESPACIOS_PATH = "data/pc_espacios.json"

class ReportesAdminFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.reporte_actual = ""
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="📊 Reportes Administrativos", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="💵 Ingresos por estacionamiento", command=self.reporte_ingresos).pack(pady=5)
        tk.Button(self, text="📋 Lista de espacios de parqueo", command=self.lista_espacios).pack(pady=5)
        tk.Button(self, text="📆 Historial de espacios usados", command=self.historial_usos).pack(pady=5)
        tk.Button(self, text="⚠️ Historial de multas", command=self.historial_multas).pack(pady=5)

        self.text = tk.Text(self, width=80, height=25)
        self.text.pack(pady=10)

        tk.Button(self, text="🔙 Volver", command=self.master.volver).pack(pady=10)

    # ------------ Reporte 1: Ingresos por fecha ------------
    def reporte_ingresos(self):
        desde = simpledialog.askstring("Desde", "Fecha inicial (dd/mm/yyyy):")
        hasta = simpledialog.askstring("Hasta", "Fecha final (dd/mm/yyyy):")
        if not desde or not hasta:
            return

        try:
            desde_dt = datetime.strptime(desde, "%d/%m/%Y")
            hasta_dt = datetime.strptime(hasta, "%d/%m/%Y")
        except ValueError:
            return messagebox.showerror("Error", "Formato incorrecto. Use dd/mm/yyyy")

        alquileres = mu.leer_json(ALQUILERES_PATH)
        ingresos_por_dia = {}
        total = 0

        for a in alquileres:
            fecha_inicio = datetime.strptime(a["inicio"], "%d/%m/%Y %H:%M")
            fecha = fecha_inicio.date()
            if desde_dt.date() <= fecha <= hasta_dt.date():
                ingresos_por_dia.setdefault(str(fecha), 0)
                ingresos_por_dia[str(fecha)] += a.get("costo_total", 0)
                total += a.get("costo_total", 0)

        contenido = "💵 Ingresos por estacionamiento:\n\n"
        for dia in sorted(ingresos_por_dia):
            contenido += f"{dia}: ₡{ingresos_por_dia[dia]:.2f}\n"
        contenido += f"\nTOTAL: ₡{total:.2f}"
        self.actualizar_texto(contenido)

    # ------------ Reporte 2: Lista de espacios ------------
    def lista_espacios(self):
        espacios = mu.leer_json(ESPACIOS_PATH)
        if not isinstance(espacios, dict):
            return messagebox.showerror("Error", "Error leyendo espacios.")

        opciones = {
            "a": "Mostrar todos",
            "b": "Mostrar ocupados",
            "c": "Mostrar vacíos"
        }

        eleccion = simpledialog.askstring("Tipo de lista", "Elige: a (todos), b (ocupados), c (vacíos):")
        if eleccion not in opciones:
            return

        ahora = datetime.now()
        resultado = []

        for id_esp, datos in sorted(espacios.items()):
            try:
                fin_dt = datetime.strptime(datos["fin"], "%d/%m/%Y %H:%M") if datos["fin"] else None
            except:
                fin_dt = None

            if eleccion == "b" and (not fin_dt or fin_dt < ahora):
                continue
            if eleccion == "c" and fin_dt and fin_dt >= ahora:
                continue

            linea = f"{id_esp} - Habilitado: {datos['habilitado']}"
            if datos["usuario"]:
                linea += f"\n  Placa: {datos['placa']}\n  Inicio: {datos['inicio']}\n  Tiempo: {datos['tiempo']} mins\n  Fin: {datos['fin']}"
            resultado.append(linea)

        contenido = f"{opciones[eleccion]}:\n\n" + "\n\n".join(resultado)
        contenido += f"\n\nTotal espacios listados: {len(resultado)}"
        self.actualizar_texto(contenido)

    # ------------ Reporte 3: Historial de usos ------------
    def historial_usos(self):
        desde = simpledialog.askstring("Desde", "Fecha inicial (dd/mm/yyyy):")
        hasta = simpledialog.askstring("Hasta", "Fecha final (dd/mm/yyyy):")
        if not desde or not hasta:
            return

        try:
            desde_dt = datetime.strptime(desde, "%d/%m/%Y")
            hasta_dt = datetime.strptime(hasta, "%d/%m/%Y")
        except ValueError:
            return messagebox.showerror("Error", "Formato incorrecto.")

        alquileres = mu.leer_json(ALQUILERES_PATH)
        usados = [
            a for a in alquileres
            if desde_dt.date() <= datetime.strptime(a["inicio"], "%d/%m/%Y %H:%M").date() <= hasta_dt.date()
        ]

        usados.sort(key=lambda x: x["inicio"], reverse=True)
        contenido = "📆 Historial de espacios usados:\n\n"
        for a in usados:
            contenido += (
                f"Espacio: {a['espacio_id']}\nInicio: {a['inicio']}\nFin: {a['fin']}\n"
                f"Tiempo: {a['usuario']} - {a['costo_total']}₡\n{'-'*40}\n"
            )
        self.actualizar_texto(contenido if usados else "No hay registros.")

    # ------------ Reporte 4: Historial de multas ------------
    def historial_multas(self):
        desde = simpledialog.askstring("Desde", "Fecha inicial (dd/mm/yyyy):")
        hasta = simpledialog.askstring("Hasta", "Fecha final (dd/mm/yyyy):")
        if not desde or not hasta:
            return

        try:
            desde_dt = datetime.strptime(desde, "%d/%m/%Y")
            hasta_dt = datetime.strptime(hasta, "%d/%m/%Y")
        except ValueError:
            return messagebox.showerror("Error", "Formato incorrecto.")

        multas = mu.leer_json(MULTAS_PATH)
        filtro = [
            m for m in multas
            if desde_dt.date() <= datetime.strptime(m["fecha"], "%d/%m/%Y").date() <= hasta_dt.date()
        ]

        filtro.sort(key=lambda x: x["fecha"], reverse=True)
        contenido = "⚠️ Historial de multas:\n\n"
        total = 0
        for m in filtro:
            contenido += (
                f"Fecha: {m['fecha']}\nEspacio: {m['espacio']}\nPlaca: {m['placa']}\n"
                f"Motivo: {m['detalle']}\n{'-'*40}\n"
            )
            total += int(m.get("monto", 0))
        contenido += f"\nTOTAL ₡ en multas: {total}"
        self.actualizar_texto(contenido if filtro else "No hay multas en ese periodo.")

    def actualizar_texto(self, texto):
        self.reporte_actual = texto
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, texto)

import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_parqueo as mp
import modulo_usuarios as mu

class AlquilarFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.usuario = usuario
        self.placa_var = tk.StringVar()
        self.espacio_var = tk.StringVar()
        self.duracion_var = tk.IntVar(value=30)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="🅿️ Alquilar espacio", font=("Arial", 16)).pack(pady=10)

        # Entrada manual de ID
        tk.Label(self, text="ID del espacio de parqueo:").pack()
        tk.Entry(self, textvariable=self.espacio_var).pack()

        # Vehículos disponibles
        placas = [v["placa"] for v in self.usuario.get("vehiculos", [])]
        if not placas:
            tk.Label(self, text="No tienes vehículos registrados.").pack()
            self.crear_boton_volver()
            return

        tk.Label(self, text="Placa del vehículo:").pack()
        self.placa_var.set(placas[0])
        tk.OptionMenu(self, self.placa_var, *placas).pack()

        # Duración
        tk.Label(self, text="Duración (minutos):").pack()
        tk.Entry(self, textvariable=self.duracion_var).pack()

        tk.Button(self, text="✅ Confirmar alquiler", command=self.confirmar_alquiler).pack(pady=10)
        self.crear_boton_volver()

    def confirmar_alquiler(self):
        espacio_id = self.espacio_var.get().strip().upper()
        duracion = self.duracion_var.get()
        placa = self.placa_var.get()

        if not espacio_id:
            return messagebox.showerror("Error", "Debe ingresar un ID de espacio.")
        if duracion < 1:
            return messagebox.showerror("Error", "La duración mínima debe ser de 1 minuto.")
        if not placa:
            return messagebox.showerror("Error", "Debe seleccionar una placa.")

        # Validar espacio
        estado = mp.verificar_estado_espacio(espacio_id)
        if estado == "no_existe":
            return messagebox.showerror("Error", f"El espacio {espacio_id} no existe.")
        elif estado != "libre":
            continuar = messagebox.askyesno(
                "Espacio ocupado",
                f"El espacio {espacio_id} no está libre (estado: {estado}). ¿Deseas continuar de todos modos?"
            )
            if not continuar:
                return

        exito = mp.alquilar_espacio(
            correo_usuario=self.usuario["correo"],
            id_espacio=espacio_id,
            minutos=duracion,
            placa=placa
        )

        if exito:
            messagebox.showinfo("Éxito", f"Espacio {espacio_id} alquilado por {duracion} minutos.")
            self.volver_al_menu()
        else:
            messagebox.showerror("Error", "No se pudo alquilar el espacio.")

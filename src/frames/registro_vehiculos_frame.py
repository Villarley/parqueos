import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame

class RegistroVehiculosFrame(BaseFrame):
    def __init__(self, master, usuario):
        super().__init__(master, usuario)
        self.vehiculos = []
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Registrar vehículos").pack(pady=10)

        tk.Label(self, text="Placa:").pack()
        self.entry_placa = tk.Entry(self)
        self.entry_placa.pack()

        tk.Label(self, text="Marca (opcional):").pack()
        self.entry_marca = tk.Entry(self)
        self.entry_marca.pack()

        tk.Label(self, text="Modelo (opcional):").pack()
        self.entry_modelo = tk.Entry(self)
        self.entry_modelo.pack()

        tk.Button(self, text="➕ Agregar vehículo", command=self.agregar_vehiculo).pack(pady=5)
        tk.Button(self, text="✅ Finalizar registro", command=self.finalizar_registro).pack(pady=5)

        self.lista_vehiculos = tk.Listbox(self)
        self.lista_vehiculos.pack(pady=10)

    def agregar_vehiculo(self):
        placa = self.entry_placa.get().strip()
        marca = self.entry_marca.get().strip()
        modelo = self.entry_modelo.get().strip()

        if not placa:
            messagebox.showerror("Error", "La placa es obligatoria")
            return

        if any(v["placa"] == placa for v in self.vehiculos):
            messagebox.showwarning("Duplicado", "Ya registraste un vehículo con esa placa")
            return

        vehiculo = {"placa": placa, "marca": marca, "modelo": modelo}
        self.vehiculos.append(vehiculo)

        self.lista_vehiculos.insert(tk.END, f"{placa} - {marca} {modelo}")
        self.entry_placa.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)

    def finalizar_registro(self):
        from frames.menu_usuario_frame import MenuUsuarioFrame

        if not self.vehiculos:
            messagebox.showwarning("Atención", "Debe registrar al menos un vehículo")
            return

        self.usuario["vehiculos"] = self.vehiculos
        self.master.cambiar_frame(MenuUsuarioFrame, self.usuario)

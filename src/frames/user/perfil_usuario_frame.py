"""
Módulo para la interfaz de gestión del perfil de usuario.

Este módulo implementa la interfaz que permite a los usuarios:
- Ver su información personal
- Editar sus datos de perfil
- Gestionar sus vehículos registrados
- Eliminar su cuenta

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from frames.base_frame import BaseFrame
import modulo_usuarios as mu

class PerfilUsuarioFrame(BaseFrame):
    """
    Frame para la interfaz de gestión del perfil de usuario.
    
    Esta clase maneja la interfaz gráfica que permite a los usuarios
    ver y modificar su información personal, así como gestionar sus
    vehículos registrados.
    
    Attributes:
        usuario (dict): Información del usuario actual
        entries (dict): Diccionario que mapea campos a sus widgets Entry
    """
    
    def __init__(self, master, usuario):
        """
        Inicializa el frame de perfil de usuario.
        
        Args:
            master: Widget padre de este frame
            usuario (dict): Información del usuario actual
            
        Si no hay usuario logueado, redirige al login.
        """
        super().__init__(master, usuario)
        self.entries = {}
        if not usuario:
            messagebox.showerror("Error", "No hay usuario logueado")
            from frames.login_frame import LoginFrame
            self.master.cambiar_frame(LoginFrame)
            return
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y secciones principales
        - Campos de información personal
        - Lista de vehículos registrados
        - Botones de edición y gestión
        - Botón para volver
        """
        tk.Label(self, text="👤 Mi Perfil", font=("Arial", 16)).pack(pady=10)
        self.mostrar_datos_usuario()
        self.mostrar_vehiculos()

        tk.Button(self, text="✏️ Editar perfil", command=self.editar_perfil).pack(pady=5)
        tk.Button(self, text="➕ Agregar vehículo", command=self.agregar_vehiculo).pack(pady=5)
        tk.Button(self, text="❌ Eliminar cuenta", command=self.eliminar_cuenta).pack(pady=5)

        self.crear_boton_volver()

    def mostrar_datos_usuario(self):
        """
        Muestra los datos personales del usuario en campos de solo lectura.
        
        Este método:
        1. Crea un frame para los datos personales
        2. Muestra campos para nombre, apellidos, teléfono, correo y dirección
        3. Configura los campos como de solo lectura
        4. Almacena las referencias a los campos en self.entries
        """
        frame = tk.Frame(self)
        frame.pack()
        campos = ["nombre", "apellidos", "telefono", "correo", "direccion"]

        for campo in campos:
            tk.Label(frame, text=f"{campo.capitalize()}:").grid(row=campos.index(campo), column=0, sticky="w", padx=5, pady=2)
            val = tk.Entry(frame)
            val.insert(0, self.usuario.get(campo, ""))
            val.config(state="readonly")
            val.grid(row=campos.index(campo), column=1, padx=5, pady=2)
            self.entries[campo] = val

    def mostrar_vehiculos(self):
        """
        Muestra la lista de vehículos registrados del usuario.
        
        Este método:
        1. Obtiene la lista de vehículos del usuario
        2. Muestra cada vehículo con su placa, marca y modelo
        3. Formatea la información para mejor legibilidad
        """
        vehiculos = self.usuario.get("vehiculos", [])
        tk.Label(self, text="🚗 Vehículos:", font=("Arial", 12)).pack(pady=(10, 0))

        for v in vehiculos:
            info = f"{v['placa']} - {v.get('marca', '')} {v.get('modelo', '')}".strip()
            tk.Label(self, text=info).pack()

    def editar_perfil(self):
        """
        Habilita la edición de los datos del perfil.
        
        Este método:
        1. Habilita la edición de todos los campos
        2. Agrega un botón para guardar los cambios
        3. Valida los datos antes de guardar
        4. Actualiza la información en la base de datos
        """
        for entry in self.entries.values():
            entry.config(state="normal")

        def guardar():
            """
            Guarda los cambios realizados en el perfil.
            
            Este método:
            1. Obtiene los valores de todos los campos
            2. Valida que los campos obligatorios no estén vacíos
            3. Actualiza la información en la base de datos
            4. Muestra mensajes de éxito o error
            """
            for campo, entry in self.entries.items():
                self.usuario[campo] = entry.get().strip()

            if not self.usuario["nombre"] or not self.usuario["correo"]:
                return messagebox.showerror("Error", "Nombre y correo son obligatorios.")

            mu.actualizar_usuario(self.usuario["identificacion"], self.usuario)
            messagebox.showinfo("Éxito", "Perfil actualizado.")
            self.master.cambiar_frame(PerfilUsuarioFrame, self.usuario)

        tk.Button(self, text="💾 Guardar cambios", command=guardar).pack(pady=5)

    def agregar_vehiculo(self):
        """
        Permite agregar un nuevo vehículo al perfil.
        
        Este método:
        1. Solicita la placa del nuevo vehículo
        2. Verifica que la placa no esté duplicada
        3. Agrega el vehículo a la lista del usuario
        4. Actualiza la información en la base de datos
        """
        nueva = simpledialog.askstring("Agregar vehículo", "Placa del nuevo vehículo:")
        if not nueva:
            return
        if any(v["placa"] == nueva for v in self.usuario.get("vehiculos", [])):
            return messagebox.showerror("Error", "Esa placa ya está registrada.")

        nuevo_vehiculo = {"placa": nueva, "marca": "", "modelo": ""}
        self.usuario.setdefault("vehiculos", []).append(nuevo_vehiculo)

        mu.actualizar_usuario(self.usuario["identificacion"], self.usuario)
        messagebox.showinfo("Éxito", "Vehículo agregado.")
        self.master.cambiar_frame(PerfilUsuarioFrame, self.usuario)

    def eliminar_cuenta(self):
        """
        Procesa la eliminación de la cuenta del usuario.
        
        Este método:
        1. Solicita confirmación al usuario
        2. Elimina la cuenta de la base de datos
        3. Redirige al login si la eliminación es exitosa
        4. Muestra mensajes de éxito o error
        """
        confirmar = messagebox.askyesno("Eliminar cuenta", "¿Seguro que deseas eliminar tu cuenta?")
        if confirmar:
            if mu.eliminar_usuario(self.usuario["identificacion"]):
                messagebox.showinfo("Cuenta eliminada", "Tu cuenta ha sido eliminada.")
                from frames.login_frame import LoginFrame
                self.master.cambiar_frame(LoginFrame)
            else:
                messagebox.showerror("Error", "No se pudo eliminar la cuenta.")

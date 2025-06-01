# src/frames/configuracion_frame.py

"""
Módulo para la configuración del perfil de usuario.

Este módulo implementa la interfaz que permite a los usuarios:
- Ver y modificar su información personal
- Actualizar sus datos de contacto
- Cambiar su contraseña
- Gestionar sus preferencias

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import messagebox
import modulo_utiles as mu
from frames.base_frame import BaseFrame

CONFIG_PATH = "data/pc_configuracion.json"

class ConfiguracionFrame(BaseFrame):
    """
    Frame para la configuración del perfil de usuario.
    
    Esta clase maneja la interfaz gráfica que permite a los usuarios
    modificar su información personal y preferencias del sistema.
    
    Attributes:
        usuario (dict): Información del usuario actual
        nombre_var (StringVar): Variable para el campo de nombre
        correo_var (StringVar): Variable para el campo de correo
        telefono_var (StringVar): Variable para el campo de teléfono
    """
    
    def __init__(self, master):
        """
        Inicializa el frame de configuración.
        
        Args:
            master: Widget padre de este frame
        """
        super().__init__(master)
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y etiquetas
        - Campos de entrada para datos personales
        - Botones de actualización y cambio de contraseña
        - Botón para volver
        """
        tk.Label(self, text="⚙️ Configuración del Sistema", font=("Arial", 16)).pack(pady=10)

        self.config = mu.leer_json(CONFIG_PATH)

        self.entradas = {}

        # Campos editables
        campos = {
            "tarifa_hora": "Tarifa por hora ($)",
            "tiempo_minimo": "Tiempo mínimo (min)",
            "horario_inicio": "Horario inicio (HH:MM)",
            "horario_fin": "Horario fin (HH:MM)",
            "multa_por_hora": "Multa por hora ($)"
        }

        for clave, texto in campos.items():
            tk.Label(self, text=texto).pack()
            entrada = tk.Entry(self)
            entrada.insert(0, str(self.config.get(clave, "")))
            entrada.pack(pady=5)
            self.entradas[clave] = entrada

        # Botones
        tk.Button(self, text="💾 Guardar cambios", command=self.guardar_config).pack(pady=10)
        self.crear_boton_volver()

    def guardar_config(self):
        """
        Guarda los cambios realizados en la configuración del sistema.
        
        Este método:
        1. Obtiene los datos ingresados
        2. Valida el formato de los campos
        3. Actualiza la configuración en el sistema
        4. Muestra mensajes de éxito o error
        """
        try:
            nueva_config = {
                "tarifa_hora": float(self.entradas["tarifa_hora"].get()),
                "tiempo_minimo": int(self.entradas["tiempo_minimo"].get()),
                "horario_inicio": self.entradas["horario_inicio"].get(),
                "horario_fin": self.entradas["horario_fin"].get(),
                "multa_por_hora": float(self.entradas["multa_por_hora"].get())
            }
            mu.escribir_json(CONFIG_PATH, nueva_config)
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

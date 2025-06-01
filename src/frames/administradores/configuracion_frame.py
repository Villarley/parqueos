"""
Módulo para la configuración del sistema por administradores.

Este módulo implementa la interfaz que permite a los administradores:
- Configurar tarifas y precios
- Establecer horarios de operación
- Definir políticas de multas
- Gestionar parámetros del sistema

La interfaz utiliza Tkinter y hereda de BaseFrame para mantener
la consistencia con el resto de la aplicación.
"""

import tkinter as tk
from tkinter import messagebox
from frames.base_frame import BaseFrame
import modulo_utiles as mu

CONFIG_PATH = "data/configuracion.json"

class ConfiguracionFrame(BaseFrame):
    """
    Frame para la configuración del sistema.
    
    Esta clase maneja la interfaz gráfica que permite a los administradores
    modificar los parámetros de configuración del sistema.
    
    Attributes:
        config (dict): Diccionario con la configuración actual
        entries (dict): Diccionario que mapea campos a sus widgets Entry
    """
    
    def __init__(self, master):
        """
        Inicializa el frame de configuración.
        
        Args:
            master: Widget padre de este frame
        """
        super().__init__(master)
        self.config = mu.leer_json(CONFIG_PATH)
        self.entries = {}
        self.crear_widgets()

    def crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        
        Este método configura:
        - Título y secciones principales
        - Campos para cada parámetro de configuración
        - Botones de guardar y volver
        """
        tk.Label(self, text="⚙️ Configuración del Sistema", font=("Arial", 16)).pack(pady=10)

        # Campos de configuración
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
            self.entries[clave] = entrada

        # Botones
        tk.Button(self, text="💾 Guardar cambios", command=self.guardar_config).pack(pady=10)
        self.crear_boton_volver()

    def guardar_config(self):
        """
        Guarda los cambios realizados en la configuración.
        
        Este método:
        1. Obtiene los valores de todos los campos
        2. Valida el formato de los datos
        3. Actualiza la configuración en el sistema
        4. Muestra mensajes de éxito o error
        """
        try:
            nueva_config = {
                "tarifa_hora": float(self.entries["tarifa_hora"].get()),
                "tiempo_minimo": int(self.entries["tiempo_minimo"].get()),
                "horario_inicio": self.entries["horario_inicio"].get(),
                "horario_fin": self.entries["horario_fin"].get(),
                "multa_por_hora": float(self.entries["multa_por_hora"].get())
            }

            # Validar horarios
            if not self.validar_horario(nueva_config["horario_inicio"]) or \
               not self.validar_horario(nueva_config["horario_fin"]):
                return messagebox.showerror("Error", "Formato de horario inválido (HH:MM)")

            # Validar valores numéricos
            if nueva_config["tarifa_hora"] < 0 or \
               nueva_config["tiempo_minimo"] < 1 or \
               nueva_config["multa_por_hora"] < 0:
                return messagebox.showerror("Error", "Los valores numéricos deben ser positivos")

            mu.escribir_json(CONFIG_PATH, nueva_config)
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", f"Valor inválido: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def validar_horario(self, horario):
        """
        Valida el formato de un horario.
        
        Args:
            horario (str): Horario a validar en formato HH:MM
            
        Returns:
            bool: True si el formato es válido, False en caso contrario
        """
        try:
            hora, minuto = map(int, horario.split(":"))
            return 0 <= hora <= 23 and 0 <= minuto <= 59
        except:
            return False

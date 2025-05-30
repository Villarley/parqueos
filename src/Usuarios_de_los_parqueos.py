import tkinter as tk
from tkinter import messagebox
import modulo_usuarios as mu


class AppUsuarios:
    def __init__(self, root):
        self.root = root
        self.root.title("Parqueo - Usuarios")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        self.mostrar_login()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Inicio de Sesión", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Correo:").pack()
        self.entry_correo = tk.Entry(self.root, width=30)
        self.entry_correo.pack()

        tk.Label(self.root, text="Contraseña:").pack()
        self.entry_contra = tk.Entry(self.root, show="*", width=30)
        self.entry_contra.pack()

        tk.Button(self.root, text="Iniciar Sesión", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Registrarse", command=self.mostrar_registro).pack()
        tk.Button(self.root, text="¿Olvidaste tu contraseña?", command=self.recuperar_contrasena).pack(pady=5)

    def mostrar_registro(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Registro de Usuario", font=("Arial", 16)).pack(pady=10)

        campos = ["Correo", "Contraseña", "Nombre", "Teléfono", "Placa"]
        self.registros = {}

        for campo in campos:
            tk.Label(self.root, text=f"{campo}:").pack()
            show = "*" if campo == "Contraseña" else ""
            entrada = tk.Entry(self.root, show=show, width=30)
            entrada.pack()
            self.registros[campo.lower()] = entrada

        tk.Button(self.root, text="Registrar", command=self.registrar).pack(pady=10)
        tk.Button(self.root, text="Volver al Login", command=self.mostrar_login).pack()

    def login(self):
        correo = self.entry_correo.get().strip()
        contra = self.entry_contra.get().strip()

        usuario = mu.autenticar_usuario(correo, contra)
        if usuario:
            messagebox.showinfo("Bienvenido", f"Hola {usuario['nombre']} 👋")
            # Acá podrías mostrar menú principal
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def registrar(self):
        datos = {k: e.get().strip() for k, e in self.registros.items()}

        exito = mu.registrar_usuario(
            correo=datos["correo"],
            contrasena=datos["contraseña"],
            nombre=datos["nombre"],
            telefono=datos["teléfono"],
            placa=datos["placa"]
        )

        if exito:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.mostrar_login()
        else:
            messagebox.showwarning("Ya existe", "Ese correo ya está registrado.")

    def recuperar_contrasena(self):
        correo = self.entry_correo.get().strip()
        if not correo:
            messagebox.showwarning("Dato faltante", "Ingrese su correo.")
            return

        enviado = mu.enviar_recordatorio_contrasena(correo)
        if enviado:
            messagebox.showinfo("Correo enviado", "Revise su bandeja de entrada.")
        else:
            messagebox.showerror("Error", "Correo no registrado.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppUsuarios(root)
    root.mainloop()

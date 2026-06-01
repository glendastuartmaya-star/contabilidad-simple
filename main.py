"""
Interfaz corregida - Archivo principal
"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager, SistemaContable
from autenticacion import GestorUsuarios
from interfaz_quickbooks import InterfazQuickBooks

class PantallaBienvenida:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Contabilidad - QuickBooks")
        self.ventana.geometry("600x500")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        frame_principal = ttk.Frame(self.ventana)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        titulo = ttk.Label(frame_principal, text="SISTEMA DE CONTABILIDAD", 
                          font=("Arial", 18, "bold"))
        titulo.pack(pady=20)
        
        ttk.Separator(frame_principal, orient="horizontal").pack(fill="x", pady=20)
        
        frame_opciones = ttk.LabelFrame(frame_principal, text="Autenticación", padding=20)
        frame_opciones.pack(fill="both", expand=True, pady=10)
        
        ttk.Label(frame_opciones, text="Empresa:").pack(anchor="w", pady=5)
        self.entrada_empresa = ttk.Entry(frame_opciones)
        self.entrada_empresa.pack(fill="x", pady=5)
        self.entrada_empresa.insert(0, "Mi Empresa")
        
        ttk.Label(frame_opciones, text="Email:").pack(anchor="w", pady=5)
        self.entrada_email = ttk.Entry(frame_opciones)
        self.entrada_email.pack(fill="x", pady=5)
        self.entrada_email.insert(0, "admin@empresa.com")
        
        ttk.Label(frame_opciones, text="Contraseña:").pack(anchor="w", pady=5)
        self.entrada_contraseña = ttk.Entry(frame_opciones, show="*")
        self.entrada_contraseña.pack(fill="x", pady=5)
        self.entrada_contraseña.insert(0, "admin123")
        
        frame_botones = ttk.Frame(frame_opciones)
        frame_botones.pack(fill="x", pady=20)
        
        ttk.Button(frame_botones, text="Iniciar", 
                  command=self.iniciar_sesion).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Registrar", 
                  command=self.registrar_usuario).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Salir", 
                  command=self.ventana.quit).pack(side="right", padx=5)
    
    def registrar_usuario(self):
        empresa = self.entrada_empresa.get()
        email = self.entrada_email.get()
        contraseña = self.entrada_contraseña.get()
        
        if not empresa or not email or not contraseña:
            messagebox.showerror("Error", "Completa todos los campos")
            return
        
        try:
            DatabaseManager(empresa)
            gestor = GestorUsuarios(empresa)
            exito, mensaje = gestor.crear_usuario(
                nombre=email.split('@')[0],
                email=email,
                contraseña=contraseña,
                rol="Admin"
            )
            
            if exito:
                sistema = SistemaContable(empresa)
                sistema.inicializar_plan_cuentas()
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def iniciar_sesion(self):
        empresa = self.entrada_empresa.get()
        email = self.entrada_email.get()
        contraseña = self.entrada_contraseña.get()
        
        if not empresa or not email or not contraseña:
            messagebox.showerror("Error", "Completa todos los campos")
            return
        
        try:
            gestor = GestorUsuarios(empresa)
            exito, resultado = gestor.login(email, contraseña)
            
            if exito:
                self.ventana.withdraw()
                ventana_principal = tk.Tk()
                app = InterfazQuickBooks(ventana_principal)
                ventana_principal.mainloop()
            else:
                messagebox.showerror("Error", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Conexión: {str(e)}")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = PantallaBienvenida(ventana)
    ventana.mainloop()

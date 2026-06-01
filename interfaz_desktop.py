import tkinter as tk
from tkinter import ttk, messagebox
from contabilidad import SistemaContabilidad
from datetime import datetime, timedelta

class InterfazContabilidad:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Contabilidad")
        self.ventana.geometry("900x600")
        self.sistema = SistemaContabilidad()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña 1: Agregar Transacción
        self.frame_agregar = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_agregar, text="Agregar Transacción")
        self.crear_pestana_agregar()
        
        # Pestaña 2: Ver Transacciones
        self.frame_ver = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_ver, text="Ver Transacciones")
        self.crear_pestana_ver()
        
        # Pestaña 3: Libro Mayor
        self.frame_libro = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_libro, text="Libro Mayor")
        self.crear_pestana_libro()
        
        # Pestaña 4: P&L
        self.frame_pl = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_pl, text="P&L")
        self.crear_pestana_pl()
        
        # Pestaña 5: Estadísticas
        self.frame_stats = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_stats, text="Estadísticas")
        self.crear_pestana_estadisticas()
    
    def crear_pestana_agregar(self):
        frame_contenido = ttk.Frame(self.frame_agregar)
        frame_contenido.pack(padx=20, pady=20)
        
        # Tipo
        ttk.Label(frame_contenido, text="Tipo:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_tipo = ttk.Combobox(frame_contenido, values=["Ingreso", "Gasto"], state="readonly")
        self.combo_tipo.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Monto
        ttk.Label(frame_contenido, text="Monto:").grid(row=1, column=0, sticky="w", pady=5)
        self.entrada_monto = ttk.Entry(frame_contenido)
        self.entrada_monto.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Categoría
        ttk.Label(frame_contenido, text="Categoría:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_categoria = ttk.Combobox(frame_contenido, values=self.sistema.obtener_categorias(), state="readonly")
        self.combo_categoria.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Descripción
        ttk.Label(frame_contenido, text="Descripción:").grid(row=3, column=0, sticky="w", pady=5)
        self.entrada_descripcion = ttk.Entry(frame_contenido)
        self.entrada_descripcion.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Botón Guardar
        ttk.Button(frame_contenido, text="Guardar", command=self.guardar_transaccion).grid(row=4, column=0, columnspan=2, pady=20)
        
        frame_contenido.columnconfigure(1, weight=1)
    
    def crear_pestana_ver(self):
        frame_contenido = ttk.Frame(self.frame_ver)
        frame_contenido.pack(fill="both", expand=True, padx=20, pady=20)
        
        # TreeView para mostrar transacciones
        self.tree = ttk.Treeview(frame_contenido, columns=("Tipo", "Monto", "Categoría", "Descripción", "Fecha"), height=15)
        self.tree.heading("#0", text="ID")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Monto", text="Monto")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.column("#0", width=30)
        self.tree.column("Tipo", width=80)
        self.tree.column("Monto", width=100)
        self.tree.column("Categoría", width=100)
        self.tree.column("Descripción", width=200)
        self.tree.column("Fecha", width=100)
        
        self.tree.pack(fill="both", expand=True)
        
        ttk.Button(frame_contenido, text="Actualizar", command=self.actualizar_transacciones).pack(pady=10)
        
        self.actualizar_transacciones()
    
    def crear_pestana_libro(self):
        frame_contenido = ttk.Frame(self.frame_libro)
        frame_contenido.pack(padx=20, pady=20)
        
        ttk.Label(frame_contenido, text="Selecciona Mes y Año:").pack()
        
        frame_fecha = ttk.Frame(frame_contenido)
        frame_fecha.pack(pady=10)
        
        ttk.Label(frame_fecha, text="Mes:").pack(side="left", padx=5)
        self.spin_mes = ttk.Spinbox(frame_fecha, from_=1, to=12, width=5)
        self.spin_mes.set(datetime.now().month)
        self.spin_mes.pack(side="left", padx=5)
        
        ttk.Label(frame_fecha, text="Año:").pack(side="left", padx=5)
        self.spin_año = ttk.Spinbox(frame_fecha, from_=2020, to=2030, width=5)
        self.spin_año.set(datetime.now().year)
        self.spin_año.pack(side="left", padx=5)
        
        ttk.Button(frame_contenido, text="Ver Libro Mayor", command=self.mostrar_libro_mayor).pack(pady=10)
        
        self.text_libro = tk.Text(frame_contenido, height=20, width=80)
        self.text_libro.pack(pady=10)
    
    def crear_pestana_pl(self):
        frame_contenido = ttk.Frame(self.frame_pl)
        frame_contenido.pack(padx=20, pady=20)
        
        ttk.Label(frame_contenido, text="Estado de Resultados (P&L):").pack()
        
        self.text_pl = tk.Text(frame_contenido, height=25, width=80)
        self.text_pl.pack(pady=10)
        
        ttk.Button(frame_contenido, text="Generar P&L", command=self.generar_pl).pack()
    
    def crear_pestana_estadisticas(self):
        frame_contenido = ttk.Frame(self.frame_stats)
        frame_contenido.pack(padx=20, pady=20)
        
        ttk.Label(frame_contenido, text="Estadísticas:").pack()
        
        self.text_stats = tk.Text(frame_contenido, height=25, width=80)
        self.text_stats.pack(pady=10)
        
        ttk.Button(frame_contenido, text="Calcular Estadísticas", command=self.calcular_estadisticas).pack()
    
    def guardar_transaccion(self):
        try:
            tipo = self.combo_tipo.get().lower()
            monto = float(self.entrada_monto.get())
            categoria = self.combo_categoria.get()
            descripcion = self.entrada_descripcion.get()
            
            if not tipo or not categoria or not descripcion:
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return
            
            self.sistema.agregar_transaccion(tipo, monto, categoria, descripcion)
            messagebox.showinfo("Éxito", "Transacción guardada correctamente")
            
            self.entrada_monto.delete(0, tk.END)
            self.entrada_descripcion.delete(0, tk.END)
            self.combo_tipo.set("")
            self.combo_categoria.set("")
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
    
    def actualizar_transacciones(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        transacciones = self.sistema.obtener_todas_transacciones()
        for i, t in enumerate(transacciones):
            self.tree.insert("", "end", text=str(i+1), values=(t["tipo"], f"${t['monto']:.2f}", t["categoria"], t["descripcion"], t["fecha"]))
    
    def mostrar_libro_mayor(self):
        mes = int(self.spin_mes.get())
        año = int(self.spin_año.get())
        
        transacciones = self.sistema.obtener_transacciones_mes(año, mes)
        
        self.text_libro.delete(1.0, tk.END)
        self.text_libro.insert(tk.END, f"LIBRO MAYOR - {mes:02d}/{año}\n")
        self.text_libro.insert(tk.END, "=" * 80 + "\n\n")
        
        for t in transacciones:
            self.text_libro.insert(tk.END, f"Fecha: {t['fecha']} | Tipo: {t['tipo'].upper()} | Monto: ${t['monto']:.2f}\n")
            self.text_libro.insert(tk.END, f"Categoría: {t['categoria']} | Descripción: {t['descripcion']}\n")
            self.text_libro.insert(tk.END, "-" * 80 + "\n")
    
    def generar_pl(self):
        self.text_pl.delete(1.0, tk.END)
        
        # Obtener todos los meses
        transacciones = self.sistema.obtener_todas_transacciones()
        
        self.text_pl.insert(tk.END, "ESTADO DE RESULTADOS (P&L)\n")
        self.text_pl.insert(tk.END, "=" * 60 + "\n\n")
        
        meses = {}
        for t in transacciones:
            fecha = datetime.strptime(t["fecha"], "%Y-%m-%d")
            mes_año = f"{fecha.month:02d}/{fecha.year}"
            if mes_año not in meses:
                meses[mes_año] = {"ingresos": 0, "gastos": 0}
            
            if t["tipo"] == "ingreso":
                meses[mes_año]["ingresos"] += t["monto"]
            else:
                meses[mes_año]["gastos"] += t["monto"]
        
        total_ingresos = 0
        total_gastos = 0
        
        for mes_año in sorted(meses.keys()):
            ingresos = meses[mes_año]["ingresos"]
            gastos = meses[mes_año]["gastos"]
            balance = ingresos - gastos
            total_ingresos += ingresos
            total_gastos += gastos
            
            self.text_pl.insert(tk.END, f"Mes: {mes_año}\n")
            self.text_pl.insert(tk.END, f"  Ingresos:  ${ingresos:>10,.2f}\n")
            self.text_pl.insert(tk.END, f"  Gastos:    ${gastos:>10,.2f}\n")
            self.text_pl.insert(tk.END, f"  Balance:   ${balance:>10,.2f}\n")
            self.text_pl.insert(tk.END, "-" * 60 + "\n")
        
        balance_acumulado = total_ingresos - total_gastos
        self.text_pl.insert(tk.END, "\nACUMULADO:\n")
        self.text_pl.insert(tk.END, f"  Ingresos:  ${total_ingresos:>10,.2f}\n")
        self.text_pl.insert(tk.END, f"  Gastos:    ${total_gastos:>10,.2f}\n")
        self.text_pl.insert(tk.END, f"  Balance:   ${balance_acumulado:>10,.2f}\n")
    
    def calcular_estadisticas(self):
        self.text_stats.delete(1.0, tk.END)
        
        transacciones = self.sistema.obtener_todas_transacciones()
        
        if not transacciones:
            self.text_stats.insert(tk.END, "No hay transacciones registradas")
            return
        
        self.text_stats.insert(tk.END, "ESTADÍSTICAS\n")
        self.text_stats.insert(tk.END, "=" * 60 + "\n\n")
        
        # Total de transacciones
        self.text_stats.insert(tk.END, f"Total de transacciones: {len(transacciones)}\n\n")
        
        # Por tipo
        ingresos = [t for t in transacciones if t["tipo"] == "ingreso"]
        gastos = [t for t in transacciones if t["tipo"] == "gasto"]
        
        self.text_stats.insert(tk.END, f"Ingresos: {len(ingresos)} transacciones\n")
        self.text_stats.insert(tk.END, f"Gastos: {len(gastos)} transacciones\n\n")
        
        # Por categoría
        self.text_stats.insert(tk.END, "Por Categoría:\n")
        categorias = {}
        for t in transacciones:
            cat = t["categoria"]
            if cat not in categorias:
                categorias[cat] = {"cantidad": 0, "total": 0}
            categorias[cat]["cantidad"] += 1
            categorias[cat]["total"] += t["monto"]
        
        for cat in sorted(categorias.keys()):
            self.text_stats.insert(tk.END, f"  {cat}: {categorias[cat]['cantidad']} transacciones - ${categorias[cat]['total']:.2f}\n")
        
        # Promedio
        monto_total = sum(t["monto"] for t in transacciones)
        promedio = monto_total / len(transacciones)
        self.text_stats.insert(tk.END, f"\nMonto promedio por transacción: ${promedio:.2f}\n")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazContabilidad(ventana)
    ventana.mainloop()
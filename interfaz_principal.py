import tkinter as tk
from tkinter import ttk, messagebox
from sistema_excel import SistemaExcel
from datetime import datetime, timedelta

class InterfazPrincipal:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Contabilidad - Libro1.xlsx")
        self.ventana.geometry("1000x700")
        
        # Cargar sistema Excel
        self.sistema = SistemaExcel("Libro1.xlsx")
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz principal con pestañas"""
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña: Agregar Ingreso
        self.frame_ingreso = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_ingreso, text="➕ Agregar Ingreso")
        self.crear_pestana_ingreso()
        
        # Pestaña: Agregar Gasto
        self.frame_gasto = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_gasto, text="➕ Agregar Gasto")
        self.crear_pestana_gasto()
        
        # Pestaña: Contract Labor
        self.frame_contrato = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_contrato, text="👷 Contract Labor")
        self.crear_pestana_contrato()
        
        # Pestaña: Ver Ingresos
        self.frame_ver_ingresos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_ver_ingresos, text="💰 Ver Ingresos")
        self.crear_pestana_ver_ingresos()
        
        # Pestaña: Ver Gastos
        self.frame_ver_gastos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_ver_gastos, text="💸 Ver Gastos")
        self.crear_pestana_ver_gastos()
        
        # Pestaña: P&L Report
        self.frame_pl = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_pl, text="📊 P&L Report")
        self.crear_pestana_pl()
    
    def crear_pestana_ingreso(self):
        """Pestaña para agregar ingresos"""
        frame = ttk.Frame(self.frame_ingreso)
        frame.pack(padx=20, pady=20)
        
        # Fecha
        ttk.Label(frame, text="Fecha:").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_fecha_ing = ttk.Entry(frame)
        self.entrada_fecha_ing.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entrada_fecha_ing.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Document Number
        ttk.Label(frame, text="Document Number:").grid(row=1, column=0, sticky="w", pady=5)
        self.entrada_doc_ing = ttk.Entry(frame)
        self.entrada_doc_ing.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Customer
        ttk.Label(frame, text="Customer:").grid(row=2, column=0, sticky="w", pady=5)
        clientes = self.sistema.obtener_clientes()
        self.combo_cliente = ttk.Combobox(frame, values=clientes, state="normal")
        self.combo_cliente.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Category
        ttk.Label(frame, text="Category:").grid(row=3, column=0, sticky="w", pady=5)
        categorias = self.sistema.obtener_categorias_ingresos()
        self.combo_cat_ing = ttk.Combobox(frame, values=categorias, state="normal")
        self.combo_cat_ing.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Payment Method
        ttk.Label(frame, text="Payment Method:").grid(row=4, column=0, sticky="w", pady=5)
        metodos = self.sistema.obtener_metodos_pago()
        self.combo_metodo_ing = ttk.Combobox(frame, values=metodos, state="normal")
        self.combo_metodo_ing.grid(row=4, column=1, sticky="ew", pady=5)
        
        # Status
        ttk.Label(frame, text="Status:").grid(row=5, column=0, sticky="w", pady=5)
        self.combo_status_ing = ttk.Combobox(frame, values=["Pending", "Completed"], state="readonly")
        self.combo_status_ing.grid(row=5, column=1, sticky="ew", pady=5)
        
        # Amount
        ttk.Label(frame, text="Amount:").grid(row=6, column=0, sticky="w", pady=5)
        self.entrada_monto_ing = ttk.Entry(frame)
        self.entrada_monto_ing.grid(row=6, column=1, sticky="ew", pady=5)
        
        # Notes
        ttk.Label(frame, text="Notes:").grid(row=7, column=0, sticky="w", pady=5)
        self.entrada_notas_ing = ttk.Entry(frame)
        self.entrada_notas_ing.grid(row=7, column=1, sticky="ew", pady=5)
        
        # Botón guardar
        ttk.Button(frame, text="💾 Guardar Ingreso", command=self.guardar_ingreso).grid(row=8, column=0, columnspan=2, pady=20)
        
        frame.columnconfigure(1, weight=1)
    
    def crear_pestana_gasto(self):
        """Pestaña para agregar gastos"""
        frame = ttk.Frame(self.frame_gasto)
        frame.pack(padx=20, pady=20)
        
        # Fecha
        ttk.Label(frame, text="Fecha:").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_fecha_gas = ttk.Entry(frame)
        self.entrada_fecha_gas.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entrada_fecha_gas.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Document Number
        ttk.Label(frame, text="Document Number:").grid(row=1, column=0, sticky="w", pady=5)
        self.entrada_doc_gas = ttk.Entry(frame)
        self.entrada_doc_gas.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Description
        ttk.Label(frame, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
        self.entrada_desc = ttk.Entry(frame)
        self.entrada_desc.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Supplier
        ttk.Label(frame, text="Supplier:").grid(row=3, column=0, sticky="w", pady=5)
        proveedores = self.sistema.obtener_proveedores()
        self.combo_proveedor = ttk.Combobox(frame, values=proveedores, state="normal")
        self.combo_proveedor.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Category
        ttk.Label(frame, text="Category:").grid(row=4, column=0, sticky="w", pady=5)
        categorias = self.sistema.obtener_categorias_gastos()
        self.combo_cat_gas = ttk.Combobox(frame, values=categorias, state="normal")
        self.combo_cat_gas.grid(row=4, column=1, sticky="ew", pady=5)
        
        # Type
        ttk.Label(frame, text="Type:").grid(row=5, column=0, sticky="w", pady=5)
        self.combo_tipo = ttk.Combobox(frame, values=["Operating", "COGS", "Payroll", "Financial", "Taxes", "Non-Deductible"], state="normal")
        self.combo_tipo.grid(row=5, column=1, sticky="ew", pady=5)
        
        # Payment Method
        ttk.Label(frame, text="Payment Method:").grid(row=6, column=0, sticky="w", pady=5)
        metodos = self.sistema.obtener_metodos_pago()
        self.combo_metodo_gas = ttk.Combobox(frame, values=metodos, state="normal")
        self.combo_metodo_gas.grid(row=6, column=1, sticky="ew", pady=5)
        
        # Status
        ttk.Label(frame, text="Status:").grid(row=7, column=0, sticky="w", pady=5)
        self.combo_status_gas = ttk.Combobox(frame, values=["Pending", "Completed"], state="readonly")
        self.combo_status_gas.grid(row=7, column=1, sticky="ew", pady=5)
        
        # Amount
        ttk.Label(frame, text="Amount:").grid(row=8, column=0, sticky="w", pady=5)
        self.entrada_monto_gas = ttk.Entry(frame)
        self.entrada_monto_gas.grid(row=8, column=1, sticky="ew", pady=5)
        
        # Notes
        ttk.Label(frame, text="Notes:").grid(row=9, column=0, sticky="w", pady=5)
        self.entrada_notas_gas = ttk.Entry(frame)
        self.entrada_notas_gas.grid(row=9, column=1, sticky="ew", pady=5)
        
        # Botón guardar
        ttk.Button(frame, text="💾 Guardar Gasto", command=self.guardar_gasto).grid(row=10, column=0, columnspan=2, pady=20)
        
        frame.columnconfigure(1, weight=1)
    
    def crear_pestana_contrato(self):
        """Pestaña para agregar contratos de labor"""
        frame = ttk.Frame(self.frame_contrato)
        frame.pack(padx=20, pady=20)
        
        # Fecha
        ttk.Label(frame, text="Fecha:").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_fecha_con = ttk.Entry(frame)
        self.entrada_fecha_con.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entrada_fecha_con.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Document Number
        ttk.Label(frame, text="Document Number:").grid(row=1, column=0, sticky="w", pady=5)
        self.entrada_doc_con = ttk.Entry(frame)
        self.entrada_doc_con.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Contractor Name
        ttk.Label(frame, text="Contractor Name:").grid(row=2, column=0, sticky="w", pady=5)
        self.entrada_contratista = ttk.Entry(frame)
        self.entrada_contratista.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Description
        ttk.Label(frame, text="Description:").grid(row=3, column=0, sticky="w", pady=5)
        self.entrada_desc_con = ttk.Entry(frame)
        self.entrada_desc_con.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Payment Method
        ttk.Label(frame, text="Payment Method:").grid(row=4, column=0, sticky="w", pady=5)
        metodos = self.sistema.obtener_metodos_pago()
        self.combo_metodo_con = ttk.Combobox(frame, values=metodos, state="normal")
        self.combo_metodo_con.grid(row=4, column=1, sticky="ew", pady=5)
        
        # Amount
        ttk.Label(frame, text="Amount:").grid(row=5, column=0, sticky="w", pady=5)
        self.entrada_monto_con = ttk.Entry(frame)
        self.entrada_monto_con.grid(row=5, column=1, sticky="ew", pady=5)
        
        # Notes
        ttk.Label(frame, text="Notes:").grid(row=6, column=0, sticky="w", pady=5)
        self.entrada_notas_con = ttk.Entry(frame)
        self.entrada_notas_con.grid(row=6, column=1, sticky="ew", pady=5)
        
        # Botón guardar
        ttk.Button(frame, text="💾 Guardar Contrato", command=self.guardar_contrato).grid(row=7, column=0, columnspan=2, pady=20)
        
        frame.columnconfigure(1, weight=1)
    
    def crear_pestana_ver_ingresos(self):
        """Pestaña para ver ingresos"""
        # TreeView
        self.tree_ingresos = ttk.Treeview(self.frame_ver_ingresos, columns=("Fecha", "Doc", "Cliente", "Categoría", "Método", "Estado", "Monto"), height=20)
        self.tree_ingresos.heading("#0", text="ID")
        self.tree_ingresos.heading("Fecha", text="Fecha")
        self.tree_ingresos.heading("Doc", text="Doc #")
        self.tree_ingresos.heading("Cliente", text="Cliente")
        self.tree_ingresos.heading("Categoría", text="Categoría")
        self.tree_ingresos.heading("Método", text="Método")
        self.tree_ingresos.heading("Estado", text="Estado")
        self.tree_ingresos.heading("Monto", text="Monto")
        
        self.tree_ingresos.column("#0", width=30)
        self.tree_ingresos.column("Fecha", width=100)
        self.tree_ingresos.column("Doc", width=80)
        self.tree_ingresos.column("Cliente", width=100)
        self.tree_ingresos.column("Categoría", width=100)
        self.tree_ingresos.column("Método", width=100)
        self.tree_ingresos.column("Estado", width=80)
        self.tree_ingresos.column("Monto", width=100)
        
        self.tree_ingresos.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botón actualizar
        ttk.Button(self.frame_ver_ingresos, text="🔄 Actualizar", command=self.actualizar_ingresos).pack(pady=10)
        
        self.actualizar_ingresos()
    
    def crear_pestana_ver_gastos(self):
        """Pestaña para ver gastos"""
        # TreeView
        self.tree_gastos = ttk.Treeview(self.frame_ver_gastos, columns=("Fecha", "Doc", "Descripción", "Proveedor", "Categoría", "Monto"), height=20)
        self.tree_gastos.heading("#0", text="ID")
        self.tree_gastos.heading("Fecha", text="Fecha")
        self.tree_gastos.heading("Doc", text="Doc #")
        self.tree_gastos.heading("Descripción", text="Descripción")
        self.tree_gastos.heading("Proveedor", text="Proveedor")
        self.tree_gastos.heading("Categoría", text="Categoría")
        self.tree_gastos.heading("Monto", text="Monto")
        
        self.tree_gastos.column("#0", width=30)
        self.tree_gastos.column("Fecha", width=100)
        self.tree_gastos.column("Doc", width=80)
        self.tree_gastos.column("Descripción", width=150)
        self.tree_gastos.column("Proveedor", width=100)
        self.tree_gastos.column("Categoría", width=100)
        self.tree_gastos.column("Monto", width=100)
        
        self.tree_gastos.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botón actualizar
        ttk.Button(self.frame_ver_gastos, text="🔄 Actualizar", command=self.actualizar_gastos).pack(pady=10)
        
        self.actualizar_gastos()
    
    def crear_pestana_pl(self):
        """Pestaña para P&L Report"""
        frame = ttk.Frame(self.frame_pl)
        frame.pack(padx=20, pady=20)
        
        # Selección de mes/año
        frame_fecha = ttk.Frame(frame)
        frame_fecha.pack(pady=10)
        
        ttk.Label(frame_fecha, text="Mes:").pack(side="left", padx=5)
        self.spin_mes = ttk.Spinbox(frame_fecha, from_=1, to=12, width=5)
        self.spin_mes.set(datetime.now().month)
        self.spin_mes.pack(side="left", padx=5)
        
        ttk.Label(frame_fecha, text="Año:").pack(side="left", padx=5)
        self.spin_año = ttk.Spinbox(frame_fecha, from_=2020, to=2030, width=5)
        self.spin_año.set(datetime.now().year)
        self.spin_año.pack(side="left", padx=5)
        
        ttk.Button(frame_fecha, text="📊 Generar P&L", command=self.generar_pl).pack(side="left", padx=10)
        
        # Text widget para mostrar P&L
        self.text_pl = tk.Text(frame, height=25, width=100)
        self.text_pl.pack(pady=10, fill="both", expand=True)
        
        self.generar_pl()
    
    def guardar_ingreso(self):
        """Guarda un ingreso"""
        try:
            fecha = datetime.strptime(self.entrada_fecha_ing.get(), "%Y-%m-%d")
            doc = self.entrada_doc_ing.get()
            cliente = self.combo_cliente.get()
            categoria = self.combo_cat_ing.get()
            metodo = self.combo_metodo_ing.get()
            estado = self.combo_status_ing.get()
            monto = float(self.entrada_monto_ing.get())
            notas = self.entrada_notas_ing.get()
            
            if not cliente or not categoria or not metodo or not estado:
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return
            
            self.sistema.agregar_ingreso(fecha, doc, cliente, categoria, metodo, estado, monto, notas)
            messagebox.showinfo("Éxito", "Ingreso guardado correctamente")
            
            # Limpiar campos
            self.entrada_doc_ing.delete(0, tk.END)
            self.combo_cliente.delete(0, tk.END)
            self.combo_cat_ing.delete(0, tk.END)
            self.combo_metodo_ing.delete(0, tk.END)
            self.combo_status_ing.set("")
            self.entrada_monto_ing.delete(0, tk.END)
            self.entrada_notas_ing.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor verifica la fecha y el monto")
    
    def guardar_gasto(self):
        """Guarda un gasto"""
        try:
            fecha = datetime.strptime(self.entrada_fecha_gas.get(), "%Y-%m-%d")
            doc = self.entrada_doc_gas.get()
            descripcion = self.entrada_desc.get()
            proveedor = self.combo_proveedor.get()
            categoria = self.combo_cat_gas.get()
            tipo = self.combo_tipo.get()
            metodo = self.combo_metodo_gas.get()
            estado = self.combo_status_gas.get()
            monto = float(self.entrada_monto_gas.get())
            notas = self.entrada_notas_gas.get()
            
            if not descripcion or not proveedor or not categoria or not tipo or not metodo or not estado:
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return
            
            self.sistema.agregar_gasto(fecha, doc, descripcion, proveedor, categoria, tipo, metodo, estado, monto, notas)
            messagebox.showinfo("Éxito", "Gasto guardado correctamente")
            
            # Limpiar campos
            self.entrada_doc_gas.delete(0, tk.END)
            self.entrada_desc.delete(0, tk.END)
            self.combo_proveedor.delete(0, tk.END)
            self.combo_cat_gas.delete(0, tk.END)
            self.combo_tipo.delete(0, tk.END)
            self.combo_metodo_gas.delete(0, tk.END)
            self.combo_status_gas.set("")
            self.entrada_monto_gas.delete(0, tk.END)
            self.entrada_notas_gas.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor verifica la fecha y el monto")
    
    def guardar_contrato(self):
        """Guarda un contrato de labor"""
        try:
            fecha = datetime.strptime(self.entrada_fecha_con.get(), "%Y-%m-%d")
            doc = self.entrada_doc_con.get()
            contratista = self.entrada_contratista.get()
            descripcion = self.entrada_desc_con.get()
            metodo = self.combo_metodo_con.get()
            monto = float(self.entrada_monto_con.get())
            notas = self.entrada_notas_con.get()
            
            if not contratista or not descripcion or not metodo:
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return
            
            self.sistema.agregar_contrato_labor(fecha, doc, contratista, descripcion, metodo, monto, notas)
            messagebox.showinfo("Éxito", "Contrato guardado correctamente")
            
            # Limpiar campos
            self.entrada_doc_con.delete(0, tk.END)
            self.entrada_contratista.delete(0, tk.END)
            self.entrada_desc_con.delete(0, tk.END)
            self.combo_metodo_con.delete(0, tk.END)
            self.entrada_monto_con.delete(0, tk.END)
            self.entrada_notas_con.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor verifica la fecha y el monto")
    
    def actualizar_ingresos(self):
        """Actualiza la tabla de ingresos"""
        for item in self.tree_ingresos.get_children():
            self.tree_ingresos.delete(item)
        
        ingresos = self.sistema.obtener_ingresos()
        for i, ingreso in enumerate(ingresos, 1):
            self.tree_ingresos.insert("", "end", text=str(i), values=(
                ingreso['Date'],
                ingreso['Document Number'],
                ingreso['Customer'],
                ingreso['Category'],
                ingreso['Payment Method'],
                ingreso['Status'],
                f"${ingreso['Amount']:.2f}" if ingreso['Amount'] else "$0.00"
            ))
    
    def actualizar_gastos(self):
        """Actualiza la tabla de gastos"""
        for item in self.tree_gastos.get_children():
            self.tree_gastos.delete(item)
        
        gastos = self.sistema.obtener_gastos()
        for i, gasto in enumerate(gastos, 1):
            self.tree_gastos.insert("", "end", text=str(i), values=(
                gasto['Date'],
                gasto['Document Number'],
                gasto['Description'],
                gasto['Supplier'],
                gasto['Category'],
                f"${gasto['Amount']:.2f}" if gasto['Amount'] else "$0.00"
            ))
    
    def generar_pl(self):
        """Genera el reporte P&L"""
        mes = int(self.spin_mes.get())
        año = int(self.spin_año.get())
        
        totales = self.sistema.calcular_totales_mes(año, mes)
        
        self.text_pl.delete(1.0, tk.END)
        
        mes_nombre = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes-1]
        
        reporte = f"""
╔════════════════════════════════════════════════╗
║     PROFIT & LOSS STATEMENT (P&L REPORT)      ║
║               {mes_nombre} {año}                      ║
╚════════════════════════════════════════════════╝

REVENUE / INGRESOS:
─────────────────────────────────────────────────
Total Revenue ........................... ${totales['ingresos']:>12,.2f}

EXPENSES / GASTOS:
─────────────────────────────────────────────────
Total Expenses .......................... ${totales['gastos']:>12,.2f}

NET PROFIT / UTILIDAD NETA:
─────────────────────────────────────────────────
Net Profit .............................. ${totales['neto']:>12,.2f}

═════════════════════════════════════════════════
"""
        
        self.text_pl.insert(tk.END, reporte)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazPrincipal(ventana)
    ventana.mainloop()

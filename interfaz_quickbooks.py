import tkinter as tk
from tkinter import ttk, messagebox
from sistema_excel import SistemaExcel
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class InterfazQuickBooks:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Contabilidad - QuickBooks Style")
        self.ventana.geometry("1400x800")
        
        # Cargar sistema Excel
        self.sistema = SistemaExcel("Libro1.xlsx")
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz principal con sidebar"""
        # Frame principal horizontal
        frame_main = ttk.Frame(self.ventana)
        frame_main.pack(fill="both", expand=True)
        
        # SIDEBAR
        self.sidebar = ttk.Frame(frame_main, width=200)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Título del sidebar
        titulo_sidebar = ttk.Label(self.sidebar, text="MENÚ", font=("Arial", 14, "bold"))
        titulo_sidebar.pack(pady=20, padx=10)
        
        # Botones del sidebar
        botones = [
            ("📊 Dashboard", lambda: self.mostrar_dashboard()),
            ("💰 Ingresos", lambda: self.mostrar_ingresos()),
            ("💸 Gastos", lambda: self.mostrar_gastos()),
            ("👷 Contract Labor", lambda: self.mostrar_contratos()),
            ("👥 Clientes", lambda: self.mostrar_clientes()),
            ("🏢 Proveedores", lambda: self.mostrar_proveedores()),
            ("📈 Reportes", lambda: self.mostrar_reportes()),
            ("⚙️ Configuración", lambda: self.mostrar_configuracion()),
        ]
        
        for texto, comando in botones:
            btn = ttk.Button(self.sidebar, text=texto, command=comando, width=20)
            btn.pack(pady=5, padx=10)
        
        # CONTENIDO PRINCIPAL
        self.frame_contenido = ttk.Frame(frame_main)
        self.frame_contenido.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Mostrar dashboard por defecto
        self.mostrar_dashboard()
    
    def limpiar_contenido(self):
        """Limpia el frame de contenido"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
    
    def mostrar_dashboard(self):
        """Muestra el dashboard principal"""
        self.limpiar_contenido()
        
        # Título
        titulo = ttk.Label(self.frame_contenido, text="DASHBOARD", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        # Obtener datos del mes actual
        ahora = datetime.now()
        totales = self.sistema.calcular_totales_mes(ahora.year, ahora.month)
        
        # KPIs
        frame_kpis = ttk.Frame(self.frame_contenido)
        frame_kpis.pack(fill="x", pady=10)
        
        # KPI Ingresos
        frame_kpi_ingresos = ttk.LabelFrame(frame_kpis, text="Total Ingresos", padding=10)
        frame_kpi_ingresos.pack(side="left", padx=10, fill="x", expand=True)
        label_ingresos = ttk.Label(frame_kpi_ingresos, text=f"${totales['ingresos']:,.2f}", 
                                   font=("Arial", 16, "bold"), foreground="green")
        label_ingresos.pack()
        
        # KPI Gastos
        frame_kpi_gastos = ttk.LabelFrame(frame_kpis, text="Total Gastos", padding=10)
        frame_kpi_gastos.pack(side="left", padx=10, fill="x", expand=True)
        label_gastos = ttk.Label(frame_kpi_gastos, text=f"${totales['gastos']:,.2f}", 
                                font=("Arial", 16, "bold"), foreground="red")
        label_gastos.pack()
        
        # KPI Neto
        frame_kpi_neto = ttk.LabelFrame(frame_kpis, text="Utilidad Neta", padding=10)
        frame_kpi_neto.pack(side="left", padx=10, fill="x", expand=True)
        color_neto = "green" if totales['neto'] >= 0 else "red"
        label_neto = ttk.Label(frame_kpi_neto, text=f"${totales['neto']:,.2f}", 
                              font=("Arial", 16, "bold"), foreground=color_neto)
        label_neto.pack()
        
        # Gráficos
        frame_graficos = ttk.Frame(self.frame_contenido)
        frame_graficos.pack(fill="both", expand=True, pady=10)
        
        # Gráfico de ingresos vs gastos (últimos 6 meses)
        self.crear_grafico_ingresos_gastos(frame_graficos)
        
        # Gráfico de gastos por categoría
        self.crear_grafico_gastos_categoria(frame_graficos)
    
    def crear_grafico_ingresos_gastos(self, parent):
        """Crea gráfico de ingresos vs gastos"""
        frame = ttk.LabelFrame(parent, text="Ingresos vs Gastos (últimos 6 meses)", padding=5)
        frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Datos
        meses = []
        ingresos_data = []
        gastos_data = []
        
        ahora = datetime.now()
        for i in range(5, -1, -1):
            fecha = ahora - timedelta(days=30*i)
            totales = self.sistema.calcular_totales_mes(fecha.year, fecha.month)
            meses.append(fecha.strftime("%b"))
            ingresos_data.append(totales['ingresos'])
            gastos_data.append(totales['gastos'])
        
        # Crear figura
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        
        x = np.arange(len(meses))
        width = 0.35
        
        ax.bar(x - width/2, ingresos_data, width, label='Ingresos', color='green', alpha=0.7)
        ax.bar(x + width/2, gastos_data, width, label='Gastos', color='red', alpha=0.7)
        
        ax.set_xlabel('Mes')
        ax.set_ylabel('Monto ($)')
        ax.set_title('Ingresos vs Gastos')
        ax.set_xticks(x)
        ax.set_xticklabels(meses)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def crear_grafico_gastos_categoria(self, parent):
        """Crea gráfico de gastos por categoría"""
        frame = ttk.LabelFrame(parent, text="Distribución de Gastos por Categoría", padding=5)
        frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Obtener datos
        gastos = self.sistema.obtener_gastos()
        categorias_dict = {}
        
        for gasto in gastos:
            cat = gasto['Category'] or 'Sin categoría'
            monto = gasto['Amount'] or 0
            categorias_dict[cat] = categorias_dict.get(cat, 0) + monto
        
        if not categorias_dict:
            label = ttk.Label(frame, text="No hay datos")
            label.pack()
            return
        
        # Crear figura
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        
        labels = list(categorias_dict.keys())[:5]  # Top 5
        sizes = list(categorias_dict.values())[:5]
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title('Gastos por Categoría')
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def mostrar_ingresos(self):
        """Muestra ingresos con opción de agregar"""
        self.limpiar_contenido()
        
        titulo = ttk.Label(self.frame_contenido, text="INGRESOS", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        # Frame para agregar
        frame_agregar = ttk.LabelFrame(self.frame_contenido, text="Agregar Nuevo Ingreso", padding=10)
        frame_agregar.pack(fill="x", padx=10, pady=10)
        
        # Campos
        ttk.Label(frame_agregar, text="Fecha:").grid(row=0, column=0, sticky="w")
        entrada_fecha = ttk.Entry(frame_agregar)
        entrada_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        entrada_fecha.grid(row=0, column=1)
        
        ttk.Label(frame_agregar, text="Cliente:").grid(row=1, column=0, sticky="w")
        clientes = self.sistema.obtener_clientes()
        combo_cliente = ttk.Combobox(frame_agregar, values=clientes)
        combo_cliente.grid(row=1, column=1)
        
        ttk.Label(frame_agregar, text="Categoría:").grid(row=2, column=0, sticky="w")
        categorias = self.sistema.obtener_categorias_ingresos()
        combo_cat = ttk.Combobox(frame_agregar, values=categorias)
        combo_cat.grid(row=2, column=1)
        
        ttk.Label(frame_agregar, text="Monto:").grid(row=3, column=0, sticky="w")
        entrada_monto = ttk.Entry(frame_agregar)
        entrada_monto.grid(row=3, column=1)
        
        ttk.Label(frame_agregar, text="Método de Pago:").grid(row=4, column=0, sticky="w")
        metodos = self.sistema.obtener_metodos_pago()
        combo_metodo = ttk.Combobox(frame_agregar, values=metodos)
        combo_metodo.grid(row=4, column=1)
        
        def guardar():
            try:
                fecha = datetime.strptime(entrada_fecha.get(), "%Y-%m-%d")
                cliente = combo_cliente.get()
                categoria = combo_cat.get()
                monto = float(entrada_monto.get())
                metodo = combo_metodo.get()
                
                if not cliente or not categoria or not metodo:
                    messagebox.showerror("Error", "Completa todos los campos")
                    return
                
                self.sistema.agregar_ingreso(fecha, "", cliente, categoria, metodo, "Completed", monto, "")
                messagebox.showinfo("Éxito", "Ingreso guardado")
                self.mostrar_ingresos()
            except ValueError:
                messagebox.showerror("Error", "Verifica los datos")
        
        ttk.Button(frame_agregar, text="💾 Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Tabla de ingresos
        frame_tabla = ttk.LabelFrame(self.frame_contenido, text="Listado de Ingresos", padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=("Fecha", "Cliente", "Categoría", "Monto"), height=15)
        tree.heading("#0", text="ID")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Cliente", text="Cliente")
        tree.heading("Categoría", text="Categoría")
        tree.heading("Monto", text="Monto")
        
        tree.column("#0", width=30)
        tree.column("Fecha", width=100)
        tree.column("Cliente", width=150)
        tree.column("Categoría", width=150)
        tree.column("Monto", width=100)
        
        ingresos = self.sistema.obtener_ingresos()
        for i, ingreso in enumerate(ingresos, 1):
            tree.insert("", "end", text=str(i), values=(
                ingreso['Date'],
                ingreso['Customer'],
                ingreso['Category'],
                f"${ingreso['Amount']:.2f}" if ingreso['Amount'] else "$0.00"
            ))
        
        tree.pack(fill="both", expand=True)
    
    def mostrar_gastos(self):
        """Muestra gastos con opción de agregar"""
        self.limpiar_contenido()
        
        titulo = ttk.Label(self.frame_contenido, text="GASTOS", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        # Frame para agregar
        frame_agregar = ttk.LabelFrame(self.frame_contenido, text="Agregar Nuevo Gasto", padding=10)
        frame_agregar.pack(fill="x", padx=10, pady=10)
        
        # Campos
        ttk.Label(frame_agregar, text="Fecha:").grid(row=0, column=0, sticky="w")
        entrada_fecha = ttk.Entry(frame_agregar)
        entrada_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        entrada_fecha.grid(row=0, column=1)
        
        ttk.Label(frame_agregar, text="Descripción:").grid(row=1, column=0, sticky="w")
        entrada_desc = ttk.Entry(frame_agregar)
        entrada_desc.grid(row=1, column=1)
        
        ttk.Label(frame_agregar, text="Proveedor:").grid(row=2, column=0, sticky="w")
        proveedores = self.sistema.obtener_proveedores()
        combo_proveedor = ttk.Combobox(frame_agregar, values=proveedores)
        combo_proveedor.grid(row=2, column=1)
        
        ttk.Label(frame_agregar, text="Categoría:").grid(row=3, column=0, sticky="w")
        categorias = self.sistema.obtener_categorias_gastos()
        combo_cat = ttk.Combobox(frame_agregar, values=categorias)
        combo_cat.grid(row=3, column=1)
        
        ttk.Label(frame_agregar, text="Monto:").grid(row=4, column=0, sticky="w")
        entrada_monto = ttk.Entry(frame_agregar)
        entrada_monto.grid(row=4, column=1)
        
        def guardar():
            try:
                fecha = datetime.strptime(entrada_fecha.get(), "%Y-%m-%d")
                desc = entrada_desc.get()
                proveedor = combo_proveedor.get()
                categoria = combo_cat.get()
                monto = float(entrada_monto.get())
                
                if not desc or not proveedor or not categoria:
                    messagebox.showerror("Error", "Completa todos los campos")
                    return
                
                self.sistema.agregar_gasto(fecha, "", desc, proveedor, categoria, "Operating", "Cash", "Completed", monto, "")
                messagebox.showinfo("Éxito", "Gasto guardado")
                self.mostrar_gastos()
            except ValueError:
                messagebox.showerror("Error", "Verifica los datos")
        
        ttk.Button(frame_agregar, text="💾 Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Tabla de gastos
        frame_tabla = ttk.LabelFrame(self.frame_contenido, text="Listado de Gastos", padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=("Fecha", "Descripción", "Proveedor", "Categoría", "Monto"), height=15)
        tree.heading("#0", text="ID")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Descripción", text="Descripción")
        tree.heading("Proveedor", text="Proveedor")
        tree.heading("Categoría", text="Categoría")
        tree.heading("Monto", text="Monto")
        
        tree.column("#0", width=30)
        tree.column("Fecha", width=80)
        tree.column("Descripción", width=150)
        tree.column("Proveedor", width=150)
        tree.column("Categoría", width=120)
        tree.column("Monto", width=100)
        
        gastos = self.sistema.obtener_gastos()
        for i, gasto in enumerate(gastos, 1):
            tree.insert("", "end", text=str(i), values=(
                gasto['Date'],
                gasto['Description'],
                gasto['Supplier'],
                gasto['Category'],
                f"${gasto['Amount']:.2f}" if gasto['Amount'] else "$0.00"
            ))
        
        tree.pack(fill="both", expand=True)
    
    def mostrar_contratos(self):
        """Muestra Contract Labor"""
        self.limpiar_contenido()
        
        titulo = ttk.Label(self.frame_contenido, text="CONTRACT LABOR", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        # Tabla
        tree = ttk.Treeview(self.frame_contenido, columns=("Fecha", "Contratista", "Descripción", "Monto"), height=20)
        tree.heading("#0", text="ID")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Contratista", text="Contratista")
        tree.heading("Descripción", text="Descripción")
        tree.heading("Monto", text="Monto")
        
        tree.column("#0", width=30)
        tree.column("Fecha", width=100)
        tree.column("Contratista", width=150)
        tree.column("Descripción", width=200)
        tree.column("Monto", width=100)
        
        contratos = self.sistema.obtener_contratos_labor()
        for i, contrato in enumerate(contratos, 1):
            tree.insert("", "end", text=str(i), values=(
                contrato['Date'],
                contrato['Contractor Name'],
                contrato['Description'],
                f"${contrato['Amount']:.2f}" if contrato['Amount'] else "$0.00"
            ))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    def mostrar_clientes(self):
        """Muestra clientes"""
        self.limpiar_contenido()
        
        titulo = ttk.Label(self.frame_contenido, text="CLIENTES", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        clientes = self.sistema.obtener_clientes()
        label = ttk.Label(self.frame_contenido, text=f"Total de clientes: {len(clientes)}", font=("Arial", 12))
        label.pack(pady=10)
        
        text = tk.Text(self.frame_contenido, height=20, width=50)
        text.pack(padx=10, pady=10, fill="both", expand=True)
        
        for cliente in clientes:
            text.insert(tk.END, f"• {cliente}\n")
        
        text.config(state="disabled")
    
    def mostrar_proveedores(self):
        """Muestra proveedores"""
        self.limpiar_contenido()
        
        titulo = ttk.Label(self.frame_contenido, text="PROVEEDORES", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        proveedores = self.sistema.obtener_proveedores()
        label = ttk.Label(self.frame_contenido, text=f"Total de proveedores: {len(proveedores)}", font=("Arial", 12))
        label.pack(pady=10)
        
        text = tk.Text(self.frame_contenido, height=20, width=50)
        text.pack(padx=10, pady=10, fill="both", expand=True)
        
        for proveedor in proveedores:
            text.insert(tk.END, f"• {proveedor}\n")
        
        text.config(state="disabled")
    
    def mostrar_reportes(self):
        """Muestra reportes"""
        self.limpiar_contenido()
        
        titulo = ttk.Label(self.frame_contenido, text="REPORTES", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        # Selección de mes/año
        frame_fecha = ttk.Frame(self.frame_contenido)
        frame_fecha.pack(pady=10)
        
        ttk.Label(frame_fecha, text="Mes:").pack(side="left", padx=5)
        spin_mes = ttk.Spinbox(frame_fecha, from_=1, to=12, width=5)
        spin_mes.set(datetime.now().month)
        spin_mes.pack(side="left", padx=5)
        
        ttk.Label(frame_fecha, text="Año:").pack(side="left", padx=5)
        spin_año = ttk.Spinbox(frame_fecha, from_=2020, to=2030, width=5)
        spin_año.set(datetime.now().year)
        spin_año.pack(side="left", padx=5)
        
        # Text para mostrar reporte
        text_reporte = tk.Text(self.frame_contenido, height=25, width=100)
        text_reporte.pack(padx=10, pady=10, fill="both", expand=True)
        
        def generar_reporte():
            mes = int(spin_mes.get())
            año = int(spin_año.get())
            totales = self.sistema.calcular_totales_mes(año, mes)
            
            mes_nombre = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                          "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes-1]
            
            reporte = f"""
╔════════════════════════════════════════════════════╗
║        INCOME STATEMENT (P&L REPORT)              ║
║               {mes_nombre} {año}                       ║
╚════════════════════════════════════════════════════╝

REVENUE / INGRESOS:
─────────────────────────────────────────────────────
Gross receipts or sales .................... ${totales['ingresos']:>12,.2f}

TOTAL REVENUE ............................. ${totales['ingresos']:>12,.2f}

EXPENSES / GASTOS:
─────────────────────────────────────────────────────
Total Operating Expenses .................. ${totales['gastos']:>12,.2f}

TOTAL EXPENSES ............................ ${totales['gastos']:>12,.2f}

NET INCOME / UTILIDAD NETA:
─────────────────────────────────────────────────────
Net Profit / Loss ......................... ${totales['neto']:>12,.2f}

═════════════════════════════════════════════════════
"""
            text_reporte.delete(1.0, tk.END)
            text_reporte.insert(tk.END, reporte)
        
        ttk.Button(frame_fecha, text="📊 Generar", command=generar_reporte).pack(side="left", padx=10)
        generar_reporte()
    
    def mostrar_configuracion(self):
        """Muestra configuración"""
        self.limpiar_contenido()
        
        titulo = ttk.Label(self.frame_contenido, text="CONFIGURACIÓN", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)
        
        frame = ttk.Frame(self.frame_contenido)
        frame.pack(padx=20, pady=20)
        
        ttk.Label(frame, text="Configuración del Sistema", font=("Arial", 12)).pack(pady=10)
        
        ttk.Label(frame, text="Archivo Excel: Libro1.xlsx").pack(pady=5)
        ttk.Label(frame, text="Última actualización: " + datetime.now().strftime("%Y-%m-%d %H:%M")).pack(pady=5)
        
        ttk.Button(frame, text="🔄 Recargar datos", command=lambda: messagebox.showinfo("Info", "Datos recargados")).pack(pady=10)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazQuickBooks(ventana)
    ventana.mainloop()

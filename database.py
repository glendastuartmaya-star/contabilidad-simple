import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """Maneja la base de datos SQLite para cada empresa"""
    
    def __init__(self, empresa_nombre):
        self.empresa_nombre = empresa_nombre
        self.db_folder = "empresas_db"
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)
        
        self.db_path = os.path.join(self.db_folder, f"{empresa_nombre}.db")
        self.conexion = None
        self.conectar()
        self.crear_tablas()
    
    def conectar(self):
        """Conecta a la base de datos"""
        self.conexion = sqlite3.connect(self.db_path)
        self.conexion.row_factory = sqlite3.Row
    
    def ejecutar(self, sql, parametros=()):
        """Ejecuta un comando SQL"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, parametros)
            self.conexion.commit()
            return cursor
        except Exception as e:
            print(f"Error en base de datos: {e}")
            return None
    
    def consultar(self, sql, parametros=()):
        """Consulta datos"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, parametros)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en consulta: {e}")
            return []
    
    def crear_tablas(self):
        """Crea todas las tablas necesarias"""
        
        # Tabla de Usuarios
        self.ejecutar('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL,
                rol TEXT NOT NULL,
                estado TEXT DEFAULT 'activo',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de Plan de Cuentas (Chart of Accounts)
        self.ejecutar('''
            CREATE TABLE IF NOT EXISTS plan_cuentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_cuenta TEXT UNIQUE NOT NULL,
                nombre_cuenta TEXT NOT NULL,
                tipo_cuenta TEXT NOT NULL,
                tipo_movimiento TEXT NOT NULL,
                categoria_principal TEXT NOT NULL,
                categoria_secundaria TEXT,
                saldo_inicial REAL DEFAULT 0,
                saldo_actual REAL DEFAULT 0,
                estado TEXT DEFAULT 'activo',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de Asientos Contables (Journal Entries)
        self.ejecutar('''
            CREATE TABLE IF NOT EXISTS asientos_contables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_asiento TEXT UNIQUE NOT NULL,
                fecha DATE NOT NULL,
                descripcion TEXT NOT NULL,
                total_deudor REAL DEFAULT 0,
                total_acreedor REAL DEFAULT 0,
                usuario_id INTEGER NOT NULL,
                estado TEXT DEFAULT 'registrado',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabla de Detalles de Asientos (Journal Entry Details)
        self.ejecutar('''
            CREATE TABLE IF NOT EXISTS detalles_asientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asiento_id INTEGER NOT NULL,
                cuenta_id INTEGER NOT NULL,
                concepto TEXT NOT NULL,
                debe REAL DEFAULT 0,
                haber REAL DEFAULT 0,
                FOREIGN KEY(asiento_id) REFERENCES asientos_contables(id),
                FOREIGN KEY(cuenta_id) REFERENCES plan_cuentas(id)
            )
        ''')
        
        # Tabla de Ingresos
        self.ejecutar('''
            CREATE TABLE IF NOT EXISTS ingresos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_documento TEXT UNIQUE NOT NULL,
                fecha DATE NOT NULL,
                cliente TEXT NOT NULL,
                categoria TEXT NOT NULL,
                metodo_pago TEXT NOT NULL,
                monto REAL NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                notas TEXT,
                usuario_id INTEGER NOT NULL,
                asiento_id INTEGER,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY(asiento_id) REFERENCES asientos_contables(id)
            )
        ''')
        
        # Tabla de Gastos
        self.ejecutar('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_documento TEXT UNIQUE NOT NULL,
                fecha DATE NOT NULL,
                descripcion TEXT NOT NULL,
                proveedor TEXT NOT NULL,
                categoria TEXT NOT NULL,
                tipo TEXT NOT NULL,
                metodo_pago TEXT NOT NULL,
                monto REAL NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                notas TEXT,
                usuario_id INTEGER NOT NULL,
                asiento_id INTEGER,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY(asiento_id) REFERENCES asientos_contables(id)
            )
        ''')
        
        # Tabla de Contratos de Labor
        self.ejecutar('''
            CREATE TABLE IF NOT EXISTS contratos_labor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_documento TEXT UNIQUE NOT NULL,
                fecha DATE NOT NULL,
                contratista TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                metodo_pago TEXT NOT NULL,
                monto REAL NOT NULL,
                notas TEXT,
                usuario_id INTEGER NOT NULL,
                asiento_id INTEGER,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY(asiento_id) REFERENCES asientos_contables(id)
            )
        ''')
        
        # Tabla de Auditoría
        self.ejecutar('''
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                accion TEXT NOT NULL,
                tabla_afectada TEXT NOT NULL,
                registro_id INTEGER,
                descripcion TEXT,
                fecha_accion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        ''')

class SistemaContable:
    """Sistema de contabilidad con doble entrada"""
    
    def __init__(self, empresa_nombre):
        self.db = DatabaseManager(empresa_nombre)
        self.empresa_nombre = empresa_nombre
    
    def crear_usuario(self, nombre, email, contraseña, rol):
        """Crea un nuevo usuario"""
        self.db.ejecutar('''
            INSERT INTO usuarios (nombre, email, contraseña, rol)
            VALUES (?, ?, ?, ?)
        ''', (nombre, email, contraseña, rol))
        
        self.registrar_auditoria(1, "CREAR_USUARIO", "usuarios", None, f"Usuario {nombre} creado")
    
    def inicializar_plan_cuentas(self):
        """Inicializa el plan de cuentas tipo QuickBooks"""
        plan_cuentas = [
            # ACTIVOS
            ("1000", "Caja", "ACTIVO", "DEUDOR", "ACTIVOS CIRCULANTES", "Efectivo"),
            ("1010", "Caja Chica", "ACTIVO", "DEUDOR", "ACTIVOS CIRCULANTES", "Efectivo"),
            ("1100", "Banco Checking", "ACTIVO", "DEUDOR", "ACTIVOS CIRCULANTES", "Bancos"),
            ("1110", "Banco Savings", "ACTIVO", "DEUDOR", "ACTIVOS CIRCULANTES", "Bancos"),
            ("1200", "Cuentas por Cobrar", "ACTIVO", "DEUDOR", "ACTIVOS CIRCULANTES", "Cuentas por Cobrar"),
            ("1300", "Inventario", "ACTIVO", "DEUDOR", "ACTIVOS CIRCULANTES", "Inventario"),
            ("1500", "Activos Fijos", "ACTIVO", "DEUDOR", "ACTIVOS NO CIRCULANTES", "Propiedad, Planta y Equipo"),
            ("1510", "Depreciación Acumulada", "ACTIVO", "ACREEDOR", "ACTIVOS NO CIRCULANTES", "Depreciación"),
            
            # PASIVOS
            ("2000", "Cuentas por Pagar", "PASIVO", "ACREEDOR", "PASIVOS CIRCULANTES", "Cuentas por Pagar"),
            ("2100", "Impuestos por Pagar", "PASIVO", "ACREEDOR", "PASIVOS CIRCULANTES", "Impuestos"),
            ("2200", "Préstamos Corto Plazo", "PASIVO", "ACREEDOR", "PASIVOS CIRCULANTES", "Préstamos"),
            ("2500", "Préstamos Largo Plazo", "PASIVO", "ACREEDOR", "PASIVOS NO CIRCULANTES", "Préstamos"),
            
            # PATRIMONIO
            ("3000", "Capital Social", "PATRIMONIO", "ACREEDOR", "PATRIMONIO", "Capital"),
            ("3100", "Ganancias Retenidas", "PATRIMONIO", "ACREEDOR", "PATRIMONIO", "Ganancias Retenidas"),
            ("3200", "Ganancias del Período", "PATRIMONIO", "ACREEDOR", "PATRIMONIO", "Ganancias Actuales"),
            
            # INGRESOS
            ("4000", "Ventas de Productos", "INGRESO", "ACREEDOR", "INGRESOS", "Ventas"),
            ("4100", "Ingresos por Servicios", "INGRESO", "ACREEDOR", "INGRESOS", "Servicios"),
            ("4200", "Otros Ingresos", "INGRESO", "ACREEDOR", "INGRESOS", "Otros"),
            
            # GASTOS - OPERATING
            ("5000", "Publicidad", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Marketing"),
            ("5100", "Comisiones", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Comisiones"),
            ("5200", "Suministros de Oficina", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Suministros"),
            ("5300", "Servicios Profesionales", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Servicios"),
            ("5400", "Renta de Oficina", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Renta"),
            ("5500", "Servicios Públicos", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Utilidades"),
            ("5600", "Seguros", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Seguros"),
            ("5700", "Reparaciones y Mantenimiento", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Mantenimiento"),
            ("5800", "Depreciación", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Depreciación"),
            ("5900", "Gastos Varios", "GASTO", "DEUDOR", "GASTOS OPERACIONALES", "Otros"),
            
            # GASTOS - COGS
            ("6000", "Costo de Bienes Vendidos", "GASTO", "DEUDOR", "COGS", "COGS"),
            ("6100", "Materiales Directos", "GASTO", "DEUDOR", "COGS", "Materiales"),
            
            # GASTOS - PAYROLL
            ("7000", "Sueldos y Salarios", "GASTO", "DEUDOR", "PAYROLL", "Nómina"),
            ("7100", "Impuestos Nómina", "GASTO", "DEUDOR", "PAYROLL", "Impuestos Nómina"),
            ("7200", "Beneficios Empleados", "GASTO", "DEUDOR", "PAYROLL", "Beneficios"),
            
            # GASTOS - FINANCIEROS
            ("8000", "Intereses", "GASTO", "DEUDOR", "GASTOS FINANCIEROS", "Intereses"),
            ("8100", "Comisiones Bancarias", "GASTO", "DEUDOR", "GASTOS FINANCIEROS", "Comisiones"),
            
            # GASTOS - IMPUESTOS
            ("9000", "Impuesto a la Renta", "GASTO", "DEUDOR", "IMPUESTOS", "Impuesto Renta"),
            ("9100", "Impuesto Sobre Ventas", "GASTO", "DEUDOR", "IMPUESTOS", "Impuesto Ventas"),
            
            # GASTOS - NO DEDUCTIBLES
            ("9500", "Ganancias/Pérdidas de Capital", "GASTO", "DEUDOR", "NO DEDUCTIBLES", "Capital"),
            ("9600", "Distribución a Propietarios", "GASTO", "DEUDOR", "NO DEDUCTIBLES", "Distribución"),
        ]
        
        for cuenta in plan_cuentas:
            self.db.ejecutar('''
                INSERT OR IGNORE INTO plan_cuentas 
                (numero_cuenta, nombre_cuenta, tipo_cuenta, tipo_movimiento, categoria_principal, categoria_secundaria)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', cuenta)
    
    def crear_asiento_contable(self, fecha, descripcion, usuario_id, detalles):
        """
        Crea un asiento contable con detalles
        detalles = [(cuenta_id, concepto, debe, haber), ...]
        """
        # Generar número de asiento
        resultado = self.db.consultar('SELECT COUNT(*) as count FROM asientos_contables')
        numero_asiento = f"ASI-{resultado[0][0] + 1:06d}"
        
        # Validar que debita = acredita
        total_debe = sum(d[2] for d in detalles)
        total_haber = sum(d[3] for d in detalles)
        
        if abs(total_debe - total_haber) > 0.01:
            return None, "El debe no es igual al haber"
        
        # Insertar asiento
        self.db.ejecutar('''
            INSERT INTO asientos_contables (numero_asiento, fecha, descripcion, total_deudor, total_acreedor, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (numero_asiento, fecha, descripcion, total_debe, total_haber, usuario_id))
        
        # Obtener ID del asiento
        resultado = self.db.consultar('SELECT id FROM asientos_contables WHERE numero_asiento = ?', (numero_asiento,))
        asiento_id = resultado[0][0]
        
        # Insertar detalles
        for cuenta_id, concepto, debe, haber in detalles:
            self.db.ejecutar('''
                INSERT INTO detalles_asientos (asiento_id, cuenta_id, concepto, debe, haber)
                VALUES (?, ?, ?, ?, ?)
            ''', (asiento_id, cuenta_id, concepto, debe, haber))
            
            # Actualizar saldo de cuenta
            if debe > 0:
                self.db.ejecutar('UPDATE plan_cuentas SET saldo_actual = saldo_actual + ? WHERE id = ?', (debe, cuenta_id))
            else:
                self.db.ejecutar('UPDATE plan_cuentas SET saldo_actual = saldo_actual - ? WHERE id = ?', (haber, cuenta_id))
        
        self.registrar_auditoria(usuario_id, "CREAR_ASIENTO", "asientos_contables", asiento_id, f"Asiento {numero_asiento}")
        
        return asiento_id, "Asiento creado correctamente"
    
    def registrar_auditoria(self, usuario_id, accion, tabla, registro_id, descripcion):
        """Registra una acción en la auditoría"""
        self.db.ejecutar('''
            INSERT INTO auditoria (usuario_id, accion, tabla_afectada, registro_id, descripcion)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, accion, tabla, registro_id, descripcion))
    
    def obtener_balance_general(self, fecha):
        """Obtiene el Balance General (Balance Sheet) a una fecha específica"""
        resultado = self.db.consultar('''
            SELECT 
                numero_cuenta, 
                nombre_cuenta, 
                categoria_principal,
                saldo_actual
            FROM plan_cuentas
            WHERE estado = 'activo'
            ORDER BY numero_cuenta
        ''')
        
        balance = {
            'ACTIVOS': {},
            'PASIVOS': {},
            'PATRIMONIO': {}
        }
        
        for row in resultado:
            categoria = row[2]
            if 'ACTIVOS' in categoria:
                if 'ACTIVOS CIRCULANTES' not in balance['ACTIVOS']:
                    balance['ACTIVOS']['ACTIVOS CIRCULANTES'] = []
                balance['ACTIVOS']['ACTIVOS CIRCULANTES'].append({
                    'numero': row[0],
                    'nombre': row[1],
                    'saldo': row[3]
                })
            elif 'PASIVOS' in categoria:
                if 'PASIVOS CIRCULANTES' not in balance['PASIVOS']:
                    balance['PASIVOS']['PASIVOS CIRCULANTES'] = []
                balance['PASIVOS']['PASIVOS CIRCULANTES'].append({
                    'numero': row[0],
                    'nombre': row[1],
                    'saldo': row[3]
                })
            elif 'PATRIMONIO' in categoria:
                if 'PATRIMONIO' not in balance['PATRIMONIO']:
                    balance['PATRIMONIO']['PATRIMONIO'] = []
                balance['PATRIMONIO']['PATRIMONIO'].append({
                    'numero': row[0],
                    'nombre': row[1],
                    'saldo': row[3]
                })
        
        return balance
    
    def obtener_estado_resultados(self, fecha_inicio, fecha_fin):
        """Obtiene el Estado de Resultados (Income Statement)"""
        resultado = self.db.consultar('''
            SELECT 
                numero_cuenta,
                nombre_cuenta,
                categoria_principal,
                SUM(CASE WHEN debe > 0 THEN debe ELSE 0 END) as debe,
                SUM(CASE WHEN haber > 0 THEN haber ELSE 0 END) as haber
            FROM plan_cuentas pc
            LEFT JOIN detalles_asientos da ON pc.id = da.cuenta_id
            LEFT JOIN asientos_contables ac ON da.asiento_id = ac.id
            WHERE ac.fecha BETWEEN ? AND ?
            AND pc.tipo_cuenta IN ('INGRESO', 'GASTO')
            GROUP BY pc.id
            ORDER BY pc.numero_cuenta
        ''', (fecha_inicio, fecha_fin))
        
        estado = {
            'INGRESOS': [],
            'GASTOS': []
        }
        
        for row in resultado:
            if 'INGRESO' in row[2]:
                estado['INGRESOS'].append({
                    'numero': row[0],
                    'nombre': row[1],
                    'monto': row[3] - row[4]
                })
            else:
                estado['GASTOS'].append({
                    'numero': row[0],
                    'nombre': row[1],
                    'monto': row[3]
                })
        
        return estado

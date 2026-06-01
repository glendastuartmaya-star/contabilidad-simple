"""
Sistema de Flujo de Caja
Proyecta y monitorea el flujo de efectivo
"""
from datetime import datetime
from database import DatabaseManager

class GestorFlujoCaja:
    """Gestiona proyecciones de flujo de caja"""
    
    def __init__(self, empresa_nombre):
        self.db = DatabaseManager(empresa_nombre)
        self.crear_tablas()
    
    def crear_tablas(self):
        """Crea tablas para flujo de caja"""
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS proyecciones_flujo_caja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE NOT NULL,
                saldo_inicial REAL NOT NULL,
                ingresos_proyectados REAL NOT NULL DEFAULT 0,
                egresos_proyectados REAL NOT NULL DEFAULT 0,
                saldo_final REAL,
                estado TEXT DEFAULT 'borrador',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS lineas_flujo_caja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proyeccion_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                concepto TEXT NOT NULL,
                tipo TEXT NOT NULL,
                monto REAL NOT NULL,
                FOREIGN KEY(proyeccion_id) REFERENCES proyecciones_flujo_caja(id)
            )
        ''')
    
    def obtener_saldo_efectivo(self):
        """Obtiene saldo de efectivo"""
        resultado = self.db.consultar('''
            SELECT SUM(saldo_actual) 
            FROM plan_cuentas 
            WHERE numero_cuenta LIKE '1%' AND (nombre_cuenta LIKE '%Caja%' OR nombre_cuenta LIKE '%Banco%')
        ''')
        
        return resultado[0][0] or 0
    
    def crear_proyeccion(self, fecha_inicio, fecha_fin, saldo_inicial):
        """Crea una proyección de flujo de caja"""
        self.db.ejecutar('''
            INSERT INTO proyecciones_flujo_caja 
            (fecha_inicio, fecha_fin, saldo_inicial)
            VALUES (?, ?, ?)
        ''', (fecha_inicio, fecha_fin, saldo_inicial))
        
        resultado = self.db.consultar(
            'SELECT id FROM proyecciones_flujo_caja WHERE fecha_inicio = ? AND saldo_inicial = ?',
            (fecha_inicio, saldo_inicial)
        )
        
        return resultado[0][0] if resultado else None
    
    def agregar_linea_flujo_caja(self, proyeccion_id, fecha, concepto, tipo, monto):
        """Agrega una línea de flujo de caja"""
        self.db.ejecutar('''
            INSERT INTO lineas_flujo_caja 
            (proyeccion_id, fecha, concepto, tipo, monto)
            VALUES (?, ?, ?, ?, ?)
        ''', (proyeccion_id, fecha, concepto, tipo, monto))
        
        return True
    
    def calcular_saldo_proyectado(self, proyeccion_id):
        """Calcula el saldo final proyectado"""
        resultado = self.db.consultar(
            'SELECT saldo_inicial FROM proyecciones_flujo_caja WHERE id = ?',
            (proyeccion_id,)
        )
        
        if not resultado:
            return None
        
        saldo = resultado[0][0]
        
        ingresos = self.db.consultar('''
            SELECT SUM(monto) 
            FROM lineas_flujo_caja 
            WHERE proyeccion_id = ? AND tipo = 'INGRESO'
        ''', (proyeccion_id,))
        
        saldo += (ingresos[0][0] or 0)
        
        egresos = self.db.consultar('''
            SELECT SUM(monto) 
            FROM lineas_flujo_caja 
            WHERE proyeccion_id = ? AND tipo = 'EGRESO'
        ''', (proyeccion_id,))
        
        saldo -= (egresos[0][0] or 0)
        
        self.db.ejecutar('''
            UPDATE proyecciones_flujo_caja 
            SET saldo_final = ?, 
                ingresos_proyectados = ?,
                egresos_proyectados = ?
            WHERE id = ?
        ''', (saldo, ingresos[0][0] or 0, egresos[0][0] or 0, proyeccion_id))
        
        return saldo
    
    def obtener_proyecciones(self):
        """Obtiene todas las proyecciones"""
        return self.db.consultar(
            'SELECT * FROM proyecciones_flujo_caja ORDER BY fecha_inicio DESC'
        )

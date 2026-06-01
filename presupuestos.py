"""
Sistema de Presupuestos
Crea y compara presupuestos con resultados reales
"""
from datetime import datetime
from database import DatabaseManager

class GestorPresupuestos:
    """Gestiona presupuestos"""
    
    def __init__(self, empresa_nombre):
        self.db = DatabaseManager(empresa_nombre)
        self.crear_tablas()
    
    def crear_tablas(self):
        """Crea tablas para presupuestos"""
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS presupuestos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE NOT NULL,
                año INTEGER NOT NULL,
                estado TEXT DEFAULT 'borrador',
                usuario_id INTEGER,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS lineas_presupuesto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                presupuesto_id INTEGER NOT NULL,
                cuenta_id INTEGER NOT NULL,
                nombre_cuenta TEXT NOT NULL,
                monto_presupuestado REAL NOT NULL,
                FOREIGN KEY(presupuesto_id) REFERENCES presupuestos(id),
                FOREIGN KEY(cuenta_id) REFERENCES plan_cuentas(id)
            )
        ''')
    
    def crear_presupuesto(self, nombre, año, fecha_inicio, fecha_fin, usuario_id, descripcion=""):
        """Crea un nuevo presupuesto"""
        self.db.ejecutar('''
            INSERT INTO presupuestos 
            (nombre, descripcion, fecha_inicio, fecha_fin, año, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, fecha_inicio, fecha_fin, año, usuario_id))
        
        resultado = self.db.consultar(
            'SELECT id FROM presupuestos WHERE nombre = ? AND año = ?',
            (nombre, año)
        )
        
        return resultado[0][0] if resultado else None
    
    def agregar_linea_presupuesto(self, presupuesto_id, cuenta_id, nombre_cuenta, monto):
        """Agrega una línea al presupuesto"""
        self.db.ejecutar('''
            INSERT INTO lineas_presupuesto 
            (presupuesto_id, cuenta_id, nombre_cuenta, monto_presupuestado)
            VALUES (?, ?, ?, ?)
        ''', (presupuesto_id, cuenta_id, nombre_cuenta, monto))
        
        return True
    
    def obtener_presupuesto(self, presupuesto_id):
        """Obtiene detalles de un presupuesto"""
        resultado = self.db.consultar(
            'SELECT * FROM presupuestos WHERE id = ?',
            (presupuesto_id,)
        )
        
        if not resultado:
            return None
        
        presupuesto = resultado[0]
        lineas = self.db.consultar(
            'SELECT * FROM lineas_presupuesto WHERE presupuesto_id = ?',
            (presupuesto_id,)
        )
        
        return {
            'presupuesto': presupuesto,
            'lineas': lineas
        }
    
    def obtener_presupuestos(self, estado=None):
        """Obtiene presupuestos"""
        if estado:
            return self.db.consultar(
                'SELECT * FROM presupuestos WHERE estado = ? ORDER BY año DESC',
                (estado,)
            )
        return self.db.consultar(
            'SELECT * FROM presupuestos ORDER BY año DESC'
        )
    
    def aprobar_presupuesto(self, presupuesto_id):
        """Aprueba un presupuesto"""
        self.db.ejecutar(
            'UPDATE presupuestos SET estado = "aprobado" WHERE id = ?',
            (presupuesto_id,)
        )
        return True

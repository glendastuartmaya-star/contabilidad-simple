"""
Módulo de Reconciliación Bancaria
Permite reconciliar transacciones del banco con el sistema
"""
from datetime import datetime
from database import DatabaseManager

class ReconciliacionBancaria:
    """Gestiona la reconciliación de cuentas bancarias"""
    
    def __init__(self, empresa_nombre):
        self.db = DatabaseManager(empresa_nombre)
        self.crear_tablas()
    
    def crear_tablas(self):
        """Crea tablas para reconciliación"""
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS reconciliaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cuenta_banco TEXT NOT NULL,
                fecha_reconciliacion DATE NOT NULL,
                saldo_banco REAL NOT NULL,
                saldo_sistema REAL NOT NULL,
                diferencia REAL,
                estado TEXT DEFAULT 'pendiente',
                notas TEXT,
                usuario_id INTEGER,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS movimientos_reconciliacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reconciliacion_id INTEGER NOT NULL,
                fecha_transaccion DATE NOT NULL,
                descripcion TEXT NOT NULL,
                monto_banco REAL NOT NULL,
                monto_sistema REAL,
                estado_reconciliacion TEXT DEFAULT 'pendiente',
                FOREIGN KEY(reconciliacion_id) REFERENCES reconciliaciones(id)
            )
        ''')
    
    def iniciar_reconciliacion(self, cuenta_banco, saldo_banco, usuario_id):
        """Inicia un nuevo proceso de reconciliación"""
        # Calcular saldo en sistema
        resultado = self.db.consultar(
            'SELECT saldo_actual FROM plan_cuentas WHERE numero_cuenta = ?',
            (cuenta_banco,)
        )
        
        saldo_sistema = resultado[0][0] if resultado else 0
        diferencia = saldo_banco - saldo_sistema
        
        self.db.ejecutar('''
            INSERT INTO reconciliaciones 
            (cuenta_banco, fecha_reconciliacion, saldo_banco, saldo_sistema, diferencia, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (cuenta_banco, datetime.now().date(), saldo_banco, saldo_sistema, diferencia, usuario_id))
        
        return {
            'saldo_banco': saldo_banco,
            'saldo_sistema': saldo_sistema,
            'diferencia': diferencia
        }
    
    def obtener_movimientos_sin_reconciliar(self, cuenta_banco):
        """Obtiene movimientos sin reconciliar"""
        return self.db.consultar('''
            SELECT id, fecha, descripcion, monto 
            FROM asientos_contables
            WHERE estado != 'reconciliado'
            ORDER BY fecha DESC
        ''')
    
    def marcar_como_reconciliado(self, asiento_id):
        """Marca un asiento como reconciliado"""
        self.db.ejecutar(
            'UPDATE asientos_contables SET estado = "reconciliado" WHERE id = ?',
            (asiento_id,)
        )
        return True
    
    def finalizar_reconciliacion(self, reconciliacion_id, estado):
        """Finaliza una reconciliación"""
        self.db.ejecutar(
            'UPDATE reconciliaciones SET estado = ? WHERE id = ?',
            (estado, reconciliacion_id)
        )
        return True
    
    def obtener_reconciliaciones(self):
        """Obtiene todas las reconciliaciones"""
        return self.db.consultar('''
            SELECT id, cuenta_banco, fecha_reconciliacion, saldo_banco, 
                   saldo_sistema, diferencia, estado
            FROM reconciliaciones
            ORDER BY fecha_reconciliacion DESC
        ''')
    
    def generar_reporte_reconciliacion(self, reconciliacion_id):
        """Genera reporte detallado de una reconciliación"""
        resultado = self.db.consultar(
            'SELECT * FROM reconciliaciones WHERE id = ?',
            (reconciliacion_id,)
        )
        
        if not resultado:
            return None
        
        recon = resultado[0]
        movimientos = self.db.consultar(
            'SELECT * FROM movimientos_reconciliacion WHERE reconciliacion_id = ?',
            (reconciliacion_id,)
        )
        
        return {
            'reconciliacion': recon,
            'movimientos': movimientos
        }

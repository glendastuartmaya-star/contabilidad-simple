"""
Módulo de Gestión de Impuestos
Calcula retenciones y reportes de impuestos
"""
from datetime import datetime
from database import DatabaseManager

class GestorImpuestos:
    """Gestiona cálculos y reportes de impuestos"""
    
    def __init__(self, empresa_nombre):
        self.db = DatabaseManager(empresa_nombre)
        self.crear_tablas()
        self.tasa_isr = 0.25
        self.tasa_itbis = 0.18
        self.tasa_retencion_compra = 0.02
        self.tasa_retencion_venta = 0.01
    
    def crear_tablas(self):
        """Crea tablas para impuestos"""
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS retenciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                numero_documento TEXT NOT NULL,
                fecha DATE NOT NULL,
                concepto TEXT NOT NULL,
                monto_base REAL NOT NULL,
                tasa_retencion REAL NOT NULL,
                monto_retenido REAL NOT NULL,
                tercero TEXT,
                numero_comprobante TEXT,
                estado TEXT DEFAULT 'registrada',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS declaraciones_impuestos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_impuesto TEXT NOT NULL,
                periodo_mes INTEGER NOT NULL,
                periodo_año INTEGER NOT NULL,
                monto_base REAL NOT NULL,
                impuesto_causado REAL NOT NULL,
                retenciones_recibidas REAL DEFAULT 0,
                a_pagar REAL,
                a_favor REAL,
                estado TEXT DEFAULT 'borrador',
                fecha_presentacion DATE,
                numero_formulario TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def calcular_isr(self, ingresos_netos):
        """Calcula Impuesto Sobre la Renta"""
        return ingresos_netos * self.tasa_isr
    
    def calcular_itbis(self, monto):
        """Calcula ITBIS"""
        return monto * self.tasa_itbis
    
    def registrar_retencion(self, tipo, numero_documento, concepto, monto_base, 
                           tercero=None, numero_comprobante=None):
        """Registra una retención"""
        if tipo == "compra":
            monto_retenido = monto_base * self.tasa_retencion_compra
        else:
            monto_retenido = monto_base * self.tasa_retencion_venta
        
        self.db.ejecutar('''
            INSERT INTO retenciones 
            (tipo, numero_documento, fecha, concepto, monto_base, 
             tasa_retencion, monto_retenido, tercero, numero_comprobante)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tipo, numero_documento, datetime.now().date(), concepto, 
              monto_base, (self.tasa_retencion_compra if tipo == "compra" 
              else self.tasa_retencion_venta), monto_retenido, tercero, numero_comprobante))
        
        return monto_retenido
    
    def obtener_retenciones(self, tipo=None):
        """Obtiene retenciones registradas"""
        if tipo:
            return self.db.consultar(
                'SELECT * FROM retenciones WHERE tipo = ? ORDER BY fecha DESC',
                (tipo,)
            )
        return self.db.consultar(
            'SELECT * FROM retenciones ORDER BY fecha DESC'
        )

"""
Módulo de Facturación
Genera y gestiona facturas
"""
from datetime import datetime
from database import DatabaseManager
import random

class SistemaFacturacion:
    """Gestiona facturación de ventas"""
    
    def __init__(self, empresa_nombre):
        self.db = DatabaseManager(empresa_nombre)
        self.crear_tablas()
    
    def crear_tablas(self):
        """Crea tablas para facturación"""
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE NOT NULL,
                fecha DATE NOT NULL,
                cliente_id TEXT NOT NULL,
                cliente_nombre TEXT NOT NULL,
                cliente_ruc TEXT,
                subtotal REAL NOT NULL,
                impuesto REAL DEFAULT 0,
                total REAL NOT NULL,
                estado TEXT DEFAULT 'borrador',
                fecha_vencimiento DATE,
                notas TEXT,
                usuario_id INTEGER,
                asiento_id INTEGER,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY(asiento_id) REFERENCES asientos_contables(id)
            )
        ''')
        
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS lineas_factura (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                cantidad REAL NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                impuesto_linea REAL DEFAULT 0,
                total_linea REAL NOT NULL,
                FOREIGN KEY(factura_id) REFERENCES facturas(id)
            )
        ''')
    
    def crear_factura(self, cliente_id, cliente_nombre, cliente_ruc, lineas, impuesto_pct=0, usuario_id=None):
        """Crea una nueva factura"""
        numero_factura = self._generar_numero_factura()
        
        subtotal = sum(l['cantidad'] * l['precio_unitario'] for l in lineas)
        impuesto = subtotal * (impuesto_pct / 100)
        total = subtotal + impuesto
        
        self.db.ejecutar('''
            INSERT INTO facturas 
            (numero_factura, fecha, cliente_id, cliente_nombre, cliente_ruc, 
             subtotal, impuesto, total, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (numero_factura, datetime.now().date(), cliente_id, cliente_nombre, 
              cliente_ruc, subtotal, impuesto, total, usuario_id))
        
        resultado = self.db.consultar(
            'SELECT id FROM facturas WHERE numero_factura = ?',
            (numero_factura,)
        )
        factura_id = resultado[0][0]
        
        for linea in lineas:
            impuesto_linea = linea['cantidad'] * linea['precio_unitario'] * (impuesto_pct / 100)
            total_linea = linea['cantidad'] * linea['precio_unitario'] + impuesto_linea
            
            self.db.ejecutar('''
                INSERT INTO lineas_factura 
                (factura_id, descripcion, cantidad, precio_unitario, 
                 subtotal, impuesto_linea, total_linea)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (factura_id, linea['descripcion'], linea['cantidad'], 
                  linea['precio_unitario'], linea['cantidad'] * linea['precio_unitario'],
                  impuesto_linea, total_linea))
        
        return {
            'numero_factura': numero_factura,
            'factura_id': factura_id,
            'total': total
        }
    
    def emitir_factura(self, factura_id):
        """Emite una factura"""
        self.db.ejecutar(
            'UPDATE facturas SET estado = "emitida" WHERE id = ?',
            (factura_id,)
        )
        return True
    
    def obtener_factura(self, factura_id):
        """Obtiene detalles de una factura"""
        resultado = self.db.consultar(
            'SELECT * FROM facturas WHERE id = ?',
            (factura_id,)
        )
        
        if not resultado:
            return None
        
        factura = resultado[0]
        lineas = self.db.consultar(
            'SELECT * FROM lineas_factura WHERE factura_id = ?',
            (factura_id,)
        )
        
        return {
            'factura': factura,
            'lineas': lineas
        }
    
    def obtener_facturas(self, estado=None):
        """Obtiene todas las facturas"""
        if estado:
            return self.db.consultar(
                'SELECT * FROM facturas WHERE estado = ? ORDER BY fecha DESC',
                (estado,)
            )
        return self.db.consultar(
            'SELECT * FROM facturas ORDER BY fecha DESC'
        )
    
    def _generar_numero_factura(self):
        """Genera número único de factura"""
        fecha = datetime.now()
        numero = random.randint(10000, 99999)
        return f"FAC-{fecha.year}{fecha.month:02d}{fecha.day:02d}-{numero}"

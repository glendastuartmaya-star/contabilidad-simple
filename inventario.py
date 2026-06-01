"""
Sistema de Inventario
Gestiona el inventario y costo de bienes vendidos
"""
from datetime import datetime
from database import DatabaseManager

class GestorInventario:
    """Gestiona el inventario de productos"""
    
    def __init__(self, empresa_nombre):
        self.db = DatabaseManager(empresa_nombre)
        self.crear_tablas()
    
    def crear_tablas(self):
        """Crea tablas para inventario"""
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                categoria TEXT NOT NULL,
                precio_costo REAL NOT NULL,
                precio_venta REAL NOT NULL,
                stock_actual REAL NOT NULL DEFAULT 0,
                stock_minimo REAL NOT NULL DEFAULT 0,
                stock_maximo REAL NOT NULL,
                unidad_medida TEXT DEFAULT 'unidad',
                estado TEXT DEFAULT 'activo',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.db.ejecutar('''
            CREATE TABLE IF NOT EXISTS movimientos_inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                tipo_movimiento TEXT NOT NULL,
                cantidad REAL NOT NULL,
                precio_unitario REAL NOT NULL,
                costo_total REAL NOT NULL,
                documento_numero TEXT,
                referencia TEXT,
                usuario_id INTEGER,
                fecha_movimiento DATE NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(producto_id) REFERENCES productos(id),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        ''')
    
    def crear_producto(self, codigo, nombre, categoria, precio_costo, 
                      precio_venta, stock_minimo, stock_maximo, descripcion=""):
        """Crea un nuevo producto"""
        try:
            self.db.ejecutar('''
                INSERT INTO productos 
                (codigo, nombre, descripcion, categoria, precio_costo, 
                 precio_venta, stock_minimo, stock_maximo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (codigo, nombre, descripcion, categoria, precio_costo, 
                  precio_venta, stock_minimo, stock_maximo))
            return True, f"Producto {nombre} creado"
        except Exception as e:
            return False, str(e)
    
    def registrar_entrada_inventario(self, producto_id, cantidad, precio_unitario, 
                                     documento_numero, usuario_id):
        """Registra entrada de inventario"""
        costo_total = cantidad * precio_unitario
        
        self.db.ejecutar('''
            INSERT INTO movimientos_inventario 
            (producto_id, tipo_movimiento, cantidad, precio_unitario, 
             costo_total, documento_numero, usuario_id, fecha_movimiento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (producto_id, 'ENTRADA', cantidad, precio_unitario, 
              costo_total, documento_numero, usuario_id, datetime.now().date()))
        
        self.db.ejecutar('''
            UPDATE productos 
            SET stock_actual = stock_actual + ? 
            WHERE id = ?
        ''', (cantidad, producto_id))
        
        return True, f"Se ingresaron {cantidad} unidades"
    
    def registrar_salida_inventario(self, producto_id, cantidad, documento_numero, usuario_id):
        """Registra salida de inventario"""
        resultado = self.db.consultar(
            'SELECT precio_costo, stock_actual FROM productos WHERE id = ?',
            (producto_id,)
        )
        
        if not resultado:
            return False, "Producto no encontrado"
        
        precio_costo = resultado[0][0]
        stock_actual = resultado[0][1]
        
        if stock_actual < cantidad:
            return False, f"Stock insuficiente"
        
        costo_total = cantidad * precio_costo
        
        self.db.ejecutar('''
            INSERT INTO movimientos_inventario 
            (producto_id, tipo_movimiento, cantidad, precio_unitario, 
             costo_total, documento_numero, usuario_id, fecha_movimiento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (producto_id, 'SALIDA', cantidad, precio_costo, 
              costo_total, documento_numero, usuario_id, datetime.now().date()))
        
        self.db.ejecutar('''
            UPDATE productos 
            SET stock_actual = stock_actual - ? 
            WHERE id = ?
        ''', (cantidad, producto_id))
        
        return True, f"Se sacaron {cantidad} unidades"
    
    def obtener_productos(self):
        """Obtiene productos activos"""
        return self.db.consultar('''
            SELECT id, codigo, nombre, categoria, precio_costo, precio_venta, 
                   stock_actual, stock_minimo, stock_maximo
            FROM productos 
            WHERE estado = 'activo'
            ORDER BY nombre
        ''')
    
    def obtener_valor_inventario(self):
        """Calcula el valor total del inventario"""
        resultado = self.db.consultar('''
            SELECT SUM(stock_actual * precio_costo) 
            FROM productos 
            WHERE estado = 'activo'
        ''')
        
        return resultado[0][0] or 0
    
    def calcular_cogs(self, fecha_inicio, fecha_fin):
        """Calcula Costo de Bienes Vendidos"""
        resultado = self.db.consultar('''
            SELECT SUM(costo_total) 
            FROM movimientos_inventario 
            WHERE tipo_movimiento = 'SALIDA' 
            AND fecha_movimiento BETWEEN ? AND ?
        ''', (fecha_inicio, fecha_fin))
        
        return resultado[0][0] or 0

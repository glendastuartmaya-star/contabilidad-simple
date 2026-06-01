import hashlib
from database import DatabaseManager

class GestorUsuarios:
    """Gestiona usuarios y roles"""
    
    def __init__(self, empresa_nombre):
        self.db = DatabaseManager(empresa_nombre)
        self.usuario_actual = None
    
    def hash_contraseña(self, contraseña):
        """Convierte contraseña a hash"""
        return hashlib.sha256(contraseña.encode()).hexdigest()
    
    def crear_usuario(self, nombre, email, contraseña, rol):
        """Crea un nuevo usuario"""
        roles_validos = ["Admin", "Contador", "Gerente", "Operario"]
        
        if rol not in roles_validos:
            return False, f"Rol debe ser: {', '.join(roles_validos)}"
        
        contraseña_hash = self.hash_contraseña(contraseña)
        
        try:
            self.db.ejecutar('''
                INSERT INTO usuarios (nombre, email, contraseña, rol)
                VALUES (?, ?, ?, ?)
            ''', (nombre, email, contraseña_hash, rol))
            return True, f"Usuario {nombre} creado como {rol}"
        except Exception as e:
            return False, str(e)
    
    def login(self, email, contraseña):
        """Verifica credenciales de usuario"""
        contraseña_hash = self.hash_contraseña(contraseña)
        
        resultado = self.db.consultar(
            'SELECT * FROM usuarios WHERE email = ? AND contraseña = ? AND estado = "activo"',
            (email, contraseña_hash)
        )
        
        if resultado:
            self.usuario_actual = resultado[0]
            return True, resultado[0]
        
        return False, "Email o contraseña incorrectos"
    
    def obtener_usuarios(self):
        """Obtiene lista de usuarios"""
        return self.db.consultar('SELECT id, nombre, email, rol, estado FROM usuarios')
    
    def cambiar_contraseña(self, usuario_id, contraseña_nueva):
        """Cambia contraseña de usuario"""
        contraseña_hash = self.hash_contraseña(contraseña_nueva)
        self.db.ejecutar(
            'UPDATE usuarios SET contraseña = ? WHERE id = ?',
            (contraseña_hash, usuario_id)
        )
        return True, "Contraseña actualizada"
    
    def desactivar_usuario(self, usuario_id):
        """Desactiva un usuario"""
        self.db.ejecutar(
            'UPDATE usuarios SET estado = "inactivo" WHERE id = ?',
            (usuario_id,)
        )
        return True, "Usuario desactivado"
import json
import os
from datetime import datetime
from pathlib import Path

class SistemaContabilidad:
    def __init__(self):
        self.archivo_datos = "datos_contabilidad.json"
        self.cargar_datos()
    
    def cargar_datos(self):
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                self.datos = json.load(f)
        else:
            self.datos = {
                "transacciones": [],
                "categorias": ["Salario", "Alimento", "Transporte", "Utilidades", "Entretenimiento", "Otro"]
            }
            self.guardar_datos()
    
    def guardar_datos(self):
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=2)
    
    def agregar_transaccion(self, tipo, monto, categoria, descripcion, fecha=None):
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        transaccion = {
            "tipo": tipo,  # "ingreso" o "gasto"
            "monto": float(monto),
            "categoria": categoria,
            "descripcion": descripcion,
            "fecha": fecha
        }
        self.datos["transacciones"].append(transaccion)
        self.guardar_datos()
        return transaccion
    
    def obtener_transacciones_mes(self, año, mes):
        resultado = []
        for t in self.datos["transacciones"]:
            fecha = datetime.strptime(t["fecha"], "%Y-%m-%d")
            if fecha.year == año and fecha.month == mes:
                resultado.append(t)
        return resultado
    
    def calcular_balance_mes(self, año, mes):
        transacciones = self.obtener_transacciones_mes(año, mes)
        ingresos = sum(t["monto"] for t in transacciones if t["tipo"] == "ingreso")
        gastos = sum(t["monto"] for t in transacciones if t["tipo"] == "gasto")
        balance = ingresos - gastos
        return {"ingresos": ingresos, "gastos": gastos, "balance": balance}
    
    def obtener_todas_transacciones(self):
        return self.datos["transacciones"]
    
    def obtener_categorias(self):
        return self.datos["categorias"]
    
    def agregar_categoria(self, categoria):
        if categoria not in self.datos["categorias"]:
            self.datos["categorias"].append(categoria)
            self.guardar_datos()
from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email
    
    @abstractmethod
    def mostrar_info(self):
        pass

class Empleado(Persona):
    def __init__(self, id, nombre, email, salario, depto_id=None):
        super().__init__(nombre, email)
        self.id = id
        self.salario = salario
        self.depto_id = depto_id
        self.direccion = None 
        self.telefono = None

    def mostrar_info(self):
        return f"ID: {self.id} | {self.nombre} | Email: {self.email} | Depto ID: {self.depto_id}"

class Departamento:
    def __init__(self, id, nombre, gerente):
        self.id = id
        self.nombre = nombre
        self.gerente = gerente

    def __str__(self):
        return f"ID: {self.id} | Dept: {self.nombre} | Gerente: {self.gerente}"

class Proyecto:
    def __init__(self, id, nombre, descripcion, fecha_inicio):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

    def __str__(self):
        return f"ID: {self.id} | Proyecto: {self.nombre} | Inicio: {self.fecha_inicio}"
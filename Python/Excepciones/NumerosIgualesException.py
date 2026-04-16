class NumerosIgualesException(Exception): # extiende de la clase
    def __init__(self, mensaje="Los números son iguales."): # constructor de la clase, recibe un mensaje opcional
        self.mensaje = mensaje # asigna el mensaje a un atributo de la clase
    super().__init__(self.mensaje) # llama al constructor de la clase padre (Exception) con el mensaje como argumento
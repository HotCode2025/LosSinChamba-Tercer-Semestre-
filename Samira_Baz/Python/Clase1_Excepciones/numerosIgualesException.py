#Clases excepciones personalizadas: podemos crear excepciones aparte de las que ya están definidas

class NumerosIgualesIguales (Exception): #Se extiende de la clase exception
    def __innit__(self, mensaje):
        self.message = mensaje


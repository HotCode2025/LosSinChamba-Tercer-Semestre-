class ManejoArchivos: # Creamos una clase para manejar el contexto de los archivos
    def __init__(self, nombre): # el constructor recibe el nombre del archivo
        self.nombre = nombre # guardamos el nombre del archivo en un atributo de la clase

    def __enter__(self): # este método se ejecuta al entrar al contexto del with
        print('Obtenemos el recurso'.center(50, '-')) # imprimimos un mensaje centrado con guiones
        self.nombre = open(self.nombre, 'r', encoding='utf8')  # Encapsulamos el código dentro del método
        return self.nombre # devolvemos el recurso para que pueda ser utilizado dentro del bloque del with

    def __exit__(self, tipo_excepcion, valor_excepcion, traza_error): # este método se ejecuta al salir del contexto del with, recibe información sobre la excepción si es que ocurrió
        print('cerramos el recurso'.center(50, '-')) # imprimimos un mensaje centrado con guiones
        if self.nombre: # si el recurso existe, lo cerramos
            self.nombre.close()  # cerramos el archivo
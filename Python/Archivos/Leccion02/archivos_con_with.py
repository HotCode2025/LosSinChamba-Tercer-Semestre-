# MANEJO DE CONTEXTO WITH: sintaxis simplificada, abre y cierra el archivo
import ManejoArchivos # importamos la clase que creamos para manejar el contexto de los archivos

with open('prueba.txt', 'r', encoding='utf8') as archivo: # con esta sintaxis, el archivo se abre y se cierra automaticamente al salir del bloque del with
    print(archivo.read()) # con esta sintaxis, el archivo se abre y se cierra automaticamente al salir del bloque del with, no hace falta ni el try, ni el finally

# No hace falta ni el try, ni el finally
# el contexto de with lo que hace es que se ejecuta de manera automatica
# Utiliza diferentes metodos: __enter__ este es el que abre
# Ahora el siguiente metodo es el que cierra: __exit__

with ManejoArchivos('prueba.txt') as archivo: # con esta sintaxis, el archivo se abre y se cierra automaticamente al salir del bloque del with, no hace falta ni el try, ni el finally
    print(archivo.read()) # con esta sintaxis, el archivo se abre y se cierra automaticamente al salir del bloque del with, no hace falta ni el try, ni el finally
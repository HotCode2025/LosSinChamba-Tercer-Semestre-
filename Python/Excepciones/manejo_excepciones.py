"""""
try:
    10/0
except Exception as e:
    print(f"Ocurrió un error: {e}")

/ / / / /
    
resultado = None
a = '10'
b = 0
try:
    resultado = a / b #modificamos
except ZeroDivisionError as e:
    print(f"Ocurrió un error: {e}")

print(f"El resultado es: {resultado}")
print('seguimos con el programa')

/ / / / /

try:
    a = int(input("Ingrese un número: ")) #solicitamos al usuario que ingrese un número y lo convertimos a entero
    b = int(input("Ingrese otro número: ")) #solicitamos al usuario que ingrese otro número y lo convertimos a entero
    resultado = a / b # modificamos
except TypeError as e: # capturamos el error de tipo
    print(f"Ocurrió un error de tipo: {e}") # imprimimos el mensaje de error
except ZeroDivisionError as e: # capturamos el error de división por cero
    print(f"Ocurrió un error de división por cero: {e}") # imprimimos el mensaje de error
except Exception as e: # capturamos cualquier otro error que pueda ocurrir
    print(f"Ocurrió un error: {e}") # imprimimos el mensaje de error

"""""

from NumerosIgualesException import NumerosIgualesException
try:
    a = int(input("Ingrese un número: ")) #solicitamos al usuario que ingrese un número y lo convertimos a entero
    b = int(input("Ingrese otro número: ")) #solicitamos al usuario que ingrese otro número y lo convertimos a entero
    if a == b: # verificamos si los números son iguales
        raise NumerosIgualesException("Los números son iguales.") # si son iguales, lanzamos la excepción personalizada
    resultado = a / b # modificamos
except TypeError as e: # capturamos el error de tipo
    print(f"Ocurrió un error de tipo: {e}") # imprimimos el mensaje de error
except ZeroDivisionError as e: # capturamos el error de división por cero
    print(f"Ocurrió un error de división por cero: {e}") # imprimimos el mensaje de error
except Exception as e: # capturamos cualquier otro error que pueda ocurrir
    print(f"Ocurrió un error: {e}") # imprimimos el mensaje de error
else:
    print(f"no se arrojó ninguna excepcion") # imprimimos un mensaje indicando que no se arrojó ninguna excepción
finally: # este bloque se ejecutará siempre, independientemente de si se arrojó una excepción o no
    print(f"Ejecucion de este bloque finally") # imprimimos un mensaje indicando que se ejecutó el bloque finally

print(f"El resultado es: {resultado}")
print('seguimos con el programa')





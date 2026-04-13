"""
Las excepciones sirven para prevenir el error antes de que suceda, haciendo que no se detenga
el programa en caso de errores y que el código siga corriendo 
"""
from numerosIgualesException import NumerosIgualesIguales #Importamos la clase

#Capturar la excepcion a través de un try 
resultado = None #Variable global

try:
    #Variable que fuera del bloque no tendran valor
    a = int(input("Digite el primer número: "))
    b = int(input("Digite el segundo número: "))

    if a == b:
        raise NumerosIgualesIguales("Son números iguales") #A través de raice se puede acceder a axcepciones
    resultado = a / b #Modificamos
#exceptions más específica (para ser precisos en el tipo de error): 
except TypeError as e:
    print(f"TypeError - Ocurrió un error: {type(e)}")
except ZeroDivisionError as e:
    print(f"ZeroDivisionError - Ocurrió un error: {type(e)}")

#exception más generica(para abarcar todo y prevenir errores):
except Exception as e: #Clase padre
    print(f"Exception - Ocurrió un error: {type(e)}")

else: #Se va a ejecutar solo en el caso de que no haya lanzado ninguna excepcion:
    print("No se arrojo ninguna excepción")

finally: #Siempre se va a ejecutar:
    print("Ejecución de este bloque finally")

print(f"El resultado es: {resultado}")#La variable no va sufrir ninguna modificación ya que es una excepcion lo que se le asigna en try
print("seguimos...")
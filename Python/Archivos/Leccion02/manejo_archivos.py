# declaramos una variable
try:
    archivo = open('prueba.txt', 'w')
    archivo.write('Programamos con diferentes tiposde archivos, ahora en txt. \n')
    archivo.write('Los acentos son importantes para las palabras\n')
    archivo.write('como por ejemplo: acción, ejecución y canción\n')
    archivo.write('\nt Esta es para texto o text, \nb archivos binarios, \nw+ lee y escribe, \n')
    archivo.write('Con esto terminamos.') #
except Exception as e: #si ocurre una excepcion, la guardamos en la variable e
    print(e) #imprimimos la excepcion
finally: #siempre se ejecuta
    archivo.close() #cerramos el archivo
# archivo.write('Todo quedo perfecto') este es un error



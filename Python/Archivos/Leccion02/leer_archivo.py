archivo = open('prueba.txt', 'r', encoding='utf8') #las letras son: 'r' read, 'w' write, 'a' append, 'x' exclusive creation y 'b' binary mode
# print(archivo.read())
# print(archivo.read(15)) #lee los primeros 15 caracteres
# print(archivo.read(5)) 
# print(archivo.read(8)) 
# print(archivo.readline()) #lee la primera linea
# print(archivo.readline()) #lee la segunda linea

# vamos a iterar el archivo, cada una de las lineas
# for linea in archivo:
#     print(linea): iteramos todos los elementos del archivo
# print(archivo.readlines()[11]) #lee todas las lineas y las devuelve como una lista

# anexamos informacion, copiamos a otro
archivo2 = open('copia_prueba.txt', 'w', encoding='utf8') #creamos un nuevo archivo para escribir, si no existe lo crea, si existe lo sobreescribe
archivo2.write(archivo.read()) #leemos el archivo y lo escribimos en el nuevo
archivo.close() # cerramos el archivo original, pero el nuevo sigue abierto
archivo2.close() # cerramos el nuevo archivo

print('se ha terminado el proceso de lectura y copiar archivos') # imprimimos un mensaje para indicar que el proceso ha terminado

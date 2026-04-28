import psycopg2  # Esto es para poder conectarnos a Postgre

conexion = psycopg2.connect(
    user='postgres',
    password='1212',
    host='127.0.0.1',
    port='5432',
    database='test_db'
)

cursor = conexion.cursor()
sentencia = 'SELECT * FROM persona'
cursor.execute(sentencia) # de esta manera se ejecuta la sentencia
registros = cursor.fetchall() # Recuperamos todos los registros
print(registros)

cursor.close()
conexion.close()

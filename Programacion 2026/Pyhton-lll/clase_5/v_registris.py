import psycopg2 # Esto es para poder conectarnos a PostgreSQL

# Configuración de la conexión (asegúrate de que los datos coincidan con tu DB local)
conexion = psycopg2.connect(user='postgres', password='admin', host='127.0.0.1', port='5432', database='tienda_db')

try:
    with conexion:
        with conexion.cursor() as cursor:
            # Cambié 'persona' por 'producto' y los IDs (1, 2) por (10, 20)
            sentencia = 'SELECT * FROM producto WHERE id_producto IN (10, 20)' # Placeholder
            
            # Ejecutamos la sentencia
            cursor.execute(sentencia)
            
            # Recuperamos todos los registros que serán una lista
            registros = cursor.fetchall()
            
            for registro in registros:
                print(registro)

except Exception as e:
    print(f'Ocurrió un error: {e}')

finally:
    # Cerramos la conexión al terminar
    conexion.close()
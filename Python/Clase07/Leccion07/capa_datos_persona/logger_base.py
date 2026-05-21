import logging as log

# docs.python.org/3/howto/logging.html
# Llamamos una configuración básica

log.basicConfig(level=log.DEBUG,
                format='%(asctime)s:%(levelname)s [%(filename)s:%(lineno)s] %(message)s', # formato del mensaje
                datefmt='%I:%M:%S %p', # formato de la fecha
                handlers=[ # manejadores de log, pueden ser varios
                    log.FileHandler('capa_datos.log'), # manejador de archivo, guarda los logs en un archivo
                    log.StreamHandler() # manejador de consola, muestra los logs en la consola
                ])

if __name__ == '__main__': # si se ejecuta este archivo directamente, se ejecuta el bloque de código
    log.debug('Mensaje a nivel debug') 
    log.info('Mensaje a nivel info') 
    log.warning('Mensaje a nivel warning')
    log.error('Mensaje a nivel error')
    log.critical('Mensaje a nivel critical')
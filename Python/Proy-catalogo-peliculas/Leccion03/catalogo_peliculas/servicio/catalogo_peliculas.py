import os
from catalogo_peliculas.dominio.pelicula import Pelicula


class CatalogoPeliculas:
    """Realiza las operaciones sobre el archivo de peliculas.txt."""

    ruta_archivo: str = "peliculas.txt"

    @staticmethod
    def agregar_pelicula(pelicula: Pelicula) -> None:
        with open(CatalogoPeliculas.ruta_archivo, "a", encoding="utf-8") as archivo:
            archivo.write(str(pelicula) + "\n")
        print(f'Película "{pelicula}" agregada correctamente.')

    @staticmethod
    def listar_peliculas() -> None:
        if not os.path.exists(CatalogoPeliculas.ruta_archivo):
            print("No hay películas registradas.")
            return
        with open(CatalogoPeliculas.ruta_archivo, "r", encoding="utf-8") as archivo:
            lineas = [l.strip() for l in archivo.readlines() if l.strip()]
        if not lineas:
            print("No hay películas registradas.")
        else:
            print("\n--- Catálogo de Películas ---")
            for i, nombre in enumerate(lineas, start=1):
                print(f"  {i}. {nombre}")
            print(f"Total: {len(lineas)} película(s)\n")

    @staticmethod
    def eliminar() -> None:
        if os.path.exists(CatalogoPeliculas.ruta_archivo):
            os.remove(CatalogoPeliculas.ruta_archivo)
            print("Archivo de películas eliminado correctamente.")
        else:
            print("No existe un archivo de películas para eliminar.")

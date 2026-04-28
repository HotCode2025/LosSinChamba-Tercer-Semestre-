from catalogo_peliculas.dominio.pelicula import Pelicula
from catalogo_peliculas.servicio.catalogo_peliculas import CatalogoPeliculas


def mostrar_menu() -> None:
    print("\n=============================")
    print("   Catálogo de Películas")
    print("=============================")
    print("1. Agregar película")
    print("2. Listar películas")
    print("3. Eliminar archivo de películas")
    print("4. Salir")
    print("=============================")


def main() -> None:
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Ingrese el nombre de la película: ").strip()
            if nombre:
                pelicula = Pelicula(nombre)
                CatalogoPeliculas.agregar_pelicula(pelicula)
            else:
                print("El nombre no puede estar vacío.")
        elif opcion == "2":
            CatalogoPeliculas.listar_peliculas()
        elif opcion == "3":
            confirmacion = input("¿Está seguro que desea eliminar el archivo? (s/n): ").strip().lower()
            if confirmacion == "s":
                CatalogoPeliculas.eliminar()
            else:
                print("Operación cancelada.")
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, seleccione entre 1 y 4.")


if __name__ == "__main__":
    main()

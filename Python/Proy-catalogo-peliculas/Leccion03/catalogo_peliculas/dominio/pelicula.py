class Pelicula:
    """Representa un objeto película."""

    def __init__(self, nombre: str):
        self.__nombre = nombre

    @property
    def nombre(self) -> str:
        return self.__nombre

    def __str__(self) -> str:
        return self.__nombre

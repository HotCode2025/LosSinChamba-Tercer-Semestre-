"""Cámara (viewport).

El mapa completo mide miles de píxeles y no entra en pantalla: todo se dibuja
desplazado por el offset de la cámara, que sigue al jugador y se frena en los
bordes del mundo para no mostrar "vacío".
"""


class Camara:
    def __init__(self, ancho_ventana, alto_ventana, ancho_mundo_px, alto_mundo_px):
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana
        self.ancho_mundo = ancho_mundo_px
        self.alto_mundo = alto_mundo_px
        self.x = 0.0
        self.y = 0.0

    def seguir(self, x_px, y_px):
        """Centra la cámara en (x, y) sin salirse de los límites del mundo."""
        self.x = min(max(x_px - self.ancho_ventana / 2, 0),
                     max(self.ancho_mundo - self.ancho_ventana, 0))
        self.y = min(max(y_px - self.alto_ventana / 2, 0),
                     max(self.alto_mundo - self.alto_ventana, 0))

    def a_pantalla(self, x_px, y_px):
        """Convierte coordenadas del mundo a coordenadas de pantalla."""
        return x_px - self.x, y_px - self.y

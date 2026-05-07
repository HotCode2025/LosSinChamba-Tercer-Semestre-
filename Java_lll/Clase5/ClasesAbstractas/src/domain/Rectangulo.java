package domain;

public class Rectangulo extends FiguraGeometrica {
//constructor
    public Rectangulo(String tipoFigura) {
        super(tipoFigura);
    }

    @Override
    public void dibujar() { //implementar el metodo
        System.out.println("Se imprime un: " + this.getClass().getSimpleName());
    }
}
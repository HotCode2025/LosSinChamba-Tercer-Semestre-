package ar.com.system2023.mundopc;

public class DispositivoEntrada {

    // Atributos privados
    private String tipoEntrada;
    private String marca;

    // Constructor
    public DispositivoEntrada(String tipoEntrada, String marca) {
        this.tipoEntrada = tipoEntrada;
        this.marca = marca;
    }

    // Getter y Setter de tipoEntrada
    public String getTipoEntrada() {
        return tipoEntrada;
    }

    public void setTipoEntrada(String tipoEntrada) {
        this.tipoEntrada = tipoEntrada;
    }

    // Getter y Setter de marca
    public String getMarca() {
        return this.marca;
    }

    public void setMarca(String marca) {
        this.marca = marca;
    }

}

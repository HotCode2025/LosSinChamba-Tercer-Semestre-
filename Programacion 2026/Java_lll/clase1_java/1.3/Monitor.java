package ar.com.system2023.mundopc;

public class Monitor {

    private final int idMonitor;
    private String marca;
    private double tamanio;
    private static int contadorMonitores;

    // Constructor privado vacío (incrementa el contador)
    private Monitor() {
        this.idMonitor = ++Monitor.contadorMonitores;
    }

    // Constructor público (llama al constructor vacío)
    public Monitor(String marca, double tamanio) {
        this(); // Llamado al constructor vacío
        this.marca = marca;
        this.tamanio = tamanio;
    }

    // Getter y Setter de marca
    public String getMarca() {
        return this.marca;
    }

    public void setMarca(String marca) {
        this.marca = marca;
    }

    // Getter y Setter de tamanio
    public double getTamanio() {
        return this.tamanio;
    }

    public void setTamanio(double tamanio) {
        this.tamanio = tamanio;
    }

    // Ingresamos manualmente el getIdMonitor
    public int getIdMonitor() {
        return this.idMonitor;
    }

}

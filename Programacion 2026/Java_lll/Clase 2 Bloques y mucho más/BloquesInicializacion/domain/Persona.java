package domain;

public class Persona {
    private final int idPersona;
    private static int contadorPersonas;

    static { //Bloque de inicialización estático
        System.out.println("Ejecución del bloque estático");
        ++Persona.contadorPersonas;
    }

    { //Bloque de inicialización NO estático (contexto dinámico)
        System.out.println("Ejecución del bloque NO estático");
        this.idPersona = Persona.contadorPersonas++;
    }

    public Persona() {
        System.out.println("Ejecución del constructor");
    }

    public int getIdPersona() {
        return this.idPersona;
    }

    @Override
    public String toString() {
        return "Persona{idPersona=" + idPersona + "}";
    }
}

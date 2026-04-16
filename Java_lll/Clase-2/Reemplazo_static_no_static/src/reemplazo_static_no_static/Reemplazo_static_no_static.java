package domain;

/**
 * TAREA: ¿Cómo reemplazarías un bloque static o no static de inicialización?
 *
 * CONCLUSIÓN:
 * - Bloque static {}     → se reemplaza con un método estático privado
 * - Bloque de instancia {} → se reemplaza con un método de instancia privado
 *                            o moviendo la lógica directo al constructor
 */

// ============================================================
// VERSIÓN ORIGINAL — con bloques de inicialización
// ============================================================
class Reemplazo_static_no_static.java {

    private final int idPersona;
    private static int contadorPersonas;

    // Bloque de inicialización ESTÁTICO
    static {
        System.out.println("Ejecución del bloque estático");
        ++PersonaConBloques.contadorPersonas;
    }

    // Bloque de inicialización NO estático (de instancia)
    {
        System.out.println("Ejecución del bloque NO estático");
        this.idPersona = PersonaConBloques.contadorPersonas++;
    }

    public PersonaConBloques() {
        System.out.println("Ejecución del constructor");
    }

    public int getIdPersona() { return idPersona; }

    @Override
    public String toString() {
        return "PersonaConBloques{idPersona=" + idPersona + "}";
    }
}


// ============================================================
// VERSIÓN REEMPLAZADA — sin bloques de inicialización
// ============================================================
public class Reemplazo_static_no_static.java {

    private final int idPersona;

    // El método estático privado REEMPLAZA al bloque static {}
    private static int contadorPersonas = inicializarContador();

    private static int inicializarContador() {
        System.out.println("Ejecución del bloque estático (reemplazado por método estático)");
        return 1;
    }

    // El método de instancia privado REEMPLAZA al bloque de instancia {}
    private int inicializarInstancia() {
        System.out.println("Ejecución del bloque NO estático (reemplazado por método de instancia)");
        return contadorPersonas++;
    }

    public PersonaSinBloques() {
        // Llamamos al método de instancia ANTES de la lógica del constructor
        this.idPersona = inicializarInstancia();
        System.out.println("Ejecución del constructor");
    }

    public int getIdPersona() { return idPersona; }

    @Override
    public String toString() {
        return "PersonaSinBloques{idPersona=" + idPersona + "}";
    }
}

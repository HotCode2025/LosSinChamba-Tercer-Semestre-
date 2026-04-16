package clase2_reemplazo_no_static;

public class Persona_factory {
    
    private final int idPersona;
    // El estado global (contador) se mantiene privado y estático
    private static int contadorPersonas = 0;

    // Constructor privado para forzar el uso del método factory
    private Persona_factory(int id) {
        this.idPersona = id;
    }

    public static Persona_factory crearPersona() {
        // Lógica que antes estaba repartida en bloques static y dinámicos
        int nuevoId = ++Persona_factory.contadorPersonas;
        
        System.out.println("Factory: Creando instancia con ID " + nuevoId);
        return new Persona_factory(nuevoId);
    }

    public int getIdPersona() {
        return this.idPersona;
    }

    @Override
    public String toString() {
        return "Persona_factory{idPersona=" + idPersona + "}";
    }
}
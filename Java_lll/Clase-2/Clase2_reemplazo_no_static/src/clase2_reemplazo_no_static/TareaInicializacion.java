package clase2_reemplazo_no_static;

public class TareaInicializacion {
// ==========================================================
// 1. EL BLOQUE ESTÁTICO (LO QUE QUEREMOS REEMPLAZAR)
// ==========================================================

    public static String configuracionSistema;

/* POR QUÉ LO REEMPLAZAMOS:
Los bloques estáticos son como "cajas negras". Si algo falla acá adentro,
es difícil de capturar. Además, no se ve claramente en la declaración
de la variable de dónde sale su valor inicial.
*/
    static {
        configuracionSistema = "Modo Producción - Activo";
        System.out.println("[BLOQUE STATIC] Se ejecutó automáticamente al cargar la clase.");
    }
// ==========================================================
// 2. EL REEMPLAZO DEL BLOQUE ESTÁTICO (FORMA PROFESIONAL)
// ==========================================================
// CUÁNDO LO REEMPLAZAMOS: Siempre que la inicialización requiera lógica.
// Usamos un método estático privado. Es mucho más legible.
    public static String versionApp = obtenerVersion();

    private static String obtenerVersion() {
// Acá podemos poner lógica compleja, try-catch, etc.
        System.out.println("[REEMPLAZO STATIC] Se inicializó 'versionApp' mediante un método explícito.");
        return "v2.4.1";
    }
// ==========================================================
// 3. EL BLOQUE DE INSTANCIA (LO QUE QUEREMOS REEMPLAZAR)
// ==========================================================
    public String estadoUsuario;

    /* POR QUÉ LO REEMPLAZAMOS:
Este bloque se ejecuta antes del constructor cada vez que hacés un 'new'.
Es muy fácil olvidarse de que existe porque suele estar "tirado" en
cualquier parte de la clase. Causa confusión en el flujo de lectura.
     */
    {
        this.estadoUsuario = "Pendiente";
        System.out.println("[BLOQUE INSTANCIA] Se ejecutó antes que el constructor.");
    }
// ==========================================================
// 4. EL REEMPLAZO DEL BLOQUE DE INSTANCIA (CONSTRUCTOR)
// ==========================================================

    public String rolUsuario;
// CUÁNDO LO REEMPLAZAMOS: Siempre. El lugar natural para inicializar objetos es el constructor.

    public TareaInicializacion() {
// Todo programador de Java sabe que esto se ejecuta al crear el objeto.
        this.rolUsuario = "Invitado";
        System.out.println("[REEMPLAZO INSTANCIA] Se inicializó 'rolUsuario' dentro del CONSTRUCTOR.");
    }

    public static void main(String[] args) {
        System.out.println("--- INICIO DE LA EJECUCIÓN ---");
// Al crear el objeto, veremos el orden en la consola
        TareaInicializacion app = new TareaInicializacion();
        System.out.println("\n--- RESULTADOS FINALES ---");
        System.out.println("Configuración (Bloque): " + configuracionSistema);
        System.out.println("Versión (Método): " + versionApp);
        System.out.println("Estado (Bloque): " + app.estadoUsuario);
        System.out.println("Rol (Constructor): " + app.rolUsuario);
    }
}

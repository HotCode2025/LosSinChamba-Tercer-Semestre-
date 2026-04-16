package clase2_reemplazo_no_static;

public class Clase2_reemplazo_no_static {

    public static void main(String[] args) {
        
        /*
            RESPUESTA A LA TAREA: ¿Cómo reemplazarías un bloque static o no static de inicialización?*
            Bloque Static: Lo reemplazamos moviendo su lógica a un método estático privado,
            el cual se llama directamente al declarar la variable estática. Esto mejora
            mucho la legibilidad y el control de errores al cargar la clase.*
            Bloque No Static (de instancia): Lo reemplazamos trasladando su código directamente
            al Constructor de la clase. Es la forma estándar, predecible y más clara de
            inicializar atributos cada vez que se crea un nuevo objeto.

        */
        System.out.println("");
        
        TareaInicializacion t = new TareaInicializacion();
        System.out.println(t.toString());
        
                
    }
    
}

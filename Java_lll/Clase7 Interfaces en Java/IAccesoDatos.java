package accesodatos;

public interface IAccessoDatos {
    int MAX_REGISTRO = 10;
    
    // Método insertar es abstracto y sin cuerpo
    void insertar();
    
    void listar();
    
    void actualizar();
    
    void eliminar();
}
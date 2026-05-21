package test;

import accesodatos.*;

public class TestInterfaces {
    public static void main(String[] args) {
        // Una interfaz no se puede instanciar directamente: 
        // IAccessoDatos datos = new IAccessoDatos(); -> Esto da error.
        
        // Aplicando Polimorfismo: la variable de tipo interfaz apunta a una implementación de MySQL
        IAccessoDatos datos = new ImplementacionMySql();
        // datos.listar(); // Imprime: Listar desde MySQL
        imprimir(datos);
        
        // Reutilizamos la misma variable para que ahora apunte a la implementación de Oracle
        datos = new ImplementacionOracle();
        // datos.listar(); // Imprime: Listar desde Oracle
        imprimir(datos);
    }
    
    // Método totalmente genérico que recibe un tipo Interfaz
    public static void imprimir(IAccessoDatos datos) {
        datos.listar();
    }
}
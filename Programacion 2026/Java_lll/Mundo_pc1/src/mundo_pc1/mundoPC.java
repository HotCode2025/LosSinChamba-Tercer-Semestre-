package ar.com.system2023.mundopc;

import ar.com.system2023.mundopc.*;

public class mundoPC {

    public static void main(String[] args) {

        // Objetos HP
        Monitor monitorHP = new Monitor("HP", 13);
        Teclado tecladoHP = new Teclado("Bluetooth", "HP");
        Raton ratonHP = new Raton("Bluetooth", "HP");
        Computadora computadoraHP = new Computadora("Computadora HP", monitorHP, tecladoHP, ratonHP);

        // Objetos Gamer
        Monitor monitorGamer = new Monitor("Gamer", 32);
        Teclado tecladoGamer = new Teclado("Bluetooth", "Gamer");
        Raton ratonGamer = new Raton("Bluetooth", "Gamer");
        Computadora computadoraGamer = new Computadora("Computadora Gamer", monitorGamer, tecladoGamer, ratonGamer);

        // Computadoras para completar orden1 hasta 10
        Computadora computadora3 = new Computadora("Computadora Dell",
                new Monitor("Dell", 24), new Teclado("USB", "Dell"), new Raton("USB", "Dell"));

        Computadora computadora4 = new Computadora("Computadora Lenovo",
                new Monitor("Lenovo", 27), new Teclado("Bluetooth", "Lenovo"), new Raton("Bluetooth", "Lenovo"));

        Computadora computadora5 = new Computadora("Computadora Asus",
                new Monitor("Asus", 29), new Teclado("USB", "Asus"), new Raton("USB", "Asus"));

        Computadora computadora6 = new Computadora("Computadora Acer",
                new Monitor("Acer", 21), new Teclado("Bluetooth", "Acer"), new Raton("Bluetooth", "Acer"));

        Computadora computadora7 = new Computadora("Computadora Samsung",
                new Monitor("Samsung", 32), new Teclado("USB", "Samsung"), new Raton("USB", "Samsung"));

        Computadora computadora8 = new Computadora("Computadora MSI",
                new Monitor("MSI", 27), new Teclado("Bluetooth", "MSI"), new Raton("Bluetooth", "MSI"));

        Computadora computadora9 = new Computadora("Computadora Apple",
                new Monitor("Apple", 24), new Teclado("Bluetooth", "Apple"), new Raton("Bluetooth", "Apple"));

        Computadora computadora10 = new Computadora("Computadora Logitech",
                new Monitor("Logitech", 19), new Teclado("USB", "Logitech"), new Raton("USB", "Logitech"));

        // Inicializamos ordenes
        Orden orden1 = new Orden();
        Orden orden2 = new Orden();

        // Agregamos 10 computadoras a orden1
        orden1.agregarComputadora(computadoraHP);
        orden1.agregarComputadora(computadoraGamer);
        orden1.agregarComputadora(computadora3);
        orden1.agregarComputadora(computadora4);
        orden1.agregarComputadora(computadora5);
        orden1.agregarComputadora(computadora6);
        orden1.agregarComputadora(computadora7);
        orden1.agregarComputadora(computadora8);
        orden1.agregarComputadora(computadora9);
        orden1.agregarComputadora(computadora10);

        // Computadora para orden2
        Computadora computadorasVarias = new Computadora("Computadora de diferentes marcas",
                new Monitor("Dell", 27), new Teclado("USB", "Logitech"), new Raton("USB", "Logitech"));
        orden2.agregarComputadora(computadorasVarias);

        orden1.mostrarOrden();
        orden2.mostrarOrden();

    }

}

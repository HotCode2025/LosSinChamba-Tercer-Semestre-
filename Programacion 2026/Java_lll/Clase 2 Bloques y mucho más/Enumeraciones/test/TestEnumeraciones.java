package test;

import enumeraciones.Continentes;
import enumeraciones.Dias;

public class TestEnumeraciones {
    public static void main(String[] args) {
        //System.out.println("Dia 1: " + Dias.LUNES);
        //indicarDiaSemana(Dias.LUNES);
        System.out.println("Continente No. 4: " + Continentes.AMERICA);
        System.out.println("No. de paises en el 4to. continente: "
                + Continentes.AMERICA.getPaises());
        System.out.println("No. de habitantes en el 4to. continente: "
                + Continentes.AMERICA.getHabitantes());
    }

    private static void indicarDiaSemana(Dias dias) {
        switch (dias) {
            case LUNES:
                System.out.println("Primer dia de la semana");
                break;
            case MARTES:
                System.out.println("Segundo dia de la semana");
                break;
            //Agregar todos los días de la semana
            //Agregar default
        }
    }
}

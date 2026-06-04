import java.util.InputMismatchException;
import java.util.Scanner;

public class Calculadora {

    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {

        // Ciclo principal: se repite hasta que el usuario elija Salir
        while (true) {
            try {
                mostrarMenu();
                System.out.print("Elegí una opción: ");
                int opcion = scanner.nextInt();

                // Salida del ciclo con break
                if (opcion == 5) {
                    System.out.println("¡Hasta luego!");
                    break;
                }

                // Validamos que la opción sea de operación (1 a 4)
                if (opcion < 1 || opcion > 4) {
                    System.out.println("Opción inválida. Elegí un número del 1 al 5.\n");
                    continue;
                }

                // Entrada de los dos operandos
                System.out.print("Ingresá el primer número: ");
                double num1 = scanner.nextDouble();
                System.out.print("Ingresá el segundo número: ");
                double num2 = scanner.nextDouble();

                ejecutarOperacion(opcion, num1, num2);

            } catch (InputMismatchException e) {
                // Captura cuando se ingresa algo que no es un número
                System.out.println("Error: ingresaste un valor que no es un número.\n");
                scanner.nextLine(); // limpiamos el buffer
            }
        }

        scanner.close();
    }

    // Menú factorizado en su propio método
    public static void mostrarMenu() {
        System.out.println("===== CALCULADORA =====");
        System.out.println("1. Sumar");
        System.out.println("2. Restar");
        System.out.println("3. Multiplicar");
        System.out.println("4. Dividir");
        System.out.println("5. Salir");
        System.out.println("=======================");
    }

    // Ejecuta la operación según la opción elegida
    public static void ejecutarOperacion(int opcion, double num1, double num2) {
        double resultado = 0;

        switch (opcion) {
            case 1: resultado = num1 + num2; break;
            case 2: resultado = num1 - num2; break;
            case 3: resultado = num1 * num2; break;
            case 4:
                // Control de división por cero
                if (num2 == 0) {
                    System.out.println("Error: no se puede dividir por cero.\n");
                    return;
                }
                resultado = num1 / num2;
                break;
        }

        System.out.println("Resultado: " + resultado + "\n");
    }
}

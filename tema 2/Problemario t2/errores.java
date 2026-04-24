public class errores {
    public static void main(String[] args) {
        errores demo = new errores();

        System.out.println("1. Error de Redondeo Binario:");
        demo.errorRedondeoBinario();
        System.out.println("\n2. Pérdida de Precisión por Magnitud:");
        demo.perdidaPrecisionMagnitud();
        System.out.println("\n3. Comparación Directa con '==':");
        demo.comparacionDirectaConIgual();
        System.out.println("\n4. Acumulación de Errores en Bucles:");
        demo.acumulacionErroresBucles();
        System.out.println("\n5. Cancelación por Resta:");
        demo.cancelacionResta();
        System.out.println("\n6. Desbordamiento Silencioso:");
        demo.desbordamientoSilencioso();
        System.out.println("\n7. Conversión Estrecha:");
        demo.conversionEstrecha();
        
    }

    //1.- Error de Redondeo Binario
    public void errorRedondeoBinario() {
        System.out.println(0.1 + 0.2); // Imprime 0.30000000000000004 en lugar de 0.3
    }

    //2. Pérdida de Precisión por Magnitud(IEEE 754 )
    public void perdidaPrecisionMagnitud() {
        // Un double tiene aproximadamente 15-17 dígitos significativos de precisión
        double numeroGrande = 1.0e16; // 1 seguido de 16 ceros
        double numeroPequeno = 1.0;

        double resultado = numeroGrande + numeroPequeno;

        System.out.println("--- Demostración de Pérdida de Precisión ---");
        System.out.println("Número Grande:   " + numeroGrande);
        System.out.println("Número Pequeño:  " + numeroPequeno);
        System.out.println("Suma Resultante: " + resultado);

        // Verificación lógica
        if (resultado == numeroGrande) {
            System.out.println("\nRESULTADO: El número pequeño 'desapareció'.");
            System.out.println("La suma es igual al número original debido a la falta de bits en la mantisa.");
        }


    }

    //Comparación Directa con ==
    public void comparacionDirectaConIgual() {
        double a = 0.1 + 0.1 + 0.1;
        double b = 0.3;

        System.out.println("Valor de a (0.1 * 3): " + a);
        System.out.println("Valor de b:           " + b);

        // 2. Intento de comparación directa (FALLARÁ)
        System.out.println("\n--- Comparación con '==' ---");
        if (a == b) {
            System.out.println("Resultado: Son iguales");
        } else {
            System.out.println("Resultado: SON DIFERENTES (Error esperado)");
        }

    }

    //4. Acumulación de Errores en Bucles
    public void acumulacionErroresBucles() {
        int iteraciones = 1000000; // Un millón de sumas
        double incremento = 0.1;
        
        // 1. Acumulación usando 'double'
        double sumaDouble = 0.0;
        for (int i = 0; i < iteraciones; i++) {
            sumaDouble += incremento;
        }

        // El resultado esperado debería ser exactamente 100,000.0
        double esperado = iteraciones * incremento;

        System.out.println("--- Acumulación en Bucle (1,000,000 de iteraciones) ---");
        System.out.println("Resultado esperado: " + esperado);
        System.out.println("Resultado double:   " + sumaDouble);
        System.out.println("Diferencia (Error): " + (sumaDouble - esperado));

    }

    //Cancelación por Resta (Loss of Significance)
    public void cancelacionResta() {
        // Dos números muy grandes y muy cercanos
        double x = 1234567890.1234567;
        double y = 1234567890.1234560;

        // El resultado esperado es 0.0000007
        double resultado = x - y;

        System.out.println("Resultado real: " + resultado); 
        // En 2026 notarás que el resultado es 0.0 o un valor basura
        // debido a que los últimos dígitos se perdieron al almacenar x e y.

    }

    //Desbordamiento Silencioso (Overflow)
    public void desbordamientoSilencioso() {
        int max = Integer.MAX_VALUE; // 2,147,483,647
        int resultado = max + 1;

        System.out.println("Máximo int: " + max);
        System.out.println("Máximo + 1: " + resultado); // Imprime -2147483648

        // Solución: Usar Math.addExact para lanzar una excepción si ocurre
        try {
            Math.addExact(max, 1);
        } catch (ArithmeticException e) {
            System.out.println("Error detectado: ¡Desbordamiento!");
        }

    }


    //Conversión Estrecha (Narrowing Primitive Conversion)
    public void conversionEstrecha() {
        double valorDouble = 3.14159e10; // Un número muy grande
        int valorInt = (int) valorDouble; // Casting explícito

        System.out.println("Valor Original: " + valorDouble);
        System.out.println("Valor Truncado: " + valorInt); 
        // Imprime 2147483647 (el máximo int) porque el double no cabe.

    }


}
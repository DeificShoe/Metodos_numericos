# ==============================================================================
# MÉTODOS NUMÉRICOS: DERIVACIÓN E INTEGRACIÓN
# Autor: [Tu nombre]
# Materia: [Nombre de la materia]
# Fecha: [Fecha de entrega]
#
# Descripción:
#   Implementación de 5 métodos numéricos organizados en clases:
#     1. Método de Tres Puntos (derivación)
#     2. Método de Cinco Puntos (derivación)
#     3. Método del Trapecio (integración)
#     4. Regla de Simpson 1/3 (integración)
#     5. Cuadratura Gaussiana (integración)
#
#   Cada clase contiene 3 casos:
#     - caso_ideal():  Donde el método funciona correctamente
#     - caso_error():  Donde el método falla o no es adecuado
#     - caso_extra():  Caso más complejo o aplicado a otro contexto
#
#   Al ejecutar el archivo, se corren TODOS los casos automáticamente.
#
# Dependencias: math, numpy, scipy
#   Instalar con: pip install numpy scipy
# ==============================================================================

import math
import numpy as np
from scipy import integrate, stats


# ==============================================================================
# CLASE 1: MÉTODO DE TRES PUNTOS
# ==============================================================================

class MetodoTresPuntos:
    """
    Derivación numérica de tres puntos.

    Fórmula del punto medio (la más precisa):
        f'(x0) ≈ [f(x0+h) - f(x0-h)] / (2h)   Error: O(h^2)

    Fórmula del extremo izquierdo (cuando no hay punto a la izquierda):
        f'(x0) ≈ [-3f(x0) + 4f(x0+h) - f(x0+2h)] / (2h)

    Fórmula del extremo derecho (cuando no hay punto a la derecha):
        f'(x0) ≈ [f(x0-2h) - 4f(x0-h) + 3f(x0)] / (2h)
    """

    def derivada_punto_medio(self, f, x0, h):
        """
        Fórmula del punto medio de 3 puntos.
        Requiere: f(x0-h) y f(x0+h).
        Error: O(h^2)
        """
        return (f(x0 + h) - f(x0 - h)) / (2 * h)

    def derivada_extremo_izquierdo(self, f, x0, h):
        """
        Fórmula del extremo izquierdo de 3 puntos.
        Útil cuando no existen datos a la izquierda de x0.
        Error: O(h^2)
        """
        return (-3 * f(x0) + 4 * f(x0 + h) - f(x0 + 2 * h)) / (2 * h)

    def derivada_extremo_derecho(self, f, x0, h):
        """
        Fórmula del extremo derecho de 3 puntos.
        Útil cuando no existen datos a la derecha de x0.
        Error: O(h^2)
        """
        return (f(x0 - 2 * h) - 4 * f(x0 - h) + 3 * f(x0)) / (2 * h)

    def caso_ideal(self):
        """
        CASO IDEAL: Derivada de T(x) = e^(-x^2) * cos(x) en x = 1.0
        ---------------------------------------------------------------
        Contexto: Distribución de temperatura en varilla de acero.
        Se necesita la tasa de cambio de temperatura en x=1.0 m para
        ajustar el sistema de enfriamiento.

        Datos:
            T(x) = e^(-x²) · cos(x)
            x₀ = 1.0 m
            h = 0.01

        Se pide: T'(1.0) con el método de 3 puntos (punto medio).
        Comparar con el valor exacto y calcular el error relativo.
        """
        print("\n" + "="*60)
        print("MÉTODO DE TRES PUNTOS - CASO IDEAL")
        print("Función: T(x) = e^(-x²) · cos(x)")
        print("Punto: x₀ = 1.0 | Paso: h = 0.01")
        print("Contexto: Distribución de temperatura en varilla de acero")
        print("="*60)

        def T(x):
            return math.exp(-x**2) * math.cos(x)

        def T_prima_exacta(x):
            # Regla del producto + cadena:
            # d/dx[e^(-x²)·cos(x)] = -2x·e^(-x²)·cos(x) - e^(-x²)·sin(x)
            return -2 * x * math.exp(-x**2) * math.cos(x) - math.exp(-x**2) * math.sin(x)

        x0 = 1.0
        h = 0.01

        aprox = self.derivada_punto_medio(T, x0, h)
        exacta = T_prima_exacta(x0)
        error = abs((aprox - exacta) / exacta) * 100

        print(f"\n  Valor aproximado (3 puntos) : {aprox:.10f}")
        print(f"  Valor exacto (analítico)    : {exacta:.10f}")
        print(f"  Error relativo              : {error:.8f}%")
        print("\n  CONCLUSIÓN: Con función suave y h pequeño, el método de")
        print("  3 puntos converge con error de orden O(h²). Funciona correctamente.")

    def caso_error(self):
        """
        CASO CON ERROR: f(x) = tan(x) cerca de la discontinuidad en π/2
        ---------------------------------------------------------------
        Problema: El paso h = 0.5 hace que f(x0+h) cruce la discontinuidad
        de tan(x) en π/2, produciendo un resultado completamente erróneo.

        Datos:
            f(x) = tan(x)
            x₀ = π/2 - 0.01 (muy cerca de la discontinuidad)
            h = 0.5 (demasiado grande, cruza π/2)

        Se pide: Observar el resultado incorrecto y entender la causa.
        """
        print("\n" + "="*60)
        print("MÉTODO DE TRES PUNTOS - CASO CON ERROR")
        print("Función: f(x) = tan(x) cerca de x = π/2")
        print("Problema: h = 0.5 cruza la discontinuidad en π/2")
        print("="*60)

        def f(x):
            return math.tan(x)

        x0 = math.pi / 2 - 0.01  # Muy cercano a la discontinuidad
        h = 0.5

        punto_derecho = x0 + h
        punto_izquierdo = x0 - h

        print(f"\n  x₀              = {x0:.6f} rad")
        print(f"  x₀ + h          = {punto_derecho:.6f} rad")
        print(f"  π/2             = {math.pi/2:.6f} rad")
        print(f"  Distancia a π/2 = {abs(punto_derecho - math.pi/2):.6f} rad")
        print("\n  ADVERTENCIA: x₀+h cruza la discontinuidad de tan(x) en π/2.")

        try:
            aprox = self.derivada_punto_medio(f, x0, h)
            exacta = 1 / math.cos(x0)**2  # Derivada de tan(x) = sec²(x)
            error_abs = abs(aprox - exacta)
            print(f"\n  Resultado incorrecto   : {aprox:.4f}")
            print(f"  Valor exacto en x₀     : {exacta:.4f}")
            print(f"  Error absoluto         : {error_abs:.2f}  ← INACEPTABLE")
            print("\n  CAUSA: f(x₀+h) evalúa tan(x) más allá de π/2, donde la función")
            print("  cambia de signo abruptamente (de +∞ a -∞).")
            print("  SOLUCIÓN: Usar h << distancia_a_discontinuidad")
            print(f"  En este caso: h debe ser mucho menor que {abs(x0 - math.pi/2):.4f}")

            # Mostrar corrección con h pequeño
            h_correcto = 0.0001
            aprox_correcto = self.derivada_punto_medio(f, x0, h_correcto)
            error_correcto = abs((aprox_correcto - exacta) / exacta) * 100
            print(f"\n  Con h = {h_correcto}: resultado = {aprox_correcto:.6f} | error = {error_correcto:.6f}%  ← CORRECTO")

        except (ValueError, ZeroDivisionError, OverflowError) as e:
            print(f"\n  ERROR NUMÉRICO: {e}")
            print("  El método falla porque la función no es continua en el intervalo evaluado.")

    def caso_extra(self):
        """
        CASO EXTRA: Velocidad y aceleración de vehículo
        ---------------------------------------------------------------
        s(t) = 3t³ - 2t² + t + 5 (posición en metros)
        Se calcula la primera derivada (velocidad) y la segunda (aceleración)
        usando diferencias finitas centradas de 3 puntos.

        Datos:
            s(t) = 3t³ - 2t² + t + 5
            t₀ = 2.0 s
            h = 0.01 s

        Se pide: s'(2.0) [velocidad] y s''(2.0) [aceleración], comparar con exactas.
        """
        print("\n" + "="*60)
        print("MÉTODO DE TRES PUNTOS - CASO EXTRA")
        print("Función: s(t) = 3t³ - 2t² + t + 5 (posición en metros)")
        print("Punto: t₀ = 2.0 s | Paso: h = 0.01 s")
        print("Se calculan: velocidad s'(t₀) y aceleración s''(t₀)")
        print("="*60)

        def s(t):
            return 3*t**3 - 2*t**2 + t + 5

        def s_prima_exacta(t):
            # ds/dt = 9t² - 4t + 1
            return 9*t**2 - 4*t + 1

        def s_doble_prima_exacta(t):
            # d²s/dt² = 18t - 4
            return 18*t - 4

        t0 = 2.0
        h = 0.01

        # Primera derivada (velocidad) con fórmula de punto medio
        vel_aprox = self.derivada_punto_medio(s, t0, h)
        vel_exacta = s_prima_exacta(t0)
        error_vel = abs((vel_aprox - vel_exacta) / vel_exacta) * 100

        # Segunda derivada (aceleración) con diferencia centrada de 3 puntos:
        # s''(t0) ≈ [s(t0-h) - 2·s(t0) + s(t0+h)] / h²
        acel_aprox = (s(t0 - h) - 2*s(t0) + s(t0 + h)) / h**2
        acel_exacta = s_doble_prima_exacta(t0)
        error_acel = abs((acel_aprox - acel_exacta) / acel_exacta) * 100

        print(f"\n  VELOCIDAD en t = {t0} s:")
        print(f"    Aproximada (3 puntos) : {vel_aprox:.8f} m/s")
        print(f"    Exacta (analítica)    : {vel_exacta:.8f} m/s")
        print(f"    Error relativo        : {error_vel:.8f}%")

        print(f"\n  ACELERACIÓN en t = {t0} s:")
        print(f"    Aproximada (3 puntos) : {acel_aprox:.8f} m/s²")
        print(f"    Exacta (analítica)    : {acel_exacta:.8f} m/s²")
        print(f"    Error relativo        : {error_acel:.8f}%")

        print("\n  CONCLUSIÓN: Las diferencias finitas centradas permiten obtener tanto")
        print("  la 1ra como la 2da derivada con alta precisión usando 3 puntos.")


# ==============================================================================
# CLASE 2: MÉTODO DE CINCO PUNTOS
# ==============================================================================

class MetodoCincoPuntos:
    """
    Derivación numérica de cinco puntos.

    Fórmula del punto medio (la más precisa):
        f'(x0) ≈ [f(x0-2h) - 8f(x0-h) + 8f(x0+h) - f(x0+2h)] / (12h)
        Error: O(h^4)

    Segunda derivada con 5 puntos:
        f''(x0) ≈ [-f(x0-2h) + 16f(x0-h) - 30f(x0) + 16f(x0+h) - f(x0+2h)] / (12h²)

    Tercera derivada con 5 puntos:
        f'''(x0) ≈ [-f(x0-2h) + 2f(x0-h) - 2f(x0+h) + f(x0+2h)] / (2h³)
    """

    def derivada_primera(self, f, x0, h):
        """
        Primera derivada con fórmula del punto medio de 5 puntos.
        Error: O(h^4)
        """
        return (f(x0 - 2*h) - 8*f(x0 - h) + 8*f(x0 + h) - f(x0 + 2*h)) / (12 * h)

    def derivada_segunda(self, f, x0, h):
        """
        Segunda derivada con fórmula de 5 puntos.
        Error: O(h^4)
        """
        return (-f(x0 - 2*h) + 16*f(x0 - h) - 30*f(x0) + 16*f(x0 + h) - f(x0 + 2*h)) / (12 * h**2)

    def derivada_tercera(self, f, x0, h):
        """
        Tercera derivada (jerk) con fórmula de 5 puntos.
        Error: O(h^2)
        """
        return (-f(x0 - 2*h) + 2*f(x0 - h) - 2*f(x0 + h) + f(x0 + 2*h)) / (2 * h**3)

    def caso_ideal(self):
        """
        CASO IDEAL: L(θ) = sin(θ)·cos²(θ) en θ = 0.5 rad
        ---------------------------------------------------------------
        Contexto: Coeficiente de sustentación de perfil alar en función
        del ángulo de ataque θ. Se compara la precisión de 3 puntos vs 5 puntos.

        Datos:
            L(θ) = sin(θ) · cos²(θ)
            θ₀ = 0.5 rad
            h = 0.1

        Se pide: L'(0.5) con 3 y 5 puntos. Comparar errores.
        """
        print("\n" + "="*60)
        print("MÉTODO DE CINCO PUNTOS - CASO IDEAL")
        print("Función: L(θ) = sin(θ)·cos²(θ) (sustentación aerodinámica)")
        print("Punto: θ₀ = 0.5 rad | Paso: h = 0.1")
        print("="*60)

        def L(theta):
            return math.sin(theta) * math.cos(theta)**2

        def L_prima_exacta(theta):
            # d/dθ [sin·cos²] = cos³ - 2·sin²·cos
            return math.cos(theta)**3 - 2 * math.sin(theta)**2 * math.cos(theta)

        theta0 = 0.5
        h = 0.1

        # Tres puntos (diferencia centrada simple)
        aprox_3p = (L(theta0 + h) - L(theta0 - h)) / (2 * h)

        # Cinco puntos
        aprox_5p = self.derivada_primera(L, theta0, h)

        exacta = L_prima_exacta(theta0)
        error_3p = abs((aprox_3p - exacta) / exacta) * 100
        error_5p = abs((aprox_5p - exacta) / exacta) * 100

        print(f"\n  Valor exacto (analítico)   : {exacta:.12f}")
        print(f"  Aprox. 3 puntos            : {aprox_3p:.12f}")
        print(f"  Error 3 puntos             : {error_3p:.8f}%")
        print(f"  Aprox. 5 puntos            : {aprox_5p:.12f}")
        print(f"  Error 5 puntos             : {error_5p:.8f}%")

        if error_5p > 0:
            mejora = error_3p / error_5p
            print(f"\n  El método de 5 puntos es {mejora:.0f}x más preciso que el de 3 puntos.")
        print("  Esto se debe a que el error pasa de O(h²) a O(h⁴).")

    def caso_error(self):
        """
        CASO CON ERROR: f(x) = |x| en x = 0 (esquina, no diferenciable)
        ---------------------------------------------------------------
        El método de 5 puntos devuelve un resultado numérico (≈ 0), pero
        este valor es matemáticamente inválido porque la derivada de |x|
        no existe en x = 0 (límites laterales son +1 y -1, distintos).

        Datos:
            f(x) = |x|
            x₀ = 0
            h = 0.1

        Se pide: Aplicar el método y analizar el resultado incorrecto.
        """
        print("\n" + "="*60)
        print("MÉTODO DE CINCO PUNTOS - CASO CON ERROR")
        print("Función: f(x) = |x| en x = 0 (función con esquina)")
        print("La derivada clásica NO existe en x = 0")
        print("="*60)

        def f(x):
            return abs(x)

        x0 = 0.0
        h = 0.1

        aprox = self.derivada_primera(f, x0, h)

        print(f"\n  Resultado numérico en x = 0 : {aprox:.10f}")
        print(f"  Derivada lateral izquierda  : -1.0")
        print(f"  Derivada lateral derecha    :  1.0")
        print(f"\n  ANÁLISIS:")
        print("  La fórmula de 5 puntos usa simetría: los términos negativos y positivos")
        print("  se cancelan y da exactamente 0.0. Esto parece 'limpio', pero es incorrecto.")
        print("  La derivada de |x| no existe en x=0 porque los límites laterales son distintos.")
        print("\n  CAUSA: La fórmula asume que la función es diferenciable en el punto.")
        print("  En una esquina (cambio de pendiente abrupto), el supuesto falla.")
        print("  SOLUCIÓN: Verificar diferenciabilidad antes de aplicar cualquier fórmula.")
        print("            Usar derivadas laterales si la función tiene esquinas.")

    def caso_extra(self):
        """
        CASO EXTRA: Sistema masa-resorte x(t) = A·cos(ω·t + φ)
        ---------------------------------------------------------------
        Calcular velocidad (x'), aceleración (x'') y jerk (x''') usando
        las fórmulas de 5 puntos para la 1ra, 2da y 3ra derivada.

        Datos:
            x(t) = 0.05·cos(10t + π/6)
            A = 0.05 m, ω = 10 rad/s, φ = π/6
            t₀ = 0.1 s
            h = 0.005 s

        Se pide: x'(0.1), x''(0.1), x'''(0.1) y comparar con exactas.
        """
        print("\n" + "="*60)
        print("MÉTODO DE CINCO PUNTOS - CASO EXTRA")
        print("Sistema masa-resorte: x(t) = 0.05·cos(10t + π/6)")
        print("Punto: t₀ = 0.1 s | Paso: h = 0.005 s")
        print("Se calculan: velocidad, aceleración y jerk")
        print("="*60)

        A = 0.05
        omega = 10
        phi = math.pi / 6

        def x(t):
            return A * math.cos(omega * t + phi)

        # Derivadas exactas
        def x_prima(t):         # velocidad: -A·ω·sin(ω·t + φ)
            return -A * omega * math.sin(omega * t + phi)

        def x_doble_prima(t):   # aceleración: -A·ω²·cos(ω·t + φ)
            return -A * omega**2 * math.cos(omega * t + phi)

        def x_triple_prima(t):  # jerk: A·ω³·sin(ω·t + φ)
            return A * omega**3 * math.sin(omega * t + phi)

        t0 = 0.1
        h = 0.005

        # Calcular con fórmulas de 5 puntos
        vel_aprox   = self.derivada_primera(x, t0, h)
        acel_aprox  = self.derivada_segunda(x, t0, h)
        jerk_aprox  = self.derivada_tercera(x, t0, h)

        vel_exacta  = x_prima(t0)
        acel_exacta = x_doble_prima(t0)
        jerk_exacta = x_triple_prima(t0)

        print(f"\n  VELOCIDAD en t = {t0} s:")
        print(f"    Aproximada  : {vel_aprox:.10f} m/s")
        print(f"    Exacta      : {vel_exacta:.10f} m/s")
        print(f"    Error abs   : {abs(vel_aprox - vel_exacta):.2e}")

        print(f"\n  ACELERACIÓN en t = {t0} s:")
        print(f"    Aproximada  : {acel_aprox:.8f} m/s²")
        print(f"    Exacta      : {acel_exacta:.8f} m/s²")
        print(f"    Error abs   : {abs(acel_aprox - acel_exacta):.2e}")

        print(f"\n  JERK (3ra derivada) en t = {t0} s:")
        print(f"    Aproximada  : {jerk_aprox:.6f} m/s³")
        print(f"    Exacta      : {jerk_exacta:.6f} m/s³")
        print(f"    Error abs   : {abs(jerk_aprox - jerk_exacta):.2e}")

        print("\n  CONCLUSIÓN: El método de 5 puntos permite estimar la 1ra, 2da y 3ra")
        print("  derivada con alta precisión para funciones analíticas suaves.")


# ==============================================================================
# CLASE 3: MÉTODO DEL TRAPECIO
# ==============================================================================

class MetodoTrapecio:
    """
    Integración numérica con el método del trapecio compuesto.

    Fórmula compuesta:
        ∫[a,b] f(x)dx ≈ (h/2)·[f(x₀) + 2·f(x₁) + 2·f(x₂) + ... + 2·f(xₙ₋₁) + f(xₙ)]

    donde h = (b-a)/n y xᵢ = a + i·h

    Error: O(h²)
    """

    def integrar(self, f, a, b, n):
        """
        Regla del trapecio compuesta.
        Parámetros:
            f : función a integrar
            a : límite inferior
            b : límite superior
            n : número de subintervalos (mientras mayor, más preciso)
        """
        h = (b - a) / n
        x = [a + i * h for i in range(n + 1)]
        suma = f(x[0]) + f(x[-1])          # Extremos con peso 1
        for i in range(1, n):
            suma += 2 * f(x[i])            # Puntos interiores con peso 2
        return (h / 2) * suma

    def integrar_tabular(self, t_vals, f_vals):
        """
        Trapecio para datos tabulados (no requiere fórmula explícita).
        Funciona con espaciado uniforme o no uniforme.
        """
        resultado = 0.0
        for i in range(len(t_vals) - 1):
            h_i = t_vals[i+1] - t_vals[i]
            resultado += h_i * (f_vals[i] + f_vals[i+1]) / 2
        return resultado

    def caso_ideal(self):
        """
        CASO IDEAL: W = ∫₀⁴ F(x) dx con F(x) = x·e^(-0.5x) + 2
        ---------------------------------------------------------------
        Contexto: Trabajo realizado por una fuerza variable sobre un
        desplazamiento de 0 a 4 metros.

        Datos:
            F(x) = x·e^(-0.5x) + 2  (Newtons)
            a = 0 m,  b = 4 m
            n = 1000 subintervalos

        Se pide: Calcular el trabajo total W en Joules.
        """
        print("\n" + "="*60)
        print("MÉTODO DEL TRAPECIO - CASO IDEAL")
        print("Función: F(x) = x·e^(-0.5x) + 2 (fuerza en Newtons)")
        print("Intervalo: [0, 4] m | n = 1000 subintervalos")
        print("Contexto: Trabajo realizado por fuerza variable")
        print("="*60)

        def F(x):
            return x * math.exp(-0.5 * x) + 2

        a, b, n = 0, 4, 1000

        aprox = self.integrar(F, a, b, n)
        exacto, _ = integrate.quad(F, a, b)
        error = abs((aprox - exacto) / exacto) * 100

        print(f"\n  Trabajo aproximado (trapecio)  : {aprox:.8f} J")
        print(f"  Valor de referencia (scipy)    : {exacto:.8f} J")
        print(f"  Error relativo                 : {error:.8f}%")
        print("\n  CONCLUSIÓN: Con n=1000, el trapecio converge con error menor al 0.001%.")
        print("  El método es apropiado para esta función suave y continua.")

    def caso_error(self):
        """
        CASO CON ERROR: ∫₀^π sin(10x) dx con n muy pequeño
        ---------------------------------------------------------------
        Sin(10x) oscila 5 veces completas en [0, π]. Con n=2, el trapecio
        no puede capturar estas oscilaciones y el error es enorme.

        Datos:
            f(x) = sin(10x)
            a = 0, b = π
            n = 2, 10, 100, 1000 (análisis comparativo)

        Se pide: Mostrar cómo el error disminuye al aumentar n.
        """
        print("\n" + "="*60)
        print("MÉTODO DEL TRAPECIO - CASO CON ERROR")
        print("Función: f(x) = sin(10x) (función altamente oscilatoria)")
        print("Análisis del error en función del número de subintervalos n")
        print("="*60)

        def f(x):
            return math.sin(10 * x)

        a, b = 0, math.pi
        valor_exacto, _ = integrate.quad(f, a, b)

        print(f"\n  {'n':>6} | {'Aproximación':>15} | {'Error absoluto':>16} | {'Error rel %':>12}")
        print(f"  {'-'*6}-+-{'-'*15}-+-{'-'*16}-+-{'-'*12}")

        for n in [2, 5, 10, 50, 100, 1000]:
            aprox = self.integrar(f, a, b, n)
            error_abs = abs(aprox - valor_exacto)
            if abs(valor_exacto) > 1e-10:
                error_rel = abs((aprox - valor_exacto) / valor_exacto) * 100
            else:
                error_rel = error_abs * 100  # Si el exacto es ~0
            print(f"  {n:>6} | {aprox:>15.8f} | {error_abs:>16.8f} | {error_rel:>12.4f}%")

        print(f"\n  Valor de referencia (scipy): {valor_exacto:.10f}")
        print("\n  CAUSA: Con n pequeño, el trapecio ignora la mayoría de las oscilaciones.")
        print("  Para sin(10x) en [0,π] existen 5 ciclos completos.")
        print("  REGLA PRÁCTICA: n debe ser >> 1/h_mínimo_de_la_función ≈ 10 ciclos/unidad.")
        print("  SOLUCIÓN: Usar n >= 500 para sin(10x) en [0,π].")

    def caso_extra(self):
        """
        CASO EXTRA: Volumen de agua en río V = ∫₀²⁴ Q(t) dt con datos tabulados
        ---------------------------------------------------------------
        Se tienen mediciones de caudal Q(t) cada 2 horas durante 24 horas.
        No se conoce la fórmula exacta, solo los datos experimentales.

        Datos (mediciones de campo):
            t (h) : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
            Q(m³/s): [5.0, 6.2, 8.1, 11.3, 14.0, 13.5, 12.0, 10.2, 8.8, 7.4, 6.5, 5.8, 5.1]

        Se pide: Calcular el volumen total de agua V en m³ y en litros.
        """
        print("\n" + "="*60)
        print("MÉTODO DEL TRAPECIO - CASO EXTRA")
        print("Datos tabulados: caudal Q(t) de un río durante 24 horas")
        print("Contexto: Hidrología - Cálculo de volumen de escorrentía")
        print("="*60)

        t = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]         # horas
        Q = [5.0, 6.2, 8.1, 11.3, 14.0, 13.5, 12.0, 10.2, 8.8, 7.4, 6.5, 5.8, 5.1]  # m³/s

        print(f"\n  Datos de caudal:")
        print(f"  {'t (h)':>6} | {'Q (m³/s)':>10}")
        print(f"  {'-'*6}-+-{'-'*10}")
        for i in range(len(t)):
            print(f"  {t[i]:>6} | {Q[i]:>10.1f}")

        # Integrar: ∫₀²⁴ Q(t) dt con t en horas → resultado en m³·h/s
        # Convertir a m³: multiplicar por 3600 s/h
        volumen_horas = self.integrar_tabular(t, Q)   # en m³·h/s
        volumen_m3 = volumen_horas * 3600              # convertir h→s

        caudal_promedio = volumen_horas / (t[-1] - t[0])  # m³/s promedio

        print(f"\n  RESULTADOS:")
        print(f"  Integral ∫Q dt (en m³·h/s)         : {volumen_horas:.4f}")
        print(f"  Volumen total de agua               : {volumen_m3:,.2f} m³")
        print(f"  Volumen total de agua               : {volumen_m3 * 1000:,.0f} litros")
        print(f"  Volumen total de agua               : {volumen_m3 / 1e6:.6f} km³")
        print(f"  Caudal promedio en 24 h             : {caudal_promedio:.4f} m³/s")


# ==============================================================================
# CLASE 4: REGLA DE SIMPSON 1/3
# ==============================================================================

class ReglaSimpson:
    """
    Integración numérica con la Regla de Simpson 1/3 compuesta.

    Fórmula compuesta:
        ∫[a,b] f(x)dx ≈ (h/3)·[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + 4f(xₙ₋₁) + f(xₙ)]

    Coeficientes: 1, 4, 2, 4, 2, ..., 4, 1
    REQUISITO: n debe ser par.
    Error: O(h^4)
    """

    def integrar(self, f, a, b, n):
        """
        Regla de Simpson 1/3 compuesta.
        Lanza ValueError si n es impar (requisito del método).
        """
        if n % 2 != 0:
            raise ValueError(
                f"ERROR: La Regla de Simpson 1/3 requiere número PAR de subintervalos. "
                f"Se recibió n = {n}. Use n = {n+1} o n = {n-1}."
            )
        h = (b - a) / n
        x = [a + i * h for i in range(n + 1)]

        suma = f(x[0]) + f(x[-1])         # Extremos con coeficiente 1
        for i in range(1, n):
            if i % 2 != 0:                 # Índice impar → coeficiente 4
                suma += 4 * f(x[i])
            else:                          # Índice par interior → coeficiente 2
                suma += 2 * f(x[i])

        return (h / 3) * suma

    def caso_ideal(self):
        """
        CASO IDEAL: ΔH = ∫₃₀₀¹⁰⁰⁰ Cp(T) dT para nitrógeno gaseoso
        ---------------------------------------------------------------
        Contexto: Ingeniería química - Cálculo de entalpía de calentamiento.
        Cp(T) = 28.58 + 3.77×10⁻³·T + 0.5×10⁵·T⁻² (J/mol·K) para N₂.

        Datos:
            Cp(T) = 28.58 + 3.77e-3·T + 0.5e5·T⁻²
            a = 300 K,  b = 1000 K
            n = 100 subintervalos (par)

        Se pide: ΔH en J/mol y comparar con valor de referencia.
        """
        print("\n" + "="*60)
        print("REGLA DE SIMPSON - CASO IDEAL")
        print("Función: Cp(T) = 28.58 + 3.77e-3·T + 0.5e5/T²  (J/mol·K)")
        print("Intervalo: [300 K, 1000 K] | n = 100")
        print("Contexto: Entalpía de calentamiento del nitrógeno gaseoso")
        print("="*60)

        def Cp(T):
            return 28.58 + 3.77e-3 * T + 0.5e5 / T**2

        a, b, n = 300, 1000, 100

        aprox = self.integrar(Cp, a, b, n)
        exacto, _ = integrate.quad(Cp, a, b)
        error = abs((aprox - exacto) / exacto) * 100

        print(f"\n  ΔH aproximado (Simpson)       : {aprox:.6f} J/mol")
        print(f"  ΔH de referencia (scipy)      : {exacto:.6f} J/mol")
        print(f"  Error relativo                : {error:.8f}%")
        print("\n  CONCLUSIÓN: Simpson 1/3 integra Cp(T) con error mínimo.")
        print("  Es mucho más preciso que el trapecio para la misma n,")
        print("  gracias a su aproximación parabólica (error O(h⁴) vs O(h²)).")

    def caso_error(self):
        """
        CASO CON ERROR: Intentar Simpson con n = 3 (impar) sobre f(x) = x²
        ---------------------------------------------------------------
        La regla de Simpson 1/3 requiere n par. Si se pasa n impar,
        el algoritmo debe detectarlo y lanzar un error claro.

        Datos:
            f(x) = x²
            a = 0, b = 3, n = 3 (impar → INVÁLIDO)
            Valor exacto: ∫₀³ x² dx = 27/3 = 9

        Se pide: Capturar el error, explicar la causa y resolver con n = 4.
        """
        print("\n" + "="*60)
        print("REGLA DE SIMPSON - CASO CON ERROR")
        print("Función: f(x) = x²  |  n = 3 (impar → inválido para Simpson 1/3)")
        print("="*60)

        def f(x):
            return x**2

        a, b = 0, 3
        valor_exacto = 9.0  # ∫₀³ x² dx = x³/3 |₀³ = 9

        # --- Intento con n impar ---
        print("\n  Intentando con n = 3 (impar)...")
        try:
            resultado = self.integrar(f, a, b, n=3)
            print(f"  Resultado inesperado: {resultado}")
        except ValueError as e:
            print(f"  EXCEPCIÓN CAPTURADA:\n  {e}")
            print("\n  CAUSA: El patrón 1,4,2,4,...,4,1 de Simpson requiere que")
            print("  los índices impares (coeficiente 4) sean correctamente alternados.")
            print("  Con n impar, el esquema de coeficientes no cierra correctamente.")

            # --- Recuperación automática ---
            n_corregido = 4
            print(f"\n  Recalculando con n = {n_corregido} (par)...")
            resultado = self.integrar(f, a, b, n=n_corregido)
            error = abs((resultado - valor_exacto) / valor_exacto) * 100

            print(f"  Resultado con n = {n_corregido}  : {resultado:.10f}")
            print(f"  Valor exacto        : {valor_exacto:.10f}")
            print(f"  Error relativo      : {error:.2e}%")
            print("\n  NOTA: Simpson integra EXACTAMENTE polinomios de grado ≤ 3.")
            print("  x² es de grado 2, por eso el error es prácticamente 0.")

    def caso_extra(self):
        """
        CASO EXTRA: Energía magnética en solenoide no uniforme
        ---------------------------------------------------------------
        Contexto: Electromagnetismo - Energía almacenada en solenoide con
        densidad de campo variable B(x) = B₀·(1 + 0.2·sin(πx/L)).

        Parámetros:
            B₀ = 0.5 T,  L = 2 m,  A = 0.01 m²
            μ₀ = 4π×10⁻⁷ H/m,  N/L = 500 vueltas/m

        Se pide:
            1. Energía total U en [0, 2] m
            2. Energía en primer metro [0, 1]
            3. Energía en segundo metro [1, 2]
            4. Verificar que las dos mitades suman la total
        """
        print("\n" + "="*60)
        print("REGLA DE SIMPSON - CASO EXTRA")
        print("Energía magnética en solenoide no uniforme")
        print("B(x) = B₀·(1 + 0.2·sin(πx/L))")
        print("Parámetros: B₀=0.5 T, L=2 m, A=0.01 m², N/L=500 vueltas/m")
        print("="*60)

        mu0 = 4 * math.pi * 1e-7   # Permeabilidad del vacío (H/m)
        B0 = 0.5                    # Campo magnético base (T)
        L = 2.0                     # Longitud del solenoide (m)
        A = 0.01                    # Área de la sección transversal (m²)
        NL = 500                    # Densidad de vueltas (N/L vueltas/m)

        def densidad_energia(x):
            """
            Densidad de energía magnética lineal:
            u(x) = (μ₀/2)·(N/L)²·A·B(x)²
            Donde B(x) = B₀·(1 + 0.2·sin(πx/L))
            """
            B = B0 * (1 + 0.2 * math.sin(math.pi * x / L))
            return (mu0 / 2) * NL**2 * A * B**2

        n = 100  # Par, requerido por Simpson

        energia_total      = self.integrar(densidad_energia, 0, 2, n)
        energia_primer_m   = self.integrar(densidad_energia, 0, 1, n)
        energia_segundo_m  = self.integrar(densidad_energia, 1, 2, n)
        suma_mitades       = energia_primer_m + energia_segundo_m
        discrepancia       = abs(energia_total - suma_mitades)

        print(f"\n  Energía total en [0, 2] m         : {energia_total:.10f} J")
        print(f"  Energía en primer metro [0, 1]    : {energia_primer_m:.10f} J")
        print(f"  Energía en segundo metro [1, 2]   : {energia_segundo_m:.10f} J")
        print(f"  Suma de las dos mitades           : {suma_mitades:.10f} J")
        print(f"  Discrepancia (debe ser ~0)        : {discrepancia:.2e} J")
        print(f"  Verificación de consistencia      : {'PASSED ✓' if discrepancia < 1e-12 else 'FAILED ✗'}")

        porcentaje_1m = energia_primer_m / energia_total * 100
        porcentaje_2m = energia_segundo_m / energia_total * 100
        print(f"\n  Distribución de energía:")
        print(f"    Primer metro  : {porcentaje_1m:.2f}% del total")
        print(f"    Segundo metro : {porcentaje_2m:.2f}% del total")


# ==============================================================================
# CLASE 5: CUADRATURA GAUSSIANA
# ==============================================================================

class CuadraturaGaussiana:
    """
    Integración numérica con cuadratura de Gauss-Legendre.

    Fórmula:
        ∫[a,b] f(x)dx ≈ ((b-a)/2) · Σᵢ wᵢ · f(((b-a)·tᵢ + (a+b)) / 2)

    donde tᵢ son los nodos (raíces del polinomio de Legendre de grado n)
    y wᵢ son los pesos asociados, ambos calculados con numpy.

    Con n puntos integra EXACTAMENTE polinomios de grado hasta 2n-1.
    Error: exponencialmente pequeño para funciones analíticas suaves.
    """

    def integrar(self, f, a, b, n):
        """
        Cuadratura de Gauss-Legendre con n puntos en [a, b].

        Parámetros:
            f : función a integrar (debe ser suave en [a,b])
            a : límite inferior
            b : límite superior
            n : número de puntos de cuadratura (mayor = más preciso)
        """
        # Obtener nodos y pesos de Gauss-Legendre en el intervalo estándar [-1, 1]
        nodos, pesos = np.polynomial.legendre.leggauss(n)

        # Factor de escala y centro para cambio de variable [-1,1] → [a,b]
        factor = (b - a) / 2.0
        centro = (a + b) / 2.0

        resultado = 0.0
        for ti, wi in zip(nodos, pesos):
            xi = factor * ti + centro     # Punto transformado en [a,b]
            resultado += wi * f(xi)       # Suma ponderada

        return factor * resultado         # Multiplicar por el jacobiano

    def caso_ideal(self):
        """
        CASO IDEAL: Longitud de arco orbital de satélite elíptico
        ---------------------------------------------------------------
        La longitud del arco de una elipse en [0, π] es:
            L = ∫₀^π √(a²·sin²(θ) + b²·cos²(θ)) dθ

        con a = 7000 km (semieje mayor) y b = 6800 km (semieje menor).
        Se compara la convergencia con 2, 5, 10 y 20 puntos gaussianos.

        Datos:
            f(θ) = √(7000²·sin²(θ) + 6800²·cos²(θ))
            a_integ = 0, b_integ = π

        Se pide: Calcular la longitud y mostrar convergencia.
        """
        print("\n" + "="*60)
        print("CUADRATURA GAUSSIANA - CASO IDEAL")
        print("Longitud de arco orbital: ∫₀^π √(a²sin²θ + b²cos²θ) dθ")
        print("Semiejes: a = 7000 km, b = 6800 km")
        print("="*60)

        a_orb = 7000.0   # km
        b_orb = 6800.0   # km

        def f(theta):
            return math.sqrt(a_orb**2 * math.sin(theta)**2 + b_orb**2 * math.cos(theta)**2)

        referencia, _ = integrate.quad(f, 0, math.pi)

        print(f"\n  {'n':>4} | {'Aproximación (km)':>20} | {'Error relativo %':>18}")
        print(f"  {'-'*4}-+-{'-'*20}-+-{'-'*18}")

        for n in [2, 3, 5, 10, 20]:
            aprox = self.integrar(f, 0, math.pi, n)
            error = abs((aprox - referencia) / referencia) * 100
            print(f"  {n:>4} | {aprox:>20.6f} | {error:>18.8f}%")

        print(f"\n  Valor de referencia (scipy): {referencia:.6f} km")
        print("\n  CONCLUSIÓN: Con solo 5 puntos gaussianos se logra un error < 0.0001%.")
        print("  La cuadratura gaussiana converge exponencialmente rápido para funciones suaves.")

    def caso_error(self):
        """
        CASO CON ERROR: ∫₀^π cos(20x) dx (función muy oscilatoria)
        ---------------------------------------------------------------
        El valor exacto de ∫₀^π cos(20x) dx = sin(20π)/20 ≈ 0.
        Con pocos puntos gaussianos, el resultado es incorrecto porque
        los nodos no pueden muestrear adecuadamente las oscilaciones.

        Datos:
            f(x) = cos(20x)
            a = 0, b = π
            Valor exacto ≈ 0

        Se pide: Mostrar la convergencia con n = 2, 5, 10, 20, 50.
        """
        print("\n" + "="*60)
        print("CUADRATURA GAUSSIANA - CASO CON ERROR")
        print("Función: f(x) = cos(20x) en [0, π] (altamente oscilatoria)")
        print("Valor exacto = sin(20π)/20 ≈ 0")
        print("="*60)

        def f(x):
            return math.cos(20 * x)

        valor_exacto = math.sin(20 * math.pi) / 20  # ≈ 0 (exactamente 0)

        print(f"\n  {'n':>4} | {'Aproximación':>16} | {'Error abs':>14} | {'Convergió':>10}")
        print(f"  {'-'*4}-+-{'-'*16}-+-{'-'*14}-+-{'-'*10}")

        for n in [2, 5, 10, 20, 50, 100]:
            aprox = self.integrar(f, 0, math.pi, n)
            error_abs = abs(aprox - valor_exacto)
            convergio = "SI" if error_abs < 1e-4 else "NO"
            print(f"  {n:>4} | {aprox:>16.8f} | {error_abs:>14.8f} | {convergio:>10}")

        print(f"\n  Valor exacto: {valor_exacto:.15f}")
        print("\n  CAUSA: cos(20x) completa 10 ciclos en [0,π]. La cuadratura gaussiana")
        print("  con n puntos integra exactamente polinomios de grado 2n-1, pero NO")
        print("  funciones trigonométricas oscilatorias con pocos puntos.")
        print("  SOLUCIÓN: Usar n >= 50, o dividir [0,π] en subintervalos pequeños")
        print("  y aplicar cuadratura gaussiana en cada uno (cuadratura adaptativa).")

    def caso_extra(self):
        """
        CASO EXTRA: Distribución Normal Estándar acumulada Φ(z)
        ---------------------------------------------------------------
        Calcular P(Z ≤ z) = 0.5 + (1/√(2π)) · ∫₀ᶻ e^(-t²/2) dt
        para z = 1.0, 1.96 y 2.576 usando cuadratura gaussiana con 10 puntos.

        Comparar con scipy.stats.norm.cdf() (valor de referencia).

        Datos:
            f(t) = (1/√(2π)) · e^(-t²/2)
            Integrar de 0 a z
            n = 10 puntos gaussianos

        Se pide: P(Z ≤ 1.0), P(Z ≤ 1.96), P(Z ≤ 2.576)
        """
        print("\n" + "="*60)
        print("CUADRATURA GAUSSIANA - CASO EXTRA")
        print("Distribución Normal Estándar Acumulada Φ(z)")
        print("Φ(z) = 0.5 + (1/√(2π))·∫₀ᶻ e^(-t²/2) dt")
        print("="*60)

        def integrando_normal(t):
            return (1.0 / math.sqrt(2 * math.pi)) * math.exp(-t**2 / 2)

        valores_z = {
            1.0:   "Intervalo ±1σ cubre el 68.27% de la distribución",
            1.96:  "Intervalo de confianza 95% (valor z crítico)",
            2.576: "Intervalo de confianza 99% (valor z crítico)"
        }

        print(f"\n  {'z':>7} | {'Φ(z) Gauss':>14} | {'Φ(z) scipy':>14} | {'Error abs':>12} | Interpretación")
        print(f"  {'-'*7}-+-{'-'*14}-+-{'-'*14}-+-{'-'*12}-+-" + "-"*40)

        n = 10

        for z, interpretacion in valores_z.items():
            integral = self.integrar(integrando_normal, 0, z, n)
            phi_gauss = 0.5 + integral
            phi_scipy = stats.norm.cdf(z)
            error = abs(phi_gauss - phi_scipy)
            print(f"  {z:>7.3f} | {phi_gauss:>14.8f} | {phi_scipy:>14.8f} | {error:>12.2e} | {interpretacion}")

        print("\n  CONCLUSIÓN: Con solo 10 puntos gaussianos se obtienen 8 cifras decimales")
        print("  correctas para la distribución normal. Esto requeriría miles de puntos")
        print("  con el método del trapecio o Simpson para igual precisión.")
        print("  La razón: e^(-t²/2) es extremadamente suave → convergencia exponencial.")


# ==============================================================================
# PROGRAMA PRINCIPAL
# Ejecuta todos los métodos y casos automáticamente al correr el archivo.
# ==============================================================================

def imprimir_separador(titulo, char="█"):
    """Imprime un separador visual decorativo para organizar la salida."""
    linea = char * 60
    print(f"\n\n{linea}")
    print(f"  {titulo}")
    print(linea)


def main():
    """Función principal: instancia todas las clases y ejecuta todos los casos."""

    print("\n" + "="*60)
    print("  MÉTODOS NUMÉRICOS: DERIVACIÓN E INTEGRACIÓN")
    print("  Ejecución automática de todos los métodos y casos")
    print("  Autor: [Tu nombre] | Fecha: [Fecha]")
    print("="*60)

    # ----------------------------------------------------------------
    # BLOQUE 1: MÉTODOS DE DERIVACIÓN
    # ----------------------------------------------------------------

    imprimir_separador("BLOQUE 1: MÉTODOS DE DERIVACIÓN NUMÉRICA")

    # --- MÉTODO 1: TRES PUNTOS ---
    imprimir_separador("MÉTODO DE TRES PUNTOS", char="─")
    m3p = MetodoTresPuntos()
    m3p.caso_ideal()
    m3p.caso_error()
    m3p.caso_extra()

    # --- MÉTODO 2: CINCO PUNTOS ---
    imprimir_separador("MÉTODO DE CINCO PUNTOS", char="─")
    m5p = MetodoCincoPuntos()
    m5p.caso_ideal()
    m5p.caso_error()
    m5p.caso_extra()

    # ----------------------------------------------------------------
    # BLOQUE 2: MÉTODOS DE INTEGRACIÓN
    # ----------------------------------------------------------------

    imprimir_separador("BLOQUE 2: MÉTODOS DE INTEGRACIÓN NUMÉRICA")

    # --- MÉTODO 3: TRAPECIO ---
    imprimir_separador("MÉTODO DEL TRAPECIO COMPUESTO", char="─")
    trap = MetodoTrapecio()
    trap.caso_ideal()
    trap.caso_error()
    trap.caso_extra()

    # --- MÉTODO 4: SIMPSON ---
    imprimir_separador("REGLA DE SIMPSON 1/3 COMPUESTA", char="─")
    simp = ReglaSimpson()
    simp.caso_ideal()
    simp.caso_error()
    simp.caso_extra()

    # --- MÉTODO 5: CUADRATURA GAUSSIANA ---
    imprimir_separador("CUADRATURA DE GAUSS-LEGENDRE", char="─")
    gauss = CuadraturaGaussiana()
    gauss.caso_ideal()
    gauss.caso_error()
    gauss.caso_extra()

    # ----------------------------------------------------------------
    # FIN
    # ----------------------------------------------------------------

    print("\n\n" + "="*60)
    print("  EJECUCIÓN COMPLETA")
    print("  Todos los métodos y casos fueron calculados exitosamente.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
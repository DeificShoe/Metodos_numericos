# 🔍 Unidad 2 - Métodos de Solución de Ecuaciones

> **Asignatura:** Métodos Numéricos  
> **Nivel:** Ingeniería / Ciencias Exactas  
> **Modalidad:** Teórico-Práctica

---

## 📋 Índice

- [1. Introducción](#1-introducción)
- [2. Objetivos](#2-objetivos)
- [3. Importancia del Tema](#3-importancia-del-tema)
- [4. Conceptos Fundamentales](#4-conceptos-fundamentales)
- [5. Desarrollo Teórico](#5-desarrollo-teórico)
  - [5.1 Métodos de Intervalo](#51-métodos-de-intervalo)
  - [5.2 Método de Bisección](#52-método-de-bisección)
  - [5.3 Método de Aproximaciones Sucesivas](#53-método-de-aproximaciones-sucesivas)
  - [5.4 Métodos de Interpolación (Newton-Raphson, Secante)](#54-métodos-de-interpolación-newton-raphson-secante)
- [6. Fórmulas Matemáticas](#6-fórmulas-matemáticas)
- [7. Explicación de Métodos](#7-explicación-de-métodos)
- [8. Ejemplos](#8-ejemplos)
- [9. Aplicaciones Reales](#9-aplicaciones-reales)
- [10. Ventajas y Desventajas](#10-ventajas-y-desventajas)
- [11. Conclusión](#11-conclusión)
- [12. Bibliografía](#12-bibliografía)

---

## 1. Introducción

La solución de ecuaciones no lineales es uno de los problemas más frecuentes en ciencias e ingeniería. Dado que la mayoría de ecuaciones reales no admiten solución algebraica exacta, los métodos numéricos proveen herramientas sistemáticas para encontrar aproximaciones de las raíces con la precisión requerida.

Una **raíz** de una ecuación $f(x) = 0$ es un valor $x^*$ tal que $f(x^*) = 0$. Geométricamente, corresponde al punto donde la curva $y = f(x)$ cruza (o toca) el eje $x$.

Esta unidad cubre los métodos fundamentales para localizar raíces: métodos de intervalo (bisección y falsa posición), métodos abiertos (Newton-Raphson, secante, punto fijo) y sus aplicaciones prácticas.

---

## 2. Objetivos

- 🎯 Entender el problema de búsqueda de raíces y su formulación matemática.
- 🎯 Aplicar correctamente el método de bisección y análizar su convergencia.
- 🎯 Implementar el método de punto fijo y determinar condiciones de convergencia.
- 🎯 Aplicar los métodos de Newton-Raphson y de la secante.
- 🎯 Comparar los distintos métodos en términos de velocidad de convergencia y requisitos.
- 🎯 Resolver problemas de ingeniería mediante la búsqueda numérica de raíces.

---

## 3. Importancia del Tema

Los problemas de búsqueda de raíces aparecen en casi todos los ámbitos de la ingeniería:

- **Estática y dinámica:** encontrar ángulos de equilibrio, frecuencias naturales de vibración.
- **Termodinámica:** calcular temperaturas y presiones de equilibrio en procesos no lineales.
- **Economía:** calcular tasas de interés internas de retorno (TIR).
- **Electrónica:** encontrar puntos de operación de circuitos con dispositivos no lineales.
- **Química:** resolver ecuaciones de estado no ideales (van der Waals, Peng-Robinson).

---

## 4. Conceptos Fundamentales

### Definición de Raíz
Sea $f: [a,b] \to \mathbb{R}$ continua. Un número $x^* \in [a,b]$ es una **raíz** de $f$ si:
$$f(x^*) = 0$$

### Teorema de Bolzano (Valor Intermedio)
Si $f$ es continua en $[a,b]$ y $f(a) \cdot f(b) < 0$, entonces existe al menos un $c \in (a,b)$ tal que $f(c) = 0$.

Este teorema es la base de los **métodos de intervalo**.

### Multiplicidad de una Raíz
- **Raíz simple:** $f(x^*) = 0$ y $f'(x^*) \neq 0$
- **Raíz múltiple de orden $m$:** $f(x^*) = f'(x^*) = \cdots = f^{(m-1)}(x^*) = 0$ y $f^{(m)}(x^*) \neq 0$

Las raíces múltiples causan problemas de convergencia en varios métodos.

---

## 5. Desarrollo Teórico

### 5.1 Métodos de Intervalo

Los métodos de intervalo garantizan la convergencia si se cumplen ciertas condiciones iniciales. Requieren dos puntos $a$ y $b$ tales que $f(a) \cdot f(b) < 0$.

#### Ventaja principal
Siempre convergen si la función es continua y existe raíz en el intervalo.

#### Desventaja principal
Son relativamente lentos comparados con métodos abiertos.

---

### 5.2 Método de Bisección

El método de **bisección** divide repetidamente el intervalo $[a,b]$ a la mitad y selecciona el subintervalo que contiene la raíz.

**Algoritmo:**
1. Verificar que $f(a) \cdot f(b) < 0$
2. Calcular punto medio: $c = \frac{a+b}{2}$
3. Si $f(a) \cdot f(c) < 0$, la raíz está en $[a,c]$: hacer $b = c$
4. Si $f(c) \cdot f(b) < 0$, la raíz está en $[c,b]$: hacer $a = c$
5. Repetir hasta convergencia

**Convergencia:** El error se reduce a la mitad en cada iteración:
$$|e_n| \leq \frac{b-a}{2^n}$$

---

### 5.3 Método de Aproximaciones Sucesivas (Punto Fijo)

Se reformula $f(x) = 0$ como $x = g(x)$ y se itera:
$$x_{n+1} = g(x_n)$$

**Teorema de Punto Fijo (Banach):** Si $g$ es continua y $|g'(x)| < 1$ en un intervalo que contiene a la raíz, el método converge.

**Condición de convergencia:**
$$|g'(x^*)| < 1$$

---

### 5.4 Métodos de Interpolación (Newton-Raphson, Secante)

#### Método de Newton-Raphson
Utiliza la tangente a la curva en el punto actual para aproximar la raíz:
$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

**Convergencia cuadrática** para raíces simples: $|e_{n+1}| \approx C \cdot |e_n|^2$

#### Método de la Secante
No requiere $f'(x)$; aproxima la derivada por diferencia finita:
$$x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$

**Convergencia superlineal** con orden $p \approx 1.618$ (número áureo).

#### Método de la Falsa Posición (Regula Falsi)
Combina la garantía de convergencia del método de intervalo con la idea de interpolación lineal:
$$c = b - f(b) \cdot \frac{b - a}{f(b) - f(a)}$$

---

## 6. Fórmulas Matemáticas

### Método de Bisección
$$c = \frac{a + b}{2}$$

$$\text{Error máximo:} \quad |e_n| \leq \frac{b_0 - a_0}{2^n}$$

$$\text{Número de iteraciones para tolerancia } \varepsilon: \quad n \geq \frac{\ln\left(\frac{b_0 - a_0}{\varepsilon}\right)}{\ln 2}$$

### Método de Newton-Raphson
$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

$$\text{Tasa de convergencia:} \quad |e_{n+1}| \approx \frac{|f''(x^*)|}{2|f'(x^*)|} |e_n|^2$$

### Método de la Secante
$$x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$

### Método de Falsa Posición
$$c = \frac{a \cdot f(b) - b \cdot f(a)}{f(b) - f(a)}$$

### Punto Fijo - Criterio de Convergencia
$$|g'(x)| < 1 \quad \text{en la vecindad de } x^*$$

### Error en el Método de Newton-Raphson para Raíz Múltiple de orden $m$
$$x_{n+1} = x_n - m \cdot \frac{f(x_n)}{f'(x_n)}$$

---

## 7. Explicación de Métodos

### 7.1 Pseudocódigo: Bisección

```
Algoritmo Bisección:
  ENTRADA: f, a, b, tol, maxIter
  SALIDA: raíz aproximada o mensaje de error

  SI f(a) * f(b) >= 0:
    ERROR "No hay cambio de signo en [a,b]"

  PARA i = 1 HASTA maxIter:
    c ← (a + b) / 2
    ea ← |(b - a) / (2 * c)| * 100

    SI f(a) * f(c) < 0:
      b ← c
    SINO SI f(c) * f(b) < 0:
      a ← c
    SINO:
      RETORNAR c    // f(c) == 0, raíz exacta

    SI ea < tol:
      RETORNAR c

  RETORNAR c        // mejor aproximación obtenida
```

### 7.2 Pseudocódigo: Newton-Raphson

```
Algoritmo NewtonRaphson:
  ENTRADA: f, f', x0, tol, maxIter
  SALIDA: raíz aproximada

  x ← x0
  PARA i = 1 HASTA maxIter:
    SI |f'(x)| < 1e-12:
      ERROR "Derivada cercana a cero"

    x_nuevo ← x - f(x) / f'(x)
    ea ← |x_nuevo - x| / |x_nuevo| * 100

    SI ea < tol:
      RETORNAR x_nuevo

    x ← x_nuevo

  RETORNAR x
```

### 7.3 Implementación en Python

```python
import numpy as np

def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """Método de bisección para encontrar raíces de f en [a,b]"""
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")
    
    historial = []
    for i in range(max_iter):
        c = (a + b) / 2
        ea = abs((b - a) / (2 * c)) * 100
        historial.append({'iter': i+1, 'a': a, 'b': b, 'c': c, 
                          'f(c)': f(c), 'ea%': ea})
        
        if abs(f(c)) < 1e-15 or ea < tol:
            return c, historial
        
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return c, historial


def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    """Método de Newton-Raphson"""
    x = x0
    historial = []
    
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        
        if abs(dfx) < 1e-12:
            raise ValueError("Derivada muy cercana a cero")
        
        x_nuevo = x - fx / dfx
        
        if i > 0:
            ea = abs((x_nuevo - x) / x_nuevo) * 100
        else:
            ea = float('inf')
        
        historial.append({'iter': i+1, 'x': x_nuevo, 'f(x)': f(x_nuevo), 'ea%': ea})
        
        if ea < tol:
            return x_nuevo, historial
        
        x = x_nuevo
    
    return x, historial


# Ejemplo: f(x) = x³ - x - 2
f  = lambda x: x**3 - x - 2
df = lambda x: 3*x**2 - 1

raiz_bis, _ = biseccion(f, 1, 2, tol=0.01)
raiz_nr, _  = newton_raphson(f, df, x0=1.5, tol=0.01)

print(f"Bisección:       raíz ≈ {raiz_bis:.6f}")
print(f"Newton-Raphson:  raíz ≈ {raiz_nr:.6f}")
```

---

## 8. Ejemplos

### Ejemplo 1: Bisección

**Problema:** Encontrar la raíz de $f(x) = x^3 - x - 2$ en $[1, 2]$.

| Iteración | $a$ | $b$ | $c$ | $f(c)$ | $\varepsilon_a$ (%) |
|-----------|-----|-----|-----|--------|---------------------|
| 1 | 1.0 | 2.0 | 1.5 | −0.125 | — |
| 2 | 1.5 | 2.0 | 1.75 | 1.6094 | 14.29 |
| 3 | 1.5 | 1.75 | 1.625 | 0.666 | 7.69 |
| 4 | 1.5 | 1.625 | 1.5625 | 0.252 | 4.00 |
| 5 | 1.5 | 1.5625 | 1.5313 | 0.059 | 2.04 |

Raíz exacta: $x^* \approx 1.5214$

---

### Ejemplo 2: Newton-Raphson

**Problema:** Encontrar $\sqrt{3}$ reformulando como $f(x) = x^2 - 3 = 0$, con $x_0 = 2$.

$f'(x) = 2x$

$$x_{n+1} = x_n - \frac{x_n^2 - 3}{2x_n} = \frac{x_n}{2} + \frac{3}{2x_n}$$

| $n$ | $x_n$ | $f(x_n)$ | $\varepsilon_a$ (%) |
|-----|--------|----------|---------------------|
| 0 | 2.000000 | 1.000000 | — |
| 1 | 1.750000 | 0.062500 | 14.286 |
| 2 | 1.732143 | 0.000026 | 1.031 |
| 3 | 1.732051 | 0.0000000 | 0.005 |

Converge en solo 3 iteraciones a $\sqrt{3} \approx 1.732051$.

---

### Ejemplo 3: Punto Fijo

**Problema:** Resolver $x^2 - x - 1 = 0$ (raíz áurea $\varphi \approx 1.618$).

Reformulación: $x = \sqrt{x + 1} = g(x)$

$g'(x) = \frac{1}{2\sqrt{x+1}}$, en $x=1.618$: $g'(1.618) \approx 0.309 < 1$ ✅

| $n$ | $x_n$ | $g(x_n)$ | $\varepsilon_a$ (%) |
|-----|--------|----------|---------------------|
| 0 | 1.0 | 1.41421 | — |
| 1 | 1.41421 | 1.55377 | 9.864 |
| 2 | 1.55377 | 1.59805 | 2.772 |
| 3 | 1.59805 | 1.61185 | 0.859 |
| 4 | 1.61185 | 1.61612 | 0.265 |

---

### Ejemplo 4: Tasa de Interés (TIR)

**Problema:** Un préstamo de \$1,000 se paga en 5 cuotas mensuales de \$250. Encontrar la tasa mensual $r$.

$$1000 = 250 \cdot \frac{1 - (1+r)^{-5}}{r}$$

$$f(r) = 250 \cdot \frac{1 - (1+r)^{-5}}{r} - 1000 = 0$$

Aplicando bisección en $[0.01, 0.5]$ se obtiene $r \approx 0.0765$ (7.65% mensual).

---

## 9. Aplicaciones Reales

### ⚡ Ingeniería Eléctrica
El punto de operación de un diodo se encuentra resolviendo:
$$I = I_s \left(e^{V/(nV_T)} - 1\right) = \frac{V_s - V}{R}$$

Esta ecuación trascendental se resuelve numéricamente con Newton-Raphson.

### 🏗️ Resistencia de Materiales
La ecuación de la viga elástica con carga distribuida lleva a ecuaciones trascendentes para los modos propios de vibración.

### 🔬 Química
Las ecuaciones cúbicas de estado (van der Waals, Peng-Robinson) para calcular volúmenes molares de gases reales:
$$\left(P + \frac{a}{V^2}\right)(V - b) = RT$$

### 💰 Finanzas
Cálculo de la Tasa Interna de Retorno (TIR):
$$\sum_{t=0}^{n} \frac{C_t}{(1+r)^t} = 0$$

---

## 10. Ventajas y Desventajas

### Comparativa de Métodos

| Método | Convergencia | Requiere $f'$ | Garantía | Orden |
|--------|-------------|---------------|----------|-------|
| Bisección | Lenta | No | Sí | Lineal |
| Falsa Posición | Media | No | Sí | Superlineal |
| Punto Fijo | Variable | No | Condicional | Lineal |
| Newton-Raphson | Muy rápida | Sí | No | Cuadrática |
| Secante | Rápida | No | No | $\approx 1.618$ |

### ✅ Ventajas Generales

- Los métodos de intervalo **garantizan convergencia** si se verifican las condiciones iniciales.
- Newton-Raphson es **extremadamente rápido** cerca de la raíz.
- La secante elimina la necesidad de calcular derivadas analíticas.
- Son implementables para cualquier función continua.

### ❌ Desventajas Generales

- Los métodos abiertos **pueden diverger** con mala aproximación inicial.
- Newton-Raphson falla si $f'(x) = 0$ en algún punto de la iteración.
- Bisección es **lento** para alta precisión.
- Ningún método es universalmente el mejor; la elección depende del problema.

---

## 11. Conclusión

La solución numérica de ecuaciones es una herramienta indispensable en la ingeniería moderna. Los métodos de intervalo como bisección ofrecen robustez y garantías de convergencia a costa de velocidad. Los métodos abiertos como Newton-Raphson son extremadamente eficientes pero requieren buenas aproximaciones iniciales y condiciones de regularidad.

La elección del método adecuado depende del conocimiento previo sobre la función, la disponibilidad de la derivada y el balance entre velocidad y seguridad requerido por la aplicación. En la práctica, a menudo se combina un método de intervalo para obtener una buena aproximación inicial, seguido de Newton-Raphson para refinar rápidamente.

---

## 12. Bibliografía

Chapra, S. C., & Canale, R. P. (2015). *Métodos numéricos para ingenieros* (7.ª ed.). McGraw-Hill Education.

Burden, R. L., & Faires, J. D. (2011). *Numerical analysis* (9th ed.). Brooks/Cole, Cengage Learning.

Atkinson, K. E. (1989). *An introduction to numerical analysis* (2nd ed.). John Wiley & Sons.

Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical recipes: The art of scientific computing* (3rd ed.). Cambridge University Press.

Quarteroni, A., & Saleri, F. (2006). *Scientific computing with MATLAB and Octave* (2nd ed.). Springer.

---

*📌 Documento generado para uso académico. Unidad 2 - Métodos Numéricos.*

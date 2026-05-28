# 📊 Unidad 4 - Diferenciación e Integración Numérica

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
  - [5.1 Diferenciación Numérica](#51-diferenciación-numérica)
  - [5.2 Integración Numérica](#52-integración-numérica)
  - [5.3 Integración Múltiple](#53-integración-múltiple)
- [6. Fórmulas Matemáticas](#6-fórmulas-matemáticas)
- [7. Explicación de Métodos](#7-explicación-de-métodos)
- [8. Ejemplos](#8-ejemplos)
- [9. Aplicaciones Reales](#9-aplicaciones-reales)
- [10. Ventajas y Desventajas](#10-ventajas-y-desventajas)
- [11. Conclusión](#11-conclusión)
- [12. Bibliografía](#12-bibliografía)

---

## 1. Introducción

La diferenciación e integración numérica son técnicas que permiten calcular derivadas e integrales de funciones cuando no se dispone de una expresión analítica (datos discretos), o cuando la integración o derivación analítica es extremadamente difícil o imposible.

La **diferenciación numérica** aproxima el valor de una derivada $f'(x)$ usando valores conocidos de la función en puntos discretos. La **integración numérica** (o cuadratura numérica) estima el valor de una integral definida $\int_a^b f(x)\,dx$ mediante sumas ponderadas de valores de la función.

Ambas operaciones son pilares del análisis numérico y sustentan innumerables algoritmos en simulación, optimización, procesamiento de señales y solución de ecuaciones diferenciales.

---

## 2. Objetivos

- 🎯 Derivar y aplicar fórmulas de diferenciación numérica mediante diferencias finitas.
- 🎯 Analizar el error de truncamiento en las fórmulas de diferenciación numérica.
- 🎯 Aplicar las reglas de Newton-Cotes: trapecio, Simpson 1/3 y Simpson 3/8.
- 🎯 Implementar la cuadratura de Gauss-Legendre y comprender sus ventajas.
- 🎯 Extender las fórmulas de integración numérica al caso múltiple (doble y triple).
- 🎯 Resolver problemas de ingeniería que involucren derivación e integración de datos discretos.

---

## 3. Importancia del Tema

- **Señales experimentales:** los datos de sensores son discretos; calcular velocidad (derivada de posición) o energía (integral de potencia) requiere métodos numéricos.
- **Simulación de sistemas dinámicos:** los métodos de integración son la base de los solucionadores de ODEs.
- **Mecánica de fluidos:** el cálculo de caudal, trabajo y energía sobre perfiles aerodinámicos involucra integraciones numéricas.
- **Procesamiento de imágenes:** los gradientes de imágenes se calculan con diferencias finitas.
- **Estadística computacional:** muchas distribuciones de probabilidad no tienen función de distribución acumulada analítica.

---

## 4. Conceptos Fundamentales

### Diferenciación Numérica
Se basa en la aproximación de la derivada como una diferencia de cocientes:
$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

Cuando $h$ es pequeño pero finito, se obtiene una aproximación.

### Integración Numérica (Cuadratura)
$$\int_a^b f(x)\,dx \approx \sum_{i=0}^{n} w_i f(x_i)$$

donde $w_i$ son **pesos** y $x_i$ son **nodos** (puntos de evaluación). La elección de nodos y pesos define el método.

### Error de Cuadratura
El error depende de:
- El método utilizado (orden de exactitud polinomial)
- El tamaño del paso $h = (b-a)/n$
- Las derivadas de la función integranda

### Reglas de Newton-Cotes
Basan los nodos en puntos igualmente espaciados. La integración se realiza ajustando polinomios a los puntos y luego integrando el polinomio exactamente.

---

## 5. Desarrollo Teórico

### 5.1 Diferenciación Numérica

#### Diferencia Finita Progresiva (Forward)
$$f'(x_i) \approx \frac{f(x_{i+1}) - f(x_i)}{h}$$
Error de truncamiento: $O(h)$

#### Diferencia Finita Regresiva (Backward)
$$f'(x_i) \approx \frac{f(x_i) - f(x_{i-1})}{h}$$
Error de truncamiento: $O(h)$

#### Diferencia Finita Central
$$f'(x_i) \approx \frac{f(x_{i+1}) - f(x_{i-1})}{2h}$$
Error de truncamiento: $O(h^2)$ — **más precisa**

#### Segunda Derivada (Diferencia Central)
$$f''(x_i) \approx \frac{f(x_{i+1}) - 2f(x_i) + f(x_{i-1})}{h^2}$$
Error de truncamiento: $O(h^2)$

#### Fórmulas de Mayor Orden
Usando más puntos se obtiene mayor precisión. Para la primera derivada con 5 puntos (error $O(h^4)$):
$$f'(x_i) \approx \frac{-f(x_{i+2}) + 8f(x_{i+1}) - 8f(x_{i-1}) + f(x_{i-2})}{12h}$$

---

### 5.2 Integración Numérica

#### Regla del Trapecio
Aproxima $f$ por un polinomio de grado 1 (línea recta):
$$\int_a^b f(x)\,dx \approx \frac{h}{2}\left[f(a) + f(b)\right]$$

**Regla compuesta del Trapecio** (con $n$ subintervalos, $h = (b-a)/n$):
$$\int_a^b f(x)\,dx \approx \frac{h}{2}\left[f(x_0) + 2\sum_{i=1}^{n-1}f(x_i) + f(x_n)\right]$$

Error: $E_t \approx -\frac{(b-a)^3}{12n^2} f''(\xi)$

#### Regla de Simpson 1/3
Aproxima $f$ por un polinomio de grado 2 (parábola). Requiere $n$ par:
$$\int_a^b f(x)\,dx \approx \frac{h}{3}\left[f(x_0) + 4f(x_1) + f(x_2)\right] \quad \text{(una aplicación)}$$

**Regla compuesta Simpson 1/3:**
$$\int_a^b f(x)\,dx \approx \frac{h}{3}\left[f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \cdots + 4f(x_{n-1}) + f(x_n)\right]$$

Error: $E_s \approx -\frac{(b-a)^5}{180n^4} f^{(4)}(\xi)$

#### Regla de Simpson 3/8
Usa polinomio de grado 3, requiere múltiplo de 3 subintervalos:
$$\int_{x_0}^{x_3} f(x)\,dx \approx \frac{3h}{8}\left[f(x_0) + 3f(x_1) + 3f(x_2) + f(x_3)\right]$$

#### Cuadratura de Gauss-Legendre
Elige nodos **no uniformes** para maximizar la precisión. Con $n$ puntos, es exacta para polinomios de grado $\leq 2n-1$:
$$\int_{-1}^{1} f(t)\,dt \approx \sum_{i=1}^{n} w_i f(t_i)$$

Para integrar en $[a,b]$, se hace el cambio de variable $x = \frac{(b-a)t + (b+a)}{2}$:
$$\int_a^b f(x)\,dx \approx \frac{b-a}{2} \sum_{i=1}^{n} w_i f\left(\frac{(b-a)t_i + (b+a)}{2}\right)$$

**Nodos y pesos para $n=3$:**

| $i$ | $t_i$ | $w_i$ |
|-----|--------|--------|
| 1 | $-\sqrt{3/5} \approx -0.77460$ | $5/9 \approx 0.5556$ |
| 2 | $0$ | $8/9 \approx 0.8889$ |
| 3 | $+\sqrt{3/5} \approx +0.77460$ | $5/9 \approx 0.5556$ |

---

### 5.3 Integración Múltiple

#### Integral Doble sobre Rectángulo
$$\int_{c}^{d}\int_{a}^{b} f(x,y)\,dx\,dy \approx \sum_{i=0}^{m}\sum_{j=0}^{n} w_i w_j f(x_i, y_j)$$

**Regla compuesta del Trapecio doble:**
$$I \approx h_x h_y \left[\frac{1}{4}f_{0,0} + \frac{1}{2}\sum_{\text{bordes}} f + \sum_{\text{interior}} f\right]$$

**Regla de Simpson doble (ambas dimensiones):**
$$I \approx \frac{h_x h_y}{9}\left[f_{0,0} + 4f_{1,0} + \cdots\right]$$

---

## 6. Fórmulas Matemáticas

### Diferencias Finitas

| Tipo | Fórmula | Error |
|------|---------|-------|
| Forward $f'$ | $\dfrac{f(x+h)-f(x)}{h}$ | $O(h)$ |
| Backward $f'$ | $\dfrac{f(x)-f(x-h)}{h}$ | $O(h)$ |
| Central $f'$ | $\dfrac{f(x+h)-f(x-h)}{2h}$ | $O(h^2)$ |
| Central $f''$ | $\dfrac{f(x+h)-2f(x)+f(x-h)}{h^2}$ | $O(h^2)$ |

### Error del Trapecio Compuesto
$$E_T = -\frac{(b-a)h^2}{12} f''(\xi), \quad \xi \in (a,b)$$

### Error de Simpson 1/3 Compuesto
$$E_S = -\frac{(b-a)h^4}{180} f^{(4)}(\xi), \quad \xi \in (a,b)$$

### Cambio de Variable para Gauss-Legendre
$$x = \frac{(b-a)t + (a+b)}{2}, \quad dx = \frac{b-a}{2}\,dt$$

$$\int_a^b f(x)\,dx = \frac{b-a}{2}\int_{-1}^{1} f\!\left(\frac{(b-a)t+(a+b)}{2}\right)dt$$

---

## 7. Explicación de Métodos

### 7.1 Pseudocódigo: Simpson 1/3 Compuesto

```
Algoritmo Simpson13Compuesto:
  ENTRADA: f, a, b, n (par)
  SALIDA: aproximación de la integral

  SI n mod 2 ≠ 0:
    ERROR "n debe ser par"

  h ← (b - a) / n
  suma ← f(a) + f(b)

  PARA i = 1 HASTA n-1:
    x ← a + i * h
    SI i mod 2 = 0:
      suma ← suma + 2 * f(x)
    SINO:
      suma ← suma + 4 * f(x)

  RETORNAR (h/3) * suma
```

### 7.2 Pseudocódigo: Gauss-Legendre

```
Algoritmo GaussLegendre:
  ENTRADA: f, a, b, nodos t[], pesos w[]
  SALIDA: aproximación de la integral

  factor ← (b - a) / 2
  suma ← 0

  PARA i = 1 HASTA n:
    x_i ← ((b - a) * t[i] + (a + b)) / 2
    suma ← suma + w[i] * f(x_i)

  RETORNAR factor * suma
```

### 7.3 Implementación en Python

```python
import numpy as np
from scipy import integrate

def trapecio_compuesto(f, a, b, n):
    """Regla compuesta del trapecio"""
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = np.array([f(xi) for xi in x])
    return h * (y[0]/2 + np.sum(y[1:-1]) + y[-1]/2)

def simpson_compuesto(f, a, b, n):
    """Regla compuesta de Simpson 1/3 (n debe ser par)"""
    if n % 2 != 0:
        raise ValueError("n debe ser par")
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = np.array([f(xi) for xi in x])
    return h/3 * (y[0] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]) + y[-1])

def diferencia_central(f, x, h=1e-5):
    """Diferencia finita central para primera derivada"""
    return (f(x + h) - f(x - h)) / (2 * h)

def segunda_derivada_central(f, x, h=1e-5):
    """Diferencia finita central para segunda derivada"""
    return (f(x + h) - 2*f(x) + f(x - h)) / h**2


# Ejemplo: integrar f(x) = e^(-x²) de 0 a 1
f = lambda x: np.exp(-x**2)

resultado_trap = trapecio_compuesto(f, 0, 1, n=100)
resultado_simp = simpson_compuesto(f, 0, 1, n=100)
resultado_exact, _ = integrate.quad(f, 0, 1)

print(f"Trapecio (n=100):  {resultado_trap:.8f}")
print(f"Simpson (n=100):   {resultado_simp:.8f}")
print(f"Scipy (referencia): {resultado_exact:.8f}")

# Diferenciación numérica
g = lambda x: np.sin(x)
x0 = np.pi / 4
der_aprox = diferencia_central(g, x0)
der_exact = np.cos(x0)
print(f"\ng'(π/4) aprox: {der_aprox:.8f}")
print(f"g'(π/4) exacto: {der_exact:.8f}")
print(f"Error: {abs(der_aprox - der_exact):.2e}")
```

---

## 8. Ejemplos

### Ejemplo 1: Trapecio Simple

**Integrar:** $\int_0^1 e^x\,dx$

Con $h = 1$:
$$I \approx \frac{1}{2}[e^0 + e^1] = \frac{1}{2}[1 + 2.71828] = 1.85914$$

Valor exacto: $e^1 - e^0 = 1.71828$

Error: $|1.85914 - 1.71828| = 0.14086$ (8.2%)

---

### Ejemplo 2: Simpson 1/3 Compuesto

**Integrar:** $\int_0^1 e^x\,dx$ con $n = 4$, $h = 0.25$

| $i$ | $x_i$ | $f(x_i)$ | Peso |
|-----|--------|-----------|------|
| 0 | 0.00 | 1.00000 | 1 |
| 1 | 0.25 | 1.28403 | 4 |
| 2 | 0.50 | 1.64872 | 2 |
| 3 | 0.75 | 2.11700 | 4 |
| 4 | 1.00 | 2.71828 | 1 |

$$I \approx \frac{0.25}{3}[1.00000 + 4(1.28403) + 2(1.64872) + 4(2.11700) + 2.71828]$$
$$= \frac{0.25}{3}[20.60481] = 1.71707$$

Error: $|1.71828 - 1.71707| = 0.00121$ (0.07%) — ¡mucho más preciso que el trapecio!

---

### Ejemplo 3: Diferenciación Numérica

**Problema:** Calcular $f'(0.5)$ para $f(x) = \cos(x)$ con $h = 0.1$.

- Forward: $\dfrac{\cos(0.6) - \cos(0.5)}{0.1} = \dfrac{0.82534 - 0.87758}{0.1} = -0.52240$
- Central: $\dfrac{\cos(0.6) - \cos(0.4)}{0.2} = \dfrac{0.82534 - 0.92106}{0.2} = -0.47860$
- Exacto: $-\sin(0.5) = -0.47943$

Error forward: $0.85\%$ | Error central: $0.17\%$

---

### Ejemplo 4: Gauss-Legendre (n=2)

**Integrar:** $\int_0^1 x^3\,dx$

Nodos para $n=2$: $t_{1,2} = \pm \frac{1}{\sqrt{3}}$, pesos: $w_1 = w_2 = 1$

Cambio: $x = \frac{t+1}{2}$, $dx = \frac{1}{2}dt$

$$I \approx \frac{1}{2}\left[f\!\left(\frac{1-1/\sqrt{3}}{2}\right) + f\!\left(\frac{1+1/\sqrt{3}}{2}\right)\right] = \frac{1}{2}[0.04811 + 0.45189] = 0.25000$$

Valor exacto: $\frac{1}{4} = 0.25000$ ✅ — Exacto con solo 2 puntos.

---

## 9. Aplicaciones Reales

### 🚗 Velocidad y Aceleración desde Telemetría
Los datos GPS dan posición en tiempos discretos; la velocidad y aceleración se calculan con diferencias finitas.

### ⚡ Energía en Sistemas Eléctricos
$$W = \int_0^T P(t)\,dt$$
La potencia $P(t)$ se mide en instantes discretos; la energía se calcula con la regla del trapecio.

### 🌊 Volumen de Presas y Canales
$$V = \int_a^b A(x)\,dx$$
donde $A(x)$ es el área de la sección transversal. Se mide en puntos discretos y se integra numéricamente.

### 🔬 Espectroscopía
El análisis de espectros de absorción/emisión requiere integrar áreas bajo curvas espectrales con datos discretos.

### 📡 Procesamiento de Señales
El cálculo de la Transformada de Fourier discreta (FFT) involucra sumas que aproximan integrales.

---

## 10. Ventajas y Desventajas

### Comparativa de Métodos de Integración

| Método | Orden Error | Nodos equiespaciados | Exacto para polinomios de grado |
|--------|------------|---------------------|----------------------------------|
| Trapecio | $O(h^2)$ | Sí | ≤ 1 |
| Simpson 1/3 | $O(h^4)$ | Sí | ≤ 3 |
| Simpson 3/8 | $O(h^4)$ | Sí | ≤ 3 |
| Gauss-Legendre ($n$) | $O(h^{2n})$ | No | ≤ $2n-1$ |

### ✅ Ventajas

- Métodos de Newton-Cotes: simples de implementar con datos igualmente espaciados.
- Gauss-Legendre: muy alta precisión con pocos puntos.
- Diferencias centrales: precisión $O(h^2)$ con solo 2 evaluaciones.
- Aplicables a datos experimentales sin expresión analítica.

### ❌ Desventajas

- Las diferencias finitas son inestables para $h$ muy pequeño (error de redondeo dominante).
- Gauss-Legendre requiere evaluar la función en puntos no uniformes.
- La integración numérica acumula errores en integraciones repetidas (EDOs).
- Para funciones muy oscilantes, se necesitan muchos puntos.

---

## 11. Conclusión

La diferenciación e integración numérica son herramientas fundamentales que permiten analizar datos discretos y funciones complejas con la precisión requerida. La elección entre métodos como el trapecio, Simpson o Gauss-Legendre depende de la estructura de los datos, la regularidad de la función y la precisión necesaria.

La comprensión del error de truncamiento y su dependencia con $h$ permite al ingeniero ajustar el número de subintervalos para satisfacer las especificaciones de precisión. La diferenciación numérica, aunque simple conceptualmente, requiere cuidado especial con el tamaño del paso para evitar que el error de redondeo domine al error de truncamiento.

---

## 12. Bibliografía

Chapra, S. C., & Canale, R. P. (2015). *Métodos numéricos para ingenieros* (7.ª ed.). McGraw-Hill Education.

Burden, R. L., & Faires, J. D. (2011). *Numerical analysis* (9th ed.). Brooks/Cole, Cengage Learning.

Davis, P. J., & Rabinowitz, P. (1984). *Methods of numerical integration* (2nd ed.). Academic Press.

Stoer, J., & Bulirsch, R. (2002). *Introduction to numerical analysis* (3rd ed.). Springer.

Dahlquist, G., & Björck, Å. (2008). *Numerical methods in scientific computing* (Vol. 1). Society for Industrial and Applied Mathematics.

Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical recipes: The art of scientific computing* (3rd ed.). Cambridge University Press.

---

*📌 Documento generado para uso académico. Unidad 4 - Métodos Numéricos.*

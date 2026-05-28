# 📈 Unidad 5 - Interpolación y Ajuste de Funciones

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
  - [5.1 Polinomio de Interpolación de Newton](#51-polinomio-de-interpolación-de-newton)
  - [5.2 Polinomio de Interpolación de Lagrange](#52-polinomio-de-interpolación-de-lagrange)
  - [5.3 Interpolación Segmentada (Splines)](#53-interpolación-segmentada-splines)
  - [5.4 Regresión y Correlación](#54-regresión-y-correlación)
  - [5.5 Mínimos Cuadrados](#55-mínimos-cuadrados)
- [6. Fórmulas Matemáticas](#6-fórmulas-matemáticas)
- [7. Explicación de Métodos](#7-explicación-de-métodos)
- [8. Ejemplos](#8-ejemplos)
- [9. Aplicaciones Reales](#9-aplicaciones-reales)
- [10. Ventajas y Desventajas](#10-ventajas-y-desventajas)
- [11. Conclusión](#11-conclusión)
- [12. Bibliografía](#12-bibliografía)

---

## 1. Introducción

La interpolación y el ajuste de funciones son técnicas que permiten **estimar valores desconocidos** a partir de datos conocidos, o bien **simplificar funciones complejas** mediante expresiones polinomiales manejables.

La **interpolación** construye una función que **pasa exactamente** por todos los puntos dados. El **ajuste de funciones** (regresión) busca una función que **aproxime** los datos minimizando algún criterio de error, sin necesariamente pasar por todos los puntos.

Esta distinción es fundamental: la interpolación es apropiada cuando los datos son exactos (sin ruido), mientras que la regresión es preferible cuando los datos contienen errores de medición.

---

## 2. Objetivos

- 🎯 Construir e implementar el polinomio de Newton mediante diferencias divididas.
- 🎯 Formular el polinomio de Lagrange y aplicarlo en problemas de ingeniería.
- 🎯 Implementar splines lineales, cuadráticos y cúbicos para interpolación segmentada.
- 🎯 Aplicar el método de mínimos cuadrados para regresión lineal y no lineal.
- 🎯 Calcular e interpretar el coeficiente de correlación.
- 🎯 Seleccionar el método de interpolación o ajuste más adecuado según el problema.

---

## 3. Importancia del Tema

- **Tablas de datos experimentales:** valores de propiedades físicas (densidad, viscosidad, conductividad) a temperaturas medidas; la interpolación permite obtener valores intermedios.
- **Diseño asistido por computadora (CAD):** los splines cúbicos son la base de las curvas Bezier y NURBS para modelado 3D.
- **Pronóstico y predicción:** la regresión permite proyectar tendencias a partir de datos históricos.
- **Calibración de instrumentos:** el ajuste de mínimos cuadrados establece la relación entre señal medida y magnitud real.
- **Machine learning:** los fundamentos de la regresión lineal son la base de redes neuronales y modelos predictivos.

---

## 4. Conceptos Fundamentales

### Problema de Interpolación
Dados $n+1$ puntos $(x_0, y_0), (x_1, y_1), \ldots, (x_n, y_n)$ con $x_i$ distintos, encontrar un polinomio $P_n(x)$ de grado $\leq n$ tal que:
$$P_n(x_i) = y_i, \quad i = 0, 1, \ldots, n$$

### Unicidad del Polinomio Interpolador
**Teorema:** Dados $n+1$ puntos con abscisas distintas, existe un único polinomio de grado $\leq n$ que los interpola.

### Error de Interpolación
$$f(x) - P_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} \prod_{i=0}^{n}(x - x_i)$$

donde $\xi \in [\min(x_i), \max(x_i)]$.

### Fenómeno de Runge
Para $n$ grande con nodos equiespaciados, el polinomio interpolador puede **oscilar** violentamente en los extremos del intervalo, aunque la función sea suave. Esto motiva el uso de **nodos de Chebyshev** o **splines**.

---

## 5. Desarrollo Teórico

### 5.1 Polinomio de Interpolación de Newton

#### Diferencias Divididas
Las diferencias divididas de orden $k$ se definen recursivamente:
$$f[x_i] = f(x_i)$$
$$f[x_i, x_{i+1}] = \frac{f[x_{i+1}] - f[x_i]}{x_{i+1} - x_i}$$
$$f[x_i, x_{i+1}, \ldots, x_{i+k}] = \frac{f[x_{i+1}, \ldots, x_{i+k}] - f[x_i, \ldots, x_{i+k-1}]}{x_{i+k} - x_i}$$

#### Polinomio de Newton (Diferencias Divididas)
$$P_n(x) = f[x_0] + f[x_0,x_1](x-x_0) + f[x_0,x_1,x_2](x-x_0)(x-x_1) + \cdots$$

$$P_n(x) = \sum_{k=0}^{n} f[x_0, x_1, \ldots, x_k] \prod_{j=0}^{k-1}(x - x_j)$$

**Ventaja:** agregar un nuevo punto solo requiere calcular una nueva diferencia dividida.

#### Tabla de Diferencias Divididas

| $x_i$ | $f[x]$ | $f[,]$ | $f[,,]$ | $f[,,,]$ |
|--------|---------|---------|---------|----------|
| $x_0$ | $f[x_0]$ | | | |
| $x_1$ | $f[x_1]$ | $f[x_0,x_1]$ | | |
| $x_2$ | $f[x_2]$ | $f[x_1,x_2]$ | $f[x_0,x_1,x_2]$ | |
| $x_3$ | $f[x_3]$ | $f[x_2,x_3]$ | $f[x_1,x_2,x_3]$ | $f[x_0,x_1,x_2,x_3]$ |

---

### 5.2 Polinomio de Interpolación de Lagrange

$$P_n(x) = \sum_{i=0}^{n} y_i L_i(x)$$

donde los **polinomios base de Lagrange** son:
$$L_i(x) = \prod_{\substack{j=0 \\ j \neq i}}^{n} \frac{x - x_j}{x_i - x_j}$$

**Propiedades:**
- $L_i(x_i) = 1$
- $L_i(x_j) = 0$ para $j \neq i$
- $\sum_{i=0}^{n} L_i(x) = 1$ para todo $x$

**Ventaja:** no requiere construir tabla de diferencias divididas.  
**Desventaja:** al agregar un nuevo punto, hay que recalcular todos los $L_i$.

---

### 5.3 Interpolación Segmentada (Splines)

Para evitar el fenómeno de Runge, se divide el intervalo en subintervalos y se ajusta un polinomio de bajo grado en cada uno.

#### Spline Lineal
Conecta puntos consecutivos con segmentos de línea recta. Continuo pero no diferenciable.

#### Spline Cuadrático
Polinomio de grado 2 en cada subintervalo. Garantiza continuidad de $f$ y $f'$.

#### Spline Cúbico Natural
Es el más utilizado. En cada subintervalo $[x_i, x_{i+1}]$:
$$S_i(x) = a_i + b_i(x-x_i) + c_i(x-x_i)^2 + d_i(x-x_i)^3$$

**Condiciones:**
1. $S_i(x_i) = f(x_i)$ — interpola los datos
2. $S_i(x_{i+1}) = S_{i+1}(x_{i+1})$ — continuidad
3. $S_i'(x_{i+1}) = S_{i+1}'(x_{i+1})$ — primera derivada continua
4. $S_i''(x_{i+1}) = S_{i+1}''(x_{i+1})$ — segunda derivada continua
5. $S_0''(x_0) = S_{n-1}''(x_n) = 0$ — condición natural (extremos libres)

---

### 5.4 Regresión y Correlación

#### Diferencia con Interpolación

| Interpolación | Regresión |
|--------------|-----------|
| Pasa por todos los puntos | No necesariamente pasa por ningún punto |
| Datos exactos | Datos con ruido/error |
| $n+1$ puntos → grado $n$ | Muchos datos → modelo simple |

#### Coeficiente de Correlación de Pearson
$$r = \frac{n\sum x_i y_i - \sum x_i \sum y_i}{\sqrt{\left(n\sum x_i^2 - \left(\sum x_i\right)^2\right)\left(n\sum y_i^2 - \left(\sum y_i\right)^2\right)}}$$

- $r = 1$: correlación lineal perfecta positiva
- $r = -1$: correlación lineal perfecta negativa
- $r \approx 0$: sin correlación lineal

#### Coeficiente de Determinación
$$r^2 = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$$

Indica la fracción de la varianza total explicada por el modelo.

---

### 5.5 Mínimos Cuadrados

#### Regresión Lineal Simple
Se busca $\hat{y} = a_0 + a_1 x$ que minimice:
$$S_r = \sum_{i=1}^{n} (y_i - a_0 - a_1 x_i)^2$$

Las **ecuaciones normales** son:
$$a_1 = \frac{n\sum x_i y_i - \sum x_i \sum y_i}{n\sum x_i^2 - \left(\sum x_i\right)^2}$$
$$a_0 = \bar{y} - a_1 \bar{x}$$

#### Regresión Lineal Múltiple
$$\hat{y} = a_0 + a_1 x_1 + a_2 x_2 + \cdots + a_m x_m$$

En forma matricial:
$$[A]^T[A]\{a\} = [A]^T\{y\}$$

#### Regresión Polinomial
$$\hat{y} = a_0 + a_1 x + a_2 x^2 + \cdots + a_m x^m$$

Se reduce a mínimos cuadrados lineales con $x_j^k$ como variables.

---

## 6. Fórmulas Matemáticas

### Polinomio de Newton (forma compacta)
$$P_n(x) = \sum_{k=0}^{n} c_k \omega_k(x)$$

donde $c_k = f[x_0, x_1, \ldots, x_k]$ y $\omega_k(x) = \prod_{j=0}^{k-1}(x-x_j)$

### Error de Interpolación
$$R_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}(x-x_0)(x-x_1)\cdots(x-x_n)$$

### Regresión Lineal: Pendiente e Intercepto
$$a_1 = \frac{n\sum_{i=1}^n x_i y_i - \left(\sum_{i=1}^n x_i\right)\left(\sum_{i=1}^n y_i\right)}{n\sum_{i=1}^n x_i^2 - \left(\sum_{i=1}^n x_i\right)^2}$$

$$a_0 = \bar{y} - a_1\bar{x}$$

### Error Estándar de la Estimación
$$s_{y/x} = \sqrt{\frac{\sum(y_i - \hat{y}_i)^2}{n-2}} = \sqrt{\frac{S_r}{n-2}}$$

### Coeficiente de Determinación
$$r^2 = \frac{S_t - S_r}{S_t} = 1 - \frac{S_r}{S_t}$$

donde $S_t = \sum(y_i - \bar{y})^2$ es la varianza total.

---

## 7. Explicación de Métodos

### 7.1 Pseudocódigo: Diferencias Divididas de Newton

```
Algoritmo DiferenciasDivididasNewton:
  ENTRADA: x[0..n], y[0..n], xval (punto a evaluar)
  SALIDA: P_n(xval)

  // Construir tabla de diferencias divididas
  dd[i][0] ← y[i]  para i = 0, ..., n

  PARA j = 1 HASTA n:
    PARA i = 0 HASTA n-j:
      dd[i][j] ← (dd[i+1][j-1] - dd[i][j-1]) / (x[i+j] - x[i])

  // Evaluar polinomio (forma de Horner)
  P ← dd[0][0]
  prod ← 1
  PARA k = 1 HASTA n:
    prod ← prod * (xval - x[k-1])
    P ← P + dd[0][k] * prod

  RETORNAR P
```

### 7.2 Pseudocódigo: Mínimos Cuadrados Lineal

```
Algoritmo MinCuadrados:
  ENTRADA: x[1..n], y[1..n]
  SALIDA: a0, a1 (intercepto y pendiente)

  n ← longitud(x)
  sum_x ← suma de x[i]
  sum_y ← suma de y[i]
  sum_xy ← suma de x[i]*y[i]
  sum_x2 ← suma de x[i]²
  
  a1 ← (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x²)
  a0 ← (sum_y - a1*sum_x) / n

  RETORNAR a0, a1
```

### 7.3 Implementación en Python

```python
import numpy as np
import matplotlib.pyplot as plt

def diferencias_divididas(x, y):
    """Tabla de diferencias divididas para interpolación de Newton"""
    n = len(x)
    dd = np.zeros((n, n))
    dd[:, 0] = y
    
    for j in range(1, n):
        for i in range(n - j):
            dd[i, j] = (dd[i+1, j-1] - dd[i, j-1]) / (x[i+j] - x[i])
    
    return dd

def evaluar_newton(x, dd, xval):
    """Evalúa el polinomio de Newton en xval"""
    n = len(x)
    resultado = dd[0, 0]
    prod = 1.0
    for k in range(1, n):
        prod *= (xval - x[k-1])
        resultado += dd[0, k] * prod
    return resultado

def lagrange(x, y, xval):
    """Interpolación de Lagrange"""
    n = len(x)
    P = 0
    for i in range(n):
        L = 1
        for j in range(n):
            if j != i:
                L *= (xval - x[j]) / (x[i] - x[j])
        P += y[i] * L
    return P

def regresion_lineal(x, y):
    """Regresión lineal por mínimos cuadrados"""
    n = len(x)
    sx = np.sum(x)
    sy = np.sum(y)
    sxy = np.sum(x * y)
    sx2 = np.sum(x**2)
    sy2 = np.sum(y**2)
    
    a1 = (n * sxy - sx * sy) / (n * sx2 - sx**2)
    a0 = (sy - a1 * sx) / n
    
    y_pred = a0 + a1 * x
    St = np.sum((y - np.mean(y))**2)
    Sr = np.sum((y - y_pred)**2)
    r2 = 1 - Sr/St
    r = np.sign(a1) * np.sqrt(r2)
    
    return a0, a1, r, r2


# Ejemplo de uso
x_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y_data = np.array([2.5, 3.4, 4.0, 5.2, 6.1])

a0, a1, r, r2 = regresion_lineal(x_data, y_data)
print(f"Regresión lineal: y = {a0:.4f} + {a1:.4f}x")
print(f"r = {r:.4f},  r² = {r2:.4f}")
```

---

## 8. Ejemplos

### Ejemplo 1: Newton con Diferencias Divididas

**Datos:**

| $x$ | 0 | 1 | 2 | 4 |
|-----|---|---|---|---|
| $f(x)$ | 1 | 3 | 2 | 5 |

**Tabla de diferencias divididas:**

| $x_i$ | $f[x]$ | $f[,]$ | $f[,,]$ | $f[,,,]$ |
|--------|---------|---------|---------|----------|
| 0 | 1 | | | |
| 1 | 3 | $\frac{3-1}{1-0}=2$ | | |
| 2 | 2 | $\frac{2-3}{2-1}=-1$ | $\frac{-1-2}{2-0}=-1.5$ | |
| 4 | 5 | $\frac{5-2}{4-2}=1.5$ | $\frac{1.5-(-1)}{4-1}=0.833$ | $\frac{0.833-(-1.5)}{4-0}=0.583$ |

**Polinomio:**
$$P_3(x) = 1 + 2(x-0) - 1.5(x-0)(x-1) + 0.583(x-0)(x-1)(x-2)$$

**Evaluación en** $x = 3$:
$$P_3(3) = 1 + 2(3) - 1.5(3)(2) + 0.583(3)(2)(1) = 1 + 6 - 9 + 3.5 = 1.5$$

---

### Ejemplo 2: Regresión Lineal

**Datos de resistencia vs temperatura:**

| $T$ (°C) | 20 | 40 | 60 | 80 | 100 |
|----------|----|----|----|----|-----|
| $R$ (Ω) | 50.2 | 54.8 | 59.3 | 63.9 | 68.5 |

Calculando:
$$a_1 = \frac{5(16710) - 300(296.7)}{5(22000) - 300^2} = \frac{83550 - 89010}{110000 - 90000} = \frac{-5460}{20000}$$

Corrección: $a_1 \approx 0.4575$ (Ω/°C), $a_0 \approx 41.55$ Ω

$$r^2 \approx 0.9999 \quad \text{(ajuste casi perfecto)}$$

---

### Ejemplo 3: Spline Cúbico Natural

Para los puntos $(0,0), (1,0.5), (2,2), (3,1.5)$, el spline cúbico natural:
- Garantiza continuidad de $f$, $f'$ y $f''$
- Condición natural: $S''(0) = S''(3) = 0$
- Produce curvas suaves sin oscilaciones artificiales

---

## 9. Aplicaciones Reales

### 🏭 Propiedades Termodinámicas
Las tablas de vapor del agua son interpoladas para obtener entalpía, entropía y volumen específico a condiciones arbitrarias.

### 🎮 Animación y Diseño 3D
Los splines cúbicos (Bezier, B-spline, NURBS) son fundamentales en el modelado de superficies en software como AutoCAD, SolidWorks y herramientas de animación.

### 📊 Análisis de Regresión en Ciencia de Datos
La regresión lineal y polinomial es la base de modelos predictivos en economía, medicina y ciencias sociales.

### 🔭 Astronomía
La interpolación de tablas ephemerides permite calcular posiciones planetarias en cualquier instante a partir de datos calculados en fechas discretas.

### 🏥 Imágenes Médicas
La reconstrucción de imágenes de tomografía computarizada (CT) usa interpolación para generar imágenes continuas desde proyecciones discretas.

---

## 10. Ventajas y Desventajas

### Comparativa de Métodos

| Método | Ventajas | Desventajas |
|--------|----------|-------------|
| Newton | Actualizable, eficiente | Puede tener oscilaciones (Runge) |
| Lagrange | Sin tabla auxiliar | Recalcular todo al agregar punto |
| Spline cúbico | Suave, sin Runge | Sistema lineal a resolver |
| Mínimos cuadrados | Maneja ruido | No interpola exactamente |
| Regresión polinomial | Flexible | Sobreajuste para grado alto |

### ✅ Ventajas Generales

- Permiten **estimar valores** en puntos no medidos.
- Los splines evitan el fenómeno de Runge.
- Mínimos cuadrados es robusto ante **datos con ruido**.
- Son aplicables a datos experimentales reales.

### ❌ Desventajas Generales

- Poliniomios de alto grado: **fenómeno de Runge** e inestabilidad.
- Extrapolación: peligrosa, puede dar valores completamente erróneos.
- Regresión: elige un modelo a priori que puede ser incorrecto.
- Splines: requieren resolver un sistema lineal tridiagonal.

---

## 11. Conclusión

La interpolación y el ajuste de funciones ofrecen un poderoso arsenal de herramientas para trabajar con datos discretos. La elección entre Newton, Lagrange, splines o regresión depende de la naturaleza de los datos (exactos o ruidosos), el número de puntos y el uso previsto de la función aproximante.

Los splines cúbicos representan el estándar moderno para interpolación suave, mientras que los mínimos cuadrados son la base de toda la regresión estadística y el aprendizaje automático. La comprensión de los errores asociados —especialmente el fenómeno de Runge y el peligro de la extrapolación— es esencial para el uso responsable de estas técnicas.

---

## 12. Bibliografía

Chapra, S. C., & Canale, R. P. (2015). *Métodos numéricos para ingenieros* (7.ª ed.). McGraw-Hill Education.

Burden, R. L., & Faires, J. D. (2011). *Numerical analysis* (9th ed.). Brooks/Cole, Cengage Learning.

de Boor, C. (2001). *A practical guide to splines* (Rev. ed.). Springer.

Cheney, W., & Kincaid, D. (2012). *Numerical mathematics and computing* (7th ed.). Brooks/Cole.

Montgomery, D. C., Peck, E. A., & Vining, G. G. (2012). *Introduction to linear regression analysis* (5th ed.). Wiley.

Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical recipes: The art of scientific computing* (3rd ed.). Cambridge University Press.

---

*📌 Documento generado para uso académico. Unidad 5 - Métodos Numéricos.*

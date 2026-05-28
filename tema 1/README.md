# 📐 Unidad 1 - Introducción a los Métodos Numéricos

> **Asignatura:** Métodos Numéricos  
> **Nivel:** Ingeniería / Ciencias Exactas  
> **Modalidad:** Teórico-Práctica

---

## 📋 Índice

- [1. Introducción](#1-introducción)
- [2. Objetivos](#2-objetivos)
- [3. Importancia del Tema](#3-importancia-del-tema)
- [4. Conceptos Fundamentales](#4-conceptos-fundamentales)
  - [4.1 Importancia de los Métodos Numéricos](#41-importancia-de-los-métodos-numéricos)
  - [4.2 Cifra Significativa](#42-cifra-significativa)
  - [4.3 Precisión y Exactitud](#43-precisión-y-exactitud)
  - [4.4 Incertidumbre y Sesgo](#44-incertidumbre-y-sesgo)
  - [4.5 Tipos de Errores](#45-tipos-de-errores)
  - [4.6 Software de Cómputo Numérico](#46-software-de-cómputo-numérico)
  - [4.7 Métodos Iterativos](#47-métodos-iterativos)
- [5. Desarrollo Teórico](#5-desarrollo-teórico)
- [6. Fórmulas Matemáticas](#6-fórmulas-matemáticas)
- [7. Explicación de Métodos](#7-explicación-de-métodos)
- [8. Ejemplos](#8-ejemplos)
- [9. Aplicaciones Reales](#9-aplicaciones-reales)
- [10. Ventajas y Desventajas](#10-ventajas-y-desventajas)
- [11. Conclusión](#11-conclusión)
- [12. Bibliografía](#12-bibliografía)

---

## 1. Introducción

Los **métodos numéricos** constituyen una disciplina fundamental en la ingeniería y las ciencias aplicadas. Se definen como un conjunto de técnicas matemáticas que permiten formular y resolver problemas matemáticos de manera aproximada mediante operaciones aritméticas sobre computadoras digitales.

Muchos problemas del mundo real involucran ecuaciones que no tienen solución analítica exacta, o bien cuya solución exacta sería demasiado costosa computacionalmente. En estos casos, los métodos numéricos ofrecen herramientas sistemáticas para obtener soluciones aproximadas con un grado de error controlable y aceptable.

Esta unidad sienta las bases conceptuales necesarias para comprender, aplicar y evaluar cualquier método numérico: desde la representación de números en una computadora hasta la cuantificación y control del error que se introduce en cada etapa de un cálculo.

---

## 2. Objetivos

- 🎯 Comprender la naturaleza y el alcance de los métodos numéricos en la solución de problemas de ingeniería.
- 🎯 Identificar y diferenciar los tipos de errores que se presentan en el cómputo numérico.
- 🎯 Aplicar correctamente los conceptos de cifra significativa, precisión, exactitud, incertidumbre y sesgo.
- 🎯 Conocer el software especializado utilizado en el cómputo numérico.
- 🎯 Entender el principio de funcionamiento de los métodos iterativos y sus criterios de convergencia.
- 🎯 Desarrollar criterios para evaluar la calidad de una solución numérica.

---

## 3. Importancia del Tema

Los métodos numéricos son indispensables en prácticamente todas las ramas de la ciencia y la ingeniería modernas:

- **Ingeniería Civil:** análisis estructural, cálculo de deformaciones.
- **Ingeniería Eléctrica:** análisis de circuitos, procesamiento de señales.
- **Física Computacional:** simulación de fenómenos físicos complejos.
- **Economía y Finanzas:** modelos estocásticos, valoración de derivados.
- **Biología y Medicina:** modelado de poblaciones, imágenes médicas.

Sin una comprensión sólida de los errores y limitaciones del cómputo numérico, un ingeniero podría obtener resultados aparentemente correctos que en realidad son completamente erróneos, con consecuencias potencialmente graves en aplicaciones reales.

---

## 4. Conceptos Fundamentales

### 4.1 Importancia de los Métodos Numéricos

Los métodos numéricos se vuelven necesarios cuando:

1. **No existe solución analítica:** muchas ecuaciones diferenciales, integrales o sistemas no lineales no tienen forma cerrada.
2. **La solución analítica es demasiado compleja:** aunque existe, su evaluación directa es impráctica.
3. **Los datos son discretos:** en muchas aplicaciones de ingeniería los datos provienen de mediciones y no de funciones continuas.
4. **Se requiere rapidez:** los métodos numéricos pueden ser implementados en computadoras para dar respuestas en tiempo real.

---

### 4.2 Cifra Significativa

Una **cifra significativa** es todo dígito que aporte información real sobre la magnitud de un número. Las reglas para identificarlas son:

| Regla | Descripción | Ejemplo |
|-------|-------------|---------|
| Dígitos distintos de cero | Siempre son significativos | `1234` → 4 cifras |
| Ceros entre dígitos no nulos | Son significativos | `1002` → 4 cifras |
| Ceros a la izquierda | No son significativos | `0.0045` → 2 cifras |
| Ceros a la derecha (con punto decimal) | Son significativos | `2.500` → 4 cifras |
| Ceros a la derecha (sin punto decimal) | Ambiguos | `2500` → 2, 3 o 4 cifras |

---

### 4.3 Precisión y Exactitud

Estos dos conceptos suelen confundirse pero tienen significados distintos:

- **Exactitud (Accuracy):** se refiere a qué tan cerca está un valor medido o calculado del valor verdadero o aceptado.
- **Precisión (Precision):** se refiere a qué tan cercanos entre sí son varios valores repetidos del mismo experimento o cálculo, independientemente de si son correctos.

```
Diagrama conceptual:

  Poco exacto         Exacto              Exacto
  Poco preciso        Poco preciso        Muy preciso
  [disperso y        [disperso pero      [agrupado en
   alejado]           centrado]           el centro]
```

---

### 4.4 Incertidumbre y Sesgo

- **Incertidumbre:** rango dentro del cual se espera que se encuentre el valor verdadero de una magnitud. Puede ser aleatoria (ruido) o sistemática.
- **Sesgo (Bias):** error sistemático constante que desplaza todos los resultados en la misma dirección respecto al valor verdadero.

---

### 4.5 Tipos de Errores

Los errores en el cómputo numérico se clasifican en:

#### Error de Redondeo
Surge de la representación finita de números reales en una computadora. Todo número real que no sea exactamente representable en punto flotante genera un error de redondeo.

#### Error de Truncamiento
Surge de reemplazar un proceso matemático infinito (serie infinita, derivada, integral) por una aproximación finita.

#### Error Absoluto
$$E_a = |V_{\text{verdadero}} - V_{\text{aproximado}}|$$

#### Error Relativo
$$E_r = \frac{|V_{\text{verdadero}} - V_{\text{aproximado}}|}{|V_{\text{verdadero}}|}$$

#### Error Relativo Porcentual
$$E_r\% = \frac{|V_{\text{verdadero}} - V_{\text{aproximado}}|}{|V_{\text{verdadero}}|} \times 100\%$$

#### Error Aproximado (cuando no se conoce el valor verdadero)
$$\varepsilon_a = \left|\frac{x_{\text{nuevo}} - x_{\text{anterior}}}{x_{\text{nuevo}}}\right| \times 100\%$$

---

### 4.6 Software de Cómputo Numérico

| Software | Tipo | Uso principal |
|----------|------|---------------|
| **MATLAB** | Comercial | Álgebra lineal, simulación, gráficas |
| **Python (NumPy/SciPy)** | Libre | Cómputo científico general |
| **GNU Octave** | Libre | Compatible con MATLAB |
| **Mathematica** | Comercial | Álgebra simbólica y numérica |
| **Maple** | Comercial | Matemáticas simbólicas |
| **R** | Libre | Estadística y análisis de datos |
| **Julia** | Libre | Alto rendimiento numérico |

---

### 4.7 Métodos Iterativos

Un **método iterativo** es un procedimiento que, a partir de una aproximación inicial, genera una secuencia de valores que converge hacia la solución deseada.

**Estructura general:**
```
x_0 → x_1 → x_2 → ... → x_n ≈ solución
```

**Criterios de parada típicos:**
- Número máximo de iteraciones alcanzado.
- Error aproximado menor que una tolerancia: $\varepsilon_a < \varepsilon_s$
- Cambio relativo entre iteraciones suficientemente pequeño.

---

## 5. Desarrollo Teórico

### 5.1 Representación de Números en Computadora

Las computadoras digitales representan números reales en **punto flotante**, con la forma:

$$x = \pm 0.d_1 d_2 d_3 \ldots d_t \times \beta^n$$

donde:
- $\beta$ es la base (generalmente 2 para computadoras digitales)
- $d_i$ son los dígitos de la mantisa
- $t$ es la precisión (número de dígitos)
- $n$ es el exponente

#### Estándar IEEE 754

| Tipo | Bits totales | Exponente | Mantisa | Rango aproximado |
|------|-------------|-----------|---------|-----------------|
| Simple precisión | 32 | 8 bits | 23 bits | $\pm 3.4 \times 10^{38}$ |
| Doble precisión | 64 | 11 bits | 52 bits | $\pm 1.8 \times 10^{308}$ |

### 5.2 Propagación de Errores

Cuando se realizan operaciones aritméticas con números aproximados, los errores se propagan. Para una función $f(x_1, x_2, \ldots, x_n)$, el error total propagado se estima como:

$$\Delta f \approx \left|\frac{\partial f}{\partial x_1}\right| \Delta x_1 + \left|\frac{\partial f}{\partial x_2}\right| \Delta x_2 + \cdots + \left|\frac{\partial f}{\partial x_n}\right| \Delta x_n$$

### 5.3 Épsilon de la Máquina

El **épsilon de la máquina** ($\varepsilon_{\text{mach}}$) es el número positivo más pequeño tal que:

$$1 + \varepsilon_{\text{mach}} > 1$$

en la aritmética de punto flotante. Para doble precisión IEEE 754:

$$\varepsilon_{\text{mach}} \approx 2.22 \times 10^{-16}$$

### 5.4 Convergencia de Métodos Iterativos

Un método iterativo converge si la secuencia $\{x_n\}$ generada satisface:

$$\lim_{n \to \infty} x_n = x^*$$

donde $x^*$ es la solución exacta. La **tasa de convergencia** se mide por:

$$\lim_{n \to \infty} \frac{|e_{n+1}|}{|e_n|^p} = C$$

- Si $p = 1$: convergencia **lineal**
- Si $p = 2$: convergencia **cuadrática**
- Si $p > 2$: convergencia **superlineal**

---

## 6. Fórmulas Matemáticas

### Error Absoluto
$$E_{\text{abs}} = |V_T - V_A|$$

### Error Relativo Porcentual Verdadero
$$\varepsilon_t = \frac{|V_T - V_A|}{|V_T|} \times 100\%$$

### Criterio de Parada de Scarborough
$$\varepsilon_s = (0.5 \times 10^{2-n})\%$$

donde $n$ es el número de cifras significativas deseadas.

### Error de Truncamiento en Series de Taylor
La serie de Taylor de $f(x)$ alrededor de $x_i$:

$$f(x_{i+1}) = f(x_i) + f'(x_i)h + \frac{f''(x_i)}{2!}h^2 + \frac{f'''(x_i)}{3!}h^3 + \cdots + R_n$$

El error de truncamiento al orden $n$ es:

$$R_n = \frac{f^{(n+1)}(\xi)}{(n+1)!} h^{n+1}, \quad \xi \in (x_i, x_{i+1})$$

### Representación de Punto Flotante Normalizada
$$\text{fl}(x) = \pm 0.d_1 d_2 \cdots d_t \times \beta^n$$

### Error Relativo de Redondeo
$$|\text{fl}(x) - x| \leq \frac{1}{2} \beta^{1-t}$$

---

## 7. Explicación de Métodos

### 7.1 Aritmética de Punto Flotante

Las operaciones básicas en punto flotante pueden introducir errores debido a:

1. **Cancelación catastrófica:** resta de números casi iguales que produce pérdida masiva de cifras significativas.
2. **Desbordamiento (overflow):** resultado mayor que el número más grande representable.
3. **Subdesbordamiento (underflow):** resultado menor que el número positivo más pequeño representable.

### 7.2 Método Iterativo General

**Pseudocódigo:**
```
Algoritmo IteraciónGeneral:
  ENTRADA: x0 (aproximación inicial), tol (tolerancia), maxIter
  
  x_ant ← x0
  PARA i = 1 HASTA maxIter:
    x_nuevo ← g(x_ant)           // función de iteración
    ea ← |x_nuevo - x_ant| / |x_nuevo| × 100
    SI ea < tol:
      RETORNAR x_nuevo            // convergencia lograda
    x_ant ← x_nuevo
  
  RETORNAR "No convergió en maxIter iteraciones"
```

### 7.3 Evaluación de Errores Paso a Paso

```python
# Ejemplo en Python: estimación del error en series de Taylor
import math

def sin_taylor(x, n_terms):
    """Aproximación de sin(x) usando n_terms términos de Taylor"""
    resultado = 0
    for n in range(n_terms):
        coef = (-1)**n
        potencia = x**(2*n + 1)
        factorial = math.factorial(2*n + 1)
        resultado += coef * potencia / factorial
    return resultado

x = math.pi / 4  # 45 grados
verdadero = math.sin(x)

for n in range(1, 6):
    aprox = sin_taylor(x, n)
    error_abs = abs(verdadero - aprox)
    error_rel = error_abs / abs(verdadero) * 100
    print(f"n={n}: aprox={aprox:.8f}, error_rel={error_rel:.6f}%")
```

---

## 8. Ejemplos

### Ejemplo 1: Cálculo de Cifras Significativas

**Problema:** Determine el número de cifras significativas en los siguientes números:
- `0.003470` → **4 cifras** (3, 4, 7, 0 final después del punto)
- `14000` → **2 cifras** (ambiguo sin notación científica)
- `1.4000 × 10⁴` → **5 cifras** (todos los dígitos son significativos)

---

### Ejemplo 2: Error en Serie de Taylor

**Problema:** Aproxime $e^{0.5}$ usando los primeros 4 términos de la serie de Taylor y calcule el error.

La serie de Taylor de $e^x$ alrededor de $x = 0$:
$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$$

Para $x = 0.5$:

$$e^{0.5} \approx 1 + 0.5 + \frac{(0.5)^2}{2} + \frac{(0.5)^3}{6} = 1 + 0.5 + 0.125 + 0.020833 = 1.645833$$

Valor verdadero: $e^{0.5} = 1.648721...$

$$E_{\text{abs}} = |1.648721 - 1.645833| = 0.002888$$

$$E_r\% = \frac{0.002888}{1.648721} \times 100\% = 0.1752\%$$

---

### Ejemplo 3: Cancelación Catastrófica

**Problema:** Evalúe la expresión $f(x) = \sqrt{x+1} - \sqrt{x}$ para $x = 10000$.

```
√10001 = 100.00499987...
√10000 = 100.00000000

f(10000) = 100.00499987 - 100.00000000 = 0.00499987

Forma alternativa estable:
f(x) = 1 / (√(x+1) + √x)
f(10000) = 1 / (200.00499987) = 0.00499987...
```

La segunda forma evita la cancelación catastrófica.

---

### Ejemplo 4: Criterio de Parada

**Problema:** Se desea calcular $\sqrt{2}$ con 4 cifras significativas. El criterio de Scarborough indica:

$$\varepsilon_s = (0.5 \times 10^{2-4})\% = 0.005\%$$

Se detiene la iteración cuando $\varepsilon_a < 0.005\%$.

---

## 9. Aplicaciones Reales

### 🏗️ Ingeniería Estructural
El análisis de esfuerzos y deformaciones en estructuras requiere resolver grandes sistemas de ecuaciones, donde el control de errores numéricos es crítico para la seguridad.

### 🚀 Ingeniería Aeroespacial
Las simulaciones de dinámica de fluidos computacional (CFD) para diseño de aeronaves dependen enteramente de métodos numéricos con control riguroso del error.

### 💊 Farmacología Computacional
El modelado de la cinética de fármacos en el organismo utiliza ecuaciones diferenciales resueltas numéricamente para predecir concentraciones en el tiempo.

### 🌍 Modelado Climático
Los modelos de predicción meteorológica y climática son sistemas enormes de ecuaciones diferenciales parciales, cuya solución numérica requiere supercómputo y control estricto del error.

### 📡 Procesamiento de Señales
La Transformada Rápida de Fourier (FFT) es un algoritmo numérico que permite procesar señales digitales en tiempo real.

---

## 10. Ventajas y Desventajas

### ✅ Ventajas

| Ventaja | Descripción |
|---------|-------------|
| **Aplicabilidad general** | Pueden aplicarse donde los métodos analíticos fallan |
| **Implementación computacional** | Son directamente programables y automatizables |
| **Control del error** | El error puede estimarse y controlarse dentro de límites aceptables |
| **Flexibilidad** | Pueden manejar datos discretos y funciones complejas |
| **Escalabilidad** | Funcionan para problemas de cualquier dimensión |

### ❌ Desventajas

| Desventaja | Descripción |
|------------|-------------|
| **Solución aproximada** | Nunca entregan la solución exacta |
| **Propagación de errores** | Los errores pueden acumularse en cálculos largos |
| **Dependencia de la aproximación inicial** | Muchos métodos divergen con mal punto de partida |
| **Costo computacional** | Algunos métodos requieren muchas iteraciones |
| **No garantizan convergencia** | En ciertos casos el método puede no converger |

---

## 11. Conclusión

Los métodos numéricos representan el puente indispensable entre la matemática teórica y la ingeniería práctica. Esta unidad establece los cimientos conceptuales y terminológicos necesarios para abordar con rigor cualquier técnica de cómputo numérico.

La comprensión profunda de los tipos de error, sus fuentes y sus mecanismos de propagación permite al ingeniero no solo obtener soluciones aproximadas, sino evaluar críticamente su calidad y confiabilidad. El dominio de herramientas como MATLAB, Python científico o Julia amplía enormemente la capacidad de resolución de problemas reales.

Los métodos iterativos, en particular, son la base de la mayoría de algoritmos numéricos modernos, y su comprensión es prerequisito para cualquier tema subsecuente en la asignatura.

---

## 12. Bibliografía

Chapra, S. C., & Canale, R. P. (2015). *Métodos numéricos para ingenieros* (7.ª ed.). McGraw-Hill Education.

Burden, R. L., & Faires, J. D. (2011). *Numerical analysis* (9th ed.). Brooks/Cole, Cengage Learning.

Kincaid, D., & Cheney, W. (2002). *Numerical analysis: Mathematics of scientific computing* (3rd ed.). American Mathematical Society.

Quarteroni, A., Saleri, F., & Gervasio, P. (2014). *Scientific computing with MATLAB and Octave* (4th ed.). Springer.

Stoer, J., & Bulirsch, R. (2002). *Introduction to numerical analysis* (3rd ed.). Springer.

IEEE Standard for Floating-Point Arithmetic. (2019). *IEEE Std 754-2019*. Institute of Electrical and Electronics Engineers.

---

*📌 Documento generado para uso académico. Unidad 1 - Métodos Numéricos.*

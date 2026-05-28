# 🔄 Unidad 6 - Solución de Ecuaciones Diferenciales

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
  - [5.1 Métodos de Un Paso](#51-métodos-de-un-paso)
  - [5.2 Métodos de Pasos Múltiples](#52-métodos-de-pasos-múltiples)
  - [5.3 Sistemas de EDOs](#53-sistemas-de-edos)
- [6. Fórmulas Matemáticas](#6-fórmulas-matemáticas)
- [7. Explicación de Métodos](#7-explicación-de-métodos)
- [8. Ejemplos](#8-ejemplos)
- [9. Aplicaciones Reales](#9-aplicaciones-reales)
- [10. Ventajas y Desventajas](#10-ventajas-y-desventajas)
- [11. Conclusión](#11-conclusión)
- [12. Bibliografía](#12-bibliografía)

---

## 1. Introducción

Las **ecuaciones diferenciales ordinarias (EDOs)** describen cómo cambian las magnitudes a lo largo del tiempo o del espacio, y son el lenguaje fundamental de la física, la ingeniería y las ciencias naturales. Desde la trayectoria de un proyectil hasta el comportamiento de circuitos eléctricos, desde la cinética química hasta la dinámica de poblaciones, casi todo fenómeno dinámico se modela mediante EDOs.

El problema de **valor inicial** (PVI) consiste en encontrar $y(t)$ tal que:
$$y' = f(t, y), \quad y(t_0) = y_0$$

Para la gran mayoría de EDOs de interés práctico, no existe solución analítica en forma cerrada. Los métodos numéricos para EDOs permiten obtener aproximaciones precisas y controladas de las soluciones.

Esta unidad cubre los métodos fundamentales: métodos de **un paso** (Euler, Runge-Kutta), métodos de **pasos múltiples** (Adams-Bashforth, Adams-Moulton, predictor-corrector) y la solución de **sistemas de EDOs**.

---

## 2. Objetivos

- 🎯 Aplicar el método de Euler explícito e implícito a problemas de valor inicial.
- 🎯 Implementar y comprender los métodos de Runge-Kutta de orden 2, 3 y 4.
- 🎯 Analizar el error local y global de los métodos de un paso.
- 🎯 Aplicar métodos de pasos múltiples: Adams-Bashforth y Adams-Moulton.
- 🎯 Construir esquemas predictor-corrector y analizar su estabilidad.
- 🎯 Resolver sistemas de EDOs de primer orden y ecuaciones de orden superior.
- 🎯 Aplicar estos métodos a problemas de ingeniería (circuitos, mecánica, transferencia de calor).

---

## 3. Importancia del Tema

Las EDOs son el modelo matemático de prácticamente todo proceso dinámico:

| Campo | Fenómeno | Ecuación diferencial |
|-------|----------|---------------------|
| Mecánica | Segunda ley de Newton | $m\ddot{x} = F(t, x, \dot{x})$ |
| Eléctrica | Circuito RC | $RC\,\dot{V} + V = V_s(t)$ |
| Transferencia de calor | Enfriamiento de Newton | $\dot{T} = -k(T - T_\infty)$ |
| Química | Cinética de reacción | $\dot{C} = -kC^n$ |
| Ecología | Predador-presa | Sistema de Lotka-Volterra |
| Epidemiología | Modelo SIR | Sistema de 3 EDOs acopladas |

---

## 4. Conceptos Fundamentales

### Problema de Valor Inicial (PVI)
$$\frac{dy}{dt} = f(t, y), \quad y(t_0) = y_0, \quad t \in [t_0, t_f]$$

### Discretización
Se divide el intervalo $[t_0, t_f]$ en $N$ subintervalos de tamaño $h$:
$$t_n = t_0 + nh, \quad n = 0, 1, \ldots, N$$

y se calcula $y_n \approx y(t_n)$.

### Error Local de Truncamiento
$$\tau_n = \frac{y(t_{n+1}) - y(t_n)}{h} - \Phi(t_n, y_n, h)$$

donde $\Phi$ es la función de incremento del método.

### Orden de un Método
El método tiene orden $p$ si:
$$\tau_n = O(h^p)$$

### Estabilidad de un Método
Para la ecuación prueba $y' = \lambda y$ (con $\text{Re}(\lambda) < 0$), el método es **A-estable** si converge para todo $h$ positivo.

### Error Global
El error global es $e_n = y(t_n) - y_n$. Para un método de orden $p$:
$$\max_n |e_n| = O(h^p)$$

---

## 5. Desarrollo Teórico

### 5.1 Métodos de Un Paso

#### Método de Euler Explícito (orden 1)
$$y_{n+1} = y_n + h f(t_n, y_n)$$

Intuitivamente: avanza desde $(t_n, y_n)$ en la dirección de la tangente.

**Error local:** $O(h^2)$  
**Error global:** $O(h)$

#### Método de Euler Implícito (orden 1)
$$y_{n+1} = y_n + h f(t_{n+1}, y_{n+1})$$

Requiere resolver una ecuación (posiblemente no lineal) en cada paso. Es **incondicionalmente estable** (A-estable).

#### Método de Euler Modificado (Heun, orden 2)

**Predictor:**
$$\tilde{y}_{n+1} = y_n + h f(t_n, y_n)$$

**Corrector:**
$$y_{n+1} = y_n + \frac{h}{2}\left[f(t_n, y_n) + f(t_{n+1}, \tilde{y}_{n+1})\right]$$

**Error global:** $O(h^2)$

#### Método del Punto Medio (orden 2)
$$k_1 = h f(t_n, y_n)$$
$$y_{n+1} = y_n + h f\!\left(t_n + \frac{h}{2},\ y_n + \frac{k_1}{2}\right)$$

#### Runge-Kutta de Orden 4 (RK4)

El método más utilizado en la práctica:
$$k_1 = h\, f(t_n,\, y_n)$$
$$k_2 = h\, f\!\left(t_n + \tfrac{h}{2},\, y_n + \tfrac{k_1}{2}\right)$$
$$k_3 = h\, f\!\left(t_n + \tfrac{h}{2},\, y_n + \tfrac{k_2}{2}\right)$$
$$k_4 = h\, f(t_n + h,\, y_n + k_3)$$

$$y_{n+1} = y_n + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

**Error global:** $O(h^4)$  
**Evaluaciones de $f$ por paso:** 4

---

### 5.2 Métodos de Pasos Múltiples

Los métodos de pasos múltiples usan información de **varios pasos previos** para calcular el siguiente, lo que los hace más eficientes (menos evaluaciones de $f$) pero requieren métodos de inicio (normalmente RK4 para los primeros pasos).

#### Métodos de Adams-Bashforth (explícitos)

**Orden 2 (2 pasos):**
$$y_{n+1} = y_n + \frac{h}{2}[3f_n - f_{n-1}]$$

**Orden 3 (3 pasos):**
$$y_{n+1} = y_n + \frac{h}{12}[23f_n - 16f_{n-1} + 5f_{n-2}]$$

**Orden 4 (4 pasos):**
$$y_{n+1} = y_n + \frac{h}{24}[55f_n - 59f_{n-1} + 37f_{n-2} - 9f_{n-3}]$$

donde $f_k = f(t_k, y_k)$.

#### Métodos de Adams-Moulton (implícitos)

**Orden 3 (2 pasos, implícito):**
$$y_{n+1} = y_n + \frac{h}{12}[5f_{n+1} + 8f_n - f_{n-1}]$$

**Orden 4 (3 pasos, implícito):**
$$y_{n+1} = y_n + \frac{h}{24}[9f_{n+1} + 19f_n - 5f_{n-1} + f_{n-2}]$$

Son más estables que los explícitos pero requieren resolver una ecuación en cada paso.

#### Esquemas Predictor-Corrector (PECE)

Combinan un método explícito como predictor y uno implícito como corrector:
1. **Predecir:** $\tilde{y}_{n+1}$ con Adams-Bashforth orden 4
2. **Evaluar:** $\tilde{f}_{n+1} = f(t_{n+1}, \tilde{y}_{n+1})$
3. **Corregir:** $y_{n+1}$ con Adams-Moulton orden 4
4. **Evaluar:** $f_{n+1} = f(t_{n+1}, y_{n+1})$

El **estimador de error** del predictor-corrector permite **control adaptivo del paso**.

---

### 5.3 Sistemas de EDOs

Un sistema de $m$ EDOs de primer orden:
$$\frac{d\mathbf{y}}{dt} = \mathbf{f}(t, \mathbf{y}), \quad \mathbf{y}(t_0) = \mathbf{y}_0$$

donde $\mathbf{y} = (y_1, y_2, \ldots, y_m)^T$ y $\mathbf{f} = (f_1, f_2, \ldots, f_m)^T$.

**RK4 vectorial:**
$$\mathbf{k}_1 = h\,\mathbf{f}(t_n, \mathbf{y}_n)$$
$$\mathbf{k}_2 = h\,\mathbf{f}\!\left(t_n+\tfrac{h}{2}, \mathbf{y}_n+\tfrac{\mathbf{k}_1}{2}\right)$$
$$\mathbf{k}_3 = h\,\mathbf{f}\!\left(t_n+\tfrac{h}{2}, \mathbf{y}_n+\tfrac{\mathbf{k}_2}{2}\right)$$
$$\mathbf{k}_4 = h\,\mathbf{f}(t_n+h, \mathbf{y}_n+\mathbf{k}_3)$$
$$\mathbf{y}_{n+1} = \mathbf{y}_n + \tfrac{1}{6}(\mathbf{k}_1+2\mathbf{k}_2+2\mathbf{k}_3+\mathbf{k}_4)$$

#### Reducción de Orden Superior
Una EDO de orden $n$ se convierte en un sistema de $n$ EDOs de primer orden:
$$y^{(n)} = f(t, y, y', \ldots, y^{(n-1)})$$

Definiendo $y_1 = y$, $y_2 = y'$, ..., $y_n = y^{(n-1)}$:
$$\begin{cases} y_1' = y_2 \\ y_2' = y_3 \\ \vdots \\ y_n' = f(t, y_1, y_2, \ldots, y_n) \end{cases}$$

---

## 6. Fórmulas Matemáticas

### Método de Euler
$$y_{n+1} = y_n + hf(t_n, y_n)$$

### RK4 (fórmula compacta)
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

### Error Local de Truncamiento (Euler)
$$\tau_n = \frac{h}{2} y''(\xi_n) = O(h)$$

### Error Local de Truncamiento (RK4)
$$\tau_n = O(h^4)$$

### Adams-Bashforth Orden 4
$$y_{n+1} = y_n + \frac{h}{24}(55f_n - 59f_{n-1} + 37f_{n-2} - 9f_{n-3})$$

### Adams-Moulton Orden 4
$$y_{n+1} = y_n + \frac{h}{24}(9f_{n+1} + 19f_n - 5f_{n-1} + f_{n-2})$$

### Estimador de Error Predictor-Corrector
$$e_{n+1} \approx \frac{y_{n+1}^{(c)} - y_{n+1}^{(p)}}{14}$$

### Ecuación Prueba de Estabilidad
$$y' = \lambda y, \quad y(0) = 1 \implies y(t) = e^{\lambda t}$$

Para Euler explícito: $y_{n+1} = (1 + h\lambda)y_n$  
Región de estabilidad: $|1 + h\lambda| \leq 1$

---

## 7. Explicación de Métodos

### 7.1 Pseudocódigo: RK4

```
Algoritmo RungeKutta4:
  ENTRADA: f, t0, tf, y0, h
  SALIDA: arreglos t[], y[]

  t ← t0
  y ← y0
  n ← (tf - t0) / h

  PARA i = 1 HASTA n:
    k1 ← h * f(t, y)
    k2 ← h * f(t + h/2, y + k1/2)
    k3 ← h * f(t + h/2, y + k2/2)
    k4 ← h * f(t + h, y + k3)

    y ← y + (k1 + 2*k2 + 2*k3 + k4) / 6
    t ← t + h

    GUARDAR (t, y)
```

### 7.2 Pseudocódigo: Adams-Bashforth-Moulton (PC de orden 4)

```
Algoritmo AdamsBashforthMoulton4:
  ENTRADA: f, t0, tf, y0, h
  
  // Inicio con RK4 (se necesitan y0, y1, y2, y3)
  Calcular y1, y2, y3 usando RK4
  
  PARA n = 3 HASTA N-1:
    // Predictor (Adams-Bashforth orden 4)
    yp ← y[n] + h/24 * (55*f[n] - 59*f[n-1] + 37*f[n-2] - 9*f[n-3])
    fp ← f(t[n+1], yp)
    
    // Corrector (Adams-Moulton orden 4)
    y[n+1] ← y[n] + h/24 * (9*fp + 19*f[n] - 5*f[n-1] + f[n-2])
    f[n+1] ← f(t[n+1], y[n+1])
    
    // Error estimado
    error ← |y[n+1] - yp| / 14
```

### 7.3 Implementación en Python

```python
import numpy as np
import matplotlib.pyplot as plt

def euler(f, t0, tf, y0, h):
    """Método de Euler explícito"""
    t = np.arange(t0, tf + h, h)
    y = np.zeros(len(t))
    y[0] = y0
    for i in range(len(t) - 1):
        y[i+1] = y[i] + h * f(t[i], y[i])
    return t, y

def rk4(f, t0, tf, y0, h):
    """Método de Runge-Kutta de orden 4"""
    t = np.arange(t0, tf + h, h)
    y = np.zeros(len(t))
    y[0] = y0
    for i in range(len(t) - 1):
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h/2, y[i] + k1/2)
        k3 = h * f(t[i] + h/2, y[i] + k2/2)
        k4 = h * f(t[i] + h, y[i] + k3)
        y[i+1] = y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6
    return t, y

def rk4_sistema(F, t0, tf, Y0, h):
    """RK4 para sistemas de EDOs. F retorna vector."""
    t = np.arange(t0, tf + h, h)
    Y = np.zeros((len(t), len(Y0)))
    Y[0] = Y0
    for i in range(len(t) - 1):
        k1 = h * np.array(F(t[i], Y[i]))
        k2 = h * np.array(F(t[i]+h/2, Y[i]+k1/2))
        k3 = h * np.array(F(t[i]+h/2, Y[i]+k2/2))
        k4 = h * np.array(F(t[i]+h, Y[i]+k3))
        Y[i+1] = Y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6
    return t, Y


# ===== Ejemplo 1: Enfriamiento de Newton =====
# dT/dt = -k(T - T_inf),  T(0) = 80°C, T_inf = 20°C, k = 0.1
k = 0.1; T_inf = 20
f_enfriamiento = lambda t, T: -k * (T - T_inf)
t_exact = np.linspace(0, 30, 300)
T_exact = 20 + 60 * np.exp(-k * t_exact)

t_euler, T_euler = euler(f_enfriamiento, 0, 30, 80, h=2)
t_rk4,   T_rk4   = rk4(f_enfriamiento, 0, 30, 80, h=2)

print("t=30: Exacto={:.4f}, Euler={:.4f}, RK4={:.4f}".format(
    20 + 60*np.exp(-k*30), T_euler[-1], T_rk4[-1]))


# ===== Ejemplo 2: Péndulo (sistema de 2 EDOs) =====
# θ'' + (g/L)sin(θ) = 0  =>  y1'=y2,  y2'=-(g/L)*sin(y1)
g = 9.81; L = 1.0
def pendulo(t, Y):
    theta, omega = Y
    return [omega, -(g/L) * np.sin(theta)]

t_pend, Y_pend = rk4_sistema(pendulo, 0, 10, [0.5, 0], h=0.01)
theta = Y_pend[:, 0]
print(f"\nPéndulo: θ_max = {np.max(theta):.4f} rad")
```

---

## 8. Ejemplos

### Ejemplo 1: Euler vs RK4

**Problema:** Resolver $y' = -2y$, $y(0) = 1$, en $[0, 2]$ con $h = 0.5$.

**Solución exacta:** $y(t) = e^{-2t}$

**Método de Euler** ($h = 0.5$):

| $t$ | $y_n$ (Euler) | $y(t)$ exacto | Error |
|-----|---------------|---------------|-------|
| 0.0 | 1.0000 | 1.0000 | 0.0000 |
| 0.5 | 0.0000 | 0.3679 | 0.3679 |
| 1.0 | 0.0000 | 0.1353 | 0.1353 |

*$h = 0.5$ es demasiado grande para Euler con esta ecuación (región de estabilidad: $|1-2h| \leq 1 \Rightarrow h \leq 1$, pero converge lentamente)*

**RK4** ($h = 0.5$):

| $t$ | $y_n$ (RK4) | $y(t)$ exacto | Error |
|-----|-------------|---------------|-------|
| 0.0 | 1.000000 | 1.000000 | 0.000000 |
| 0.5 | 0.367879 | 0.367879 | $< 10^{-6}$ |
| 1.0 | 0.135335 | 0.135335 | $< 10^{-6}$ |

RK4 es casi exacto incluso con $h = 0.5$.

---

### Ejemplo 2: Circuito RC

**Modelo:** $R\,\frac{dq}{dt} + \frac{q}{C} = V_0$

Con $R = 1000\,\Omega$, $C = 10^{-6}\,\text{F}$, $V_0 = 12\,\text{V}$, $q(0) = 0$:

$$\frac{dq}{dt} = \frac{V_0 - q/C}{R} = \frac{12 - 10^6 q}{1000}$$

Usando RK4 con $h = 0.0001$ s, la carga converge a $q_\infty = CV_0 = 1.2 \times 10^{-5}\,\text{C}$ en $\approx 5\tau$ donde $\tau = RC = 10^{-3}$ s.

---

### Ejemplo 3: Sistema Predador-Presa (Lotka-Volterra)

$$\begin{cases} \dot{x} = \alpha x - \beta xy \\ \dot{y} = -\gamma y + \delta xy \end{cases}$$

Con $\alpha = 1.5$, $\beta = 1$, $\gamma = 3$, $\delta = 1$, CI: $x(0) = 10$, $y(0) = 5$.

Usando RK4 con $h = 0.01$, se obtienen oscilaciones periódicas en ambas poblaciones, características del modelo.

---

### Ejemplo 4: Péndulo No Lineal

$$\theta'' + \frac{g}{L}\sin\theta = 0$$

Reducción de orden: $y_1 = \theta$, $y_2 = \dot\theta$

$$\begin{cases} y_1' = y_2 \\ y_2' = -\frac{g}{L}\sin(y_1) \end{cases}$$

Para $\theta_0 = 0.5\,\text{rad}$, $\dot\theta_0 = 0$, RK4 con $h = 0.01$ produce trayectorias que muestran la diferencia entre el péndulo lineal ($T = 2\pi\sqrt{L/g}$) y el no lineal.

---

## 9. Aplicaciones Reales

### ⚙️ Dinámica Orbital
Las ecuaciones de movimiento de satélites y planetas son sistemas de EDOs. La misión Apolo y las sondas espaciales actuales usan integradores de orden alto con control de paso adaptivo.

### 🔌 Circuitos Electrónicos
La simulación SPICE para circuitos analógicos y digitales resuelve sistemas grandes de EDOs/DAEs usando métodos implícitos.

### 🌡️ Transferencia de Calor Transitoria
El calentamiento o enfriamiento de componentes en procesadores, turbinas o dispositivos médicos se simula resolviendo EDOs de conducción.

### 🦠 Epidemiología
El modelo SIR (Susceptibles-Infectados-Recuperados) es un sistema de 3 EDOs usado para predecir la propagación de enfermedades.

### 🤖 Robótica
La dinámica de brazos robóticos está descrita por sistemas de EDOs no lineales que se resuelven en tiempo real con RK4 o métodos de paso adaptivo.

---

## 10. Ventajas y Desventajas

### Comparativa de Métodos

| Método | Orden | Eval. $f$ por paso | Autoarranque | Estabilidad |
|--------|-------|-------------------|--------------|-------------|
| Euler explícito | 1 | 1 | Sí | Condicional |
| Euler implícito | 1 | 1 (+ iter.) | Sí | Incondicional |
| Heun (RK2) | 2 | 2 | Sí | Condicional |
| RK4 | 4 | 4 | Sí | Condicional |
| AB orden 4 | 4 | 1 | No (usa RK4) | Condicional |
| AM orden 4 | 4 | 1 (+ iter.) | No | Mejor |
| PC-AB/AM 4 | 4 | 2 | No | Condicional |

### ✅ Ventajas

- RK4 ofrece excelente precisión con implementación sencilla.
- Los métodos de pasos múltiples son más eficientes para alta precisión.
- Los métodos implícitos son esenciales para **ecuaciones rígidas (stiff)**.
- El control adaptivo del paso optimiza automáticamente el costo computacional.

### ❌ Desventajas

- Euler tiene orden bajo y puede inestabilizarse con pasos grandes.
- RK4 requiere 4 evaluaciones de $f$ por paso.
- Los métodos multipaso necesitan **procedimiento de inicio** (arranque).
- Las ecuaciones rígidas requieren métodos especializados (BDF, Rosenbrock).
- La precisión depende críticamente de la elección del paso $h$.

---

## 11. Conclusión

Los métodos numéricos para ecuaciones diferenciales ordinarias son herramientas indispensables en la ingeniería y las ciencias. El método de Runge-Kutta de orden 4 representa el estándar de facto para muchas aplicaciones por su excelente balance entre precisión y costo computacional.

Los métodos de pasos múltiples (Adams-Bashforth-Moulton) son más eficientes para problemas que requieren alta precisión a lo largo de intervalos largos. Para ecuaciones rígidas —comunes en circuitos eléctricos, reacciones químicas rápidas y mecánica estructural— los métodos implícitos son esenciales para mantener la estabilidad.

La capacidad de reducir cualquier EDO de orden superior a un sistema de primer orden hace que los métodos de esta unidad sean universalmente aplicables. La comprensión profunda de la estabilidad, el orden de convergencia y el error global permite al ingeniero diseñar simulaciones confiables y eficientes.

---

## 12. Bibliografía

Chapra, S. C., & Canale, R. P. (2015). *Métodos numéricos para ingenieros* (7.ª ed.). McGraw-Hill Education.

Burden, R. L., & Faires, J. D. (2011). *Numerical analysis* (9th ed.). Brooks/Cole, Cengage Learning.

Hairer, E., Nørsett, S. P., & Wanner, G. (1993). *Solving ordinary differential equations I: Nonstiff problems* (2nd ed.). Springer.

Hairer, E., & Wanner, G. (1996). *Solving ordinary differential equations II: Stiff and differential-algebraic problems* (2nd ed.). Springer.

Ascher, U. M., & Petzold, L. R. (1998). *Computer methods for ordinary differential equations and differential-algebraic equations*. Society for Industrial and Applied Mathematics.

Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical recipes: The art of scientific computing* (3rd ed.). Cambridge University Press.

---

*📌 Documento generado para uso académico. Unidad 6 - Métodos Numéricos.*

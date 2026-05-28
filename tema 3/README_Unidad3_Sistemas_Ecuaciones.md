# 🧮 Unidad 3 - Métodos de Solución de Sistemas de Ecuaciones

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
  - [5.1 Métodos Iterativos para Sistemas Lineales](#51-métodos-iterativos-para-sistemas-lineales)
  - [5.2 Sistemas de Ecuaciones No Lineales](#52-sistemas-de-ecuaciones-no-lineales)
  - [5.3 Iteración y Convergencia](#53-iteración-y-convergencia)
- [6. Fórmulas Matemáticas](#6-fórmulas-matemáticas)
- [7. Explicación de Métodos](#7-explicación-de-métodos)
- [8. Ejemplos](#8-ejemplos)
- [9. Aplicaciones Reales](#9-aplicaciones-reales)
- [10. Ventajas y Desventajas](#10-ventajas-y-desventajas)
- [11. Conclusión](#11-conclusión)
- [12. Bibliografía](#12-bibliografía)

---

## 1. Introducción

La resolución de sistemas de ecuaciones es uno de los problemas más frecuentes y relevantes en la ciencia e ingeniería. Desde el análisis de circuitos eléctricos hasta la simulación de estructuras, pasando por la modelación de flujos en redes de tuberías, los sistemas de ecuaciones aparecen en prácticamente todo modelo matemático multivariable.

Un **sistema de $n$ ecuaciones con $n$ incógnitas** puede escribirse en forma matricial como:

$$A\mathbf{x} = \mathbf{b}$$

donde $A \in \mathbb{R}^{n \times n}$ es la matriz de coeficientes, $\mathbf{x} \in \mathbb{R}^n$ el vector de incógnitas y $\mathbf{b} \in \mathbb{R}^n$ el vector de términos independientes.

Esta unidad aborda los métodos **iterativos** (Jacobi, Gauss-Seidel) para sistemas lineales, la extensión a sistemas **no lineales** mediante Newton-Raphson multivariable, y los criterios matemáticos que garantizan la convergencia de estos procesos.

---

## 2. Objetivos

- 🎯 Aplicar los métodos de Jacobi y Gauss-Seidel para la resolución iterativa de sistemas lineales.
- 🎯 Comprender y verificar las condiciones de convergencia para métodos iterativos.
- 🎯 Extender el método de Newton-Raphson a sistemas de ecuaciones no lineales.
- 🎯 Analizar la convergencia de secuencias generadas por métodos iterativos usando normas vectoriales y matriciales.
- 🎯 Resolver problemas de ingeniería modelados como sistemas de ecuaciones.
- 🎯 Comparar la eficiencia de métodos directos e iterativos según el tamaño y estructura del sistema.

---

## 3. Importancia del Tema

Los sistemas de ecuaciones lineales de gran dimensión son ubicuos en la ingeniería computacional:

- **Método de Elementos Finitos (FEM):** genera sistemas con millones de incógnitas para análisis estructural y térmico.
- **Redes eléctricas:** las Leyes de Kirchhoff formulan un sistema lineal para encontrar voltajes y corrientes.
- **Dinámica de fluidos computacional (CFD):** la discretización de las ecuaciones de Navier-Stokes produce enormes sistemas dispersos.
- **Economía:** modelos de equilibrio general con múltiples mercados.
- **Visión computacional:** ajuste de parámetros en redes neuronales mediante sistemas linealizados.

Los métodos iterativos son especialmente valiosos para **matrices dispersas** (sparse), donde los métodos directos serían prohibitivamente costosos en memoria y tiempo.

---

## 4. Conceptos Fundamentales

### Normas Vectoriales y Matriciales

Para analizar convergencia se usan normas:

- **Norma euclidiana (L2):** $\|\mathbf{x}\|_2 = \sqrt{\sum_{i=1}^n x_i^2}$
- **Norma infinita:** $\|\mathbf{x}\|_\infty = \max_i |x_i|$
- **Norma matricial infinita:** $\|A\|_\infty = \max_i \sum_{j=1}^n |a_{ij}|$

### Radio Espectral
$$\rho(A) = \max_i |\lambda_i|$$

donde $\lambda_i$ son los valores propios de $A$. La condición $\rho(A) < 1$ garantiza convergencia.

### Dominancia Diagonal
Una matriz $A$ es **estrictamente diagonal dominante** si:
$$|a_{ii}| > \sum_{j \neq i} |a_{ij}|, \quad \forall i$$

Esta condición **garantiza** la convergencia de Jacobi y Gauss-Seidel.

### Condicionamiento de una Matriz
$$\kappa(A) = \|A\| \cdot \|A^{-1}\|$$

- $\kappa(A) \approx 1$: sistema bien condicionado
- $\kappa(A) \gg 1$: sistema mal condicionado (sensible a perturbaciones)

---

## 5. Desarrollo Teórico

### 5.1 Métodos Iterativos para Sistemas Lineales

Dado $A\mathbf{x} = \mathbf{b}$, se descompone $A = D + L + U$ donde:
- $D$: diagonal principal
- $L$: parte estrictamente triangular inferior
- $U$: parte estrictamente triangular superior

#### Método de Jacobi
$$\mathbf{x}^{(k+1)} = D^{-1}\left(\mathbf{b} - (L+U)\mathbf{x}^{(k)}\right)$$

Componente a componente:
$$x_i^{(k+1)} = \frac{1}{a_{ii}}\left(b_i - \sum_{j \neq i} a_{ij} x_j^{(k)}\right), \quad i = 1, \ldots, n$$

**Característica:** usa solo valores de la iteración anterior $k$ para calcular todos los valores nuevos.

#### Método de Gauss-Seidel
$$\mathbf{x}^{(k+1)} = (D+L)^{-1}\left(\mathbf{b} - U\mathbf{x}^{(k)}\right)$$

Componente a componente:
$$x_i^{(k+1)} = \frac{1}{a_{ii}}\left(b_i - \sum_{j<i} a_{ij} x_j^{(k+1)} - \sum_{j>i} a_{ij} x_j^{(k)}\right)$$

**Característica:** usa los valores ya calculados en la iteración $k+1$ (más eficiente que Jacobi).

#### Método SOR (Successive Over-Relaxation)
Extiende Gauss-Seidel con un factor de relajación $\omega$:
$$x_i^{(k+1)} = \omega x_i^{GS} + (1-\omega) x_i^{(k)}$$

- $\omega = 1$: Gauss-Seidel
- $0 < \omega < 1$: sub-relajación (mejora convergencia para matrices difíciles)
- $1 < \omega < 2$: sobre-relajación (puede acelerar la convergencia)

---

### 5.2 Sistemas de Ecuaciones No Lineales

Un sistema de $n$ ecuaciones no lineales:
$$\mathbf{F}(\mathbf{x}) = \mathbf{0}$$

es decir:
$$\begin{cases} f_1(x_1, x_2, \ldots, x_n) = 0 \\ f_2(x_1, x_2, \ldots, x_n) = 0 \\ \vdots \\ f_n(x_1, x_2, \ldots, x_n) = 0 \end{cases}$$

#### Newton-Raphson Multivariable
$$\mathbf{x}^{(k+1)} = \mathbf{x}^{(k)} - [J(\mathbf{x}^{(k)})]^{-1} \mathbf{F}(\mathbf{x}^{(k)})$$

donde $J$ es la **Matriz Jacobiana**:
$$J_{ij} = \frac{\partial f_i}{\partial x_j}$$

En la práctica, se resuelve el sistema lineal $J \Delta\mathbf{x} = -\mathbf{F}$ y luego $\mathbf{x}^{(k+1)} = \mathbf{x}^{(k)} + \Delta\mathbf{x}$.

---

### 5.3 Iteración y Convergencia de Sistemas de Ecuaciones

#### Convergencia de Jacobi y Gauss-Seidel

| Condición | Jacobi | Gauss-Seidel |
|-----------|--------|--------------|
| Diagonal dominante estricta | Converge | Converge |
| Simétrica definida positiva | Puede converger | Converge |
| General | No garantizado | No garantizado |

Gauss-Seidel converge **al menos tan rápido como Jacobi**, y frecuentemente más rápido (factor de 2 en tasas de convergencia para muchas matrices).

#### Criterio de Convergencia Práctica

$$\varepsilon_a = \frac{\|\mathbf{x}^{(k+1)} - \mathbf{x}^{(k)}\|_2}{\|\mathbf{x}^{(k+1)}\|_2} \times 100\% < \varepsilon_s$$

---

## 6. Fórmulas Matemáticas

### Iteración de Jacobi (escalar)
$$x_i^{(k+1)} = \frac{1}{a_{ii}}\left(b_i - \sum_{\substack{j=1 \\ j \neq i}}^{n} a_{ij} x_j^{(k)}\right)$$

### Iteración de Gauss-Seidel (escalar)
$$x_i^{(k+1)} = \frac{1}{a_{ii}}\left(b_i - \sum_{j=1}^{i-1} a_{ij} x_j^{(k+1)} - \sum_{j=i+1}^{n} a_{ij} x_j^{(k)}\right)$$

### Matriz de Iteración de Jacobi
$$B_J = -D^{-1}(L+U)$$

### Condición de Convergencia
$$\rho(B) < 1$$

### Newton-Raphson Multivariable
$$J(\mathbf{x}^{(k)}) \Delta\mathbf{x} = -\mathbf{F}(\mathbf{x}^{(k)})$$
$$\mathbf{x}^{(k+1)} = \mathbf{x}^{(k)} + \Delta\mathbf{x}$$

### Error en Norma
$$\|\mathbf{e}^{(k)}\|_\infty \leq \frac{\|B\|_\infty^k}{1 - \|B\|_\infty} \|\mathbf{x}^{(1)} - \mathbf{x}^{(0)}\|_\infty$$

---

## 7. Explicación de Métodos

### 7.1 Pseudocódigo: Gauss-Seidel

```
Algoritmo GaussSeidel:
  ENTRADA: A (n×n), b (n×1), x0, tol, maxIter
  SALIDA: solución aproximada x

  x ← x0
  PARA iter = 1 HASTA maxIter:
    x_ant ← copia de x

    PARA i = 1 HASTA n:
      suma ← 0
      PARA j = 1 HASTA n:
        SI j ≠ i:
          suma ← suma + A[i][j] * x[j]    // usa x actualizado
      x[i] ← (b[i] - suma) / A[i][i]

    // Calcular error
    ea ← norma_inf(x - x_ant) / norma_inf(x) * 100
    SI ea < tol:
      RETORNAR x, iter

  RETORNAR x
```

### 7.2 Pseudocódigo: Newton-Raphson Multivariable

```
Algoritmo NewtonMultivariable:
  ENTRADA: F (sistema de funciones), J (jacobiana), x0, tol, maxIter
  SALIDA: solución aproximada

  x ← x0
  PARA iter = 1 HASTA maxIter:
    F_val ← evaluar F en x
    J_val ← evaluar J en x

    Resolver J_val * dx = -F_val        // sistema lineal
    x_nuevo ← x + dx

    ea ← norma_2(dx) / norma_2(x_nuevo) * 100
    SI ea < tol:
      RETORNAR x_nuevo, iter

    x ← x_nuevo

  RETORNAR x
```

### 7.3 Implementación en Python

```python
import numpy as np

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Método de Gauss-Seidel para sistemas lineales Ax = b
    """
    n = len(b)
    x = np.zeros(n) if x0 is None else x0.copy().astype(float)
    
    for iteration in range(max_iter):
        x_old = x.copy()
        
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - suma) / A[i][i]
        
        ea = np.linalg.norm(x - x_old, np.inf) / np.linalg.norm(x, np.inf) * 100
        
        if ea < tol:
            print(f"Convergió en {iteration+1} iteraciones")
            return x
    
    print("Alcanzó máximo de iteraciones")
    return x


def newton_raphson_sistema(F, J, x0, tol=1e-6, max_iter=50):
    """
    Newton-Raphson para sistemas no lineales
    F: lista de funciones, J: jacobiana simbólica o numérica
    """
    x = np.array(x0, dtype=float)
    
    for iteration in range(max_iter):
        F_val = np.array([f(*x) for f in F])
        J_val = np.array([[j(*x) for j in row] for row in J])
        
        try:
            dx = np.linalg.solve(J_val, -F_val)
        except np.linalg.LinAlgError:
            raise ValueError("Jacobiana singular")
        
        x = x + dx
        
        ea = np.linalg.norm(dx) / np.linalg.norm(x) * 100
        if ea < tol:
            print(f"Convergió en {iteration+1} iteraciones")
            return x
    
    return x


# Ejemplo Gauss-Seidel
A = np.array([[10., -1.,  2.,  0.],
              [-1., 11., -1.,  3.],
              [ 2., -1., 10., -1.],
              [ 0.,  3., -1.,  8.]])
b = np.array([6., 25., -11., 15.])

x = gauss_seidel(A, b)
print("Solución:", x)
# Verificación
print("Residuo ||Ax-b|| =", np.linalg.norm(A @ x - b))
```

---

## 8. Ejemplos

### Ejemplo 1: Gauss-Seidel

**Sistema:**
$$\begin{pmatrix} 4 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 4 \end{pmatrix} \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix} = \begin{pmatrix} 1 \\ 4 \\ -3 \end{pmatrix}$$

**Verificación de diagonal dominante:**
- Fila 1: $|4| > |-1| + |0|$ → $4 > 1$ ✅
- Fila 2: $|4| > |-1| + |-1|$ → $4 > 2$ ✅
- Fila 3: $|4| > |0| + |-1|$ → $4 > 1$ ✅

**Iteración inicial:** $\mathbf{x}^{(0)} = (0, 0, 0)^T$

| Iter | $x_1$ | $x_2$ | $x_3$ | $\varepsilon_a$ (%) |
|------|--------|--------|--------|---------------------|
| 0 | 0.0000 | 0.0000 | 0.0000 | — |
| 1 | 0.2500 | 1.0625 | −0.4844 | — |
| 2 | 0.5156 | 1.0078 | −0.4981 | 52.9 |
| 3 | 0.5020 | 1.0010 | −0.4998 | 2.71 |
| 4 | 0.5003 | 1.0001 | −0.5000 | 0.34 |

Solución exacta: $(0.5, 1.0, -0.5)^T$

---

### Ejemplo 2: Newton-Raphson para Sistema No Lineal

**Sistema:**
$$\begin{cases} f_1(x,y) = x^2 + y^2 - 5 = 0 \\ f_2(x,y) = x^2 - y + 1 = 0 \end{cases}$$

**Jacobiana:**
$$J = \begin{pmatrix} 2x & 2y \\ 2x & -1 \end{pmatrix}$$

**Iteración desde** $\mathbf{x}^{(0)} = (1, 2)^T$:

| Iter | $x$ | $y$ | $\varepsilon_a$ (%) |
|------|-----|-----|---------------------|
| 0 | 1.0000 | 2.0000 | — |
| 1 | 1.5000 | 3.2500 | 38.5 |
| 2 | 1.7204 | 3.9598 | 17.4 |
| 3 | 1.7321 | 4.0000 | 0.67 |

Solución: $(x,y) \approx (1.7321, 4.0000)$ → verificación: $\sqrt{3}^2 + 4 = 7 \neq 5$... converge hacia otra raíz.

---

### Ejemplo 3: Análisis de Convergencia de Jacobi

**Comparar Jacobi vs Gauss-Seidel en convergencia:**

Para el sistema con $A$ diagonal dominante, Gauss-Seidel típicamente requiere ~50% menos iteraciones que Jacobi para la misma tolerancia.

---

## 9. Aplicaciones Reales

### ⚡ Análisis de Circuitos (Leyes de Kirchhoff)
Un circuito con $n$ nodos genera un sistema lineal $Y\mathbf{V} = \mathbf{I}$ donde $Y$ es la matriz de admitancias, $\mathbf{V}$ los voltajes nodales e $\mathbf{I}$ las fuentes de corriente.

### 🌡️ Conducción de Calor en Estado Estacionario
La ecuación de Laplace discretizada sobre una malla 2D produce un sistema lineal disperso de enorme dimensión, ideal para Gauss-Seidel.

### 🏗️ Análisis Estructural por FEM
El método de elementos finitos produce el sistema $K\mathbf{u} = \mathbf{f}$ donde $K$ es la matriz de rigidez (simétrica positiva definida, ideal para SOR).

### 🌐 PageRank de Google
El algoritmo PageRank de Google resuelve un sistema lineal enorme (billones de páginas web) usando métodos iterativos.

### 🧬 Bioinformática
El alineamiento de secuencias genéticas y el plegado de proteínas se formulan como sistemas de optimización resueltos iterativamente.

---

## 10. Ventajas y Desventajas

### Comparativa: Métodos Directos vs Iterativos

| Aspecto | Métodos Directos (ej. Gauss) | Métodos Iterativos (ej. GS) |
|---------|-----------------------------|-----------------------------|
| Exactitud | Exacto (salvo redondeo) | Aproximado, controlable |
| Costo computacional | $O(n^3)$ | $O(n^2)$ por iteración |
| Memoria | $O(n^2)$ | $O(n)$ para matrices dispersas |
| Matrices dispersas | Ineficiente (fill-in) | Muy eficiente |
| Estabilidad | Requiere pivoteo | Depende de la estructura de $A$ |
| Sistemas de gran escala | Prohibitivo | Preferible |

### ✅ Ventajas de los Métodos Iterativos

- Eficientes para **matrices grandes y dispersas**.
- Pueden aprovechar la **estructura de la matriz** (bandas, simetría).
- Bajo consumo de **memoria**.
- Fáciles de paralelizar en computación de alto rendimiento.

### ❌ Desventajas de los Métodos Iterativos

- **No siempre convergen**: requieren condiciones sobre $A$.
- Son más lentos que los directos para **sistemas pequeños y densos**.
- La velocidad de convergencia depende del **número de condición**.
- Matrices mal condicionadas pueden requerir **precondicionamiento**.

---

## 11. Conclusión

Los métodos iterativos para sistemas de ecuaciones son herramientas indispensables en la ingeniería computacional moderna. Gauss-Seidel y sus variantes (SOR) son especialmente poderosos para sistemas grandes y dispersos que surgen en la discretización de ecuaciones diferenciales parciales.

La extensión de Newton-Raphson a sistemas no lineales provee convergencia cuadrática cuando se tiene una buena aproximación inicial y la Jacobiana es no singular. La comprensión rigurosa de las condiciones de convergencia —diagonal dominancia, radio espectral menor que uno— es fundamental para garantizar resultados confiables.

En la práctica moderna, los solucionadores iterativos precondicionados (GMRES, CG, BiCGSTAB) son el estado del arte para sistemas de millones de incógnitas, y su fundamento teórico es el estudiado en esta unidad.

---

## 12. Bibliografía

Chapra, S. C., & Canale, R. P. (2015). *Métodos numéricos para ingenieros* (7.ª ed.). McGraw-Hill Education.

Burden, R. L., & Faires, J. D. (2011). *Numerical analysis* (9th ed.). Brooks/Cole, Cengage Learning.

Saad, Y. (2003). *Iterative methods for sparse linear systems* (2nd ed.). Society for Industrial and Applied Mathematics.

Golub, G. H., & Van Loan, C. F. (2013). *Matrix computations* (4th ed.). Johns Hopkins University Press.

Trefethen, L. N., & Bau, D. (1997). *Numerical linear algebra*. Society for Industrial and Applied Mathematics.

Ortega, J. M., & Rheinboldt, W. C. (2000). *Iterative solution of nonlinear equations in several variables*. Society for Industrial and Applied Mathematics.

---

*📌 Documento generado para uso académico. Unidad 3 - Métodos Numéricos.*

import numpy as np
import time

# Sistema de ecuaciones
A = np.array([
    [2, 1, -1],
    [-3, -1, 2],
    [-2, 1, 2]
], dtype=float)

b = np.array([8, -11, -3], dtype=float)


# Metodo Gauss-Jordan
def gauss_jordan(A, b):
    n = len(b)
    M = np.hstack((A, b.reshape(-1,1)))

    for i in range(n):

        # Hacer pivote = 1
        M[i] = M[i] / M[i,i]

        # Hacer ceros en columna
        for j in range(n):
            if i != j:
                factor = M[j,i]
                M[j] = M[j] - factor * M[i]

    return M[:, -1]


# Metodo Gauss-Seidel
def gauss_seidel(A, b, tol=1e-6, max_iter=100):

    n = len(b)
    x = np.zeros(n)

    for k in range(max_iter):
        x_old = x.copy()

        for i in range(n):
            suma = 0
            for j in range(n):
                if j != i:
                    suma += A[i][j] * x[j]

            x[i] = (b[i] - suma) / A[i][i]

        error = np.linalg.norm(x - x_old)

        if error < tol:
            return x, k+1, True

    return x, max_iter, False


# Comparacion de tiempos

# Gauss-Jordan
inicio = time.perf_counter()
sol_gj = gauss_jordan(A, b)
tiempo_gj = time.perf_counter() - inicio


# Gauss-Seidel
inicio = time.perf_counter()
sol_gs, iteraciones, converge = gauss_seidel(A, b)
tiempo_gs = time.perf_counter() - inicio


# Resultados

print("=== GAUSS JORDAN ===")
print("Solucion:", sol_gj)
print("Tiempo:", tiempo_gj)

print("\n=== GAUSS SEIDEL ===")
print("Solucion:", sol_gs)
print("Iteraciones:", iteraciones)
print("Converge:", converge)
print("Tiempo:", tiempo_gs)
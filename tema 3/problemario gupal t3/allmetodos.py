import numpy as np
import time

# METODOS DIRECTOS

def gauss_elimination(A, b):
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)

    M = np.hstack([A, b.reshape(-1,1)])

    for i in range(n):
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            M[j] = M[j] - factor * M[i]

    x = np.zeros(n)

    for i in range(n-1, -1, -1):
        x[i] = (M[i][-1] - np.dot(M[i][i+1:n], x[i+1:n])) / M[i][i]

    return x


def gauss_jordan(A, b):
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)

    M = np.hstack([A, b.reshape(-1,1)])

    for i in range(n):
        M[i] = M[i] / M[i][i]

        for j in range(n):
            if j != i:
                factor = M[j][i]
                M[j] = M[j] - factor * M[i]

    return M[:, -1]


# METODOS ITERATIVOS

def jacobi(A, b, tol=1e-8, max_iter=1000):
    n = len(b)
    x = np.zeros(n)
    x_new = np.zeros(n)

    for k in range(max_iter):
        for i in range(n):
            s = np.dot(A[i,:], x) - A[i,i]*x[i]
            x_new[i] = (b[i] - s) / A[i,i]

        if np.linalg.norm(x_new - x) < tol:
            return x_new, k+1, True

        x = x_new.copy()

    return x, max_iter, False


def gauss_seidel(A, b, tol=1e-8, max_iter=1000):
    n = len(b)
    x = np.zeros(n)

    for k in range(max_iter):
        x_old = x.copy()

        for i in range(n):
            s1 = np.dot(A[i,:i], x[:i])
            s2 = np.dot(A[i,i+1:], x_old[i+1:])
            x[i] = (b[i] - s1 - s2) / A[i,i]

        if np.linalg.norm(x - x_old) < tol:
            return x, k+1, True

    return x, max_iter, False


# FUNCION PARA ANALIZAR METODO
def analizar_metodo(nombre, metodo, A, b, iterativo=False):

    inicio = time.perf_counter()

    if iterativo:
        x, it, conv = metodo(A, b)
    else:
        x = metodo(A, b)
        it = "-"
        conv = True

    fin = time.perf_counter()

    tiempo = fin - inicio
    residual = np.linalg.norm(A @ x - b)

    print(f"\nMetodo: {nombre}")
    print("Solucion:", np.round(x,6))
    print("Tiempo:", tiempo, "segundos")
    print("Iteraciones:", it)
    print("Convergencia:", conv)
    print("Error residual:", residual)


# DEFINICION DE SISTEMAS

sistemas = []

# SISTEMA 1 (diagonal dominante)

A1 = np.array([
[5,1,1],
[2,6,1],
[1,1,7]
])

b1 = np.array([27,31,34])

sistemas.append(("Sistema 1 (Diagonal dominante)",A1,b1))


# SISTEMA 2 (sin diagonal dominante)

A2 = np.array([
[1,3,2],
[2,1,3],
[3,2,1]
])

b2 = np.array([31,29,26])

sistemas.append(("Sistema 2 (No dominante)",A2,b2))


# SISTEMA 3 (10x10)

A3 = np.array([
[4,1,1,1,1,1,1,1,1,1],
[1,5,1,1,1,1,1,1,1,1],
[1,1,6,1,1,1,1,1,1,1],
[1,1,1,7,1,1,1,1,1,1],
[1,1,1,1,8,1,1,1,1,1],
[1,1,1,1,1,9,1,1,1,1],
[1,1,1,1,1,1,10,1,1,1],
[1,1,1,1,1,1,1,11,1,1],
[1,1,1,1,1,1,1,1,12,1],
[1,1,1,1,1,1,1,1,1,13]
])

b3 = np.array([40,41,42,43,44,45,46,47,48,49])

sistemas.append(("Sistema 3 (10x10)",A3,b3))


# EJECUCION

for nombre, A, b in sistemas:

    print("\n===================================")
    print(nombre)
    print("===================================")

    analizar_metodo("Gauss", gauss_elimination, A, b)
    analizar_metodo("Gauss-Jordan", gauss_jordan, A, b)
    analizar_metodo("Jacobi", jacobi, A, b, True)
    analizar_metodo("Gauss-Seidel", gauss_seidel, A, b, True)
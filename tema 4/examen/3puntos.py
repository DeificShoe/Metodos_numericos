#En un experimento de física, la posición de un objeto está dada por:
#f(x)=x^3−2x^2+x
#Se desea aproximar la velocidad instantánea en x=2, usando un paso h=0.1.

import math

# Definir función
def f(x):
    return x**3 - 2*x**2 + x

# Datos
x = 2
h = 0.1

# Método de 3 puntos (central)
derivada = (f(x + h) - f(x - h)) / (2 * h)

print("Aproximación de la derivada:", derivada)

real = 3*x**2 - 4*x + 1
print("Valor real:", real)


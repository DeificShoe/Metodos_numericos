
#En ingeniería, se necesita calcular el trabajo realizado por una fuerza variable, dada por:

#f(x)=x^2+3x+2 en el intervalo [0,2].

import math

# Definir función
def f(x):
    return x**2 + 3*x + 2

# Intervalo
a = 0
b = 2

# Cálculos base
m = (a + b) / 2
d = (b - a) / 2

# Puntos de Gauss
x1 = m - d / math.sqrt(3)
x2 = m + d / math.sqrt(3)

# Evaluación
integral = d * (f(x1) + f(x2))

print("Aproximación de la integral:", integral)

#valor real
real = (1/3)*b**3 + (3/2)*b**2 + 2*b
print("Valor real:", real)
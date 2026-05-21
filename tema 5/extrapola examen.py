# Datos conocidos
x0=10
y0=120

x1=20
y1=150

# Valor a extrapolar
x=50

# Fórmula lineal
y = y0 + ((x-x0)*(y1-y0))/(x1-x0)

print("Tiempo estimado:",y,"ms")
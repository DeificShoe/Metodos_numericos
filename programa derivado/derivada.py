import sympy as sp


x= -2
h=0.2
punto=x+h


f_a=1/(punto*punto)

f_b=1/(x*x)

resta=f_a - f_b

resultado= resta/h
print("El resultado es: ")
print (resultado)


#x, h = sp.symbols('x h')

#expr = (1/(x+h)**2 - 1/x**2) / h

#simplificado = sp.simplify(expr)

# Aplicamos límite
#resultado = sp.limit(simplificado, h, 0)

#print("Expresión simplificada:", simplificado)
#print("Resultado final:", resultado)

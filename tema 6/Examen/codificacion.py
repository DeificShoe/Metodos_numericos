T = 80
t = 0
h = 0.5
tf = 1.5

i = 0

print("i\t t\t T\t\t f(t,T)")

while t <= tf:

    f = -0.1 * (T - 20)

    print(i, "\t", t, "\t", round(T,4), "\t\t", round(f,4))

    if t == tf:
        break

    T = T + h * f
    t = round(t + h, 2)

    i += 1

print("\nTemperatura aproximada:")
print("T(", tf, ") =", round(T,4), "°C")
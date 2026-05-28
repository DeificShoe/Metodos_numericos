"""
================================================================================
                    INTERPOLACIÓN - ANÁLISIS COMPLETO
================================================================================
Este módulo contiene implementaciones de tres métodos de interpolación:
1. Interpolación Lineal
2. Interpolación Cuadrática (Lagrange)
3. Interpolación Segmentada (Splines Cúbicos)

Cada método incluye 2 problemas:
- Problema 1: Caso ideal con datos perfectos
- Problema 2: Caso problemático con valores fuera de rango

DIFERENCIA CLAVE CON EXTRAPOLACIÓN:
La interpolación estima valores DENTRO del rango de datos conocidos.
Los valores estimados están entre x_min y x_max de los datos originales.
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, CubicSpline
from scipy.optimize import fsolve

# ============================================================================
#                    1. INTERPOLACIÓN LINEAL
# ============================================================================

print("\n" + "="*80)
print("1. INTERPOLACIÓN LINEAL")
print("="*80)

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 1: CASO IDEAL - Datos lineales perfectos
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 1: Interpolación Lineal - Caso Ideal")
print("-"*80)

"""
ENUNCIADO:
Una empresa monitorea la temperatura en un proceso industrial. Se registran
mediciones a las 10:00, 12:00 y 14:00 horas con valores 20°C, 24°C y 28°C
respectivamente. Estimar la temperatura a las 11:00 y 13:00 horas.

PROBLEMÁTICA:
Se asume que la temperatura varía linealmente entre mediciones.

QUÉ SE CALCULA:
- Interpolación lineal entre puntos consecutivos
- Valores estimados a tiempos intermedios
- Visualización de la función interpoladora
"""

# Datos originales
horas = np.array([10, 12, 14])  # Horas del día
temperaturas = np.array([20, 24, 28])  # Temperaturas en °C

# Crear función de interpolación lineal
f_lineal = interp1d(horas, temperaturas, kind='linear')

# Puntos donde queremos estimar
horas_estimar = np.array([11, 13])
temps_estimadas = f_lineal(horas_estimar)

print("\nDatos originales:")
print(f"  Horas: {horas}")
print(f"  Temperaturas (°C): {temperaturas}")

print("\nValores estimados mediante interpolación lineal:")
for h, t in zip(horas_estimar, temps_estimadas):
    print(f"  A las {h}:00 horas: {t:.2f}°C")

# Cálculo manual de interpolación lineal para verificación
print("\nVerificación manual - Fórmula: y = y₀ + (y₁ - y₀) × (x - x₀) / (x₁ - x₀)")
h_test = 11
idx = np.where(horas < h_test)[0][-1]  # Encontrar intervalo
x0, x1 = horas[idx], horas[idx+1]
y0, y1 = temperaturas[idx], temperaturas[idx+1]
y_manual = y0 + (y1 - y0) * (h_test - x0) / (x1 - x0)
print(f"  Para x={h_test}: y = {y0} + ({y1} - {y0}) × ({h_test} - {x0}) / ({x1} - {x0})")
print(f"  y = {y0} + {y1-y0} × {h_test-x0}/{x1-x0} = {y_manual:.2f}°C ✓")

# Crear gráfica
x_continuo = np.linspace(10, 14, 100)
y_continuo = f_lineal(x_continuo)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(horas, temperaturas, 'ro-', linewidth=2, markersize=8, label='Datos originales')
plt.plot(horas_estimar, temps_estimadas, 'bs', markersize=8, label='Valores interpolados')
plt.plot(x_continuo, y_continuo, 'b--', linewidth=1.5, alpha=0.7, label='Función interpoladora')
plt.xlabel('Hora del día', fontsize=11, fontweight='bold')
plt.ylabel('Temperatura (°C)', fontsize=11, fontweight='bold')
plt.title('Problema 1: Interpolación Lineal Ideal', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)
plt.xticks(range(10, 15))

# Tabla de resultados
plt.subplot(1, 2, 2)
plt.axis('off')
resultados_tabla = [
    ['Hora', 'Temperatura (°C)', 'Tipo'],
    ['10:00', f'{temperaturas[0]:.2f}', 'Original'],
    ['11:00', f'{temps_estimadas[0]:.2f}', 'Estimada'],
    ['12:00', f'{temperaturas[1]:.2f}', 'Original'],
    ['13:00', f'{temps_estimadas[1]:.2f}', 'Estimada'],
    ['14:00', f'{temperaturas[2]:.2f}', 'Original'],
]
tabla = plt.table(cellText=resultados_tabla, cellLoc='center', loc='center',
                  colWidths=[0.3, 0.4, 0.3])
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1, 2)
# Colorear encabezado
for i in range(3):
    tabla[(0, i)].set_facecolor('#2E75B6')
    tabla[(0, i)].set_text_props(weight='bold', color='white')

plt.suptitle('Problema 1: Interpolación Lineal - Caso Ideal', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✓ CONCLUSIÓN Problema 1:")
print("  La interpolación lineal funciona perfectamente cuando los datos tienen")
print("  una relación lineal clara. Los valores estimados son exactos y precisos.")
print("  Este es el caso ideal para este método.")

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 2: CASO PROBLEMÁTICO - Datos no lineales
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 2: Interpolación Lineal - Caso Problemático")
print("-"*80)

"""
ENUNCIADO:
Se mide el crecimiento de bacterias en un cultivo. Se registran mediciones
a t=0, t=2 y t=4 horas con poblaciones de 100, 200 y 600 bacterias.
Estimar la población a t=1 y t=3 horas.

PROBLEMÁTICA:
El crecimiento bacteriano es exponencial, NO lineal. La interpolación lineal
asumirá una tendencia incorrecta entre puntos.

QUÉ SE CALCULA:
- Interpolación lineal (INCORRECTA para estos datos)
- Comparación con modelo exponencial real
- Análisis del error introducido
"""

tiempos = np.array([0, 2, 4])
poblacion = np.array([100, 200, 600])

# Interpolación lineal (INCORRECTA)
f_lineal_exp = interp1d(tiempos, poblacion, kind='linear')
tiempos_estimar = np.array([1, 3])
poblacion_estimada_lineal = f_lineal_exp(tiempos_estimar)

# Modelo exponencial real: P(t) = 100 * e^(kt)
# Encontrar k: 200 = 100 * e^(2k) → k = ln(2)/2
k = np.log(2) / 2
poblacion_real = 100 * np.exp(k * tiempos_estimar)

print("\nDatos originales (Crecimiento bacteriano):")
print(f"  Tiempos (horas): {tiempos}")
print(f"  Población (bacterias): {poblacion}")

print("\nValores estimados mediante interpolación lineal (INCORRECTA):")
for t, p in zip(tiempos_estimar, poblacion_estimada_lineal):
    print(f"  t = {t} horas: {p:.0f} bacterias")

print("\nValores reales (modelo exponencial P(t) = 100·e^(ln(2)·t/2)):")
for t, p in zip(tiempos_estimar, poblacion_real):
    print(f"  t = {t} horas: {p:.0f} bacterias")

print("\nERRORES COMETIDOS por interpolación lineal:")
errores = np.abs(poblacion_estimada_lineal - poblacion_real)
errores_rel = (errores / poblacion_real) * 100
for t, error_abs, error_rel in zip(tiempos_estimar, errores, errores_rel):
    print(f"  t = {t} horas: Error absoluto = {error_abs:.0f} bacterias ({error_rel:.1f}%)")

# Gráficas comparativas
t_continuo = np.linspace(0, 4, 100)
p_lineal_continuo = f_lineal_exp(t_continuo)
p_exponencial_continuo = 100 * np.exp(k * t_continuo)

plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.plot(tiempos, poblacion, 'ro-', linewidth=2, markersize=8, label='Datos originales')
plt.plot(tiempos_estimar, poblacion_estimada_lineal, 'bs', markersize=8, 
         label='Interpolación lineal (INCORRECTA)')
plt.plot(tiempos_estimar, poblacion_real, 'g^', markersize=8, 
         label='Valores reales (exponencial)')
plt.plot(t_continuo, p_lineal_continuo, 'b--', linewidth=1.5, alpha=0.7, 
         label='Función lineal')
plt.plot(t_continuo, p_exponencial_continuo, 'g-', linewidth=2, alpha=0.7, 
         label='Función exponencial real')
plt.xlabel('Tiempo (horas)', fontsize=11, fontweight='bold')
plt.ylabel('Población (bacterias)', fontsize=11, fontweight='bold')
plt.title('Problema 2: Interpolación Lineal - Datos No Lineales', 
          fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)
plt.ylim([0, 700])

# Gráfica de errores
plt.subplot(1, 2, 2)
errores_plot = [0, errores[0], 0, errores[1], 0]
tiempos_plot = [0, 1, 2, 3, 4]
plt.bar(tiempos_plot, errores_plot, width=0.4, color=['green', 'red', 'green', 'red', 'green'],
        alpha=0.7, edgecolor='black', linewidth=1.5)
plt.xlabel('Tiempo (horas)', fontsize=11, fontweight='bold')
plt.ylabel('Error absoluto (bacterias)', fontsize=11, fontweight='bold')
plt.title('Errores de Interpolación Lineal', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
for t, e in zip(tiempos_estimar, errores):
    plt.text(t, e + 10, f'{e:.0f}', ha='center', fontweight='bold')

plt.suptitle('Problema 2: Interpolación Lineal - Caso Problemático', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✗ CONCLUSIÓN Problema 2:")
print("  La interpolación lineal produce errores significativos (~33%) cuando los")
print("  datos NO tienen relación lineal. El crecimiento exponencial no es capturado")
print("  adecuadamente. Se recomienda usar interpolación cuadrática o splines.")

# ============================================================================
#                    2. INTERPOLACIÓN CUADRÁTICA (LAGRANGE)
# ============================================================================

print("\n\n" + "="*80)
print("2. INTERPOLACIÓN CUADRÁTICA (MÉTODO DE LAGRANGE)")
print("="*80)

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 3: CASO IDEAL - Datos cuadráticos perfectos
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 3: Interpolación Cuadrática - Caso Ideal")
print("-"*80)

"""
ENUNCIADO:
Un proyectil es lanzado horizontalmente. Se registra su altura a diferentes
distancias horizontales: x=0m (h=100m), x=2m (h=99.6m), x=4m (h=98.4m).
Estimar la altura a x=1m y x=3m.

PROBLEMÁTICA:
La trayectoria de un proyectil sigue una parábola (función cuadrática).

QUÉ SE CALCULA:
- Interpolación cuadrática mediante polinomios de Lagrange
- Valores estimados en puntos intermedios
- Coeficientes del polinomio ajustado
"""

def lagrange_interpolation(x_points, y_points, x_eval):
    """
    Implementa interpolación de Lagrange.
    
    Parámetros:
    - x_points: array con coordenadas x conocidas
    - y_points: array con coordenadas y conocidas
    - x_eval: punto(s) donde evaluar
    
    Retorna: valor(es) interpolado(s)
    """
    if np.isscalar(x_eval):
        x_eval = np.array([x_eval])
    
    n = len(x_points)
    y_eval = np.zeros_like(x_eval, dtype=float)
    
    for i, x in enumerate(x_eval):
        y = 0
        for j in range(n):
            # Calcular polinomio base de Lagrange Lj(x)
            L_j = 1
            for k in range(n):
                if k != j:
                    L_j *= (x - x_points[k]) / (x_points[j] - x_points[k])
            y += y_points[j] * L_j
        y_eval[i] = y
    
    return y_eval

# Datos del proyectil
distancias = np.array([0, 2, 4])
alturas = np.array([100, 99.6, 98.4])

# Usar interpolación cuadrática de Lagrange
distancias_estimar = np.array([1, 3])
alturas_estimadas = lagrange_interpolation(distancias, alturas, distancias_estimar)

print("\nDatos originales (Trayectoria de proyectil):")
print(f"  Distancias (m): {distancias}")
print(f"  Alturas (m): {alturas}")

print("\nValores estimados mediante interpolación cuadrática:")
for d, a in zip(distancias_estimar, alturas_estimadas):
    print(f"  x = {d}m: h = {a:.4f}m")

# Ajustar polinomio cuadrático: h = ax² + bx + c
# Usar numpy.polyfit para obtener coeficientes
coef = np.polyfit(distancias, alturas, 2)
print(f"\nPolinomio cuadrático ajustado: h(x) = {coef[0]:.4f}x² + {coef[1]:.4f}x + {coef[2]:.4f}")

# Verificar ajuste
alturas_verificacion = np.polyval(coef, distancias)
print(f"\nVerificación del ajuste:")
for d, h_orig, h_ajuste in zip(distancias, alturas, alturas_verificacion):
    print(f"  x = {d}: h_original = {h_orig:.4f}m, h_ajuste = {h_ajuste:.4f}m, diferencia = {abs(h_orig-h_ajuste):.8f}m")

# Gráficas
x_continuo = np.linspace(0, 4, 100)
y_continuo = np.polyval(coef, x_continuo)

plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.plot(distancias, alturas, 'ro-', linewidth=2, markersize=10, label='Datos originales')
plt.plot(distancias_estimar, alturas_estimadas, 'bs', markersize=10, 
         label='Valores interpolados')
plt.plot(x_continuo, y_continuo, 'g-', linewidth=2.5, alpha=0.7, 
         label='Parábola interpoladora')
plt.xlabel('Distancia horizontal (m)', fontsize=11, fontweight='bold')
plt.ylabel('Altura (m)', fontsize=11, fontweight='bold')
plt.title('Problema 3: Interpolación Cuadrática Ideal', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)

# Tabla de resultados
plt.subplot(1, 2, 2)
plt.axis('off')
resultados_tabla_cuad = [
    ['x (m)', 'h (m)', 'Tipo'],
    ['0.0', f'{alturas[0]:.4f}', 'Original'],
    ['1.0', f'{alturas_estimadas[0]:.4f}', 'Estimada'],
    ['2.0', f'{alturas[1]:.4f}', 'Original'],
    ['3.0', f'{alturas_estimadas[1]:.4f}', 'Estimada'],
    ['4.0', f'{alturas[2]:.4f}', 'Original'],
]
tabla_cuad = plt.table(cellText=resultados_tabla_cuad, cellLoc='center', loc='center',
                       colWidths=[0.3, 0.4, 0.3])
tabla_cuad.auto_set_font_size(False)
tabla_cuad.set_fontsize(10)
tabla_cuad.scale(1, 2)
for i in range(3):
    tabla_cuad[(0, i)].set_facecolor('#2E75B6')
    tabla_cuad[(0, i)].set_text_props(weight='bold', color='white')

plt.suptitle('Problema 3: Interpolación Cuadrática - Caso Ideal', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✓ CONCLUSIÓN Problema 3:")
print("  La interpolación cuadrática se ajusta perfectamente a datos parabólicos.")
print("  El polinomio de segundo grado captura la curvatura de la trayectoria.")
print("  Los valores estimados son muy precisos.")

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 4: CASO PROBLEMÁTICO - Datos de alto grado
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 4: Interpolación Cuadrática - Caso Problemático")
print("-"*80)

"""
ENUNCIADO:
Se tienen mediciones de concentración de un reactivo químico en función del
tiempo: t=0s (c=100), t=2s (c=50), t=4s (c=10). Interpolar a t=1s y t=3s.

PROBLEMÁTICA:
La reacción química sigue una función exponencial (decaimiento), NO cuadrática.
La interpolación cuadrática intentará ajustar una parábola a una función exponencial.

QUÉ SE CALCULA:
- Interpolación cuadrática (INAPROPIADA para estos datos)
- Comparación con el modelo exponencial real
- Análisis del error cometido
"""

tiempos_quim = np.array([0, 2, 4])
concentracion = np.array([100, 50, 10])

# Interpolación cuadrática
concentracion_estimada_cuad = lagrange_interpolation(tiempos_quim, concentracion, 
                                                     np.array([1, 3]))

# Modelo exponencial real: c(t) = 100 * 0.5^(t/2)
concentracion_real_quim = 100 * (0.5 ** (np.array([1, 3]) / 2))

print("\nDatos originales (Decaimiento químico):")
print(f"  Tiempos (s): {tiempos_quim}")
print(f"  Concentración (mol/L): {concentracion}")

print("\nValores estimados mediante interpolación cuadrática:")
for t, c in zip([1, 3], concentracion_estimada_cuad):
    print(f"  t = {t}s: c = {c:.2f} mol/L")

print("\nValores reales (modelo exponencial c(t) = 100·0.5^(t/2)):")
for t, c in zip([1, 3], concentracion_real_quim):
    print(f"  t = {t}s: c = {c:.2f} mol/L")

print("\nERRORES COMETIDOS:")
errores_cuad = np.abs(concentracion_estimada_cuad - concentracion_real_quim)
for t, e in zip([1, 3], errores_cuad):
    print(f"  t = {t}s: Error = {e:.2f} mol/L ({(e/concentracion_real_quim[0])*100:.1f}%)")

# Ajustar polinomio cuadrático a datos
coef_quim = np.polyfit(tiempos_quim, concentracion, 2)
print(f"\nPolinomio cuadrático: c(t) = {coef_quim[0]:.4f}t² + {coef_quim[1]:.4f}t + {coef_quim[2]:.4f}")

# Gráficas comparativas
t_continuo_quim = np.linspace(0, 4, 100)
c_cuad_continuo = np.polyval(coef_quim, t_continuo_quim)
c_exp_continuo = 100 * (0.5 ** (t_continuo_quim / 2))

plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.plot(tiempos_quim, concentracion, 'ro-', linewidth=2, markersize=8, 
         label='Datos originales')
plt.plot([1, 3], concentracion_estimada_cuad, 'bs', markersize=8, 
         label='Interpolación cuadrática (INAPROPIADA)')
plt.plot([1, 3], concentracion_real_quim, 'g^', markersize=8, 
         label='Valores reales (exponencial)')
plt.plot(t_continuo_quim, c_cuad_continuo, 'b--', linewidth=1.5, alpha=0.7, 
         label='Parábola ajustada')
plt.plot(t_continuo_quim, c_exp_continuo, 'g-', linewidth=2, alpha=0.7, 
         label='Decaimiento exponencial real')
plt.xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
plt.ylabel('Concentración (mol/L)', fontsize=11, fontweight='bold')
plt.title('Problema 4: Interpolación Cuadrática - Datos Exponenciales', 
          fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=9)
plt.ylim([0, 110])

# Gráfica de diferencias
plt.subplot(1, 2, 2)
diferencias = concentracion_estimada_cuad - concentracion_real_quim
tiempos_est = [1, 3]
colores_dif = ['red' if d != 0 else 'green' for d in diferencias]
plt.bar(tiempos_est, np.abs(diferencias), width=0.4, color=colores_dif, alpha=0.7, 
        edgecolor='black', linewidth=1.5)
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
plt.ylabel('Error absoluto (mol/L)', fontsize=11, fontweight='bold')
plt.title('Errores: Cuadrática vs Exponencial Real', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
for t, e in zip(tiempos_est, np.abs(diferencias)):
    plt.text(t, e + 0.5, f'{e:.2f}', ha='center', fontweight='bold', color='darkred')

plt.suptitle('Problema 4: Interpolación Cuadrática - Caso Problemático', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✗ CONCLUSIÓN Problema 4:")
print("  La interpolación cuadrática no es apropiada para datos exponenciales.")
print("  Los errores son menores que con interpolación lineal, pero aún significativos.")
print("  Para datos de decaimiento, se recomienda ajustar exponencialmente o usar splines.")

# ============================================================================
#                    3. INTERPOLACIÓN SEGMENTADA (SPLINES CÚBICOS)
# ============================================================================

print("\n\n" + "="*80)
print("3. INTERPOLACIÓN SEGMENTADA - SPLINES CÚBICOS")
print("="*80)

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 5: CASO IDEAL - Datos suaves y continuos
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 5: Splines Cúbicos - Caso Ideal")
print("-"*80)

"""
ENUNCIADO:
Se monitorea la velocidad de un automóvil durante 10 segundos en intervalos
de 2 segundos. Datos: t=[0,2,4,6,8,10]s, v=[0,10,15,20,18,16]m/s.
Estimar la velocidad a t=1, 3, 5, 7, 9 segundos.

PROBLEMÁTICA:
La velocidad varía de manera suave y continua. Los splines cúbicos capturan
cambios suaves sin oscilaciones.

QUÉ SE CALCULA:
- Splines cúbicos naturales para interpolación suave
- Valores estimados en múltiples puntos intermedios
- Derivadas (aceleración) en los puntos
"""

tiempos_auto = np.array([0, 2, 4, 6, 8, 10])
velocidades = np.array([0, 10, 15, 20, 18, 16])

# Crear spline cúbico natural
spline_auto = CubicSpline(tiempos_auto, velocidades, bc_type='natural')

# Estimar en puntos intermedios
tiempos_estimar_auto = np.array([1, 3, 5, 7, 9])
velocidades_estimadas = spline_auto(tiempos_estimar_auto)

# Calcular derivadas (aceleración)
aceleraciones = spline_auto(tiempos_estimar_auto, 1)

print("\nDatos originales (Velocidad del automóvil):")
for t, v in zip(tiempos_auto, velocidades):
    print(f"  t = {t:2.0f}s: v = {v:5.1f} m/s")

print("\nValores estimados con Splines Cúbicos:")
for t, v, a in zip(tiempos_estimar_auto, velocidades_estimadas, aceleraciones):
    print(f"  t = {t:.1f}s: v = {v:6.2f} m/s, a = {a:6.2f} m/s²")

# Gráficas
t_continuo_auto = np.linspace(0, 10, 200)
v_continuo = spline_auto(t_continuo_auto)
a_continuo = spline_auto(t_continuo_auto, 1)  # Primera derivada

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Velocidad
ax1 = axes[0, 0]
ax1.plot(tiempos_auto, velocidades, 'ro-', linewidth=2, markersize=9, 
         label='Datos originales')
ax1.plot(tiempos_estimar_auto, velocidades_estimadas, 'bs', markersize=8, 
         label='Valores interpolados')
ax1.plot(t_continuo_auto, v_continuo, 'g-', linewidth=2.5, alpha=0.7, 
         label='Spline cúbico')
ax1.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Velocidad (m/s)', fontsize=11, fontweight='bold')
ax1.set_title('Velocidad del Automóvil', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)

# Aceleración
ax2 = axes[0, 1]
ax2.plot(t_continuo_auto, a_continuo, 'purple', linewidth=2.5)
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax2.plot(tiempos_estimar_auto, aceleraciones, 'bs', markersize=8, label='En puntos estimados')
ax2.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Aceleración (m/s²)', fontsize=11, fontweight='bold')
ax2.set_title('Aceleración (Primera Derivada)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)

# Tabla de resultados
ax3 = axes[1, 0]
ax3.axis('off')
tabla_spline = [
    ['t (s)', 'v (m/s)', 'a (m/s²)', 'Tipo'],
    ['0.0', f'{velocidades[0]:.2f}', '-', 'Original'],
    ['1.0', f'{velocidades_estimadas[0]:.2f}', f'{aceleraciones[0]:.2f}', 'Estimado'],
    ['2.0', f'{velocidades[1]:.2f}', '-', 'Original'],
    ['3.0', f'{velocidades_estimadas[1]:.2f}', f'{aceleraciones[1]:.2f}', 'Estimado'],
    ['4.0', f'{velocidades[2]:.2f}', '-', 'Original'],
    ['5.0', f'{velocidades_estimadas[2]:.2f}', f'{aceleraciones[2]:.2f}', 'Estimado'],
    ['6.0', f'{velocidades[3]:.2f}', '-', 'Original'],
    ['7.0', f'{velocidades_estimadas[3]:.2f}', f'{aceleraciones[3]:.2f}', 'Estimado'],
    ['8.0', f'{velocidades[4]:.2f}', '-', 'Original'],
    ['9.0', f'{velocidades_estimadas[4]:.2f}', f'{aceleraciones[4]:.2f}', 'Estimado'],
    ['10.0', f'{velocidades[5]:.2f}', '-', 'Original'],
]
tabla_sp = plt.table(cellText=tabla_spline, cellLoc='center', loc='center',
                     colWidths=[0.2, 0.25, 0.25, 0.25])
tabla_sp.auto_set_font_size(False)
tabla_sp.set_fontsize(9)
tabla_sp.scale(1, 1.8)
for i in range(4):
    tabla_sp[(0, i)].set_facecolor('#2E75B6')
    tabla_sp[(0, i)].set_text_props(weight='bold', color='white')

# Suavidad del spline
ax4 = axes[1, 1]
segunda_derivada = spline_auto(t_continuo_auto, 2)
ax4.plot(t_continuo_auto, segunda_derivada, 'orange', linewidth=2.5)
ax4.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax4.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Cambio de Aceleración (m/s³)', fontsize=11, fontweight='bold')
ax4.set_title('Segunda Derivada (Suavidad del Spline)', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.fill_between(t_continuo_auto, 0, segunda_derivada, alpha=0.3, color='orange')

plt.suptitle('Problema 5: Splines Cúbicos - Caso Ideal', 
             fontsize=13, fontweight='bold', y=0.995)
plt.tight_layout()
plt.show()

print("\n✓ CONCLUSIÓN Problema 5:")
print("  Los splines cúbicos producen interpolaciones suaves y continuas.")
print("  Las derivadas son continuas, lo que significa aceleración suave.")
print("  Este método es ideal para datos que varían de manera continua y suave.")

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 6: CASO PROBLEMÁTICO - Datos con discontinuidades
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 6: Splines Cúbicos - Caso Problemático")
print("-"*80)

"""
ENUNCIADO:
Se mide la carga en un capacitor durante la carga y descarga:
t=[0,1,2,3,4]s, Q=[0,50,80,75,30]C. Hay una discontinuidad en t=3s
(el capacitor se descarga abruptamente). Interpolar en t=0.5, 1.5, 2.5, 3.5s.

PROBLEMÁTICA:
Los splines cúbicos asumen suavidad. Una discontinuidad abrupta causará que
el spline intente "suavizar" la discontinuidad, produciendo oscilaciones no reales
(efecto Runge).

QUÉ SE CALCULA:
- Spline cúbico sobre datos con discontinuidad
- Comparación con lo que debería ocurrir
- Análisis de oscilaciones y comportamiento erróneo
"""

tiempos_cap = np.array([0, 1, 2, 3, 4])
carga = np.array([0, 50, 80, 75, 30])

# Spline cúbico (que intentará suavizar la discontinuidad)
spline_cap = CubicSpline(tiempos_cap, carga, bc_type='natural')

tiempos_estimar_cap = np.array([0.5, 1.5, 2.5, 3.5])
cargas_estimadas = spline_cap(tiempos_estimar_cap)

print("\nDatos originales (Carga en capacitor):")
for t, q in zip(tiempos_cap, carga):
    print(f"  t = {t}s: Q = {q:5.1f} C")

print("\nValores estimados con Splines Cúbicos:")
for t, q in zip(tiempos_estimar_cap, cargas_estimadas):
    print(f"  t = {t:.1f}s: Q = {q:6.2f} C")

print("\nPROBLEMA: La discontinuidad en t=3s causa que el spline")
print("intente 'suavizar' el cambio abrupto, lo que resulta en")
print("valores interpolados que no reflejan la realidad física.")

# Análisis del problema
print("\nAnálisis del comportamiento:")
print(f"  Salto real en t=3: {carga[2]} → {carga[3]} = {carga[3]-carga[2]:+.1f} C")
print(f"  Valor spline en t=2.99: {spline_cap(2.99):.2f} C (debería ser ~80)")
print(f"  Valor spline en t=3.01: {spline_cap(3.01):.2f} C (debería ser ~30)")
print(f"  El spline 'anticipa' y 'posterga' el cambio, causando oscilaciones.")

# Gráficas
t_continuo_cap = np.linspace(0, 4, 200)
q_continuo = spline_cap(t_continuo_cap)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfica principal
ax1 = axes[0]
ax1.plot(tiempos_cap, carga, 'ro-', linewidth=2, markersize=9, label='Datos originales')
ax1.plot(tiempos_estimar_cap, cargas_estimadas, 'bs', markersize=8, 
         label='Interpolación spline')
ax1.plot(t_continuo_cap, q_continuo, 'purple', linewidth=2.5, alpha=0.7, 
         label='Spline cúbico')
# Mostrar discontinuidad real
ax1.plot([3, 3], [75, 30], 'r--', linewidth=2, label='Discontinuidad real')
ax1.axvline(x=3, color='red', linestyle=':', alpha=0.5)
ax1.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Carga (C)', fontsize=11, fontweight='bold')
ax1.set_title('Problema 6: Spline Cúbico - Discontinuidad', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)
ax1.set_ylim([-10, 90])

# Errores/diferencias
ax2 = axes[1]
# Comparar spline cercano a t=3
t_comparacion = np.array([2.5, 2.9, 3.0, 3.1, 3.5])
q_spline = spline_cap(t_comparacion)
q_esperado = np.array([80, 80, 52.5, 30, 30])  # Esperado: 80 antes de 3, 30 después
errores_disc = np.abs(q_spline - q_esperado)

colores_err = ['green' if t < 3 or t > 3.1 else 'red' for t in t_comparacion]
ax2.bar(range(len(t_comparacion)), errores_disc, color=colores_err, alpha=0.7, 
        edgecolor='black', linewidth=1.5)
ax2.set_xticks(range(len(t_comparacion)))
ax2.set_xticklabels([f'{t:.1f}s' for t in t_comparacion])
ax2.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Error (C)', fontsize=11, fontweight='bold')
ax2.set_title('Errores cercanos a la discontinuidad', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
for i, (t, e) in enumerate(zip(t_comparacion, errores_disc)):
    ax2.text(i, e + 1, f'{e:.1f}', ha='center', fontweight='bold')

plt.suptitle('Problema 6: Splines Cúbicos - Caso Problemático (Discontinuidad)', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✗ CONCLUSIÓN Problema 6:")
print("  Los splines cúbicos NO son apropiados para datos con discontinuidades abruptas.")
print("  El método intenta suavizar cambios bruscos, produciendo oscilaciones no reales.")
print("  En estos casos, se recomienda usar splines separados antes y después de la")
print("  discontinuidad, o métodos que permitan discontinuidades (como splines lineales).")

print("\n" + "="*80)
print("FIN DEL ANÁLISIS DE INTERPOLACIÓN")
print("="*80)

# Explicación final
print("""
RESUMEN COMPARATIVO DE MÉTODOS DE INTERPOLACIÓN:

┌──────────────────────────────────────────────────────────────────────────┐
│                    MÉTODO         │  VENTAJAS  │  DESVENTAJAS  │ CASOS  │
├──────────────────────────────────────────────────────────────────────────┤
│ LINEAL                            │ Simple     │ Poco preciso  │ Datos  │
│                                   │ Rápido     │ para curvas   │ lineales│
├──────────────────────────────────────────────────────────────────────────┤
│ CUADRÁTICO (LAGRANGE)             │ Preciso    │ Requiere 3    │ Datos  │
│                                   │ para datos │ puntos        │ cuadráticos│
│                                   │ curvos     │ Oscilaciones  │        │
├──────────────────────────────────────────────────────────────────────────┤
│ SEGMENTADO (SPLINES CÚBICOS)      │ Muy suave  │ Complejo      │ Datos  │
│                                   │ Estable    │ Oscila con    │ suaves │
│                                   │ Flexible   │ discontinuidades│      │
└──────────────────────────────────────────────────────────────────────────┘

RECOMENDACIONES:
- Usar LINEAL: datos claramente lineales, cálculos rápidos
- Usar CUADRÁTICO: datos con curvatura moderada, pocas discontinuidades
- Usar SPLINES: datos suaves y continuos, múltiples puntos
""")
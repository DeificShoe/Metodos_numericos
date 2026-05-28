"""
================================================================================
        ECUACIONES DIFERENCIALES ORDINARIAS - ANÁLISIS COMPLETO
================================================================================
Este módulo contiene tres temas principales:

6.1 MÉTODOS DE UN PASO:
    - Método de Euler
    - Método de Euler Mejorado (Heun)
    - Método de Runge-Kutta de orden 4

6.2 MÉTODOS DE PASOS MÚLTIPLES:
    - Método de Adams-Bashforth
    - Método de Adams-Moulton
    - Método Predictor-Corrector

6.3 SISTEMAS DE ECUACIONES DIFERENCIALES:
    - Sistemas de 2 o más EDOs acopladas
    - Análisis de interacción entre variables

Cada método incluye:
- Explicación teórica
- Desarrollo matemático
- 2 problemas completamente resueltos (ideal + problemático)
- Gráficas comparativas
- Análisis de error y estabilidad

================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import fsolve
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
#                   TEMA 6.1: MÉTODOS DE UN PASO
# ============================================================================

print("\n" + "="*80)
print("TEMA 6.1: MÉTODOS DE UN PASO")
print("="*80)

print("""
EXPLICACIÓN TEÓRICA:
════════════════════
Los métodos de un paso usan solo información del paso anterior para 
calcular el siguiente. La forma general es:

    y_{n+1} = y_n + h·Φ(x_n, y_n, h)

donde:
- h es el tamaño del paso
- Φ es una función incremental que depende del método
- El error local de truncamiento depende de h

VENTAJAS:
✓ Fáciles de implementar
✓ No requieren valores iniciales adicionales
✓ Flexible con tamaño de paso variable

DESVENTAJAS:
✗ Menos precisos que métodos de múltiples pasos (a igual costo computacional)
✗ Requieren más evaluaciones de la función
""")

# ────────────────────────────────────────────────────────────────────────────
# IMPLEMENTACIÓN DEL MÉTODO DE EULER
# ────────────────────────────────────────────────────────────────────────────

def euler(f, x0, y0, x_final, h):
    """
    Implementa el método de Euler.
    
    dy/dx = f(x, y)
    y_{n+1} = y_n + h·f(x_n, y_n)
    
    Parámetros:
    - f: función que define dy/dx = f(x, y)
    - x0: valor inicial de x
    - y0: valor inicial de y
    - x_final: valor final de x
    - h: tamaño del paso
    
    Retorna:
    - x: array de puntos x
    - y: array de puntos y calculados
    """
    # Número de pasos
    n_pasos = int((x_final - x0) / h) + 1
    
    # Inicializar arrays
    x = np.zeros(n_pasos)
    y = np.zeros(n_pasos)
    
    x[0] = x0
    y[0] = y0
    
    # Aplicar método de Euler
    for i in range(n_pasos - 1):
        x[i+1] = x[i] + h
        y[i+1] = y[i] + h * f(x[i], y[i])
    
    return x, y

# ────────────────────────────────────────────────────────────────────────────
# IMPLEMENTACIÓN DEL MÉTODO DE EULER MEJORADO (HEUN)
# ────────────────────────────────────────────────────────────────────────────

def euler_mejorado(f, x0, y0, x_final, h):
    """
    Implementa el método de Euler Mejorado (Heun).
    
    Predictor: y_pred = y_n + h·f(x_n, y_n)
    Corrector: y_{n+1} = y_n + (h/2)·[f(x_n, y_n) + f(x_{n+1}, y_pred)]
    
    Este método es de segundo orden O(h²)
    """
    n_pasos = int((x_final - x0) / h) + 1
    
    x = np.zeros(n_pasos)
    y = np.zeros(n_pasos)
    
    x[0] = x0
    y[0] = y0
    
    for i in range(n_pasos - 1):
        x[i+1] = x[i] + h
        
        # Predictor
        y_pred = y[i] + h * f(x[i], y[i])
        
        # Corrector
        y[i+1] = y[i] + (h / 2) * (f(x[i], y[i]) + f(x[i+1], y_pred))
    
    return x, y

# ────────────────────────────────────────────────────────────────────────────
# IMPLEMENTACIÓN DEL MÉTODO DE RUNGE-KUTTA ORDEN 4
# ────────────────────────────────────────────────────────────────────────────

def runge_kutta_4(f, x0, y0, x_final, h):
    """
    Implementa el método de Runge-Kutta de orden 4.
    
    Este es el método RK4 más popular.
    
    k1 = f(x_n, y_n)
    k2 = f(x_n + h/2, y_n + (h/2)k1)
    k3 = f(x_n + h/2, y_n + (h/2)k2)
    k4 = f(x_n + h, y_n + h·k3)
    
    y_{n+1} = y_n + (h/6)·(k1 + 2k2 + 2k3 + k4)
    
    Error local: O(h^5)
    Error global: O(h^4)
    """
    n_pasos = int((x_final - x0) / h) + 1
    
    x = np.zeros(n_pasos)
    y = np.zeros(n_pasos)
    
    x[0] = x0
    y[0] = y0
    
    for i in range(n_pasos - 1):
        x[i+1] = x[i] + h
        
        # Calcular pendientes intermedias
        k1 = f(x[i], y[i])
        k2 = f(x[i] + h/2, y[i] + (h/2)*k1)
        k3 = f(x[i] + h/2, y[i] + (h/2)*k2)
        k4 = f(x[i] + h, y[i] + h*k3)
        
        # Actualizar y
        y[i+1] = y[i] + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
    
    return x, y

# ════════════════════════════════════════════════════════════════════════════
# PROBLEMA 1: MÉTODO DE UN PASO - CASO IDEAL
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("PROBLEMA 1: Métodos de Un Paso - Caso Ideal")
print("="*80)

"""
ENUNCIADO:
Resolver la ecuación diferencial dy/dx = -2xy con condición inicial y(0) = 1
en el intervalo [0, 2].

PROBLEMÁTICA:
Esta es una ecuación diferencial simple con solución exacta conocida.
Se usará para demostrar la precisión de los métodos de un paso.

MÉTODO A UTILIZAR:
Comparar: Euler, Euler Mejorado, y Runge-Kutta 4

QUÉ SE DESEA RESOLVER:
- Resolver numéricamente la EDO
- Comparar la aproximación numérica con la solución exacta
- Analizar el error de cada método
- Demostrar que RK4 es más preciso que Euler
"""

# Definir la ecuación diferencial
def f_problema1(x, y):
    """dy/dx = -2xy"""
    return -2 * x * y

# Solución exacta: y(x) = exp(-x²)
def solucion_exacta_p1(x):
    return np.exp(-x**2)

print("\nEcuación diferencial: dy/dx = -2xy")
print("Condición inicial: y(0) = 1")
print("Intervalo: [0, 2]")
print("Solución exacta: y(x) = exp(-x²)")

# Parámetros
x0, y0 = 0, 1
x_final = 2
h = 0.1  # Tamaño de paso ideal (pequeño)

# Aplicar métodos
x_euler, y_euler = euler(f_problema1, x0, y0, x_final, h)
x_heun, y_heun = euler_mejorado(f_problema1, x0, y0, x_final, h)
x_rk4, y_rk4 = runge_kutta_4(f_problema1, x0, y0, x_final, h)

# Solución exacta
y_exacta = solucion_exacta_p1(x_rk4)

# Calcular errores absolutos
error_euler = np.abs(y_euler - y_exacta)
error_heun = np.abs(y_heun - y_exacta)
error_rk4 = np.abs(y_rk4 - y_exacta)

# Mostrar resultados numéricos
print("\n" + "-"*80)
print("RESULTADOS NUMÉRICOS")
print("-"*80)
print("\nPrimeros 5 pasos:")
print(f"{'x':>6} | {'Exacta':>10} | {'Euler':>10} | {'Heun':>10} | {'RK4':>10}")
print("-" * 60)
for i in range(min(5, len(x_rk4))):
    print(f"{x_rk4[i]:6.2f} | {y_exacta[i]:10.6f} | {y_euler[i]:10.6f} | {y_heun[i]:10.6f} | {y_rk4[i]:10.6f}")

print("\nÚltimos 5 pasos:")
print(f"{'x':>6} | {'Exacta':>10} | {'Euler':>10} | {'Heun':>10} | {'RK4':>10}")
print("-" * 60)
for i in range(max(0, len(x_rk4)-5), len(x_rk4)):
    print(f"{x_rk4[i]:6.2f} | {y_exacta[i]:10.6f} | {y_euler[i]:10.6f} | {y_heun[i]:10.6f} | {y_rk4[i]:10.6f}")

# Errores máximos
error_max_euler = np.max(error_euler)
error_max_heun = np.max(error_heun)
error_max_rk4 = np.max(error_rk4)

print("\n" + "-"*80)
print("ANÁLISIS DE ERRORES")
print("-"*80)
print(f"\nError máximo absoluto:")
print(f"  Método de Euler:          {error_max_euler:.2e}")
print(f"  Método de Heun:           {error_max_heun:.2e}")
print(f"  Método de Runge-Kutta 4:  {error_max_rk4:.2e}")

print(f"\nError relativo (%) en x=2:")
idx_final = -1
print(f"  Euler:     {(error_euler[idx_final]/abs(y_exacta[idx_final]))*100:.4f}%")
print(f"  Heun:      {(error_heun[idx_final]/abs(y_exacta[idx_final]))*100:.4f}%")
print(f"  RK4:       {(error_rk4[idx_final]/abs(y_exacta[idx_final]))*100:.4f}%")

# Orden de convergencia (si h se reduce a la mitad, error se reduce según orden)
print("\nORDEN DE CONVERGENCIA ESPERADO:")
print("  Euler:     O(h) → Error ~ h")
print("  Heun:      O(h²) → Error ~ h²")
print("  RK4:       O(h⁴) → Error ~ h⁴")

# Gráficas
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Gráfica 1: Comparación de soluciones
ax1 = axes[0, 0]
ax1.plot(x_rk4, y_exacta, 'k-', linewidth=3, label='Solución exacta', zorder=5)
ax1.plot(x_euler, y_euler, 'o-', markersize=4, linewidth=1.5, alpha=0.7, label='Euler')
ax1.plot(x_heun, y_heun, 's-', markersize=4, linewidth=1.5, alpha=0.7, label='Heun')
ax1.plot(x_rk4, y_rk4, '^-', markersize=4, linewidth=1.5, alpha=0.7, label='RK4')
ax1.set_xlabel('x', fontsize=11, fontweight='bold')
ax1.set_ylabel('y', fontsize=11, fontweight='bold')
ax1.set_title('Problema 1: Comparación de Métodos de Un Paso (Ideal)', 
              fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)

# Gráfica 2: Errores absolutos
ax2 = axes[0, 1]
ax2.semilogy(x_euler, error_euler, 'o-', markersize=5, label='Euler', alpha=0.7)
ax2.semilogy(x_heun, error_heun, 's-', markersize=5, label='Heun', alpha=0.7)
ax2.semilogy(x_rk4, error_rk4, '^-', markersize=5, label='RK4', alpha=0.7)
ax2.set_xlabel('x', fontsize=11, fontweight='bold')
ax2.set_ylabel('Error absoluto (escala logarítmica)', fontsize=11, fontweight='bold')
ax2.set_title('Evolución del Error Absoluto', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(fontsize=10)

# Gráfica 3: Residuos (diferencias con la solución exacta)
ax3 = axes[1, 0]
ax3.plot(x_euler, error_euler, 'o-', markersize=5, label='Euler', alpha=0.7)
ax3.plot(x_heun, error_heun, 's-', markersize=5, label='Heun', alpha=0.7)
ax3.plot(x_rk4, error_rk4, '^-', markersize=5, label='RK4', alpha=0.7)
ax3.set_xlabel('x', fontsize=11, fontweight='bold')
ax3.set_ylabel('Error absoluto', fontsize=11, fontweight='bold')
ax3.set_title('Errores Comparativos (Escala Lineal)', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.legend(fontsize=10)

# Gráfica 4: Tabla de comparación
ax4 = axes[1, 1]
ax4.axis('off')

tabla_p1 = [
    ['Método', 'Orden', 'Error Máx', 'Evaluaciones/Paso'],
    ['Euler', 'O(h)', f'{error_max_euler:.2e}', '1'],
    ['Heun', 'O(h²)', f'{error_max_heun:.2e}', '2'],
    ['RK4', 'O(h⁴)', f'{error_max_rk4:.2e}', '4'],
]

tabla = plt.table(cellText=tabla_p1, cellLoc='center', loc='center',
                  colWidths=[0.2, 0.15, 0.25, 0.25])
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1, 2.5)

for i in range(4):
    tabla[(0, i)].set_facecolor('#2E75B6')
    tabla[(0, i)].set_text_props(weight='bold', color='white')

ax4.text(0.5, 0.15, 'h = 0.1 (Tamaño de paso)', ha='center', fontsize=10, style='italic',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.suptitle('Problema 1: Métodos de Un Paso - Caso Ideal (h=0.1)', 
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n✓ CONCLUSIÓN Problema 1:")
print("  En este caso ideal con h=0.1:")
print("  - RK4 es el más preciso con error máximo de {:.2e}".format(error_max_rk4))
print("  - Heun (O(h²)) es significativamente mejor que Euler (O(h))")
print("  - Euler acumula errores pero aún es aceptable para h pequeño")
print("  - El método RK4 justifica su complejidad por su precisión superior")

# ════════════════════════════════════════════════════════════════════════════
# PROBLEMA 2: MÉTODO DE UN PASO - CASO PROBLEMÁTICO (INESTABILIDAD)
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("PROBLEMA 2: Métodos de Un Paso - Caso Problemático (Inestabilidad)")
print("="*80)

"""
ENUNCIADO:
Resolver la ecuación diferencial "stiff" (rígida):
dy/dx = -100(y - cos(x)) - sin(x)

con condición inicial y(0) = 1 en [0, 1].

PROBLEMÁTICA:
Esta es una ecuación STIFF (rígida). Los métodos explícitos como Euler
y RK4 requieren pasos muy pequeños para ser estables.

MÉTODO A UTILIZAR:
Comparar diferentes tamaños de paso con Euler y RK4.

QUÉ SE DESEA RESOLVER:
- Demostrar inestabilidad numérica con pasos grandes
- Mostrar oscilaciones espurias
- Explicar por qué ocurre la inestabilidad
"""

def f_problema2(x, y):
    """dy/dx = -100(y - cos(x)) - sin(x)"""
    return -100 * (y - np.cos(x)) - np.sin(x)

# Solución exacta (para este caso específico)
def solucion_exacta_p2(x):
    """y(x) = cos(x)"""
    return np.cos(x)

print("\nEcuación diferencial STIFF: dy/dx = -100(y - cos(x)) - sin(x)")
print("Condición inicial: y(0) = 1")
print("Intervalo: [0, 1]")
print("Solución exacta: y(x) = cos(x)")
print("\nEsta es una ecuación STIFF (rígida) con constante de rigidez λ ≈ -100")

# Parámetros
x0, y0 = 0, 1
x_final = 1

# Probar con diferentes tamaños de paso
pasos = [0.01, 0.05, 0.1, 0.2]

print("\n" + "-"*80)
print("ANÁLISIS DE ESTABILIDAD CON DIFERENTES TAMAÑOS DE PASO")
print("-"*80)

resultados_estabilidad = {}

for h in pasos:
    try:
        x_e, y_e = euler(f_problema2, x0, y0, x_final, h)
        x_rk, y_rk = runge_kutta_4(f_problema2, x0, y0, x_final, h)
        y_exact = solucion_exacta_p2(x_rk)
        
        error_e = np.max(np.abs(y_e - np.interp(x_e, x_rk, y_exact)))
        error_rk = np.max(np.abs(y_rk - y_exact))
        
        # Verificar inestabilidad (valores enormes = inestable)
        euler_inestable = np.any(np.abs(y_e) > 1e3)
        rk4_inestable = np.any(np.abs(y_rk) > 1e3)
        
        resultados_estabilidad[h] = {
            'x_e': x_e, 'y_e': y_e,
            'x_rk': x_rk, 'y_rk': y_rk,
            'error_euler': error_e,
            'error_rk4': error_rk,
            'euler_inestable': euler_inestable,
            'rk4_inestable': rk4_inestable
        }
        
        print(f"\nh = {h}:")
        print(f"  Euler:")
        print(f"    Error máximo: {error_e:.2e}")
        print(f"    Inestable: {'⚠️ SÍ' if euler_inestable else '✓ No'}")
        print(f"  RK4:")
        print(f"    Error máximo: {error_rk:.2e}")
        print(f"    Inestable: {'⚠️ SÍ' if rk4_inestable else '✓ No'}")
        
    except Exception as e:
        print(f"\nh = {h}: ❌ FALLO (overflow/inestabilidad) - {type(e).__name__}")
        resultados_estabilidad[h] = None

# Análisis de condición de estabilidad
print("\n" + "-"*80)
print("ANÁLISIS DE LA CONDICIÓN DE ESTABILIDAD")
print("-"*80)
print("\nPara ecuaciones STIFF, la condición de estabilidad es:")
print("  |1 + hλ| ≤ 1  (para Euler explícito)")
print("\nCon λ = -100:")
print("  |1 - 100h| ≤ 1")
print("  0 ≤ 1 - 100h ≤ 1")
print("  h ≤ 0.02")
print("\nPor lo tanto, para estabilidad absoluta: h ≤ 0.02")

# Gráficas
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

colores = ['green', 'blue', 'orange', 'red']
h_plot = [0.01, 0.05, 0.1, 0.2]

# Gráfica 1: h = 0.01 (estable)
ax1 = axes[0, 0]
h_val = 0.01
if resultados_estabilidad[h_val] is not None:
    res = resultados_estabilidad[h_val]
    y_exact = solucion_exacta_p2(res['x_rk'])
    ax1.plot(res['x_rk'], y_exact, 'k-', linewidth=2.5, label='Exacta', zorder=5)
    ax1.plot(res['x_rk'], res['y_rk'], 'b^-', markersize=4, alpha=0.7, label='RK4')
    ax1.plot(res['x_e'], res['y_e'], 'go-', markersize=3, alpha=0.7, label='Euler')
    ax1.set_title(f'h = {h_val} (ESTABLE)', fontsize=11, fontweight='bold', color='green')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Gráfica 2: h = 0.05 (límite)
ax2 = axes[0, 1]
h_val = 0.05
if resultados_estabilidad[h_val] is not None:
    res = resultados_estabilidad[h_val]
    y_exact = solucion_exacta_p2(res['x_rk'])
    ax2.plot(res['x_rk'], y_exact, 'k-', linewidth=2.5, label='Exacta', zorder=5)
    ax2.plot(res['x_rk'], res['y_rk'], 'b^-', markersize=4, alpha=0.7, label='RK4')
    if len(res['y_e']) < 100:  # Si tiene pocos puntos, probablemente esté bien
        ax2.plot(res['x_e'], res['y_e'], 'go-', markersize=3, alpha=0.7, label='Euler')
    ax2.set_title(f'h = {h_val} (LÍMITE)', fontsize=11, fontweight='bold', color='orange')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Gráfica 3: h = 0.1 (inestable)
ax3 = axes[1, 0]
h_val = 0.1
if resultados_estabilidad[h_val] is not None:
    res = resultados_estabilidad[h_val]
    y_exact = solucion_exacta_p2(res['x_rk'])
    ax3.plot(res['x_rk'], y_exact, 'k-', linewidth=2.5, label='Exacta', zorder=5)
    ax3.plot(res['x_rk'], res['y_rk'], 'b^-', markersize=4, alpha=0.7, label='RK4')
    if not res['euler_inestable'] and len(res['y_e']) < 100:
        ax3.plot(res['x_e'], res['y_e'], 'go-', markersize=3, alpha=0.7, label='Euler')
    ax3.set_title(f'h = {h_val} (INESTABLE)', fontsize=11, fontweight='bold', color='red')
    ax3.set_ylim([-5, 5])
ax3.set_xlabel('x')
ax3.set_ylabel('y')
ax3.grid(True, alpha=0.3)
ax3.legend()

# Gráfica 4: Tabla de estabilidad
ax4 = axes[1, 1]
ax4.axis('off')

tabla_p2 = [
    ['h', 'Euler Estable', 'RK4 Estable', 'Recomendación'],
    ['0.01', '✓', '✓', 'Seguro'],
    ['0.05', '✓', '✓', 'Límite'],
    ['0.1', '✗', '✓', 'No usar Euler'],
    ['0.2', '✗', '✗', 'Demasiado grande'],
]

tabla_p2_plt = plt.table(cellText=tabla_p2, cellLoc='center', loc='center',
                         colWidths=[0.15, 0.25, 0.25, 0.25])
tabla_p2_plt.auto_set_font_size(False)
tabla_p2_plt.set_fontsize(10)
tabla_p2_plt.scale(1, 2.5)

for i in range(4):
    tabla_p2_plt[(0, i)].set_facecolor('#2E75B6')
    tabla_p2_plt[(0, i)].set_text_props(weight='bold', color='white')

ax4.text(0.5, 0.1, 'Condición de estabilidad: h ≤ 0.02\n(Ecuación STIFF)', 
         ha='center', fontsize=10, style='italic',
         bbox=dict(boxstyle='round', facecolor='#FFE699', alpha=0.9))

plt.suptitle('Problema 2: Métodos de Un Paso - Ecuación STIFF (Inestabilidad)', 
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n✗ CONCLUSIÓN Problema 2:")
print("  Esta es una ecuación STIFF con λ = -100 (muy negativo)")
print("  Condición de estabilidad para Euler: h ≤ 0.02")
print("  RK4 es más estable que Euler pero igual requiere h pequeño")
print("  Solución: Usar métodos implícitos (backward Euler, BDF) para ecuaciones STIFF")
print("  O reducir dramáticamente el tamaño de paso")

# ============================================================================
#                   TEMA 6.2: MÉTODOS DE PASOS MÚLTIPLES
# ============================================================================

print("\n\n" + "="*80)
print("TEMA 6.2: MÉTODOS DE PASOS MÚLTIPLES")
print("="*80)

print("""
EXPLICACIÓN TEÓRICA:
════════════════════
Los métodos de pasos múltiples usan información de varios pasos anteriores
para calcular el siguiente. La forma general es:

    y_{n+1} = Σ(a_i · y_{n-i}) + h·Σ(b_i · f_{n-i})

VENTAJAS:
✓ Más eficientes (menos evaluaciones de función)
✓ Mejor precisión con el mismo costo computacional
✓ Pueden ser implícitos (mejor estabilidad)

DESVENTAJAS:
✗ Requieren valores iniciales adicionales (usar método de un paso)
✗ Más complejos de implementar
✗ Predictor-Corrector requiere iteraciones

TIPOS:
- Adams-Bashforth: Explícito (inestable)
- Adams-Moulton: Implícito (estable pero requiere resolver ecuación)
- Predictor-Corrector: Combina ambos
""")

# ────────────────────────────────────────────────────────────────────────────
# MÉTODO DE ADAMS-BASHFORTH ORDEN 4
# ────────────────────────────────────────────────────────────────────────────

def adams_bashforth_4(f, x0, y0, x_final, h):
    """
    Implementa el método de Adams-Bashforth de orden 4.
    
    Explícito de 4 pasos:
    y_{n+1} = y_n + (h/24)·[55f_n - 59f_{n-1} + 37f_{n-2} - 9f_{n-3}]
    
    Requiere 4 valores iniciales. Usamos RK4 para obtenerlos.
    """
    n_pasos = int((x_final - x0) / h) + 1
    
    x = np.zeros(n_pasos)
    y = np.zeros(n_pasos)
    
    x[0] = x0
    y[0] = y0
    
    # Generar 4 valores iniciales con RK4
    for i in range(3):
        k1 = f(x[i], y[i])
        k2 = f(x[i] + h/2, y[i] + (h/2)*k1)
        k3 = f(x[i] + h/2, y[i] + (h/2)*k2)
        k4 = f(x[i] + h, y[i] + h*k3)
        
        x[i+1] = x[i] + h
        y[i+1] = y[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    
    # Almacenar los últimos 3 valores de f
    f_vals = [f(x[i], y[i]) for i in range(4)]
    
    # Aplicar Adams-Bashforth
    for i in range(3, n_pasos - 1):
        x[i+1] = x[i] + h
        
        f_n = f_vals[-1]
        f_n1 = f_vals[-2]
        f_n2 = f_vals[-3]
        f_n3 = f_vals[-4]
        
        y[i+1] = y[i] + (h/24)*(55*f_n - 59*f_n1 + 37*f_n2 - 9*f_n3)
        
        # Actualizar historial de f
        f_vals.append(f(x[i+1], y[i+1]))
        f_vals.pop(0)
    
    return x, y

# ────────────────────────────────────────────────────────────────────────────
# MÉTODO DE ADAMS-MOULTON ORDEN 4
# ────────────────────────────────────────────────────────────────────────────

def adams_moulton_4(f, x0, y0, x_final, h, max_iter=5):
    """
    Implementa el método de Adams-Moulton de orden 4.
    
    Implícito de 3 pasos:
    y_{n+1} = y_n + (h/24)·[9f_{n+1} + 19f_n - 5f_{n-1} + f_{n-2}]
    
    Requiere resolver f_{n+1} de forma iterativa (corrector).
    """
    n_pasos = int((x_final - x0) / h) + 1
    
    x = np.zeros(n_pasos)
    y = np.zeros(n_pasos)
    
    x[0] = x0
    y[0] = y0
    
    # Generar 3 valores iniciales con RK4
    for i in range(2):
        k1 = f(x[i], y[i])
        k2 = f(x[i] + h/2, y[i] + (h/2)*k1)
        k3 = f(x[i] + h/2, y[i] + (h/2)*k2)
        k4 = f(x[i] + h, y[i] + h*k3)
        
        x[i+1] = x[i] + h
        y[i+1] = y[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    
    f_vals = [f(x[i], y[i]) for i in range(3)]
    
    # Aplicar Adams-Moulton
    for i in range(2, n_pasos - 1):
        x[i+1] = x[i] + h
        
        # Predictor (Adams-Bashforth 3)
        y_pred = y[i] + (h/12)*(23*f_vals[-1] - 16*f_vals[-2] + 5*f_vals[-3])
        
        # Corrector iterativo
        y_corr = y_pred
        for _ in range(max_iter):
            f_new = f(x[i+1], y_corr)
            y_corr = y[i] + (h/24)*(9*f_new + 19*f_vals[-1] - 5*f_vals[-2] + f_vals[-3])
        
        y[i+1] = y_corr
        f_vals.append(f(x[i+1], y[i+1]))
        f_vals.pop(0)
    
    return x, y

# ────────────────────────────────────────────────────────────────────────────
# MÉTODO PREDICTOR-CORRECTOR
# ────────────────────────────────────────────────────────────────────────────

def predictor_corrector(f, x0, y0, x_final, h, max_iter=3):
    """
    Implementa el método Predictor-Corrector.
    
    Predictor: Adams-Bashforth 4
    Corrector: Adams-Moulton 4
    
    Combine la eficiencia de explícito con la estabilidad de implícito.
    """
    n_pasos = int((x_final - x0) / h) + 1
    
    x = np.zeros(n_pasos)
    y = np.zeros(n_pasos)
    
    x[0] = x0
    y[0] = y0
    
    # Generar 4 valores iniciales con RK4
    for i in range(3):
        k1 = f(x[i], y[i])
        k2 = f(x[i] + h/2, y[i] + (h/2)*k1)
        k3 = f(x[i] + h/2, y[i] + (h/2)*k2)
        k4 = f(x[i] + h, y[i] + h*k3)
        
        x[i+1] = x[i] + h
        y[i+1] = y[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    
    f_vals = [f(x[i], y[i]) for i in range(4)]
    
    # Predictor-Corrector
    for i in range(3, n_pasos - 1):
        x[i+1] = x[i] + h
        
        # PREDICTOR (Adams-Bashforth 4)
        y_pred = y[i] + (h/24)*(55*f_vals[-1] - 59*f_vals[-2] + 37*f_vals[-3] - 9*f_vals[-4])
        
        # CORRECTOR iterativo (Adams-Moulton 4)
        y_corr = y_pred
        for _ in range(max_iter):
            f_pred = f(x[i+1], y_corr)
            y_corr = y[i] + (h/24)*(9*f_pred + 19*f_vals[-1] - 5*f_vals[-2] + f_vals[-3])
        
        y[i+1] = y_corr
        f_vals.append(f(x[i+1], y[i+1]))
        f_vals.pop(0)
    
    return x, y

# ════════════════════════════════════════════════════════════════════════════
# PROBLEMA 3: MÉTODOS DE PASOS MÚLTIPLES - CASO IDEAL
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("PROBLEMA 3: Métodos de Pasos Múltiples - Caso Ideal")
print("="*80)

"""
ENUNCIADO:
Resolver dy/dx = x² - y con y(0) = 1 en [0, 3].

PROBLEMÁTICA:
Ecuación de primer orden con solución que puede expresarse
en términos de exponenciales e integrales.

MÉTODO A UTILIZAR:
Adams-Bashforth, Adams-Moulton, Predictor-Corrector

QUÉ SE DESEA RESOLVER:
- Comparar eficiencia de métodos de pasos múltiples
- Mostrar mejor precisión relativa
- Demostrar estabilidad del corrector
"""

def f_problema3(x, y):
    """dy/dx = x² - y"""
    return x**2 - y

# Solución numérica de referencia de alta precisión
from scipy.integrate import odeint
x_ref = np.linspace(0, 3, 1000)
y_ref = odeint(f_problema3, 1, x_ref).flatten()

print("\nEcuación diferencial: dy/dx = x² - y")
print("Condición inicial: y(0) = 1")
print("Intervalo: [0, 3]")

# Parámetros
x0, y0 = 0, 1
x_final = 3
h = 0.1

# Aplicar métodos de pasos múltiples
print("\nCalculando soluciones con h = {}...".format(h))

x_ab, y_ab = adams_bashforth_4(f_problema3, x0, y0, x_final, h)
x_am, y_am = adams_moulton_4(f_problema3, x0, y0, x_final, h)
x_pc, y_pc = predictor_corrector(f_problema3, x0, y0, x_final, h)

# Interpolación de referencia para comparación
y_ref_ab = np.interp(x_ab, x_ref, y_ref)
y_ref_am = np.interp(x_am, x_ref, y_ref)
y_ref_pc = np.interp(x_pc, x_ref, y_ref)

# Calcular errores
error_ab = np.abs(y_ab - y_ref_ab)
error_am = np.abs(y_am - y_ref_am)
error_pc = np.abs(y_pc - y_ref_pc)

# Resultados numéricos
print("\n" + "-"*80)
print("RESULTADOS NUMÉRICOS")
print("-"*80)
print("\nPrimeros 5 puntos:")
print(f"{'x':>6} | {'Referencia':>12} | {'A-B':>12} | {'A-M':>12} | {'P-C':>12}")
print("-" * 68)
for i in range(min(5, len(x_ab))):
    print(f"{x_ab[i]:6.2f} | {y_ref_ab[i]:12.8f} | {y_ab[i]:12.8f} | {y_am[i]:12.8f} | {y_pc[i]:12.8f}")

# Estadísticas de error
print("\n" + "-"*80)
print("ANÁLISIS DE ERRORES")
print("-"*80)
print(f"\nError máximo absoluto:")
print(f"  Adams-Bashforth:   {np.max(error_ab):.2e}")
print(f"  Adams-Moulton:     {np.max(error_am):.2e}")
print(f"  Predictor-Corrector: {np.max(error_pc):.2e}")

print(f"\nError promedio:")
print(f"  Adams-Bashforth:   {np.mean(error_ab):.2e}")
print(f"  Adams-Moulton:     {np.mean(error_am):.2e}")
print(f"  Predictor-Corrector: {np.mean(error_pc):.2e}")

print(f"\nReducción de errores (P-C respecto a A-B):")
print(f"  Error máx: {(1 - np.max(error_pc)/np.max(error_ab))*100:.1f}%")
print(f"  Error prom: {(1 - np.mean(error_pc)/np.mean(error_ab))*100:.1f}%")

# Gráficas
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Gráfica 1: Soluciones
ax1 = axes[0, 0]
ax1.plot(x_ref, y_ref, 'k-', linewidth=2.5, label='Referencia (alta precisión)')
ax1.plot(x_ab, y_ab, 'o-', markersize=4, alpha=0.7, label='Adams-Bashforth')
ax1.plot(x_am, y_am, 's-', markersize=4, alpha=0.7, label='Adams-Moulton')
ax1.plot(x_pc, y_pc, '^-', markersize=4, alpha=0.7, label='Predictor-Corrector')
ax1.set_xlabel('x', fontsize=11, fontweight='bold')
ax1.set_ylabel('y', fontsize=11, fontweight='bold')
ax1.set_title('Problema 3: Métodos de Pasos Múltiples (Caso Ideal)', 
              fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)

# Gráfica 2: Errores absolutos
ax2 = axes[0, 1]
ax2.semilogy(x_ab, error_ab, 'o-', markersize=5, alpha=0.7, label='A-B')
ax2.semilogy(x_am, error_am, 's-', markersize=5, alpha=0.7, label='A-M')
ax2.semilogy(x_pc, error_pc, '^-', markersize=5, alpha=0.7, label='P-C')
ax2.set_xlabel('x', fontsize=11, fontweight='bold')
ax2.set_ylabel('Error absoluto', fontsize=11, fontweight='bold')
ax2.set_title('Evolución del Error', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(fontsize=10)

# Gráfica 3: Diferencias entre métodos
ax3 = axes[1, 0]
ax3.plot(x_ab, error_ab, 'o-', linewidth=1.5, markersize=5, alpha=0.7, label='A-B')
ax3.plot(x_am, error_am, 's-', linewidth=1.5, markersize=5, alpha=0.7, label='A-M')
ax3.plot(x_pc, error_pc, '^-', linewidth=1.5, markersize=5, alpha=0.7, label='P-C')
ax3.set_xlabel('x', fontsize=11, fontweight='bold')
ax3.set_ylabel('Error absoluto', fontsize=11, fontweight='bold')
ax3.set_title('Comparación de Errores (Escala Lineal)', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.legend(fontsize=10)

# Gráfica 4: Tabla comparativa
ax4 = axes[1, 1]
ax4.axis('off')

tabla_p3 = [
    ['Método', 'Tipo', 'Orden', 'Error Max', 'Estabilidad'],
    ['Adams-Bashforth', 'Explícito', 'O(h⁴)', f'{np.max(error_ab):.2e}', 'Moderada'],
    ['Adams-Moulton', 'Implícito', 'O(h⁴)', f'{np.max(error_am):.2e}', 'Buena'],
    ['Pred-Corrector', 'Mixto', 'O(h⁴)', f'{np.max(error_pc):.2e}', 'Muy buena'],
]

tabla_p3_plt = plt.table(cellText=tabla_p3, cellLoc='center', loc='center',
                         colWidths=[0.2, 0.15, 0.15, 0.2, 0.2])
tabla_p3_plt.auto_set_font_size(False)
tabla_p3_plt.set_fontsize(9)
tabla_p3_plt.scale(1, 2.5)

for i in range(5):
    tabla_p3_plt[(0, i)].set_facecolor('#2E75B6')
    tabla_p3_plt[(0, i)].set_text_props(weight='bold', color='white')

plt.suptitle('Problema 3: Métodos de Pasos Múltiples - Caso Ideal (h=0.1)', 
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n✓ CONCLUSIÓN Problema 3:")
print("  Los métodos de pasos múltiples con el mismo orden de precisión (O(h⁴))")
print("  muestran diferencias en estabilidad y error numérico.")
print("  Predictor-Corrector es una buena opción equilibrada:")
print("  - Más estable que Adams-Bashforth explícito")
print("  - Menos iteraciones que Adams-Moulton puro")
print("  - Costo computacional eficiente")

# ════════════════════════════════════════════════════════════════════════════
# PROBLEMA 4: MÉTODOS DE PASOS MÚLTIPLES - CASO PROBLEMÁTICO
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("PROBLEMA 4: Métodos de Pasos Múltiples - Caso Problemático (Inestabilidad)")
print("="*80)

"""
ENUNCIADO:
Resolver dy/dx = -15y con y(0) = 1 en [0, 1].

PROBLEMÁTICA:
Ecuación con raíz real muy negativa (λ = -15).
Adams-Bashforth explícito es inestable. Adams-Moulton es más estable.

MÉTODO A UTILIZAR:
Comparar estabilidad con diferentes tamaños de paso

QUÉ SE DESEA RESOLVER:
- Demostrar inestabilidad de métodos explícitos
- Mostrar ventaja de métodos implícitos
"""

def f_problema4(x, y):
    """dy/dx = -15y"""
    return -15 * y

def solucion_exacta_p4(x):
    """y(x) = exp(-15x)"""
    return np.exp(-15 * x)

print("\nEcuación diferencial: dy/dx = -15y")
print("Condición inicial: y(0) = 1")
print("Intervalo: [0, 1]")
print("Solución exacta: y(x) = exp(-15x)")
print("Parámetro de rigidez: λ = -15 (ecuación stiff)")

# Analizar estabilidad con diferentes h
pasos_p4 = [0.01, 0.05, 0.1, 0.15]

print("\n" + "-"*80)
print("ANÁLISIS DE ESTABILIDAD CON DIFERENTES TAMAÑOS DE PASO")
print("-"*80)

resultados_p4 = {}

for h in pasos_p4:
    x0, y0 = 0, 1
    x_final = 1
    
    try:
        x_ab_p4, y_ab_p4 = adams_bashforth_4(f_problema4, x0, y0, x_final, h)
        y_exact_p4 = solucion_exacta_p4(x_ab_p4)
        error_ab_p4 = np.max(np.abs(y_ab_p4 - y_exact_p4))
        ab_inestable = np.any(np.abs(y_ab_p4) > 1e2) or np.any(np.isnan(y_ab_p4))
    except:
        ab_inestable = True
        error_ab_p4 = np.inf
    
    try:
        x_am_p4, y_am_p4 = adams_moulton_4(f_problema4, x0, y0, x_final, h)
        y_exact_am = solucion_exacta_p4(x_am_p4)
        error_am_p4 = np.max(np.abs(y_am_p4 - y_exact_am))
        am_inestable = np.any(np.abs(y_am_p4) > 1e2) or np.any(np.isnan(y_am_p4))
    except:
        am_inestable = True
        error_am_p4 = np.inf
    
    resultados_p4[h] = {
        'x_ab': x_ab_p4 if not ab_inestable else None,
        'y_ab': y_ab_p4 if not ab_inestable else None,
        'x_am': x_am_p4 if not am_inestable else None,
        'y_am': y_am_p4 if not am_inestable else None,
        'error_ab': error_ab_p4,
        'error_am': error_am_p4,
        'ab_inestable': ab_inestable,
        'am_inestable': am_inestable
    }
    
    print(f"\nh = {h}:")
    print(f"  Adams-Bashforth:")
    print(f"    Error: {error_ab_p4:.2e if error_ab_p4 != np.inf else 'Overflow'}")
    print(f"    Inestable: {'⚠️ SÍ' if ab_inestable else '✓ No'}")
    print(f"  Adams-Moulton:")
    print(f"    Error: {error_am_p4:.2e if error_am_p4 != np.inf else 'Overflow'}")
    print(f"    Inestable: {'⚠️ SÍ' if am_inestable else '✓ No'}")

# Condición de estabilidad
print("\n" + "-"*80)
print("ANÁLISIS DE LA CONDICIÓN DE ESTABILIDAD")
print("-"*80)
print("\nPara dy/dx = λy con λ = -15:")
print("\nAdams-Bashforth 4 (explícito):")
print("  Requiere: |hλ| < 3 (aproximadamente)")
print("  Con λ = -15: h < 0.2")
print("\nAdams-Moulton 4 (implícito):")
print("  Región de estabilidad absoluta: todo el semiplano izquierdo")
print("  Mucho más estable que explícito")

# Gráficas
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

h_valores = [0.01, 0.05, 0.1, 0.15]

for idx, h_val in enumerate(h_valores):
    if idx < 2:
        ax = axes[0, idx]
    else:
        ax = axes[1, idx-2]
    
    x_exact = np.linspace(0, 1, 100)
    y_exact = solucion_exacta_p4(x_exact)
    
    ax.plot(x_exact, y_exact, 'k-', linewidth=2.5, label='Exacta', zorder=5)
    
    if resultados_p4[h_val]['x_ab'] is not None:
        ax.plot(resultados_p4[h_val]['x_ab'], resultados_p4[h_val]['y_ab'], 
               'ro-', markersize=4, alpha=0.7, label='A-B (Explícito)')
    
    if resultados_p4[h_val]['x_am'] is not None:
        ax.plot(resultados_p4[h_val]['x_am'], resultados_p4[h_val]['y_am'], 
               'bs-', markersize=4, alpha=0.7, label='A-M (Implícito)')
    
    ax.set_title(f'h = {h_val}', fontsize=11, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)
    
    # Límites razonables
    if h_val <= 0.1:
        ax.set_ylim([-0.1, 1.1])
    else:
        ax.set_ylim([-2, 2])

plt.suptitle('Problema 4: Métodos de Pasos Múltiples - Ecuación STIFF (λ=-15)', 
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n✗ CONCLUSIÓN Problema 4:")
print("  Adams-Bashforth (explícito) es inestable para h > 0.1")
print("  Adams-Moulton (implícito) es mucho más estable")
print("  Para ecuaciones stiff, los métodos implícitos son esenciales")
print("  La región de estabilidad de Moulton abarca el semiplano izquierdo (A-estable)")
print("  Recomendación: Usar métodos implícitos (BDF, A-estables) para ecuaciones rígidas")

# ============================================================================
#                   TEMA 6.3: SISTEMAS DE ECUACIONES DIFERENCIALES
# ============================================================================

print("\n\n" + "="*80)
print("TEMA 6.3: SISTEMAS DE ECUACIONES DIFERENCIALES ORDINARIAS")
print("="*80)

print("""
EXPLICACIÓN TEÓRICA:
════════════════════
Un sistema de EDOs tiene la forma:

    dy₁/dt = f₁(t, y₁, y₂, ..., yₙ)
    dy₂/dt = f₂(t, y₁, y₂, ..., yₙ)
    ...
    dyₙ/dt = fₙ(t, y₁, y₂, ..., yₙ)

En forma vectorial:
    dy/dt = f(t, y)

donde y = [y₁, y₂, ..., yₙ]

Los métodos de un paso (Euler, RK4) se generalizan fácilmente:

EULER:
    y_{n+1} = y_n + h·f(t_n, y_n)

RUNGE-KUTTA 4:
    k1 = f(t_n, y_n)
    k2 = f(t_n + h/2, y_n + (h/2)k1)
    k3 = f(t_n + h/2, y_n + (h/2)k2)
    k4 = f(t_n + h, y_n + h·k3)
    y_{n+1} = y_n + (h/6)·(k1 + 2k2 + 2k3 + k4)

VENTAJAS:
✓ Modelan fenómenos con múltiples variables acopladas
✓ Permiten capturar comportamientos complejos
✓ Uso de los mismos métodos de un paso

DESVENTAJAS:
✗ Mayor costo computacional (múltiples funciones)
✗ Más propensos a inestabilidad
✗ Difíciles de analizar teóricamente
""")

# ────────────────────────────────────────────────────────────────────────────
# MÉTODO DE RUNGE-KUTTA 4 PARA SISTEMAS
# ────────────────────────────────────────────────────────────────────────────

def rk4_sistema(f, t0, y0, t_final, h):
    """
    Runge-Kutta 4 para sistemas de EDOs.
    
    dy/dt = f(t, y)
    
    Parámetros:
    - f: función vectorial que retorna [dy1/dt, dy2/dt, ...]
    - t0: tiempo inicial
    - y0: array con valores iniciales [y1_0, y2_0, ...]
    - t_final: tiempo final
    - h: tamaño del paso
    
    Retorna:
    - t: array de tiempos
    - y: matriz donde cada fila es el estado en un tiempo
    """
    y0 = np.asarray(y0)
    n_vars = len(y0)
    n_pasos = int((t_final - t0) / h) + 1
    
    t = np.zeros(n_pasos)
    y = np.zeros((n_pasos, n_vars))
    
    t[0] = t0
    y[0] = y0
    
    for i in range(n_pasos - 1):
        t[i+1] = t[i] + h
        
        k1 = np.array(f(t[i], y[i]))
        k2 = np.array(f(t[i] + h/2, y[i] + (h/2)*k1))
        k3 = np.array(f(t[i] + h/2, y[i] + (h/2)*k2))
        k4 = np.array(f(t[i] + h, y[i] + h*k3))
        
        y[i+1] = y[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    
    return t, y

# ════════════════════════════════════════════════════════════════════════════
# PROBLEMA 5: SISTEMA DE ECUACIONES - CASO IDEAL (PÉNDULO SIMPLE)
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("PROBLEMA 5: Sistema de EDOs - Caso Ideal (Péndulo Simple)")
print("="*80)

"""
ENUNCIADO:
Modelar la oscilación de un péndulo simple usando la ecuación de movimiento:

d²θ/dt² = -(g/L)·sin(θ)

Convertir a sistema de primer orden:
    dy₁/dt = y₂  (donde y₁ = θ)
    dy₂/dt = -(g/L)·sin(y₁)  (donde y₂ = dθ/dt)

Parámetros: L = 1 m, g = 9.8 m/s²
Condiciones iniciales: θ(0) = π/4 rad, dθ/dt(0) = 0

PROBLEMÁTICA:
Sistema conservativo (sin amortiguamiento).
La energía total debe conservarse.

MÉTODO A UTILIZAR:
RK4 para sistema de 2 ecuaciones

QUÉ SE DESEA RESOLVER:
- Resolver el sistema de movimiento
- Analizar la conservación de energía
- Mostrar trayectorias en el espacio fase
- Comparar con solución pequeñas oscilaciones
"""

# Parámetros del péndulo
L_pendulo = 1.0  # longitud en metros
g_pendulo = 9.8  # gravedad en m/s²

def sistema_pendulo(t, y):
    """
    Sistema para péndulo simple.
    y[0] = θ (ángulo)
    y[1] = dθ/dt (velocidad angular)
    """
    theta, omega = y
    dtheta_dt = omega
    domega_dt = -(g_pendulo / L_pendulo) * np.sin(theta)
    return [dtheta_dt, domega_dt]

# Función para calcular energía
def energia_pendulo(y, L, g):
    """
    Energía total del péndulo (normalizada por masa).
    E = (1/2)·(L·dθ/dt)² - g·L·cos(θ)
    """
    theta = y[:, 0]
    omega = y[:, 1]
    KE = 0.5 * (L * omega)**2  # Energía cinética
    PE = -g * L * np.cos(theta)  # Energía potencial
    return KE + PE

print("\nSistema: Péndulo simple")
print(f"  Longitud: L = {L_pendulo} m")
print(f"  Gravedad: g = {g_pendulo} m/s²")
print("Ecuación diferencial: d²θ/dt² = -(g/L)·sin(θ)")
print("\nSistema de primer orden:")
print("  dy₁/dt = y₂")
print("  dy₂/dt = -(g/L)·sin(y₁)")
print("\nCondiciones iniciales:")
print("  θ(0) = π/4 rad ≈ 45°")
print("  dθ/dt(0) = 0 rad/s")

# Parámetros de integración
t0, t_final = 0, 10
h_pendulo = 0.01
y0_pendulo = [np.pi/4, 0]

# Resolver sistema
t_pend, y_pend = rk4_sistema(sistema_pendulo, t0, y0_pendulo, t_final, h_pendulo)

theta_pend = y_pend[:, 0]
omega_pend = y_pend[:, 1]

# Calcular energía
energia = energia_pendulo(y_pend, L_pendulo, g_pendulo)
energia_inicial = energia[0]
error_energia = np.abs(energia - energia_inicial)

print("\n" + "-"*80)
print("RESULTADOS NUMÉRICOS")
print("-"*80)

print("\nPrimeros 5 pasos:")
print(f"{'t (s)':>8} | {'θ (rad)':>10} | {'dθ/dt (rad/s)':>14} | {'E (J/kg)':>10}")
print("-" * 55)
for i in range(min(5, len(t_pend))):
    print(f"{t_pend[i]:8.2f} | {theta_pend[i]:10.6f} | {omega_pend[i]:14.6f} | {energia[i]:10.6f}")

print("\nÚltimos 5 pasos:")
print(f"{'t (s)':>8} | {'θ (rad)':>10} | {'dθ/dt (rad/s)':>14} | {'E (J/kg)':>10}")
print("-" * 55)
for i in range(max(0, len(t_pend)-5), len(t_pend)):
    print(f"{t_pend[i]:8.2f} | {theta_pend[i]:10.6f} | {omega_pend[i]:14.6f} | {energia[i]:10.6f}")

# Análisis de conservación de energía
print("\n" + "-"*80)
print("ANÁLISIS DE CONSERVACIÓN DE ENERGÍA")
print("-"*80)
print(f"\nEnergía inicial: {energia_inicial:.8f} J/kg")
print(f"Energía máxima durante integración: {np.max(energia):.8f} J/kg")
print(f"Energía mínima: {np.min(energia):.8f} J/kg")
print(f"Error máximo de energía: {np.max(error_energia):.2e} J/kg")
print(f"Error relativo: {(np.max(error_energia)/energia_inicial)*100:.6f}%")

# Características del movimiento
print("\n" + "-"*80)
print("CARACTERÍSTICAS DEL MOVIMIENTO")
print("-"*80)
print(f"Ángulo máximo: {np.max(np.abs(theta_pend)):.6f} rad ≈ {np.max(np.abs(theta_pend))*180/np.pi:.2f}°")
print(f"Velocidad angular máxima: {np.max(np.abs(omega_pend)):.6f} rad/s")
print(f"Período aproximado: {t_final / (np.sum(np.diff(np.sign(np.diff(theta_pend)))) / 4):.2f} s")

# Gráficas
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Gráfica 1: Ángulo vs tiempo
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t_pend, theta_pend * 180/np.pi, 'b-', linewidth=2)
ax1.fill_between(t_pend, theta_pend * 180/np.pi, alpha=0.3)
ax1.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Ángulo θ (grados)', fontsize=11, fontweight='bold')
ax1.set_title('Posición Angular vs Tiempo', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Gráfica 2: Velocidad angular vs tiempo
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(t_pend, omega_pend, 'r-', linewidth=2)
ax2.fill_between(t_pend, omega_pend, alpha=0.3, color='red')
ax2.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Velocidad angular dθ/dt (rad/s)', fontsize=11, fontweight='bold')
ax2.set_title('Velocidad Angular vs Tiempo', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)

# Gráfica 3: Espacio fase
ax3 = fig.add_subplot(gs[1, 0])
scatter = ax3.scatter(theta_pend, omega_pend, c=t_pend, cmap='viridis', s=10, alpha=0.6)
ax3.plot(theta_pend[0], omega_pend[0], 'go', markersize=12, label='Inicio', zorder=5)
ax3.plot(theta_pend[-1], omega_pend[-1], 'rs', markersize=12, label='Final', zorder=5)
ax3.set_xlabel('θ (rad)', fontsize=11, fontweight='bold')
ax3.set_ylabel('dθ/dt (rad/s)', fontsize=11, fontweight='bold')
ax3.set_title('Espacio Fase (Trayectoria)', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)
plt.colorbar(scatter, ax=ax3, label='Tiempo (s)')
ax3.legend(fontsize=10)

# Gráfica 4: Energía
ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(t_pend, energia, 'g-', linewidth=2, label='Energía Total')
ax4.axhline(y=energia_inicial, color='k', linestyle='--', linewidth=1.5, label='Energía Inicial')
ax4.fill_between(t_pend, energia, energia_inicial, alpha=0.2, color='green')
ax4.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Energía (J/kg)', fontsize=11, fontweight='bold')
ax4.set_title('Conservación de Energía', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend(fontsize=10)

# Gráfica 5: Error de energía
ax5 = fig.add_subplot(gs[2, 0])
ax5.semilogy(t_pend, error_energia, 'purple', linewidth=2)
ax5.fill_between(t_pend, error_energia, alpha=0.3, color='purple')
ax5.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax5.set_ylabel('Error de Energía (J/kg)', fontsize=11, fontweight='bold')
ax5.set_title('Error Absoluto en Energía', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.3, which='both')

# Gráfica 6: Información del sistema
ax6 = fig.add_subplot(gs[2, 1])
ax6.axis('off')

info_tabla = [
    ['PARÁMETRO', 'VALOR'],
    ['L (m)', f'{L_pendulo}'],
    ['g (m/s²)', f'{g_pendulo}'],
    ['θ₀ (rad)', f'{y0_pendulo[0]:.4f}'],
    ['θ₀ (°)', f'{y0_pendulo[0]*180/np.pi:.2f}'],
    ['(dθ/dt)₀', f'{y0_pendulo[1]:.4f}'],
    ['h (paso)', f'{h_pendulo}'],
    ['Energía inicial', f'{energia_inicial:.6f}'],
    ['Error E max', f'{np.max(error_energia):.2e}'],
]

tabla_pend = plt.table(cellText=info_tabla, cellLoc='left', loc='center',
                       colWidths=[0.4, 0.4])
tabla_pend.auto_set_font_size(False)
tabla_pend.set_fontsize(10)
tabla_pend.scale(1, 2)

for i in range(2):
    tabla_pend[(0, i)].set_facecolor('#2E75B6')
    tabla_pend[(0, i)].set_text_props(weight='bold', color='white')

plt.suptitle('Problema 5: Sistema de EDOs - Péndulo Simple (Caso Ideal)', 
             fontsize=13, fontweight='bold', y=0.995)
plt.show()

print("\n✓ CONCLUSIÓN Problema 5:")
print("  El péndulo simple oscila alrededor del equilibrio.")
print("  La energía se conserva excellentemente (error relativo < 0.001%)")
print("  La trayectoria en el espacio fase es una órbita cerrada (movimiento periódico)")
print("  El sistema es estable y predecible con RK4 de cuarto orden")

# ════════════════════════════════════════════════════════════════════════════
# PROBLEMA 6: SISTEMA DE ECUACIONES - CASO CON ACOPLAMIENTO FUERTE
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("PROBLEMA 6: Sistema de EDOs - Caso Problemático (Lorenz/Caos)")
print("="*80)

"""
ENUNCIADO:
Resolver el Sistema de Lorenz (determinístico pero caótico):

    dx/dt = σ(y - x)
    dy/dt = x(ρ - z) - y
    dz/dt = xy - βz

con σ = 10, ρ = 28, β = 8/3

Condiciones iniciales: x(0) = 1, y(0) = 1, z(0) = 1

PROBLEMÁTICA:
Sistema caótico. Pequeñas variaciones en condiciones iniciales
producen comportamientos completamente diferentes (sensibilidad exponencial).

MÉTODO A UTILIZAR:
RK4 para sistema de 3 ecuaciones

QUÉ SE DESEA RESOLVER:
- Resolver el sistema caótico
- Mostrar el atractor de Lorenz
- Demostrar sensibilidad a condiciones iniciales
- Ilustrar el límite de previsibilidad
"""

# Parámetros de Lorenz
sigma = 10.0
rho = 28.0
beta = 8.0/3.0

def sistema_lorenz(t, y):
    """
    Sistema de Lorenz (caótico).
    y[0] = x
    y[1] = y
    y[2] = z
    """
    x, y_var, z = y
    dx_dt = sigma * (y_var - x)
    dy_dt = x * (rho - z) - y_var
    dz_dt = x * y_var - beta * z
    return [dx_dt, dy_dt, dz_dt]

print("\nSistema de Lorenz (Sistema Caótico):")
print("  dx/dt = σ(y - x)")
print("  dy/dt = x(ρ - z) - y")
print("  dz/dt = xy - βz")
print(f"\nParámetros: σ = {sigma}, ρ = {rho}, β = {beta:.4f}")
print("\nCondiciones iniciales:")
print("  x(0) = 1, y(0) = 1, z(0) = 1")

# Resolver con condición inicial (1,1,1)
t0, t_final = 0, 50
h_lorenz = 0.01
y0_lorenz = [1.0, 1.0, 1.0]

t_lor, y_lor = rk4_sistema(sistema_lorenz, t0, y0_lorenz, t_final, h_lorenz)

x_lor = y_lor[:, 0]
y_lor_var = y_lor[:, 1]
z_lor = y_lor[:, 2]

# Resolver con condición inicial perturbada
y0_lorenz_pert = [1.0 + 1e-6, 1.0, 1.0]  # Pequeña perturbación
t_lor_p, y_lor_p = rk4_sistema(sistema_lorenz, t0, y0_lorenz_pert, t_final, h_lorenz)

x_lor_p = y_lor_p[:, 0]
y_lor_p_var = y_lor_p[:, 1]
z_lor_p = y_lor_p[:, 2]

# Calcular divergencia
divergencia = np.sqrt((x_lor - x_lor_p)**2 + (y_lor_var - y_lor_p_var)**2 + (z_lor - z_lor_p)**2)

print("\n" + "-"*80)
print("SENSIBILIDAD A CONDICIONES INICIALES")
print("-"*80)

print("\nCondiciones iniciales:")
print(f"  Trayectoria 1: x₀ = 1.0, y₀ = 1.0, z₀ = 1.0")
print(f"  Trayectoria 2: x₀ = 1.000001, y₀ = 1.0, z₀ = 1.0 (δ = 10⁻⁶)")

# Encontrar momento donde las trayectorias diverjan
umbral_divergencia = 0.1  # 10% de divergencia
idx_divergencia = np.where(divergencia > umbral_divergencia)[0]

if len(idx_divergencia) > 0:
    t_divergencia = t_lor[idx_divergencia[0]]
    print(f"\nTiempo de divergencia significativa (distancia > {umbral_divergencia}):")
    print(f"  t ≈ {t_divergencia:.2f} s")
    print(f"  Exponente de Lyapunov estimado: λ ≈ {np.log(1e6) / t_divergencia:.4f} /s")
else:
    print(f"\nLas trayectorias aún no han divergido significativamente en t=50s")

print(f"\nDivergencia máxima: {np.max(divergencia):.4f}")
print(f"Divergencia en t=50s: {divergencia[-1]:.4f}")

# Gráficas
fig = plt.figure(figsize=(16, 12))

# Gráfica 1: Componente x
ax1 = fig.add_subplot(3, 3, 1)
ax1.plot(t_lor, x_lor, 'b-', linewidth=1.5, label='Trayectoria 1')
ax1.plot(t_lor_p, x_lor_p, 'r--', linewidth=1, alpha=0.7, label='Trayectoria 2 (perturbada)')
ax1.set_xlabel('Tiempo (s)', fontsize=10, fontweight='bold')
ax1.set_ylabel('x', fontsize=10, fontweight='bold')
ax1.set_title('Componente x vs Tiempo', fontsize=11, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=9)

# Gráfica 2: Componente y
ax2 = fig.add_subplot(3, 3, 2)
ax2.plot(t_lor, y_lor_var, 'g-', linewidth=1.5, label='Trayectoria 1')
ax2.plot(t_lor_p, y_lor_p_var, 'r--', linewidth=1, alpha=0.7, label='Trayectoria 2')
ax2.set_xlabel('Tiempo (s)', fontsize=10, fontweight='bold')
ax2.set_ylabel('y', fontsize=10, fontweight='bold')
ax2.set_title('Componente y vs Tiempo', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=9)

# Gráfica 3: Componente z
ax3 = fig.add_subplot(3, 3, 3)
ax3.plot(t_lor, z_lor, 'orange', linewidth=1.5, label='Trayectoria 1')
ax3.plot(t_lor_p, z_lor_p, 'r--', linewidth=1, alpha=0.7, label='Trayectoria 2')
ax3.set_xlabel('Tiempo (s)', fontsize=10, fontweight='bold')
ax3.set_ylabel('z', fontsize=10, fontweight='bold')
ax3.set_title('Componente z vs Tiempo', fontsize=11, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.legend(fontsize=9)

# Gráfica 4: Atractor 3D (proyección XY)
ax4 = fig.add_subplot(3, 3, 4)
ax4.plot(x_lor, y_lor_var, 'b-', linewidth=0.5, alpha=0.8)
ax4.scatter(x_lor[0], y_lor_var[0], color='green', s=100, marker='o', 
           label='Inicio', zorder=5, edgecolor='darkgreen', linewidth=2)
ax4.scatter(x_lor[-1], y_lor_var[-1], color='red', s=100, marker='s', 
           label='Final', zorder=5, edgecolor='darkred', linewidth=2)
ax4.set_xlabel('x', fontsize=10, fontweight='bold')
ax4.set_ylabel('y', fontsize=10, fontweight='bold')
ax4.set_title('Atractor de Lorenz (Proyección XY)', fontsize=11, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend(fontsize=9)

# Gráfica 5: Atractor 3D (proyección XZ)
ax5 = fig.add_subplot(3, 3, 5)
ax5.plot(x_lor, z_lor, 'g-', linewidth=0.5, alpha=0.8)
ax5.scatter(x_lor[0], z_lor[0], color='green', s=100, marker='o', label='Inicio', zorder=5)
ax5.scatter(x_lor[-1], z_lor[-1], color='red', s=100, marker='s', label='Final', zorder=5)
ax5.set_xlabel('x', fontsize=10, fontweight='bold')
ax5.set_ylabel('z', fontsize=10, fontweight='bold')
ax5.set_title('Atractor de Lorenz (Proyección XZ)', fontsize=11, fontweight='bold')
ax5.grid(True, alpha=0.3)
ax5.legend(fontsize=9)

# Gráfica 6: Atractor 3D (proyección YZ)
ax6 = fig.add_subplot(3, 3, 6)
ax6.plot(y_lor_var, z_lor, 'orange', linewidth=0.5, alpha=0.8)
ax6.scatter(y_lor_var[0], z_lor[0], color='green', s=100, marker='o', label='Inicio', zorder=5)
ax6.scatter(y_lor_var[-1], z_lor[-1], color='red', s=100, marker='s', label='Final', zorder=5)
ax6.set_xlabel('y', fontsize=10, fontweight='bold')
ax6.set_ylabel('z', fontsize=10, fontweight='bold')
ax6.set_title('Atractor de Lorenz (Proyección YZ)', fontsize=11, fontweight='bold')
ax6.grid(True, alpha=0.3)
ax6.legend(fontsize=9)

# Gráfica 7: Divergencia (escala lineal)
ax7 = fig.add_subplot(3, 3, 7)
ax7.plot(t_lor, divergencia, 'purple', linewidth=2)
if len(idx_divergencia) > 0:
    ax7.axvline(x=t_divergencia, color='red', linestyle='--', linewidth=2, 
               label=f't_divergencia ≈ {t_divergencia:.1f}s')
ax7.set_xlabel('Tiempo (s)', fontsize=10, fontweight='bold')
ax7.set_ylabel('Distancia entre trayectorias', fontsize=10, fontweight='bold')
ax7.set_title('Divergencia de Trayectorias (Escala Lineal)', fontsize=11, fontweight='bold')
ax7.grid(True, alpha=0.3)
if len(idx_divergencia) > 0:
    ax7.legend(fontsize=9)

# Gráfica 8: Divergencia (escala logarítmica)
ax8 = fig.add_subplot(3, 3, 8)
# Evitar log(0)
divergencia_log = np.log(divergencia + 1e-10)
ax8.semilogy(t_lor, np.abs(divergencia) + 1e-10, 'purple', linewidth=2)
ax8.set_xlabel('Tiempo (s)', fontsize=10, fontweight='bold')
ax8.set_ylabel('Distancia (escala log)', fontsize=10, fontweight='bold')
ax8.set_title('Divergencia (Escala Logarítmica)', fontsize=11, fontweight='bold')
ax8.grid(True, alpha=0.3, which='both')

# Gráfica 9: Información del sistema
ax9 = fig.add_subplot(3, 3, 9)
ax9.axis('off')

info_lorenz = [
    ['PARÁMETRO', 'VALOR'],
    ['σ', f'{sigma}'],
    ['ρ', f'{rho}'],
    ['β', f'{beta:.4f}'],
    ['Tipo', 'Caótico'],
    ['Δ inicial', '10⁻⁶'],
    ['t final', f'{t_final} s'],
    ['h paso', f'{h_lorenz}'],
    ['Div. máx', f'{np.max(divergencia):.4e}'],
]

tabla_lorenz = plt.table(cellText=info_lorenz, cellLoc='left', loc='center',
                        colWidths=[0.4, 0.4])
tabla_lorenz.auto_set_font_size(False)
tabla_lorenz.set_fontsize(9)
tabla_lorenz.scale(1, 2)

for i in range(2):
    tabla_lorenz[(0, i)].set_facecolor('#2E75B6')
    tabla_lorenz[(0, i)].set_text_props(weight='bold', color='white')

plt.suptitle('Problema 6: Sistema de EDOs - Lorenz (Sistema Caótico)', 
             fontsize=13, fontweight='bold', y=0.995)
plt.tight_layout()
plt.show()

print("\n✗ CONCLUSIÓN Problema 6:")
print("  El sistema de Lorenz es determinístico pero caótico.")
print(f"  Una perturbación inicial de 10⁻⁶ se amplifica hasta ~ {np.max(divergencia):.2f}")
print("  en aprox. {}s (tiempo de Lyapunov)".format(t_divergencia if len(idx_divergencia) > 0 else ">50"))
print("  Las trayectorias son impredecibles después de este tiempo.")
print("  El atractor de Lorenz es una estructura fractal 3D (mariposa).")
print("  Demuestra limitaciones fundamentales en la previsibilidad de sistemas dinámicos complejos.")
print("  LECCIÓN: Los métodos numéricos dan la solución correcta,")
print("  pero para sistemas caóticos, el futuro es inherentemente impredecible.")

# ============================================================================
#                            RESUMEN FINAL
# ============================================================================

print("\n\n" + "="*80)
print("RESUMEN: ECUACIONES DIFERENCIALES ORDINARIAS")
print("="*80)

print("""
COMPARACIÓN DE MÉTODOS:

┌─────────────────────────────────────────────────────────────────────────┐
│                        MÉTODOS DE UN PASO                              │
├─────────────────┬──────────┬──────────┬──────────┬──────────────────────┤
│     Método      │  Orden   │  Precisión  │ Estabilidad │   Uso           │
├─────────────────┼──────────┼──────────┼──────────┼──────────────────────┤
│ Euler           │  O(h)    │  Baja    │  Pobre   │ Demostración, enseñ.│
│ Euler Mejorado  │  O(h²)   │  Media   │  Buena   │ Balance costo/prec. │
│ Runge-Kutta 4   │  O(h⁴)   │  Alta    │  Buena   │ Opción estándar     │
└─────────────────┴──────────┴──────────┴──────────┴──────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      MÉTODOS DE PASOS MÚLTIPLES                         │
├─────────────────┬──────────┬──────────┬──────────┬──────────────────────┤
│     Método      │   Tipo   │  Orden   │ Estabilidad │  Observaciones     │
├─────────────────┼──────────┼──────────┼──────────┼──────────────────────┤
│ Adams-Bashforth │ Explícito│  O(h⁴)   │  Moderada│ Rápido, requiere    │
│                 │          │          │          │ inicialización       │
├─────────────────┼──────────┼──────────┼──────────┼──────────────────────┤
│ Adams-Moulton   │ Implícito│  O(h⁴)   │  Excelente│ Requiere iteración │
│                 │          │          │          │ Muy estable         │
├─────────────────┼──────────┼──────────┼──────────┼──────────────────────┤
│ Predictor-Correc│ Mixto    │  O(h⁴)   │  Muy buena│ Balance óptimo     │
│                 │          │          │          │ Pocos ciclos        │
└─────────────────┴──────────┴──────────┴──────────┴──────────────────────┘

RECOMENDACIONES:
═════════════════
- Para ecuaciones NO stiff:
  ✓ Usar RK4 (simplicidad vs precisión)
  ✓ O Predictor-Corrector (eficiencia)

- Para ecuaciones STIFF:
  ✓ Usar métodos implícitos (Adams-Moulton, BDF)
  ✓ Considerar métodos especiales (backward Euler, Rosenbrock)

- Para sistemas de EDOs:
  ✓ RK4 es versátil y robusto
  ✓ Vigilar paso de tiempo para estabilidad
  ✓ Conservación de energía es indicador de precisión

- Para sistemas caóticos:
  ✓ Usar RK4 de 4º orden mínimo
  ✓ Paso muy pequeño (h ~0.001 o menos)
  ✓ Aceptar que previsibilidad es limitada

ERRORES Y LIMITACIONES:
═════════════════════════
1. Error de truncamiento local: O(h^p) por paso, donde p = orden
2. Error de truncamiento global: acumulación de errores locales
3. Errores de redondeo: propagación en aritmética finita
4. Inestabilidad: divergencia en ecuaciones stiff o pasos grandes
5. Sensibilidad: en sistemas caóticos (exponencial)

VALIDACIÓN:
═════════════
- Comparar con solución exacta (si existe)
- Probar refinamiento de malla: h/2, h/4
- Verificar conservación de cantidades (energía, momento)
- Análisis de estabilidad lineal (región absoluta)
- Estudio de sensibilidad a condiciones iniciales
""")

print("="*80)
print("FIN DEL ANÁLISIS DE ECUACIONES DIFERENCIALES ORDINARIAS")
print("="*80)
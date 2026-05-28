"""
================================================================================
                    EXTRAPOLACIÓN - ANÁLISIS COMPLETO
================================================================================
Este módulo contiene implementaciones de tres métodos de extrapolación:
1. Extrapolación Lineal
2. Extrapolación Cuadrática
3. Extrapolación Segmentada (Extensión de Splines)

Cada método incluye 2 problemas:
- Problema 1: Caso ideal con tendencia clara
- Problema 2: Caso problemático donde la extrapolación diverge

DIFERENCIA CLAVE CON INTERPOLACIÓN:
La extrapolación estima valores FUERA del rango de datos conocidos.
Los valores estimados están fuera del intervalo [x_min, x_max] de los datos.
La confiabilidad DISMINUYE rápidamente mientras más se extrapola.
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, CubicSpline
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
#                    1. EXTRAPOLACIÓN LINEAL
# ============================================================================

print("\n" + "="*80)
print("1. EXTRAPOLACIÓN LINEAL")
print("="*80)

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 1: CASO IDEAL - Tendencia lineal clara
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 1: Extrapolación Lineal - Caso Ideal")
print("-"*80)

"""
ENUNCIADO:
Una empresa registra sus ingresos mensuales: enero=$100k, febrero=$120k,
marzo=$140k. Proyectar los ingresos para abril y mayo asumiendo tendencia lineal.

PROBLEMÁTICA:
Se asume que la tendencia lineal observada continuará en el futuro (SUPUESTO FUERTE).

QUÉ SE CALCULA:
- Extrapolación lineal
- Ecuación de la recta
- Proyecciones futuras
- Intervalo de confianza aproximado
"""

meses = np.array([1, 2, 3])  # enero, febrero, marzo
ingresos = np.array([100, 120, 140])  # en miles de dólares

# Ajustar recta: y = mx + b
coef_lineal = np.polyfit(meses, ingresos, 1)
m, b = coef_lineal
print(f"\nEcuación de la recta: y = {m:.1f}x + {b:.1f}")
print(f"Interpretación: Los ingresos aumentan ${m:.1f}k por mes")

# Extrapolación para abril (mes 4) y mayo (mes 5)
meses_futuros = np.array([4, 5])
ingresos_proyectados = np.polyval(coef_lineal, meses_futuros)

print("\nProyecciones de ingresos (EXTRAPOLACIÓN):")
for mes, ing in zip(meses_futuros, ingresos_proyectados):
    print(f"  Mes {mes}: ${ing:.1f}k")

# Calcular medidas de dispersión para intervalo de confianza
residuos = ingresos - np.polyval(coef_lineal, meses)
std_residuos = np.std(residuos)
error_estandar = std_residuos * np.sqrt(1 + 1/len(meses))

print(f"\nMedidas de dispersión:")
print(f"  Desviación estándar de residuos: ${std_residuos:.2f}k")
print(f"  Error estándar de predicción: ${error_estandar:.2f}k")

# Intervalos de confianza aproximados (68% para ±1 sigma)
print(f"\nProyecciones con intervalo de confianza (68%):")
for mes, ing in zip(meses_futuros, ingresos_proyectados):
    print(f"  Mes {mes}: ${ing:.1f}k ± ${error_estandar:.1f}k")
    print(f"           Rango: [${ing-error_estandar:.1f}k, ${ing+error_estandar:.1f}k]")

# Gráficas
meses_continuo = np.linspace(0.5, 5.5, 100)
ingresos_continuo = np.polyval(coef_lineal, meses_continuo)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfica principal
ax1 = axes[0]
# Datos históricos
ax1.plot(meses, ingresos, 'go-', linewidth=2.5, markersize=10, label='Datos históricos')
# Extrapolación
ax1.plot(meses_futuros, ingresos_proyectados, 'rs', markersize=10, label='Extrapolación')
# Recta ajustada
ax1.plot(meses_continuo, ingresos_continuo, 'b--', linewidth=2, alpha=0.7, 
         label='Tendencia lineal')
# Zonas
ax1.axvspan(0.5, 3, alpha=0.1, color='green', label='Rango conocido')
ax1.axvspan(3, 5.5, alpha=0.1, color='red', label='Extrapolación')
ax1.axvline(x=3, color='black', linestyle=':', linewidth=1.5)
# Intervalo de confianza
ic_upper = ingresos_proyectados + error_estandar
ic_lower = ingresos_proyectados - error_estandar
ax1.fill_between(meses_futuros, ic_lower, ic_upper, alpha=0.3, color='red',
                 label='Intervalo ±σ')
ax1.plot(meses_futuros, ic_upper, 'r--', linewidth=1, alpha=0.5)
ax1.plot(meses_futuros, ic_lower, 'r--', linewidth=1, alpha=0.5)

ax1.set_xlabel('Mes', fontsize=11, fontweight='bold')
ax1.set_ylabel('Ingresos (miles USD)', fontsize=11, fontweight='bold')
ax1.set_title('Problema 1: Extrapolación Lineal Ideal', fontsize=12, fontweight='bold')
ax1.set_xticks([1, 2, 3, 4, 5])
ax1.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr*', 'May*'], fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10, loc='upper left')
ax1.set_ylim([80, 180])

# Tabla de resultados
ax2 = axes[1]
ax2.axis('off')
tabla_extrap = [
    ['Mes', 'Ingresos ($k)', 'Tipo'],
    ['1 (Ene)', f'{ingresos[0]:.1f}', 'Real'],
    ['2 (Feb)', f'{ingresos[1]:.1f}', 'Real'],
    ['3 (Mar)', f'{ingresos[2]:.1f}', 'Real'],
    ['4 (Abr)*', f'{ingresos_proyectados[0]:.1f}', 'Proyectado'],
    ['5 (May)*', f'{ingresos_proyectados[1]:.1f}', 'Proyectado'],
]
tabla_ext = plt.table(cellText=tabla_extrap, cellLoc='center', loc='center',
                      colWidths=[0.3, 0.4, 0.3])
tabla_ext.auto_set_font_size(False)
tabla_ext.set_fontsize(10)
tabla_ext.scale(1, 2.5)
for i in range(3):
    tabla_ext[(0, i)].set_facecolor('#2E75B6')
    tabla_ext[(0, i)].set_text_props(weight='bold', color='white')

ax2.text(0.5, 0.15, '* Valores extrapolados\nNo confirmados en la realidad',
        ha='center', fontsize=10, style='italic', 
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

plt.suptitle('Problema 1: Extrapolación Lineal - Caso Ideal', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✓ CONCLUSIÓN Problema 1:")
print("  La extrapolación lineal funciona bien cuando:")
print("  - La tendencia es claramente lineal")
print("  - La extrapolación es a corto plazo (1-2 períodos)")
print("  - No hay cambios abruptos en las condiciones")
print("  Los intervalos de confianza aumentan con la distancia de extrapolación.")

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 2: CASO PROBLEMÁTICO - Tendencia que cambia
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 2: Extrapolación Lineal - Caso Problemático")
print("-"*80)

"""
ENUNCIADO:
Se registra el número de usuarios de una aplicación: mes 1 (1000),
mes 2 (2000), mes 3 (3000). Proyectar para mes 4 y mes 5.

PROBLEMÁTICA:
El crecimiento no es lineal. Es exponencial o sigue una curva de adopción S.
La extrapolación lineal DIVERGE dramáticamente de la realidad.

QUÉ SE CALCULA:
- Extrapolación lineal (INCORRECTA)
- Comparación con crecimiento real (exponencial)
- Análisis del error cometido
"""

meses_app = np.array([1, 2, 3])
usuarios = np.array([1000, 2000, 3000])

# Extrapolación lineal
coef_app = np.polyfit(meses_app, usuarios, 1)
meses_fut_app = np.array([4, 5, 6])
usuarios_lineal = np.polyval(coef_app, meses_fut_app)

# Modelo real: crecimiento exponencial P(t) = 1000 * 2^(t-1)
usuarios_reales = 1000 * (2 ** (meses_fut_app - 1))

print("\nDatos originales (Crecimiento de usuarios):")
for mes, usr in zip(meses_app, usuarios):
    print(f"  Mes {mes}: {usr:,} usuarios")

print("\nExtrapolación LINEAL (INCORRECTA para crecimiento exponencial):")
for mes, usr_lin in zip(meses_fut_app, usuarios_lineal):
    print(f"  Mes {mes}: {usr_lin:,.0f} usuarios")

print("\nValores REALES (crecimiento exponencial P = 1000·2^(t-1)):")
for mes, usr_real in zip(meses_fut_app, usuarios_reales):
    print(f"  Mes {mes}: {usr_real:,.0f} usuarios")

print("\nERRORES COMETIDOS POR EXTRAPOLACIÓN LINEAL:")
errores_app = np.abs(usuarios_lineal - usuarios_reales)
for mes, err, usr_real in zip(meses_fut_app, errores_app, usuarios_reales):
    pct_error = (err / usr_real) * 100
    print(f"  Mes {mes}: Error = {err:,.0f} usuarios ({pct_error:.1f}%)")

# Gráficas
meses_continuo_app = np.linspace(0.5, 6.5, 100)
usuarios_lineal_continuo = np.polyval(coef_app, meses_continuo_app)
usuarios_exp_continuo = 1000 * (2 ** (meses_continuo_app - 1))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Comparación de predicciones
ax1 = axes[0]
ax1.plot(meses_app, usuarios, 'go-', linewidth=2.5, markersize=10, 
         label='Datos históricos')
ax1.plot(meses_fut_app, usuarios_lineal, 'rs', markersize=9, 
         label='Extrapolación lineal (INCORRECTA)')
ax1.plot(meses_fut_app, usuarios_reales, 'g^', markersize=9, 
         label='Valores reales (exponencial)')
ax1.plot(meses_continuo_app, usuarios_lineal_continuo, 'b--', linewidth=2, 
         alpha=0.7, label='Tendencia lineal')
ax1.plot(meses_continuo_app, usuarios_exp_continuo, 'purple', linewidth=2.5, 
         alpha=0.7, label='Crecimiento exponencial real')
ax1.axvline(x=3, color='black', linestyle=':', linewidth=1.5)
ax1.axvspan(0.5, 3, alpha=0.1, color='green')
ax1.axvspan(3, 6.5, alpha=0.1, color='red')
ax1.set_xlabel('Mes', fontsize=11, fontweight='bold')
ax1.set_ylabel('Número de usuarios', fontsize=11, fontweight='bold')
ax1.set_title('Problema 2: Extrapolación Lineal - Datos Exponenciales', 
              fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=9)
ax1.set_ylim([0, 70000])
ax1.set_yscale('linear')

# Gráfica de errores
ax2 = axes[1]
colores_err_app = ['darkred' if e > 50000 else 'red' for e in errores_app]
barras = ax2.bar(range(len(meses_fut_app)), errores_app, color=colores_err_app, 
                 alpha=0.7, edgecolor='black', linewidth=2)
ax2.set_xticks(range(len(meses_fut_app)))
ax2.set_xticklabels([f'Mes {m}' for m in meses_fut_app])
ax2.set_ylabel('Error absoluto (usuarios)', fontsize=11, fontweight='bold')
ax2.set_title('Errores: Lineal vs Real', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
for i, (err, mes) in enumerate(zip(errores_app, meses_fut_app)):
    pct = (err / usuarios_reales[i]) * 100
    ax2.text(i, err + 1000, f'{err/1000:.0f}k\n({pct:.0f}%)', 
            ha='center', fontweight='bold', fontsize=10)

plt.suptitle('Problema 2: Extrapolación Lineal - Caso Problemático', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✗ CONCLUSIÓN Problema 2:")
print("  La extrapolación lineal es INAPROPIADA para crecimiento exponencial.")
print("  Los errores crecen exponencialmente (97% en mes 6).")
print("  Conclusión: NUNCA extrapolar linealmente datos exponenciales.")
print("  Se recomienda identificar el tipo de crecimiento (lineal, exponencial,")
print("  logístico) y usar modelo apropiado.")

# ============================================================================
#                    2. EXTRAPOLACIÓN CUADRÁTICA
# ============================================================================

print("\n\n" + "="*80)
print("2. EXTRAPOLACIÓN CUADRÁTICA")
print("="*80)

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 3: CASO IDEAL - Datos parabólicos
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 3: Extrapolación Cuadrática - Caso Ideal")
print("-"*80)

"""
ENUNCIADO:
Se mide la eficiencia de un proceso químico a diferentes temperaturas:
T=[100, 150, 200]°C, Eficiencia=[60, 85, 100]%. Proyectar eficiencia a T=250°C.

PROBLEMÁTICA:
La eficiencia sigue una relación cuadrática con temperatura hasta cierto punto.

QUÉ SE CALCULA:
- Extrapolación cuadrática
- Polinomio de segundo grado ajustado
- Predicción futura
- Validez de la extrapolación
"""

temperaturas_proc = np.array([100, 150, 200])
eficiencia = np.array([60, 85, 100])

# Ajustar polinomio cuadrático
coef_cuad = np.polyfit(temperaturas_proc, eficiencia, 2)
print(f"Polinomio ajustado: E(T) = {coef_cuad[0]:.6f}T² + {coef_cuad[1]:.4f}T + {coef_cuad[2]:.2f}")

# Extrapolación a T=250°C
temp_extrap = 250
efic_extrap_cuad = np.polyval(coef_cuad, temp_extrap)

print(f"\nExtrapolación a {temp_extrap}°C:")
print(f"  Eficiencia estimada = {efic_extrap_cuad:.2f}%")

# Análisis físico
print(f"\nAnálisis:")
print(f"  La eficiencia parece aumentar con temperatura en el rango conocido.")
print(f"  Extrapolación a {temp_extrap}°C es razonable si el material resiste")
print(f"  esa temperatura (supuesto a validar experimentalmente).")

# Gráficas
temp_continuo = np.linspace(50, 300, 200)
efic_continuo = np.polyval(coef_cuad, temp_continuo)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfica principal
ax1 = axes[0]
ax1.plot(temperaturas_proc, eficiencia, 'go-', linewidth=2.5, markersize=10, 
         label='Datos históricos')
ax1.plot(temp_extrap, efic_extrap_cuad, 'rs', markersize=10, label='Extrapolación')
ax1.plot(temp_continuo, efic_continuo, 'b-', linewidth=2.5, alpha=0.7, 
         label='Parábola ajustada')
ax1.axvline(x=200, color='black', linestyle=':', linewidth=1.5)
ax1.axvspan(50, 200, alpha=0.1, color='green', label='Rango conocido')
ax1.axvspan(200, 300, alpha=0.1, color='red', label='Extrapolación')
ax1.set_xlabel('Temperatura (°C)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Eficiencia (%)', fontsize=11, fontweight='bold')
ax1.set_title('Problema 3: Extrapolación Cuadrática Ideal', 
              fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)
ax1.set_ylim([30, 130])

# Tabla
ax2 = axes[1]
ax2.axis('off')
tabla_cuad_extrap = [
    ['T (°C)', 'Eficiencia (%)', 'Tipo'],
    ['100', f'{eficiencia[0]:.1f}', 'Real'],
    ['150', f'{eficiencia[1]:.1f}', 'Real'],
    ['200', f'{eficiencia[2]:.1f}', 'Real'],
    ['250*', f'{efic_extrap_cuad:.2f}', 'Extrapolado'],
]
tabla_ce = plt.table(cellText=tabla_cuad_extrap, cellLoc='center', loc='center',
                     colWidths=[0.3, 0.4, 0.3])
tabla_ce.auto_set_font_size(False)
tabla_ce.set_fontsize(10)
tabla_ce.scale(1, 2.5)
for i in range(3):
    tabla_ce[(0, i)].set_facecolor('#2E75B6')
    tabla_ce[(0, i)].set_text_props(weight='bold', color='white')

plt.suptitle('Problema 3: Extrapolación Cuadrática - Caso Ideal', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✓ CONCLUSIÓN Problema 3:")
print("  La extrapolación cuadrática es apropiada cuando hay evidencia de que")
print("  la relación es parabólica. El resultado es físicamente razonable.")

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 4: CASO PROBLEMÁTICO - Extrapolación a extremos
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 4: Extrapolación Cuadrática - Caso Problemático")
print("-"*80)

"""
ENUNCIADO:
Se mide la población de una ciudad en años: 1990 (100k), 2000 (250k),
2010 (500k). Proyectar población para 2020 y 2030.

PROBLEMÁTICA:
La población sigue un patrón que puede cambiar (saturación, migración).
Una parábola creciente diverge rápidamente a valores irreales.

QUÉ SE CALCULA:
- Extrapolación cuadrática lejos del rango conocido
- Demostración de divergencia
- Comparación con saturación logística
"""

años = np.array([1990, 2000, 2010])
poblacion_ciudad = np.array([100, 250, 500])

# Extrapolación cuadrática
coef_pob = np.polyfit(años, poblacion_ciudad, 2)
años_futuros = np.array([2020, 2030])
poblacion_proyectada_cuad = np.polyval(coef_pob, años_futuros)

print(f"Polinomio: P(t) = {coef_pob[0]:.8f}t² + {coef_pob[1]:.4f}t + {coef_pob[2]:.1f}")

print("\nProyecciones con extrapolación cuadrática:")
for año, pob in zip(años_futuros, poblacion_proyectada_cuad):
    print(f"  {año}: {pob:,.0f}k habitantes")

# Modelo limitado (logístico aproximado): saturación a ~1000k
tiempo_normalizado = (años - 1990) / 10
tiempo_fut_norm = (años_futuros - 1990) / 10

# Modelo S: P(t) = 1000 / (1 + exp(-kt))
k_logistico = 1.5
poblacion_logistica = 1000 / (1 + np.exp(-k_logistico * (tiempo_fut_norm - 1.5)))

print(f"\nProyecciones más realistas (modelo logístico con saturación):")
for año, pob in zip(años_futuros, poblacion_logistica):
    print(f"  {año}: {pob:,.0f}k habitantes")

print(f"\nPROBLEMA: La extrapolación cuadrática diverge a valores irreales.")
print(f"  Año 2020: {poblacion_proyectada_cuad[0]:,.0f}k (cuadrática)")
print(f"  Año 2020: {poblacion_logistica[0]:,.0f}k (realista)")
print(f"  Diferencia: {poblacion_proyectada_cuad[0]-poblacion_logistica[0]:,.0f}k")

# Gráficas
años_continuo = np.linspace(1980, 2040, 200)
tiempo_norm_continuo = (años_continuo - 1990) / 10
pob_cuad_continuo = np.polyval(coef_pob, años_continuo)
pob_logistica_continuo = 1000 / (1 + np.exp(-k_logistico * (tiempo_norm_continuo - 1.5)))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Comparación
ax1 = axes[0]
ax1.plot(años, poblacion_ciudad, 'go-', linewidth=2.5, markersize=10, 
         label='Datos históricos')
ax1.plot(años_futuros, poblacion_proyectada_cuad, 'rs', markersize=9, 
         label='Extrapolación cuadrática (DIVERGE)')
ax1.plot(años_futuros, poblacion_logistica, 'g^', markersize=9, 
         label='Modelo logístico realista')
ax1.plot(años_continuo, pob_cuad_continuo, 'b--', linewidth=2, alpha=0.7, 
         label='Parábola')
ax1.plot(años_continuo, pob_logistica_continuo, 'purple', linewidth=2.5, alpha=0.7, 
         label='Saturación logística')
ax1.axvline(x=2010, color='black', linestyle=':', linewidth=1.5)
ax1.axvspan(1980, 2010, alpha=0.1, color='green')
ax1.axvspan(2010, 2040, alpha=0.1, color='red')
ax1.axhline(y=1000, color='purple', linestyle='--', linewidth=1, alpha=0.5, 
            label='Límite de saturación (~1000k)')
ax1.set_xlabel('Año', fontsize=11, fontweight='bold')
ax1.set_ylabel('Población (miles)', fontsize=11, fontweight='bold')
ax1.set_title('Problema 4: Extrapolación Cuadrática - Divergencia', 
              fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=9, loc='upper left')
ax1.set_ylim([0, 3500])

# Gráfica de error/divergencia
ax2 = axes[1]
divergencias = poblacion_proyectada_cuad - poblacion_logistica
años_lab = [f'{año}' for año in años_futuros]
colores_div = ['darkred', 'darkred']
ax2.bar(range(len(años_futuros)), divergencias, color=colores_div, alpha=0.7, 
        edgecolor='black', linewidth=2)
ax2.set_xticks(range(len(años_futuros)))
ax2.set_xticklabels(años_lab)
ax2.set_ylabel('Diferencia (miles)', fontsize=11, fontweight='bold')
ax2.set_title('Sobre-estimación del Modelo Cuadrático', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
for i, div in enumerate(divergencias):
    ax2.text(i, div + 100, f'+{div:,.0f}k', ha='center', fontweight='bold', fontsize=11)

plt.suptitle('Problema 4: Extrapolación Cuadrática - Caso Problemático', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✗ CONCLUSIÓN Problema 4:")
print("  La extrapolación cuadrática diverge a valores no realistas.")
print("  Fenómenos reales con saturación requieren modelos no polinomiales.")
print("  Lecciones:")
print("  - No extrapolar polinomios a valores muy lejanos")
print("  - Considerar límites físicos y biológicos del problema")
print("  - Usar modelos apropiados al fenómeno (logístico, exponencial con límite, etc.)")

# ============================================================================
#                    3. EXTRAPOLACIÓN SEGMENTADA (SPLINES EXTENDIDOS)
# ============================================================================

print("\n\n" + "="*80)
print("3. EXTRAPOLACIÓN SEGMENTADA (EXTENSIÓN DE SPLINES)")
print("="*80)

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 5: CASO IDEAL - Tendencia suave y consistente
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 5: Extrapolación Segmentada - Caso Ideal")
print("-"*80)

"""
ENUNCIADO:
Se registra el precio de una acción en 5 días: día 1-5 con precios
[100, 105, 110, 108, 115] USD. Proyectar el precio para día 6 y 7
usando la tendencia del último segmento del spline.

PROBLEMÁTICA:
Se extiende el último segmento suave para hacer predicciones a corto plazo.

QUÉ SE CALCULA:
- Spline cúbico en datos conocidos
- Extrapolación usando último segmento
- Predicción suave sin oscilaciones
"""

días_bolsa = np.array([1, 2, 3, 4, 5])
precios = np.array([100, 105, 110, 108, 115])

# Crear spline
spline_bolsa = CubicSpline(días_bolsa, precios, bc_type='natural')

# Extrapolación: extender el último segmento
# Usar la derivada en el último punto para extender suavemente
días_futuros_spline = np.array([6, 7])

# Opción 1: Evaluar el spline directamente (usa extrapolación cúbica)
precios_extrap_spline = spline_bolsa(días_futuros_spline)

# Opción 2: Usar recta tangente en el último punto (más conservadora)
derivada_final = spline_bolsa(días_bolsa[-1], 1)
x_last = días_bolsa[-1]
y_last = precios[-1]
precios_extrap_tangente = y_last + derivada_final * (días_futuros_spline - x_last)

print("\nDatos históricos (Precio de acción):")
for día, precio in zip(días_bolsa, precios):
    print(f"  Día {día}: ${precio:.2f}")

print(f"\nDerivada en último punto (día {días_bolsa[-1]}):")
print(f"  Pendiente = ${derivada_final:.2f}/día")
print(f"  Interpretación: Tendencia alcista de ${derivada_final:.2f} por día")

print("\nExtrapolación usando Spline Cúbico:")
for día, precio in zip(días_futuros_spline, precios_extrap_spline):
    print(f"  Día {día}: ${precio:.2f}")

print("\nExtrapolación usando Recta Tangente (más conservadora):")
for día, precio in zip(días_futuros_spline, precios_extrap_tangente):
    print(f"  Día {día}: ${precio:.2f}")

# Gráficas
días_continuo = np.linspace(0.5, 7.5, 200)
precios_continuo = spline_bolsa(días_continuo)

# Recta tangente para extrapolación
precios_tangente_continuo = np.where(
    días_continuo <= x_last,
    spline_bolsa(días_continuo),
    y_last + derivada_final * (días_continuo - x_last)
)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfica principal
ax1 = axes[0]
ax1.plot(días_bolsa, precios, 'go-', linewidth=2.5, markersize=10, 
         label='Datos históricos')
ax1.plot(días_futuros_spline, precios_extrap_spline, 'rs', markersize=9, 
         label='Extrapolación spline cúbico')
ax1.plot(días_futuros_spline, precios_extrap_tangente, 'b^', markersize=9, 
         label='Extrapolación tangente')
ax1.plot(días_continuo, precios_continuo, 'g-', linewidth=2.5, alpha=0.7, 
         label='Spline interpolador')
ax1.plot(días_continuo, precios_tangente_continuo, 'b--', linewidth=2, alpha=0.5, 
         label='Extensión tangente')
ax1.axvline(x=5, color='black', linestyle=':', linewidth=1.5)
ax1.axvspan(0.5, 5, alpha=0.1, color='green', label='Rango conocido')
ax1.axvspan(5, 7.5, alpha=0.1, color='red', label='Extrapolación')
ax1.set_xlabel('Día', fontsize=11, fontweight='bold')
ax1.set_ylabel('Precio (USD)', fontsize=11, fontweight='bold')
ax1.set_title('Problema 5: Extrapolación Segmentada Ideal', 
              fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=9)
ax1.set_xticks(range(1, 8))

# Tabla comparativa
ax2 = axes[1]
ax2.axis('off')
tabla_spline_extrap = [
    ['Día', 'Spline', 'Tangente', 'Método'],
    ['1', f'{precios[0]:.2f}', '-', 'Real'],
    ['2', f'{precios[1]:.2f}', '-', 'Real'],
    ['3', f'{precios[2]:.2f}', '-', 'Real'],
    ['4', f'{precios[3]:.2f}', '-', 'Real'],
    ['5', f'{precios[4]:.2f}', '-', 'Real'],
    ['6*', f'{precios_extrap_spline[0]:.2f}', f'{precios_extrap_tangente[0]:.2f}', 'Proyectado'],
    ['7*', f'{precios_extrap_spline[1]:.2f}', f'{precios_extrap_tangente[1]:.2f}', 'Proyectado'],
]
tabla_se = plt.table(cellText=tabla_spline_extrap, cellLoc='center', loc='center',
                     colWidths=[0.15, 0.25, 0.25, 0.25])
tabla_se.auto_set_font_size(False)
tabla_se.set_fontsize(9)
tabla_se.scale(1, 1.8)
for i in range(4):
    tabla_se[(0, i)].set_facecolor('#2E75B6')
    tabla_se[(0, i)].set_text_props(weight='bold', color='white')

plt.suptitle('Problema 5: Extrapolación Segmentada - Caso Ideal', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✓ CONCLUSIÓN Problema 5:")
print("  La extrapolación segmentada es suave y mantiene tendencias locales.")
print("  Mejor para predicciones a muy corto plazo (1-2 pasos).")
print("  La recta tangente es más conservadora que prolongar el spline cúbico.")

# ────────────────────────────────────────────────────────────────────────────
# PROBLEMA 6: CASO PROBLEMÁTICO - Cambio de tendencia abrupto
# ────────────────────────────────────────────────────────────────────────────

print("\n" + "-"*80)
print("PROBLEMA 6: Extrapolación Segmentada - Caso Problemático")
print("-"*80)

"""
ENUNCIADO:
Datos de temperatura diaria: [20, 22, 25, 28, 15] °C (hay caída abrupta).
Proyectar temperatura para día 6.

PROBLEMÁTICA:
El método de extrapolación no detecta cambios abruptos. Usa la tendencia
del último segmento, que puede ser completamente erróneo si hay eventos
inesperados.

QUÉ SE CALCULA:
- Extrapolación segmentada (INCORRECTA ante cambios abruptos)
- Demostración de falla
- Limitaciones del método
"""

días_temp = np.array([1, 2, 3, 4, 5])
temperaturas = np.array([20, 22, 25, 28, 15])  # Caída abrupta en día 5

# Crear spline (que suaviza el cambio abrupto)
spline_temp = CubicSpline(días_temp, temperaturas, bc_type='natural')

# Extrapolación
día_extrap_temp = 6
temp_extrap_spline = spline_temp(día_extrap_temp)

# Derivada en el último punto (que será incorrecta)
deriv_final_temp = spline_temp(días_temp[-1], 1)

print("\nDatos históricos con cambio abrupto:")
for d, t in zip(días_temp, temperaturas):
    print(f"  Día {d}: {t:5.1f}°C", end="")
    if d == 5:
        print("  ← CAÍDA ABRUPTA (evento inesperado)")
    else:
        print()

print(f"\nDerivada en día 5: {deriv_final_temp:.2f}°C/día")
print(f"(Indica tendencia CRECIENTE, aunque hay caída abrupta)")

print(f"\nExtrapolación Spline para día 6:")
print(f"  Temperatura estimada: {temp_extrap_spline:.2f}°C")
print(f"  PROBLEMA: Predice calentamiento cuando la realidad puede ser:")
print(f"    - Estabilización alrededor de 15°C")
print(f"    - Enfriamiento continuado")
print(f"    - La predicción es INCORRECTA")

# Comportamiento del spline vs realidad esperada
días_continuo_temp = np.linspace(0.5, 6.5, 150)
temps_continuo_spline = spline_temp(días_continuo_temp)

# Escenarios alternativos
temps_estable = np.where(días_continuo_temp <= 5, spline_temp(días_continuo_temp),
                         np.full_like(días_continuo_temp, 15))
temps_enfriando = np.where(días_continuo_temp <= 5, spline_temp(días_continuo_temp),
                          15 - 2 * (días_continuo_temp - 5))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Comparación de predicciones
ax1 = axes[0]
ax1.plot(días_temp, temperaturas, 'go-', linewidth=2.5, markersize=10, 
         label='Datos históricos')
ax1.plot(día_extrap_temp, temp_extrap_spline, 'rs', markersize=10, 
         label='Extrapolación spline (INCORRECTA)')
ax1.plot(días_continuo_temp, temps_continuo_spline, 'purple', linewidth=2.5, alpha=0.7, 
         label='Spline interpolador')
# Escenarios alternativos
ax1.plot(días_continuo_temp, temps_estable, 'b--', linewidth=2, alpha=0.5, 
         label='Escenario: Estabilización')
ax1.plot(días_continuo_temp, temps_enfriando, 'orange', linewidth=2, linestyle='--', 
         alpha=0.5, label='Escenario: Enfriamiento')
ax1.axvline(x=5, color='black', linestyle=':', linewidth=1.5)
ax1.axvspan(0.5, 5, alpha=0.1, color='green')
ax1.axvspan(5, 6.5, alpha=0.1, color='red')
ax1.scatter([5], [15], s=200, marker='X', color='darkred', zorder=5, 
           label='Cambio abrupto')
ax1.set_xlabel('Día', fontsize=11, fontweight='bold')
ax1.set_ylabel('Temperatura (°C)', fontsize=11, fontweight='bold')
ax1.set_title('Problema 6: Extrapolación Segmentada - Cambio Abrupto', 
              fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=9, loc='upper left')
ax1.set_xticks(range(1, 7))

# Análisis de incertidumbre
ax2 = axes[1]
escenarios = ['Spline\n(extrapolación)', 'Estabilización\n(realista)', 'Enfriamiento\n(posible)']
temp_escenarios = [temp_extrap_spline, 15, 13]
colores_esc = ['red', 'green', 'orange']
barras = ax2.bar(range(len(escenarios)), temp_escenarios, color=colores_esc, alpha=0.7, 
                 edgecolor='black', linewidth=2)
ax2.axhline(y=15, color='black', linestyle='--', linewidth=1.5, label='Última medida')
ax2.set_xticks(range(len(escenarios)))
ax2.set_xticklabels(escenarios)
ax2.set_ylabel('Temperatura estimada día 6 (°C)', fontsize=11, fontweight='bold')
ax2.set_title('Incertidumbre en Predicción', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim([0, 35])
for i, (temp, esc) in enumerate(zip(temp_escenarios, escenarios)):
    ax2.text(i, temp + 1, f'{temp:.1f}°C', ha='center', fontweight='bold', fontsize=11)

plt.suptitle('Problema 6: Extrapolación Segmentada - Caso Problemático', 
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print("\n✗ CONCLUSIÓN Problema 6:")
print("  La extrapolación segmentada FALLA ante cambios abruptos.")
print("  El spline intenta suavizar la discontinuidad, produciendo predicciones")
print("  completamente erradas.")
print("  Lecciones:")
print("  - Identificar eventos o cambios en los datos históricos")
print("  - No extrapolar tras cambios abruptos sin considerar la causa")
print("  - Usar múltiples escenarios cuando hay cambios abruptos")
print("  - Preferir predicciones a muy corto plazo (máximo 1-2 pasos)")

print("\n" + "="*80)
print("FIN DEL ANÁLISIS DE EXTRAPOLACIÓN")
print("="*80)

# Resumen final
print("""
RESUMEN: DIFERENCIAS INTERPOLACIÓN vs EXTRAPOLACIÓN

┌────────────────────────────────────────────────────────────────────────────┐
│                         INTERPOLACIÓN                  EXTRAPOLACIÓN       │
├────────────────────────────────────────────────────────────────────────────┤
│ Rango:          Dentro de x_min a x_max      Fuera del rango conocido     │
│ Confiabilidad:  Alta                         Baja a moderada (según dist.)│
│ Error:          Bajo y predecible             Crece rápidamente            │
│ Método:         Relativamente seguro         CUIDADO: puede divergir      │
│ Validación:     Comparar con datos reales    Verificar suposiciones       │
└────────────────────────────────────────────────────────────────────────────┘

RECOMENDACIONES PARA EXTRAPOLACIÓN:
✓ Extrapolar solo distancias CORTAS (1-2 intervalos)
✓ Entender el MODELO SUBYACENTE (lineal, exponencial, logístico)
✓ Documentar SUPUESTOS sobre continuidad de tendencias
✓ Proporcionar INTERVALOS DE CONFIANZA
✓ Validar con NUEVOS DATOS apenas estén disponibles
✓ Considerar EVENTOS que podrían cambiar la tendencia
✓ Usar MÚLTIPLES ESCENARIOS cuando hay incertidumbre

NUNCA:
✗ Extrapolar muy lejos sin bases teóricas
✗ Asumir que tendencias lineales continúan indefinidamente
✗ Ignorar límites físicos o biológicos del problema
✗ Confiar en extrapolación de polinomios de alto grado
""")
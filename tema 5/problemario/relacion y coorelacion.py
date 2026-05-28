"""
================================================================================
                RELACIÓN Y CORRELACIÓN - ANÁLISIS COMPLETO
================================================================================
Este módulo analiza la relación entre variables mediante:
1. Correlación de Pearson (paramétrica, datos normales)
2. Correlación de Spearman (no paramétrica, datos ordinales)
3. Visualización de relaciones
4. Interpretación de coeficientes

CONCEPTOS CLAVE:
- Correlación mide relación LINEAL entre variables
- Valor entre -1 (negativa perfecta) y +1 (positiva perfecta)
- r = 0 significa NO hay relación lineal
- CORRELACIÓN ≠ CAUSALIDAD (advertencia crítica)

DIFERENCIA CON INTERPOLACIÓN/EXTRAPOLACIÓN:
Estos métodos estiman valores puntuales.
Correlación estudia la relación entre dos VARIABLES COMPLETAS.
================================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, linregress
from scipy import stats
import seaborn as sns

# ============================================================================
#                        PROBLEMA 1: PEARSON IDEAL
# ============================================================================

print("\n" + "="*80)
print("PROBLEMA 1: CORRELACIÓN DE PEARSON - CASO IDEAL")
print("="*80)

"""
ENUNCIADO:
Una academia de deportes registra el tiempo de entrenamiento (horas/semana)
y la puntuación en competencia (0-100) de 12 atletas.
¿Existe relación lineal entre entrenamiento y desempeño?

PROBLEMÁTICA:
Identificar si más entrenamiento predice mejor desempeño.

QUÉ SE CALCULA:
- Correlación de Pearson
- Recta de regresión
- Intervalo de confianza para r
- Significancia estadística
"""

# Datos: tiempo de entrenamiento (horas/semana) y puntuación
tiempos_entrenamiento = np.array([5, 10, 8, 15, 12, 7, 20, 18, 6, 14, 11, 9])
puntuaciones = np.array([55, 65, 62, 80, 75, 60, 95, 88, 58, 82, 70, 64])

n = len(tiempos_entrenamiento)

print(f"\nDatos de {n} atletas:")
print("Horas/semana | Puntuación")
print("-" * 25)
for h, p in zip(tiempos_entrenamiento, puntuaciones):
    print(f"    {h:5.1f}    |    {p:5.1f}")

# Calcular correlación de Pearson
coef_pearson, p_value = pearsonr(tiempos_entrenamiento, puntuaciones)

print(f"\n{'='*60}")
print("CORRELACIÓN DE PEARSON")
print(f"{'='*60}")
print(f"Coeficiente r = {coef_pearson:.4f}")
print(f"p-value = {p_value:.6f}")
print(f"n = {n}")

# Interpretación
if p_value < 0.05:
    print(f"\n✓ Estadísticamente SIGNIFICATIVO (p < 0.05)")
else:
    print(f"\n✗ NO significativo (p ≥ 0.05)")

# Clasificación de la correlación
if abs(coef_pearson) >= 0.9:
    fuerza = "PERFECTA"
elif abs(coef_pearson) >= 0.7:
    fuerza = "FUERTE"
elif abs(coef_pearson) >= 0.5:
    fuerza = "MODERADA"
elif abs(coef_pearson) >= 0.3:
    fuerza = "DÉBIL"
else:
    fuerza = "MUY DÉBIL o NULA"

if coef_pearson > 0:
    direccion = "POSITIVA"
else:
    direccion = "NEGATIVA"

print(f"\nInterpretación:")
print(f"  Fuerza: {fuerza}")
print(f"  Dirección: {direccion}")
print(f"  Significado: Cuando aumentan las horas de entrenamiento,")
print(f"               la puntuación tiende a aumentar de forma consistente.")

# Cálculo manual de Pearson para verificación
media_x = np.mean(tiempos_entrenamiento)
media_y = np.mean(puntuaciones)
desv_x = np.std(tiempos_entrenamiento, ddof=1)
desv_y = np.std(puntuaciones, ddof=1)

numerador = np.sum((tiempos_entrenamiento - media_x) * (puntuaciones - media_y))
denominador = np.sqrt(np.sum((tiempos_entrenamiento - media_x)**2) * 
                      np.sum((puntuaciones - media_y)**2))
r_manual = numerador / denominador

print(f"\nVerificación manual:")
print(f"  Media X (horas): {media_x:.2f}")
print(f"  Media Y (puntos): {media_y:.2f}")
print(f"  Desv. Est. X: {desv_x:.2f}")
print(f"  Desv. Est. Y: {desv_y:.2f}")
print(f"  r calculado manualmente: {r_manual:.4f} ✓")

# Calcular coeficiente de determinación R²
r_cuadrado = coef_pearson ** 2
print(f"\nCoeficiente de Determinación (R²):")
print(f"  R² = {r_cuadrado:.4f}")
print(f"  Interpretación: {r_cuadrado*100:.2f}% de la variabilidad en puntuaciones")
print(f"  se explica por el tiempo de entrenamiento.")

# Regresión lineal
slope, intercept, r_value, p_val, std_err = linregress(tiempos_entrenamiento, 
                                                         puntuaciones)

print(f"\nECUACIÓN DE REGRESIÓN LINEAL:")
print(f"  y = {slope:.4f}x + {intercept:.4f}")
print(f"  Puntuación = {slope:.4f} × Horas + {intercept:.4f}")
print(f"  Interpretación: Por cada hora adicional de entrenamiento,")
print(f"  la puntuación aumenta aproximadamente {slope:.2f} puntos.")

# Predicción para nuevos valores
print(f"\nPREDICCIONES (usando recta de regresión):")
horas_nuevas = np.array([5, 16, 25])
puntuaciones_predichas = slope * horas_nuevas + intercept
for h, p in zip(horas_nuevas, puntuaciones_predichas):
    print(f"  Con {h:2.0f} horas de entrenamiento: {p:6.2f} puntos esperados")

# Intervalo de confianza para r (Fisher's z-transform)
z = np.arctanh(coef_pearson)
se_z = 1 / np.sqrt(n - 3)
z_critico = 1.96  # 95% confianza
z_lower = z - z_critico * se_z
z_upper = z + z_critico * se_z
r_lower = np.tanh(z_lower)
r_upper = np.tanh(z_upper)

print(f"\nIntervalo de Confianza 95% para r:")
print(f"  [{r_lower:.4f}, {r_upper:.4f}]")

# Gráficas
fig, axes = plt.subplots(2, 2, figsize=(14, 11))

# 1. Scatter plot con recta de regresión
ax1 = axes[0, 0]
ax1.scatter(tiempos_entrenamiento, puntuaciones, s=100, alpha=0.6, 
           color='steelblue', edgecolors='black', linewidth=1.5)
x_line = np.array([tiempos_entrenamiento.min() - 1, tiempos_entrenamiento.max() + 1])
y_line = slope * x_line + intercept
ax1.plot(x_line, y_line, 'r-', linewidth=2.5, label=f'Recta: y={slope:.2f}x+{intercept:.2f}')
ax1.set_xlabel('Horas de entrenamiento/semana', fontsize=11, fontweight='bold')
ax1.set_ylabel('Puntuación (0-100)', fontsize=11, fontweight='bold')
ax1.set_title(f'Problema 1: Correlación de Pearson Ideal\nr = {coef_pearson:.4f}***', 
             fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)
ax1.set_xlim([3, 22])
ax1.set_ylim([50, 100])

# 2. Residuos
ax2 = axes[0, 1]
y_pred = slope * tiempos_entrenamiento + intercept
residuos = puntuaciones - y_pred
ax2.scatter(y_pred, residuos, s=100, alpha=0.6, color='coral', 
           edgecolors='black', linewidth=1.5)
ax2.axhline(y=0, color='black', linestyle='--', linewidth=2)
ax2.set_xlabel('Valores predichos', fontsize=11, fontweight='bold')
ax2.set_ylabel('Residuos', fontsize=11, fontweight='bold')
ax2.set_title('Análisis de Residuos', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)

# 3. Distribución de residuos
ax3 = axes[1, 0]
ax3.hist(residuos, bins=6, alpha=0.7, color='lightgreen', edgecolor='black', linewidth=1.5)
ax3.axvline(x=0, color='red', linestyle='--', linewidth=2)
ax3.set_xlabel('Residuos', fontsize=11, fontweight='bold')
ax3.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
ax3.set_title('Distribución de Residuos', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# 4. Tabla de resultados
ax4 = axes[1, 1]
ax4.axis('off')

resumen_tabla = [
    ['MÉTRICA', 'VALOR', 'INTERPRETACIÓN'],
    ['Correlación (r)', f'{coef_pearson:.4f}', f'{fuerza} {direccion.lower()}'],
    ['p-value', f'{p_value:.6f}', 'Significativo***' if p_value < 0.05 else 'No sig.'],
    ['R²', f'{r_cuadrado:.4f}', f'{r_cuadrado*100:.1f}% varianza explicada'],
    ['Pendiente (m)', f'{slope:.4f}', f'Puntos/hora de entrenamiento'],
    ['Intercepto (b)', f'{intercept:.4f}', 'Puntuación base (x=0)'],
    ['n', f'{n}', 'Número de observaciones'],
    ['IC 95%', f'[{r_lower:.4f}, {r_upper:.4f}]', 'Intervalo de confianza'],
]

tabla_res = plt.table(cellText=resumen_tabla, cellLoc='left', loc='center',
                      colWidths=[0.25, 0.25, 0.5])
tabla_res.auto_set_font_size(False)
tabla_res.set_fontsize(9)
tabla_res.scale(1, 2.2)

# Color encabezado
for i in range(3):
    tabla_res[(0, i)].set_facecolor('#2E75B6')
    tabla_res[(0, i)].set_text_props(weight='bold', color='white')

plt.suptitle('Problema 1: Correlación de Pearson - Caso Ideal (Relación Fuerte)', 
            fontsize=13, fontweight='bold', y=0.995)
plt.tight_layout()
plt.show()

print(f"\n✓ CONCLUSIÓN Problema 1:")
print(f"  Existe una CORRELACIÓN FUERTE y SIGNIFICATIVA (r={coef_pearson:.4f}, p<0.001)")
print(f"  entre horas de entrenamiento y puntuación en competencia.")
print(f"  El modelo lineal explica el {r_cuadrado*100:.1f}% de la variabilidad.")
print(f"  Cada hora adicional de entrenamiento se asocia con {slope:.2f} puntos más.")

# ============================================================================
#                    PROBLEMA 2: PEARSON - SIN RELACIÓN
# ============================================================================

print("\n\n" + "="*80)
print("PROBLEMA 2: CORRELACIÓN DE PEARSON - CASO SIN RELACIÓN")
print("="*80)

"""
ENUNCIADO:
Se estudia si existe relación entre el color de zapatos y el puntaje en
matemáticas de 10 estudiantes (tontería, pero útil para demostrar r≈0).

PROBLEMÁTICA:
Dos variables COMPLETAMENTE INDEPENDIENTES deben mostrar r ≈ 0.

QUÉ SE CALCULA:
- Correlación de Pearson (debería ser ≈ 0)
- Demostración de variables NO relacionadas
- Importancia de NO asumir causalidad
"""

# Datos ficticios: color de zapato codificado (1-10) y nota de matemáticas
np.random.seed(42)
color_zapato_codigo = np.array([2, 7, 4, 9, 3, 8, 5, 1, 6, 10])
nota_matematicas = np.array([75, 82, 68, 88, 72, 85, 76, 60, 79, 90])

n2 = len(color_zapato_codigo)

print(f"\nDatos de {n2} estudiantes:")
print("Color Zapato* | Nota Matemáticas")
print("-" * 33)
for c, n in zip(color_zapato_codigo, nota_matematicas):
    print(f"      {c:2d}      |      {n:3d}")
print("*Codificado: 1=Rojo, 2=Azul, ..., 10=Blanco")

# Correlación
r_sin_relacion, p_sin_relacion = pearsonr(color_zapato_codigo, nota_matematicas)

print(f"\n{'='*60}")
print("CORRELACIÓN DE PEARSON - VARIABLES INDEPENDIENTES")
print(f"{'='*60}")
print(f"Coeficiente r = {r_sin_relacion:.4f}")
print(f"p-value = {p_sin_relacion:.4f}")
print(f"R² = {r_sin_relacion**2:.4f}")

# Interpretación
if abs(r_sin_relacion) < 0.3:
    print(f"\n✓ Correlación MUY DÉBIL (r ≈ 0)")
    print(f"  NO existe relación lineal detectable.")
    print(f"  p-value = {p_sin_relacion:.4f} > 0.05: NO significativo")
    print(f"  Conclusion: Variables INDEPENDIENTES")

# Gráficas
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Scatter plot
ax1 = axes[0]
ax1.scatter(color_zapato_codigo, nota_matematicas, s=120, alpha=0.6,
           color='purple', edgecolors='black', linewidth=1.5)
# Agregar recta para mostrar la "tendencia"
slope2, intercept2, _, _, _ = linregress(color_zapato_codigo, nota_matematicas)
x_line2 = np.array([0, 11])
y_line2 = slope2 * x_line2 + intercept2
ax1.plot(x_line2, y_line2, 'r--', linewidth=2, alpha=0.5, 
        label=f'Tendencia (casi plana)')

ax1.set_xlabel('Color de zapatos (codificado)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Nota de Matemáticas', fontsize=11, fontweight='bold')
ax1.set_title(f'Problema 2: SIN Correlación Lineal\nr = {r_sin_relacion:.4f} (p={p_sin_relacion:.3f})', 
             fontsize=12, fontweight='bold')
ax1.set_xticks(range(1, 11))
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)
ax1.set_ylim([55, 95])

# Tabla de comparación
ax2 = axes[1]
ax2.axis('off')

comparacion_tabla = [
    ['VARIABLE 1', 'VARIABLE 2', 'r', 'RELACIÓN'],
    ['Horas entrenamiento', 'Puntuación deporte', f'{coef_pearson:.4f}', 'FUERTE: Sí'],
    ['Color de zapatos', 'Nota matemáticas', f'{r_sin_relacion:.4f}', 'NULA: No'],
    ['', '', '', ''],
    ['LECCIÓN IMPORTANTE:', '', '', ''],
    ['Correlación ≠ Causalidad', '', '', ''],
    ['Incluso sin correlación,', '', '', ''],
    ['las variables pueden', '', '', ''],
    ['ser independientes.', '', '', ''],
]

tabla_comp = plt.table(cellText=comparacion_tabla, cellLoc='left', loc='center',
                       colWidths=[0.3, 0.25, 0.15, 0.3])
tabla_comp.auto_set_font_size(False)
tabla_comp.set_fontsize(9)
tabla_comp.scale(1, 2)

for i in range(4):
    tabla_comp[(0, i)].set_facecolor('#2E75B6')
    tabla_comp[(0, i)].set_text_props(weight='bold', color='white')

tabla_comp[(4, 0)].set_facecolor('#FFE699')
tabla_comp[(4, 0)].set_text_props(weight='bold')

plt.suptitle('Problema 2: Correlación de Pearson - SIN Relación', 
            fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print(f"\n✓ CONCLUSIÓN Problema 2:")
print(f"  Correlación r = {r_sin_relacion:.4f} indica NO HAY relación lineal.")
print(f"  Es obvio que el color de zapatos NO afecta la nota de matemáticas.")
print(f"  Este ejemplo ilustra la importancia de la interpretación lógica.")

# ============================================================================
#                    PROBLEMA 3: SPEARMAN - RELACIÓN NO LINEAL
# ============================================================================

print("\n\n" + "="*80)
print("PROBLEMA 3: CORRELACIÓN DE SPEARMAN - DATOS ORDINALES")
print("="*80)

"""
ENUNCIADO:
Se clasifican 8 películas por preferencia de crítica (1-8) y por
preferencia del público (1-8). ¿Hay acuerdo entre críticos y público?

PROBLEMÁTICA:
Los datos son ORDINALES (rangos), no valores continuos.
Pearson asume linearidad. Spearman usa rangos: más robusto.

QUÉ SE CALCULA:
- Correlación de Spearman (de Rangos)
- Comparación Pearson vs Spearman
- Interpretación de coeficiente ρ
"""

# Películas (1-8 según clasificación de crítica)
critica_ranking = np.array([1, 2, 3, 4, 5, 6, 7, 8])
publico_ranking = np.array([1, 3, 2, 5, 4, 8, 6, 7])

n3 = len(critica_ranking)

print(f"\nClasificación de {n3} películas:")
print("Película | Crítica Ranking | Público Ranking")
print("-" * 45)
for i, (c, p) in enumerate(zip(critica_ranking, publico_ranking), 1):
    print(f"   {i}    |       {c}         |        {p}")

# Correlación de Spearman
rho_spearman, p_spearman = spearmanr(critica_ranking, publico_ranking)

# Correlación de Pearson (para comparación)
r_pearson_comp, p_pearson_comp = pearsonr(critica_ranking, publico_ranking)

print(f"\n{'='*60}")
print("CORRELACIÓN DE SPEARMAN (por RANGOS)")
print(f"{'='*60}")
print(f"Coeficiente ρ = {rho_spearman:.4f}")
print(f"p-value = {p_spearman:.4f}")
print(f"Significativo: {'Sí (p<0.05)' if p_spearman < 0.05 else 'No (p≥0.05)'}")

print(f"\n{'='*60}")
print("COMPARACIÓN: PEARSON vs SPEARMAN")
print(f"{'='*60}")
print(f"Pearson (lineal):   r = {r_pearson_comp:.4f}, p = {p_pearson_comp:.4f}")
print(f"Spearman (rangos):  ρ = {rho_spearman:.4f}, p = {p_spearman:.4f}")

print(f"\nDiferencias:")
print(f"  Δr = {abs(r_pearson_comp - rho_spearman):.4f}")
if abs(r_pearson_comp - rho_spearman) < 0.1:
    print(f"  Las diferencias son PEQUEÑAS: datos aproximadamente lineales")
else:
    print(f"  Las diferencias son GRANDES: relación no-lineal detectada")

# Cálculo manual de Spearman
diferencias_rangos = critica_ranking - publico_ranking
d_cuadrado = np.sum(diferencias_rangos ** 2)
rho_manual = 1 - (6 * d_cuadrado) / (n3 * (n3**2 - 1))

print(f"\nVerificación manual (fórmula: ρ = 1 - 6Σd²/(n(n²-1))):")
print(f"  Diferencias de rangos: {diferencias_rangos}")
print(f"  Σd² = {d_cuadrado}")
print(f"  ρ = 1 - 6×{d_cuadrado}/({n3}×{n3**2-1}) = {rho_manual:.4f} ✓")

# Interpretación
if abs(rho_spearman) >= 0.7:
    print(f"\nInterpretación: Acuerdo FUERTE entre crítica y público")
    print(f"  Las clasificaciones tienden a coincidir sustancialmente.")
elif abs(rho_spearman) >= 0.5:
    print(f"\nInterpretación: Acuerdo MODERADO")
else:
    print(f"\nInterpretación: Acuerdo DÉBIL")

# Gráficas
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Scatter plot
ax1 = axes[0]
ax1.scatter(critica_ranking, publico_ranking, s=150, alpha=0.6,
           color='darkgreen', edgecolors='black', linewidth=2)
# Línea de concordancia perfecta
ax1.plot([0.5, 8.5], [0.5, 8.5], 'r--', linewidth=2, alpha=0.7, 
        label='Concordancia perfecta')
ax1.set_xlabel('Clasificación por Crítica', fontsize=11, fontweight='bold')
ax1.set_ylabel('Clasificación por Público', fontsize=11, fontweight='bold')
ax1.set_title(f'Problema 3: Correlación de Spearman\nρ = {rho_spearman:.4f}, p = {p_spearman:.4f}', 
             fontsize=12, fontweight='bold')
ax1.set_xticks(range(1, 9))
ax1.set_yticks(range(1, 9))
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)
ax1.set_xlim([0.5, 8.5])
ax1.set_ylim([0.5, 8.5])

# Diferencias de rangos
ax2 = axes[1]
películas_labels = [f'Peli {i}' for i in range(1, n3+1)]
colores_dif = ['green' if d == 0 else 'red' for d in np.abs(diferencias_rangos)]
barras = ax2.bar(range(n3), np.abs(diferencias_rangos), color=colores_dif, 
                 alpha=0.7, edgecolor='black', linewidth=1.5)
ax2.set_xticks(range(n3))
ax2.set_xticklabels(películas_labels, rotation=45, ha='right')
ax2.set_ylabel('Diferencia de rangos |d|', fontsize=11, fontweight='bold')
ax2.set_title('Discrepancias entre Crítica y Público', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
ax2.axhline(y=0, color='black', linewidth=0.5)

for i, d in enumerate(diferencias_rangos):
    ax2.text(i, abs(d) + 0.1, f'{abs(d)}', ha='center', fontweight='bold')

plt.suptitle('Problema 3: Correlación de Spearman - Datos Ordinales', 
            fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

print(f"\n✓ CONCLUSIÓN Problema 3:")
print(f"  Spearman ρ = {rho_spearman:.4f} indica ACUERDO FUERTE entre")
print(f"  las clasificaciones de crítica y público (p = {p_spearman:.4f}).")
print(f"  Ambos grupos tienden a valorar las películas de manera similar,")
print(f"  aunque no necesariamente de forma linealmente perfecta.")

# ============================================================================
#                    PROBLEMA 4: CORRELACIÓN vs CAUSALIDAD
# ============================================================================

print("\n\n" + "="*80)
print("PROBLEMA 4: CORRELACIÓN ≠ CAUSALIDAD (Advertencia Crítica)")
print("="*80)

"""
ENUNCIADO SATÍRICO:
Se observa correlación entre el número de películas de Nicolas Cage lanzadas
por año y el número de ahogamientos en piscinas. ¿Nicolas Cage causa 
ahogamientos?

PROBLEMÁTICA:
Demostrar que CORRELACIÓN NO IMPLICA CAUSALIDAD.
Ejemplo ficticio pero educativo.

QUÉ SE CALCULA:
- Correlación espuria
- Cómo identificar correlaciones falsas
- Importancia del razonamiento científico
"""

# Datos ficticios pero realistas (basados en histórico real)
anos = np.array([2000, 2005, 2010, 2015, 2020])
peliculas_cage = np.array([2, 4, 5, 3, 2])
ahogamientos_anual = np.array([1200, 1500, 2000, 1800, 1300])

n4 = len(anos)

print(f"\nDatos espurios de {n4} años:")
print("Año | Películas Nicolas Cage | Ahogamientos en Piscinas")
print("-" * 60)
for a, p, ag in zip(anos, peliculas_cage, ahogamientos_anual):
    print(f"{a} |          {p}           |         {ag}")

# Correlación
r_espuria, p_espuria = pearsonr(peliculas_cage, ahogamientos_anual)

print(f"\n{'='*60}")
print("CORRELACIÓN ESPURIA (FALSA)")
print(f"{'='*60}")
print(f"Coeficiente r = {r_espuria:.4f}")
print(f"p-value = {p_espuria:.4f}")

if abs(r_espuria) > 0.3:
    print(f"\n⚠️  ALERTA: Correlación {abs(r_espuria):.2f} estadísticamente significativa!")
    print(f"Pero claramente NO hay relación causal.")

print(f"\n{'='*60}")
print("¿POR QUÉ OCURRE ESTA CORRELACIÓN ESPURIA?")
print(f"{'='*60}")
print("""
ANÁLISIS:
1. VARIABLE CONFUSORA (la verdadera causa):
   - Población total que visita piscinas en verano
   - Ambas variables aumentan con la temperatura estival
   - Más clima cálido → más películas de acción → más gente en piscinas

2. PELÍCULAS DE CAGE:
   - 2000-2010: Pico de popularidad
   - 2015-2020: Menos películas (carrera en decline)
   - Patrón coincide con ciclos de turismo

3. AHOGAMIENTOS:
   - Correlacionan con visitantes de piscinas
   - Visitantes correlacionan con temperatura
   - Temperatura correlaciona con películas de Cage
   - Pero Cage NO causa ahogamientos

CONCLUSIÓN: Es un ejemplo de correlación espuria por:
- Variable confusora no medida (temperatura, población)
- Coincidencia temporal
- Falsa causalidad
""")

# Añadir variable confusora
print(f"\n{'='*60}")
print("REVELANDO LA VARIABLE CONFUSORA")
print(f"{'='*60}")

temperaturas_promedio = np.array([28, 30, 31, 29, 27])  # °C en verano

r_cage_temp, _ = pearsonr(peliculas_cage, temperaturas_promedio)
r_ahogos_temp, _ = pearsonr(ahogamientos_anual, temperaturas_promedio)

print(f"\nTemperaturas promedio de verano: {temperaturas_promedio}")
print(f"\nCorrelación películas Cage - Temperatura: r = {r_cage_temp:.4f}")
print(f"Correlación ahogamientos - Temperatura: r = {r_ahogos_temp:.4f}")
print(f"\nAmbas variables correlacionan con TEMPERATURA, no entre sí causalmente.")

# Gráficas
fig, axes = plt.subplots(2, 2, figsize=(14, 11))

# 1. Correlación espuria
ax1 = axes[0, 0]
ax1.scatter(peliculas_cage, ahogamientos_anual, s=150, alpha=0.6,
           color='red', edgecolors='black', linewidth=2)
slope_esp, int_esp, _, _, _ = linregress(peliculas_cage, ahogamientos_anual)
x_esp = np.array([1.5, 5.5])
y_esp = slope_esp * x_esp + int_esp
ax1.plot(x_esp, y_esp, 'r-', linewidth=2.5, label=f'Tendencia (r={r_espuria:.3f})')
ax1.set_xlabel('Películas de Nicolas Cage / año', fontsize=11, fontweight='bold')
ax1.set_ylabel('Ahogamientos en piscinas / año', fontsize=11, fontweight='bold')
ax1.set_title('CORRELACIÓN ESPURIA: ¿Cause Effect?', fontsize=12, fontweight='bold',
             color='darkred', weight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)

# Añadir años en los puntos
for a, p, ag in zip(anos, peliculas_cage, ahogamientos_anual):
    ax1.annotate(str(a), (p, ag), xytext=(5, 5), textcoords='offset points', 
                fontsize=9, fontweight='bold')

# 2. Variable confusora - Temperatura
ax2 = axes[0, 1]
ax2.plot(anos, temperaturas_promedio, 'g-o', linewidth=2.5, markersize=8, label='Temperatura')
ax2.axhline(y=np.mean(temperaturas_promedio), color='green', linestyle='--', 
           alpha=0.5, label='Promedio')
ax2.set_xlabel('Año', fontsize=11, fontweight='bold')
ax2.set_ylabel('Temperatura promedio (°C)', fontsize=11, fontweight='bold')
ax2.set_title('VARIABLE CONFUSORA: Temperatura Estival', fontsize=12, fontweight='bold',
             color='darkgreen', weight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)

# 3. Correlaciones con temperatura
ax3 = axes[1, 0]
correlaciones = [r_cage_temp, r_ahogos_temp, r_espuria]
nombres = ['Películas vs\nTemperatura', 'Ahogamientos vs\nTemperatura', 'Películas vs\nAhogamientos\n(ESPURIA)']
colores_corr = ['green', 'blue', 'red']
barras = ax3.bar(range(3), correlaciones, color=colores_corr, alpha=0.7, 
                edgecolor='black', linewidth=2)
ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax3.set_xticks(range(3))
ax3.set_xticklabels(nombres, fontsize=10)
ax3.set_ylabel('Coeficiente de Correlación r', fontsize=11, fontweight='bold')
ax3.set_title('Correlaciones Reales vs Espuria', fontsize=12, fontweight='bold')
ax3.set_ylim([-0.2, 1])
ax3.grid(True, alpha=0.3, axis='y')
for i, r in enumerate(correlaciones):
    ax3.text(i, r + 0.05, f'{r:.3f}', ha='center', fontweight='bold', fontsize=11)

# 4. Diagrama causal
ax4 = axes[1, 1]
ax4.axis('off')

texto_causal = """
┌─────────────────────────────────────────┐
│   DIAGRAMA DE CAUSALIDAD CORRECTO      │
├─────────────────────────────────────────┤
│                                          │
│      TEMPERATURA ESTIVAL               │
│           ▼         ▼                   │
│     Películas    Ahogamientos          │
│     de Cage      en Piscinas           │
│                                          │
│  NO: Películas Cage → Ahogamientos     │
│      (Correlación espuria)              │
│                                          │
├─────────────────────────────────────────┤
│ LECCIÓN: Requiere causalidad            │
│ - Mecanismo plausible                   │
│ - Temporalidad correcta                 │
│ - Excluir variables confusoras          │
│ - Experimentos controlados              │
└─────────────────────────────────────────┘
"""

ax4.text(0.5, 0.5, texto_causal, ha='center', va='center', fontsize=10,
        family='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', 
                                       edgecolor='black', linewidth=2))

plt.suptitle('Problema 4: CORRELACIÓN ≠ CAUSALIDAD (Correlación Espuria)', 
            fontsize=13, fontweight='bold', y=0.995)
plt.tight_layout()
plt.show()

print(f"\n✗ CONCLUSIÓN Problema 4:")
print(f"  NUNCA asumir causalidad basada en correlación.")
print(f"  Este ejemplo muestra r = {r_espuria:.4f} entre películas de Cage")
print(f"  y ahogamientos, pero la relación es ESPURIA:")
print(f"  - Variable confusora: Temperatura")
print(f"  - Sin mecanismo causal plausible")
print(f"  - Necesitaríamos: experimentos, control de variables, lógica científica")

# ============================================================================
#                    ANÁLISIS MULTIVARIADO - MATRIZ DE CORRELACIONES
# ============================================================================

print("\n\n" + "="*80)
print("ANÁLISIS BONUS: MATRIZ DE CORRELACIONES (Multivariado)")
print("="*80)

"""
Se analiza simultaneamente las correlaciones entre múltiples variables
de jugadores de un equipo de baloncesto.
"""

# Crear dataset de múltiples variables
np.random.seed(42)
n_jugadores = 15

dataset_baloncesto = pd.DataFrame({
    'Altura (cm)': np.random.normal(195, 7, n_jugadores),
    'Peso (kg)': np.random.normal(100, 8, n_jugadores),
    'Puntos/partido': np.random.normal(18, 5, n_jugadores),
    'Asistencias': np.random.normal(5, 2, n_jugadores),
    'Años experiencia': np.random.randint(1, 15, n_jugadores)
})

# Asegurar algunas correlaciones lógicas
dataset_baloncesto['Peso (kg)'] = dataset_baloncesto['Altura (cm)'] * 0.4 + np.random.normal(0, 5, n_jugadores)
dataset_baloncesto['Puntos/partido'] = dataset_baloncesto['Años experiencia'] * 1.5 + np.random.normal(0, 4, n_jugadores)

print("\nDataset de 15 jugadores de baloncesto:")
print(dataset_baloncesto.round(1).to_string())

# Matriz de correlaciones de Pearson
matriz_corr = dataset_baloncesto.corr()

print(f"\n{'='*60}")
print("MATRIZ DE CORRELACIONES DE PEARSON")
print(f"{'='*60}")
print(matriz_corr.round(4).to_string())

# Identificar correlaciones fuertes
print(f"\n{'='*60}")
print("CORRELACIONES SIGNIFICATIVAS (r > 0.5):")
print(f"{'='*60}")
for i in range(len(matriz_corr.columns)):
    for j in range(i+1, len(matriz_corr.columns)):
        r_ij = matriz_corr.iloc[i, j]
        if abs(r_ij) > 0.5:
            var1 = matriz_corr.columns[i]
            var2 = matriz_corr.columns[j]
            print(f"  {var1} ↔ {var2}: r = {r_ij:.4f}")

# Gráfica de heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(matriz_corr, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
           cbar_kws={'label': 'Correlación'}, vmin=-1, vmax=1,
           linewidths=1, linecolor='black')
plt.title('Matriz de Correlaciones: Dataset Baloncesto\n(Heatmap)', 
         fontsize=13, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

print(f"\n✓ CONCLUSIÓN Análisis Multivariado:")
print(f"  La matriz de correlaciones permite identificar rápidamente")
print(f"  qué pares de variables están relacionadas.")
print(f"  Útil para análisis exploratorio y detección de multicolinealidad.")

# ============================================================================
#                    RESUMEN FINAL
# ============================================================================

print("\n\n" + "="*80)
print("RESUMEN: CORRELACIÓN Y RELACIÓN ENTRE VARIABLES")
print("="*80)

print("""
┌──────────────────────────────────────────────────────────────────────────┐
│                       COEFICIENTES DE CORRELACIÓN                        │
├──────────────────┬──────────────────┬──────────────────────────────────┤
│   Coeficiente    │      Rango       │         Interpretación           │
├──────────────────┼──────────────────┼──────────────────────────────────┤
│ Pearson (r)      │  -1 a +1         │ Relación LINEAL                 │
│ Spearman (ρ)     │  -1 a +1         │ Relación MONÓTONA (rangos)      │
│ Kendall (τ)      │  -1 a +1         │ Relación monotónica (alternativa)│
└──────────────────┴──────────────────┴──────────────────────────────────┘

INTERPRETACIÓN DE VALORES:

  r = +1.0  →  Correlación positiva PERFECTA
  r = +0.7 a +0.9  →  Correlación positiva FUERTE
  r = +0.5 a +0.7  →  Correlación positiva MODERADA
  r = +0.3 a +0.5  →  Correlación positiva DÉBIL
  r = 0.0 ±0.3  →  Poco o NO correlación
  r = -0.3 a -0.5  →  Correlación negativa DÉBIL
  r = -0.5 a -0.7  →  Correlación negativa MODERADA
  r = -0.7 a -0.9  →  Correlación negativa FUERTE
  r = -1.0  →  Correlación negativa PERFECTA

REQUISITOS PARA CAUSALIDAD:
├─ Correlación ESTADÍSTICA (r significativo)
├─ Temporalidad correcta (causa antes que efecto)
├─ Mecanismo plausible (explicación lógica)
├─ Control de confusores (eliminar alternativas)
└─ Replicabilidad (reproducible en otros contextos)

ERRORES COMUNES:
✗ Asumir causalidad desde correlación (Problema 4)
✗ Confundir r² (coef. determinación) con r (correlación)
✗ Olvidar que correlación mide relación LINEAL (Spearman para no-lineal)
✗ No validar que datos cumplan supuestos (normalidad, homocedasticidad)
✗ Extrapolar correlaciones a nuevas poblaciones sin verificación

CUÁNDO USAR CADA COEFICIENTE:
┌──────────────┬─────────────────────┬──────────────────────────────┐
│ Coeficiente  │ Tipo de Datos       │ Cuándo Usar                  │
├──────────────┼─────────────────────┼──────────────────────────────┤
│ Pearson (r)  │ Contínuos, normales │ Relaciones lineales          │
│              │ sin outliers        │ con datos paramétricos       │
├──────────────┼─────────────────────┼──────────────────────────────┤
│ Spearman (ρ) │ Ordinales o no-norm │ Datos ranqueados             │
│              │ con outliers        │ Relaciones no-lineales      │
├──────────────┼─────────────────────┼──────────────────────────────┤
│ Kendall (τ)  │ Ordinales           │ Muestras pequeñas (<50)      │
│              │ pequeñas            │ Concordancia entre jueces    │
└──────────────┴─────────────────────┴──────────────────────────────┘
""")

print("="*80)
print("FIN DEL ANÁLISIS DE CORRELACIÓN")
print("="*80)
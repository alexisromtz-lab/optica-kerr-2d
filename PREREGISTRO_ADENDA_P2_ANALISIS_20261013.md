# ADENDA P2 — PLAN DE ANÁLISIS PRE-DECLARADO (ANTES DE LA PRIMERA CIFRA)

## §0. TUPLA A2.1 · CLASE BOOTSTRAP
- `TARGET` = este archivo · `BLOB_PRE` = `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` (semilla vacía) · `LINEAS_PRE` = 0 · `HUELLA` = `ADENDA`.
- Gate de pre-vuelo corrido **antes** de escribir: `bash /Users/marlene/platino-labs/tools/gate_pre_escritura.sh PREREGISTRO_ADENDA_P2_ANALISIS_20261013.md e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 ADENDA` ⇒ **RC = 10** (`no existe`).
- **RC 10 en objeto nuevo = clase BOOTSTRAP, no append.** No hay fila previa que colisionar. Guardián sustituto del A2.1 para todo artefacto nuevo: **igualdad de blob** (`git hash-object` en disco vs `git rev-parse HEAD:<ruta>` tras el commit).
- Hora de la adenda: **2026-10-13T02:13:33Z**.
- Estado honesto de las fases: los tres procesos del ciclo (nulo del motor con χ³=0 · objeto χ³=1 · control de energía) fueron **disparados a 2026-10-13T02:12:14Z**; esta adenda se escribe **con CERO salidas leídas** (medido: `data/propagador_*.json` = *no matches*). El plan de análisis queda sellado **antes** de ver el primer número del objeto.

## §1. QUÉ DECIDE P2 Y QUÉ NO
- **Decide (sellado, heredado de §8 del pre-registro):** `residuo_plano_max = max_{x∈[1λ, x_fin]} |σ_y(x)/σ_y(0) − 1| ≤ 0.03`. Es el único veredicto de esta fase. El valor lo calcula el propio motor dentro de `correr()`; no se recalcula por fuera ni se redefine la ventana.
- **No decide:** `residuo_ley_segundo_momento`. La ley de segundo momento es la ley **LINEAL** `σ_y(x)² = σ_y(0)² (1 + (x/z_R^σ)²)`. El objeto χ³=1 **no** la sigue: sigue la relación de solitón (anchura constante). Por tanto, para el objeto, `res_ley` **se espera ROJO por construcción**, y leerlo como fallo sería confundir el objeto con el metro. Se reporta, no adjudica.
- **No decide:** el acierto de la relación `E0² w0² = 2/(k0² χ³)`. P2 mide **estabilidad de anchura**, no el valor exacto de la relación. Una familia desajustada también podría mantener anchura media y respirar (ver §3.c).

## §2. MÉTRICAS PRE-DECLARADAS
| id | qué | fuente | estatus |
|----|-----|--------|---------|
| A1 | `residuo_plano_max` con χ³=1 | motor, `data/propagador_objeto.json` | **ADJUDICA P2** (umbral 3%) |
| A2 | `residuo_plano_max` **y** `residuo_ley_segundo_momento` con χ³=0 | motor, `data/propagador_nulo_lineal.json` | **ADJUDICA como falsador del instrumento** |
| A3 | contraste `res_plano(χ³=1)` vs `res_plano(χ³=0)`; razón `σ_y(x_fin)/σ_y(0)` en ambos | ambas salidas | descriptivo |
| A4 | respiración: mínimos cuadrados de `σ_y(x)` sobre la ventana juzgada (χ³=1) ⇒ pendiente relativa, residuo máximo, RMS del residuo | `x`,`sigma_y` del objeto | **descriptivo, sin umbral sellado ⇒ NO adjudica** |
| A5 | si RMS de A4 ≠ 0: FFT de `(σ_y(x) − recta)` sobre la ventana ⇒ pico dominante en longitud de onda espacial y fracción de potencia | idem | descriptivo |
| A6 | estabilidad: deriva relativa máxima de `hist_energia` y `pico_Ez_final` del objeto vs el nulo | ambas salidas | descriptivo |
| A7 | control de energía en caja PEC sin fuente (χ³=0) | `data/propagador_control_energia.json` | adjudica **su propia** prueba (umbral sellado 1e-9, heredado) |

**A2 es el control duro.** Si el MISMO motor con χ³=0 **también** mantuviera la anchura (A2 plano ≤ 3%), el contraste no sería atribuible a Kerr y **A1 no probaría nada**: el motor sería el que confina, no la no linealidad. La forma exigida a A2 es de **dos lados**: `res_ley ≤ 0.02` (reproduce P1b con este motor) **y** `res_plano > 0.03` (no confina sin Kerr). Un A2 que cumpla sólo uno de los dos lados se reporta como **fallo del instrumento**, no de P2.

## §3. LOS TRES FENÓMENOS PEDIDOS POR EL DUEÑO — ESTADO DIMENSIONAL
El dictado pide explorar «colapso del haz (catastrophic self-focusing en 2D)», «inestabilidad modulacional» y «breathers». Los tres se declaran aquí antes de medir, para que la salida no elija su propia lectura.

**(a) Colapso / autofocalización catastrófica: EXCLUIDO POR DIMENSIÓN — no es un fallo de la corrida.**
Este objeto tiene **una** coordenada transversal (`y`); la propagación es en `x` y el campo es `E_z` ⇒ es **(1+1)D**, no (2+1)D. El colapso y la potencia crítica `P_cr = λ²/(2π n₀ n₂)` son el umbral del objeto **(2+1)D**. En (1+1)D la familia de solitones es **continua y sin umbral**. Ya está asentado en §1 del pre-registro (`PREREGISTRO_SOLITON_ESPACIAL_KERR_20261012.md`) con fecha del dueño (12-Oct-2026). **No se explora porque no existe en este objeto**; se reporta como frontera declarada, no como resultado faltante.

**(b) Inestabilidad modulacional: OTRO OBJETO — no se ejecuta.**
La IM es inestabilidad de un haz **ancho** (o de un fondo continuo) contra perturbaciones laterales; su firma exige una semilla de perturbación con número de onda sellado y un umbral de ganancia sellado. El objeto sellado de P2 es el solitón `sech` **fundamental**, que no es un fondo continuo. Ejecutarla aquí sería mover el objeto sin preregistro. **Se declara y no se corre.**

**(c) Breather / solitón oscilante: medible en la traza, pero NO adjudicable con este presupuesto.**
Un breather aparece cuando la entrada **no** satisface `E0² w0² = 2/(k0² χ³)` (desajuste ≠ 0); el objeto sellado está construido **sobre** la relación (desajuste 0) ⇒ la predicción pre-registrada es **anchura constante**, no respiración. Aun así A4/A5 miden la traza **sin umbral**: si hay respiración, se reporta como hallazgo **descriptivo**. Corolario declarado: la firma de un breather **no se puede adjudicar** con el residuo de P2, porque el residuo es un máximo de `|σ_y/σ_y(0) − 1|` que ya incluye discretización (~0.5% declarado a priori) y el borde de la esponja. Un breather exigiría su **propio pre-registro** con desajuste sellado y ventana sellada.

## §4. LO QUE ESTA ADENDA NO EJECUTA (DECLARADO, NO OMITIDO)
- **P3 (borde de la cota).** El pre-registro §8 lo pide en `w0 = 0.7117625434171772 λ` con `Δε_NL = 0.1`, verificando `control_energia` y `control_cfl`. **Los instrumentos sellados NO corren en el borde**: usan la malla y la amplitud de `w0 = 5 λ`. Correrlos ahí **no descarga P3** — es la familia «un umbral sellado puede comparar dos objetos distintos; su dominio se mide antes de disparar». ⇒ P3 **no se declara cumplido**; exige malla y amplitud propias ⇒ preregistro propio.
- **P4 (dos cinturas, 3λ y 5λ).** Cambia `L_y = 20 w0` y `L_x = 2 z_R + 6λ` ⇒ **otra malla** (sellada en §7 para `w0 = 5`) ⇒ otro objeto ⇒ preregistro propio.
- **`control_cfl`.** Costo medido ≈ 68 min (2 × 6994 pasos a 0.2936 s/paso). No descarga P3 (corre a `w0 = 5`). Se deja fuera de este ciclo; queda disponible como instrumento.

## §5. REGLA DE LECTURA DEL CIERRE
Toda cifra del acta de cierre viaja con: **comando que la respalda · hora UTC · universo/ventana declarada · unidad** (`grep -c` cuenta LÍNEAS, no ocurrencias). Los artefactos nuevos se cierran por **igualdad de blob** (disco vs `HEAD`), no por lectura del mensaje de éxito.

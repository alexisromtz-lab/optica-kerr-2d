# ACTA P2 - SOLITON ESPACIAL KERR 2D TE (1+1)D: CIERRE DEL CICLO

T_UTC_ACTA = 2026-10-13T05:33Z
T_UTC_DISPARO = 2026-10-13T02:12:14Z

UNIVERSO DECLARADO: el motor `propagador_2d_te.py` (disco == HEAD == blob `c103ef6c218414a5e1980a30aa24489b938de557`) + los 2 crudos P2 + los 3 crudos de control + los 2 pre-registros de addenda + el instrumento de analisis `control_energia_invariante.py`. MOTOR = `git hash-object` + `shasum -a 256` + `python3 -B` con numpy 2.4.6. UNIDAD = celda / linea / byte / blob. VENTANA = reloj UTC de la linea `T_UTC_ACTA`.

REGLA DURA: los umbrales que adjudican (A1 = 0.03; A2 = 0.02 y 0.03 en dos lados; control de energia = 1e-9) estaban SELLADOS en `PREREGISTRO_SOLITON_ESPACIAL_KERR_20261012.md` 8, en `PREREGISTRO_ADENDA_P2_ANALISIS_20261013.md` 1 y 2, y en el CLI del motor, ANTES de la primera cifra. **Ninguno se movio.** Toda cifra de esta acta viaja con su comando, su hora UTC, su universo y su unidad.

## 1. Que se corrio, con que, y cuando

| proceso | CLI | PID | inicio UTC | salida | mtime | segundos internos |
|---|---|---|---|---|---|---|
| objeto no lineal | `python3 -B propagador_2d_te.py --correr` | 84147 | 02:12:15Z | `data/propagador_objeto.json` | Oct 13 04:25 | 8016.366888046265 |
| nulo lineal | `python3 -B propagador_2d_te.py --nulo-lineal` | 84146 | 02:12:15Z | `data/propagador_nulo_lineal.json` | Oct 13 04:25 | 8013.468793153763 |
| control de energia PEC | `python3 -B propagador_2d_te.py --control-energia` | 84148 | 02:12:15Z | `data/propagador_control_energia.json` | Oct 13 02:20 | no impreso en el crudo |
| invariante (V1 a V4) | `python3 -B control_energia_invariante.py --correr` | - | - | `data/control_energia_invariante.json` | Oct 13 03:02 | 816.1310479640961 (rama chi3 = 1) |
| reserva barrido dt | `python3 -B control_energia_invariante.py --barrido-dt` | - | - | `data/control_energia_barrido_dt.json` | Oct 13 03:45 | no impreso en el crudo |

Parametros del objeto, leidos de los crudos: `pasos = 6994` (6590 de transito + 404 de asentar), `dt = 0.02474873734152916`, `dx = 0.05`, `NX = 3262`, `NY = 2000`, `I_SRC = 60`, `n_acc = 121`, `ventana_juzgada = [1.0, 157.05]`. `z_R = 78.5398163`; la ventana sellada es `[0, 2 z_R] = [0, 157.0796327]`.

**Declaracion de ventana:** el motor juzga desde `VENTANA_I0 = 80` (x = 1.0 lam) y hasta `VENTANA_I1` (x = 157.05 lam). Respecto de la ventana sellada se excluye la primera longitud de onda (agua arriba de la fuente) y el ultimo tercio de celda. Se declara; no cambia el veredicto.

## 2. Codigos de retorno: lo que el crudo NO guarda

`RC_CONTROL_ENERGIA = 0`, `RC_CORRIDA = 0` (03:02:18Z), `RC_BARRIDO = 0` (03:45:27Z) fueron impresos por la terminal que lanzo los procesos, **no** por el crudo. Los dos corridos pesados **no llevan RC dentro del artefacto**. Lo que el artefacto si testifica, y es lo que se lee: (i) **no hay linea `FALLO DEL ESQUEMA`** en ninguno de los dos logs (la guarda `RuntimeError` de `paso()` no disparo), y (ii) **la ultima linea de cada log es la escritura exitosa** `escrito: .../data/propagador_*.json`, o sea `guardar()` corrio hasta el final. Se declara como limite de medicion: **el RC de los dos corridos pesados no esta medido; lo que esta medido es que la guarda no disparo y que la escritura se completo.**

## 3. Los crudos: identidad

| pieza | bytes | mtime | sha16 | sha256 |
|---|---|---|---|---|
| `data/propagador_objeto.json` | 184004 | Oct 13 04:25 | `aff2d59f04ebe3ef` | `aff2d59f04ebe3ef9bff3f17b0041f95d4a7d1e902d8f946f6183829c6a14d8a` |
| `data/propagador_nulo_lineal.json` | 183946 | Oct 13 04:25 | `c4c932c4fe232dda` | `c4c932c4fe232ddae6ac4cd352709fc03db92a6d70cf114f5b593c06d55d3eb6` |
| `data/logs/p2_objeto.log` | 1179 | Oct 13 03:13 | - | `4e8c7156f70a198f294dda88ce2f5c5e296616a3b3c57d45e94bc22c344c9722` |
| `data/logs/p2_nulo.log` | 1184 | Oct 13 03:13 | - | `f32867b9fb1d1acc376e0886a1152ec2bb026565879ac045a2d511f7849abdb3` |
| `data/propagador_control_energia.json` | 952 | Oct 13 02:20 | - | `d18550d9543cbfe74b5add4d17cbf317e37e45cd2472577be99d4aa149ac9a48` |
| `data/control_energia_invariante.json` | 7352 | Oct 13 03:02 | - | `7a41421ddedfaffe469925a7231ba082b3c95dc6498132e9e5b0738cdaf24ad0` |
| `data/control_energia_barrido_dt.json` | 6718 | Oct 13 03:45 | - | `86960efe2635931870308c1084040ededcb7ad011852d71f314277c5945448b7` |

Identidad por **igualdad de blob** contra HEAD para las piezas que HEAD contiene: motor `c103ef6c218414a5e1980a30aa24489b938de557` (disco == HEAD, medido 05:31:43Z), `nulo_lineal.py` `69f94564db2e61891dda59a9ef666f0c856d8587`, `MANIFIESTO.txt` `d218de6b25c5c186e75ae056fdfe79503b60c8af`, preregistro `45fa6e96b707bd5c780cb3b9e160ac94a3be2a91`. Las piezas nuevas se identifican por su blob de disco: addenda de analisis `25fc8f04a5610b4040804bdd153a95da5110a413`, addenda de invariante `08cc54ec20863cd39c7369aed0f27a413d4f67c1` (270 l, 15496 B, cabezas 25 = 1 + 10 + 14), instrumento `a9753d90ae217a47aace794a6410f890983b000`.

## 4. A1 - EL VEREDICTO DE ESTA FASE: ROJO

### 4.a Criterio sellado (pre-registro 8, P2)

`max_{x en [1.0, 157.05]} | sigma_y(x)/sigma_y(0) - 1 | <= 0.03` (3.0%). El pre-registro lo escribe como `max_{x en [0, 2 z_R]}`; la ventana efectiva del motor se declara en 1.

### 4.b Medido (chi3 = 1, `data/propagador_objeto.json`)

| cifra | valor | comando |
|---|---|---|
| `residuo_plano_max` | **0.13113286486070153** | lectura del crudo, 05:30:08Z |
| umbral sellado | 0.03 | pre-registro 8 |
| exceso | **4.3711 x** el umbral | `0.13113286486070153 / 0.03` |
| `sigma_y(0)` | 4.534053888222207 | idem |
| `sigma_y(x_fin)` | 5.12805 | idem |
| `sigma_y(x_fin)/sigma_y(0)` | 1.131007722 | idem |

### 4.c Veredicto y lectura pre-escrita

**ROJO.** El haz no lineal se ensancha **13.1133%** sobre la ventana juzgada (x de 1 lam a 157.05 lam, o sea ~2 z_R), contra el 3% sellado.

La lectura **ya estaba escrita** en el pre-registro del objeto, 8 P2, antes de correr: *«Si ensancha mas, **la relacion congelada no sostiene el haz** y se declara; **no se recalibra la constante**.»* ⇒ Esto es lo que se declara. **No se recalibra la constante `2` del 3.** El ROJO **no se adjudica por argumento**: se adjudica por la regla sellada, que solo devuelve dos salidas.

## 5. A2 - FALSADOR DEL INSTRUMENTO: PASA EN LOS DOS LADOS

| lado | criterio sellado | medido (chi3 = 0) | veredicto |
|---|---|---|---|
| ley | `residuo_ley_segundo_momento <= 0.02` | **0.004567974999664992** (0.457%) | **PASA** |
| plano | `residuo_plano_max > 0.03` | **0.19064381668848895** (19.0644%) | **PASA** |

**Consecuencia: el instrumento queda exonerado.** (i) Con chi3 = 0 el motor reproduce la ley de segundo momento del pre-registro 4 al 0.457%, que es la misma cifra sellada de P1b (`data/nulo_lineal_sech_fdtd.json`, `residuo_max = 4.5680e-03`) ⇒ **P1b se reproduce con este motor**. (ii) Con chi3 = 0 el haz difracta 19.06% ⇒ **el motor NO confina por si mismo**: no hay confinamiento espurio que pueda fabricar el resultado del objeto.

**Declaracion de dominio del umbral.** El control lineal **falla** el criterio A1 (19.06% = 6.35 x el umbral). Eso **no** es defecto de dominio: un nulo que pasara el criterio no discriminaria nada; el nulo **debe** fallarlo. Lo que adjudica el criterio es que **el objeto tambien lo falla** (13.11%).

## 6. A3 - CONTRASTE (descriptivo)

| cifra | chi3 = 0 | chi3 = 1 |
|---|---|---|
| `residuo_plano_max` | 0.190643816688 | 0.131132864861 |
| `sigma_y(x_fin)/sigma_y(0)` | 1.190534116 | 1.131007722 |

Reduccion absoluta del ensanche por la no linealidad: **0.059511** (5.9511 puntos porcentuales). Reduccion relativa: **0.312158** (31.2158%).

Lectura descriptiva: la no linealidad **empuja en la direccion predicha** (V2, 7.c de la adenda de invariante), pero **queda lejos del autoatrapamiento**: falta reducir 0.1011 de residuo (de 0.1311 a 0.03) y el factor relativo observado es 0.312. **A3 no adjudica** (sin umbral sellado propio).

## 7. A4 y A5 - RESPIRACION (descriptivo, sin umbral: NO ADJUDICA)

### 7.a A4: recta de minimos cuadrados de sigma_y(x) sobre la ventana

| rama | pendiente (por lam) | pendiente relativa total | residuo max | RMS del residuo |
|---|---|---|---|---|
| chi3 = 0 | 0.00561858899 | 0.193355523 | 0.138774 | 0.0593044 |
| chi3 = 1 | 0.00386334884 | 0.132966127 | 0.10773 | 0.0463403 |

### 7.b A5: FFT del residuo de la recta (chi3 = 1)

| pico | longitud espacial | fraccion de potencia (>0) |
|---|---|---|
| 1 | **156.1 lam** | **0.886795** |
| 2 | 78.05 lam | 0.110096 |
| 3 | 52.0333 lam | 0.0022902 |

**Lectura declarada, y su limite.** La ventana mide 157.05 lam. El pico dominante es **156.1 lam: la longitud de la ventana**. El residuo esta dominado por **tendencia/curvatura**, no por una oscilacion. El segundo pico, **78.05 lam, es media ventana, o sea z_R** (78.5398 lam). ⇒ **Con este presupuesto no se lee una firma de respiracion discreta.** A4 y A5 son descriptivos; la adenda de analisis, 2, ya habia declarado que **el breather no es adjudicable con este presupuesto** (terminos de ~0.5% de discretizacion mas borde de esponja, del mismo orden que el residuo). **No se declara breather.** Le corresponde su propio pre-registro.

## 8. A6 - ESTABILIDAD, Y EL DEFECTO DE SU METRO

| cifra | chi3 = 0 | chi3 = 1 | lectura |
|---|---|---|---|
| `pico_Ez_final` | 0.04501276734891828 | 0.04498835058364458 | Δ relativo -5.423e-4: el pico no crece ni decae |
| `S0_fuga_max_rel` | 0.002779059291007524 | 0.051652077899901006 | fuga x18.59 mayor con Kerr |
| deriva relativa de `hist_energia` | 1.13285e+11 | 1.13421e+11 | **INERTE: no se reporta** |

**Defecto del metro, declarado.** La pata «deriva relativa maxima de `hist_energia`» que la adenda de analisis, 2, pre-declaro para A6 es **inerte por construccion**: el primer par de `hist_energia` es `[t = 0.01237436867076458, E = 7.72151223e-13]` ⇒ **el denominador es ruido de maquina** y la razon sale 1.13e+11 en las dos ramas, coincidiendo hasta el cuarto digito. Dos cifras que coinciden porque el cero es el mismo **no miden el objeto**. Se declara la inertancia y **no se reporta deriva**. Lo que A6 si mide son `pico_Ez_final` y `S0_fuga_max_rel`. (Familia ya registrada: *un cero que cuadra consigo mismo es un verde falso* · *una salida que no puede diferir no es evidencia*.)

## 9. A7 - CONTROL DE ENERGIA, SU DEFECTO DE UNIDAD, Y LA RESERVA

### 9.a El ROJO, citado tal cual

`data/propagador_control_energia.json`: `veredicto = "ROJO"`, `deriva_global = 0.15686501125907726`, `deriva_peor_par = 0.11693477574005584`, `umbral = 1e-09`, chi3 = 0 en caja PEC cerrada, sin fuente ni esponja, 400 pasos libres. **Se cita el ROJO tal cual resulto.** El ROJO **no se sustituye** por el verde de un metro nuevo: los dos se imprimen, el umbral sellado de 1e-9 se mantiene, y **su defecto de dominio se declara**.

### 9.b El defecto de unidad, medido

El instrumento nuevo (`control_energia_invariante.py`, `_invariante`) suma energias **sin el factor de area de celda** que su referencia colocal si lleva ⇒ `defecto_metro_max_rel = 0.9975 = 1 - DX*DY` **exacto** (`DX*DY = 0.0025`). Prueba analitica en k = 0: `DX*DY * U2(k=0) = 5.066059161232e-04 = U1_colocal(k=0)`. Prueba de independencia: el mismo 0.9975 sale en las **dos** ramas del barrido (9.d), o sea es un factor de unidad, no un efecto del paso de tiempo.

### 9.c Veredictos V1 a V4 del instrumento

V3 fidelidad: **PASA**, bit-exacto (`peor_diferencia_abs = 0.0`, `REPRODUCE`). V4 reduccion TE: **PASA** exacto (`max_Ex = max_Ey = max_Hz = 0.0`, `CERO_EXACTO`). V2 el metro puede moverse: **PASA en direccion** (3.2042e-03 con chi3 = 0 a 5.3177e-03 con chi3 = 1). V1 el invariante se conserva: **FALLA** (`disparador_reserva_barrido_dt = "CORRER (V1 fallo)"`).

### 9.d Reserva barrido dt: veredicto sellado

| rama | cfl | pasos | dt | deriva_global_ancla0 (M2) | deriva_global_ancla0 (M1) | segundos |
|---|---|---|---|---|---|---|
| A | 0.70 | 400 | 0.02474873734152916 | 0.003204237419178968 | 0.15686501125907726 | 861.0 |
| B | 0.35 | 800 | 0.01237436867076458 | 0.0224012938800231 | 0.02221259463092684 | 1064.4 |

`razon = 0.14303805112062856` (< 3) ⇒ **`lectura = "DEL OBJETO"`**. Se incorpora formalmente como veredicto sellado. **Y se declara su limite:** al afinar dt la deriva M2 **subio** x6.99 (3.2042e-03 a 2.2401e-02), direccion **contraria** a O(dt^2); y `M1/M2` vale 48.955 en A contra 0.99158 en B. ⇒ **el cociente tiene bajo poder discriminativo** porque el termino constante (el factor de unidad 1 - DX*DY) domina sobre el termino que escala con dt. La lectura `DEL OBJETO` se mantiene porque es lo que la regla sellada devuelve, no porque discrimine bien.

## 10. Fronteras declaradas: lo que NO se midio y por que

- **Colapso y autofocalizacion catastrofica: EXCLUIDO POR DIMENSION.** El objeto es **(1+1)D**: campo `E_z`, sin variacion en `z`, propagacion en `x`, confinamiento en `y`. En (1+1)D transversal **no hay umbral ni potencia critica**; `P_cr = lambda^2/(2 pi n0 n2)` es el umbral del colapso de **(2+1)D** y **no aplica**. **No se explora porque no existe en este objeto** (pre-registro 1 y adenda de analisis 3.a).
- **Inestabilidad modulacional: OTRO OBJETO - NO EJECUTADA.** Exige perturbacion sembrada y umbral de ganancia; no es este banco (adenda de analisis 3.b).
- **Breather: medible en la traza, NO adjudicable con este presupuesto** (adenda de analisis 3.c). A4/A5 lo miran sin umbral (7).
- **P3 (borde, `w0 = 0.7117625434171772`): NO ejecutado.** Exige malla y amplitud propias ⇒ pre-registro propio.
- **P4 (dos cinturas, 3 lam y 5 lam): NO ejecutado.** Malla nueva + pre-registro nuevo.
- **`control_cfl` (CFL 0.9 contra 0.70, ~68 min): NO ejecutado.** No descarga P3.
- **THG (tercer armonico): NO MEDIDO.** Es observable co-medido declarado en el pre-registro 6 con cota a priori 4.1e-06; en este ciclo no se instrumento el observador a 3 omega.

## 11. Causa candidata del ROJO: DECLARADA, NO ADJUDICADA

El pre-registro 3 deriva `E0^2 * w0^2 = 2/(k0^2 * chi3)` de la NLSE paraxial **escrita con coeficiente 1** en el termino cubico: `2 i k0 E_x + E_yy + k0^2 chi3 |E|^2 E = 0`. El motor **no resuelve esa NLSE**: resuelve Maxwell escalar con `eps = eps0 * (1 + chi3 * Ez^2)` aplicado como factor sobre la derivada espacial en `paso()`, con `Ez` **instantanea**, y guarda `Ez` en una malla escalonada Yee con leapfrog explicito.

**Candidato declarado, sin adjudicar:** una reduccion paraxial del **modelo del motor** puede llevar un coeficiente cubico **distinto de 1**. Si lo lleva, el `E0` del 3 queda **por debajo** del necesario, el sech lanzado **no es el punto fijo de esta ecuacion**, y el 13.11% de ensanche seria **defecto del lanzamiento**, no del soliton. **Este ciclo no midio ese coeficiente: por eso no se adjudica.** El acta lo declara como candidato, no como causa.

**Test falsable pre-declarado para el ciclo siguiente** (umbral a sellar antes de la primera cifra):

1. **Medir primero el coeficiente cubico efectivo del motor** con un banco propio y barato: onda plana uniforme en `y`, amplitud conocida, y fase no lineal acumulada contra amplitud. H0: el coeficiente efectivo es 1 (el `2` del 3 es el correcto para este motor). H1: difiere.
2. **Solo si H0 se refuta**, barrer `E0` con `w0 = 5 lam` y `chi3` fijo y localizar `E0*` que **minimiza** `residuo_plano_max`. Se reporta `E0*/E0_SELLADO` con su presupuesto de metro. Prediccion de H0: indistinguible de 1 dentro de 0.5%. Si sale indistinguible de 1, **el candidato muere y el ROJO es del objeto**.
3. **La constante del 3 NO se toca en ningun caso**, ni antes ni despues del barrido: la regla del pre-registro del objeto (*no se recalibra la constante*) se respeta. Lo que el barrido mide es **si el motor tiene otra**, no cuanto hay que mover la constante sellada.

Regla que el candidato respeta y que aqui se vuelve a imprimir: **un mapeo exige que existan los dos terminos.** La derivacion del 3 es un mapeo entre la NLSE paraxial y el perfil lanzado; el segundo termino de ese mapeo (la ecuacion que el motor **realmente** integra) **no esta medido en este ciclo**. Todo argumento posterior al ROJO tiene que pasar por esa medicion, no por la derivacion en prosa.

## 12. Presupuesto real, contencion, y deuda tecnica declarada

- Costo **en corrida**: 8013.468793153763 / 6994 = **1.1458 s por paso** (nulo) y 8016.366888046265 / 6994 = **1.1462 s por paso** (objeto). Duracion real: **2 h 13 min 33 s** y **2 h 13 min 36 s**.
- El costo medido **aislado**, antes de lanzar, fue 0.2936 s por paso ⇒ el costo en corrida es **x3.90** el aislado. Atribucion declarada, no adjudicada: contencion (los dos pesados + el invariante + el barrido corriendo a la vez) y swap.
- **Swap medido 4910.19 MB de 6144 MB**; RAM libre ~61 MB. Mecanismo declarado del sobrecosto: `paso()` crea del orden de 50 temporales de malla completa (52 MB cada uno) por paso ⇒ del orden de 2.6 GB de asignacion y transito por paso; los slices con stride obligan a iteracion buffereada de numpy.
- **Deuda tecnica declarada, NO corregida:** buffers reutilizados y `out=` en las operaciones de `paso()`. **No se toca el motor**: la custodia prohibe editar la pieza en vuelo, y el motor debe permanecer byte a byte identico a HEAD. Optimizar es deuda para un ciclo propio.

## 13. Sello del cierre (se mide FUERA, no se imprime aqui)

Una identidad impresa **dentro** de la pieza describe su version **anterior**. Por eso las lineas, los bytes, el sha16, el blob y el hash de commit de esta acta se miden **en la terminal, despues de escribirla**, y se imprimen en el cierre del ciclo - no aqui.

Estado de identidad que si se declara en la pieza, porque estaba medido **antes** de escribirla (`05:31:43Z`): el motor en disco es **igual** a HEAD (`c103ef6c218414a5e1980a30aa24489b938de557`), y `git status --porcelain` daba **10 entradas, todas `??`, cero modificadas** (`05:30:08Z`). El commit atomico de este ciclo debe llevar el arbol a `sucios = 0` **sin** tocar el motor.

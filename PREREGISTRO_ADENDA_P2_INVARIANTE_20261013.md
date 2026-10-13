# PRE-REGISTRO ADENDA P2 — EL INVARIANTE (metro nuevo) — 2026-10-13

## 0. Contrato A2.1 (clase bootstrap)

- TARGET = `PREREGISTRO_ADENDA_P2_INVARIANTE_20261013.md`
- BLOB_PRE = `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` (blob vacio: el archivo NO existia)
- LINEAS_PRE = 0 · HUELLA = `INVARIANTE`
- GATE = **RC 10** (no existe) ⇒ clase bootstrap; guardian sustituto = **igualdad de blob**.
- T_UTC_PREVUELO = 2026-10-13T02:28:30Z. Cero cifras leidas de esta pieza (no existia).
- Este archivo se escribe **antes** de correr el instrumento: sella las predicciones antes de la primera cifra.

## 1. El crudo que motiva esta adenda (medido, no argumentado)

`data/propagador_control_energia.json` — T_UTC 2026-10-13T02:12:15Z, RC 0:

| campo | valor |
|---|---|
| chi3 | 0.0 |
| pasos_libres | 400 |
| pares | 5 |
| umbral | 1e-09 |
| U0 | 5.066059161232340e-04 |
| U_fin | 5.860746588598202e-04 |
| deriva_global | 1.5686501125907726e-01 |
| deriva_peor_par | 1.1693477574005584e-01 |
| deriva_por_par | 1.1693477574005584e-01 · 6.943300755272275e-02 · 6.207741888182505e-02 · 7.474479289240721e-03 · 2.494425034993153e-02 |
| veredicto | **ROJO** |

Un ROJO a ocho ordenes del umbral **no se adjudica por argumento**: hay que separar
**defecto del OBJETO** de **defecto del METRO**. Ese es el unico proposito de esta adenda.

## 2. Dos metros, un objeto

- **M1 — el metro del motor** (`propagador_2d_te.energia`): suma **colocal** — misma celda,
  mismo indice temporal — de `(1/2)(eps0 |E|^2 + |B|^2/mu0)`. Pero `paso()` es una
  **saltarina entrecruzada**: `E` vive en pasos enteros (`E^n`) y `H` en semienteros
  (`H^{n+1/2}`). Sumar cuadrado-a-cuadrado los mezcla con defecto `O((omega dt)^2)`.
  Con `omega dt = 1.555009028355428e-01` ⇒ `(omega dt)^2 = 2.418051...e-02`.
- **M2 — el invariante del esquema** (nuevo):

  `U^n = (1/2) eps0 sum |E^n|^2 + (1/2) mu0 sum H^{n-1/2} . H^{n+1/2}`

  forma **bilineal intercalada** en `H`, **no** cuadratica. Derivacion (con `C` = rizo del
  esquema y `C^T = -C` skew-adjunto por PEC):

  ```
  H^{n+3/2} - H^{n-1/2} = -(dt/mu0) C (E^n + E^{n+1})
  |E^{n+1}|^2 - |E^n|^2 = (dt/eps0) (E^{n+1}+E^n) . C^T H^{n+1/2}
  dU = (1/2)dt (E^{n+1}+E^n).C^T H^{n+1/2}
       - (1/2)dt H^{n+1/2}.C(E^{n+1}+E^n) = 0      [usando u.Cv = -v.Cu]
  ```

  ⇒ **M2 es el invariante exacto del esquema lineal** (`chi3 = 0`).

**DECLARADO (no corregido):** el IC (una columna de `Ez` con `H = 0`) **no esta en la
cascara** — `H` no tiene par en `k = 0` — y `pec_muros` recorta la `Ez` de pared despues del
paso. Las dos cosas son parte del OBJETO: el protocolo las mide, no las arregla.

## 3. Protocolo (identico al del motor: la MISMA trayectoria, dos metros)

- Malla sellada: `NX 3262`, `NY 2000`, `dx 5e-2`, `DT` (CFL 0.70), `I_SRC 60`, **PEC** en las
  cuatro paredes, **sin** esponja, **sin** fuente, `chi3 = 0`.
- IC identica: `F["Ez"][I_SRC,:] = sech sellado` (via `perfiles()`).
- **400** pasos libres; muestreo en `k = 0, 80, 160, 240, 320, 400` (`h = pasos_libres//5 = 80`)
  ⇒ **6 muestras, 5 pares**. Identico al motor.
- En **cada** muestra se evaluan **los dos metros sobre el MISMO estado**:
  `M1 = energia(F)` y `M2` con la pareja `H^{k-1/2} . H^{k+1/2}`.
- Elemento aislado: los dos metros **comparten el objeto** y difieren **solo** en la unidad
  temporal con que suman `H`. Ninguna otra diferencia.

## 4. Predicciones falsables (selladas antes de la primera cifra)

- **V1 — el invariante se conserva (ADJUDICA el color del §1).**
  `|deriva_global(M2)| <= 1e-9` **Y** `|deriva_peor_par(M2)| <= 1e-9` ⇒ el esquema conserva
  EXACTAMENTE su invariante en esta caja ⇒ el ROJO del §1 es **defecto del METRO** (dominio del
  umbral), no del objeto. Si M2 tambien deriva, el ROJO es del **objeto** y se declara asi.
- **V2 — el metro nuevo PUEDE moverse (control negativo obligatorio).**
  Con `chi3 = 1.0`, mismo protocolo y mismo M2 ⇒ `|deriva_global(M2)| > 1e-9` (el propio
  docstring del motor declara que la via Kerr explicita NO es exactamente conservativa).
  **Si M2 sale plano tambien con `chi3 = 1`, M2 es CIEGO por construccion y V1 no vale.**
- **V3 — fidelidad de la replica (control positivo obligatorio).**
  Mi corrida con `chi3 = 0` debe reproducir el crudo del motor **digito a digito**:
  `U0 5.066059161232340e-04` · `U_fin 5.860746588598202e-04` ·
  `deriva_global 1.5686501125907726e-01` · `deriva_peor_par 1.1693477574005584e-01`.
  Si no reproduce, mi instrumento **no corrio el mismo objeto** y nada de esta adenda adjudica.
- **V4 — dominio del metro nuevo (declarado).**
  La reduccion TE de este objeto deja `max|Ex| = max|Ey| = max|Hz| = 0` **exactos** ⇒ los pares
  que M2 omite (`Ex.Ex`, `Ey.Ey`, `Hz.Hz`) son exactamente cero. Si alguno es distinto de 0,
  M2 esta midiendo otro objeto: se **declara incompleto**, no se completa a mano.
- **Reserva (instrumento escrito, NO corrido).** Si V1 falla (`|deriva_global(M2)| > 1e-9`), se
  corre el **barrido de dt**: CFL 0.70 con 400 pasos contra CFL 0.35 con 800 pasos (mismo tiempo
  fisico). Si la deriva cae por ~4 es `O(dt^2)` **del metro**; si no cae, es **del objeto**. El
  disparador (`V1 falla`) se pre-declara aqui para no elegirlo despues de ver la salida.

## 5. Que NO se hace

- NO se baja el umbral `1e-9`: queda sellado tal cual.
- NO se edita el motor: `propagador_2d_te.py` es **testigo de control de P1** — se **importa**, no se toca.
- NO se re-ancla en silencio: se reportan **las dos anclas** (ancla `k=0`, la del sello, para
  comparabilidad; y ancla en la primera muestra **en cascara**, `k=80`) como **lecturas distintas**.
- NO se sustituye el ROJO por un verde: los dos numeros se imprimen **juntos**.
- NO se adjudica P2 con esta adenda: P2 lo adjudica `residuo_plano_max <= 3e-2` en la adenda P2.

## 6. Regla de lectura

Toda cifra viaja con **comando + hora UTC + universo + unidad**. El cierre de la pieza nueva se
hace por **igualdad de blob**, nunca leyendo el mensaje de exito.
UNIVERSO DECLARADO: el del motor (`UNIVERSO` de `propagador_2d_te.py`) mas los artefactos de
`data/` de esta pieza. UNIDAD = celda / linea / byte.

## 7. Adjudicacion medida del §1 y de las predicciones V1–V4

Crudo: `data/control_energia_invariante.json` (7352 B), `T_UTC 2026-10-13T02:30:58Z` (inicio del
instrumento); `data/logs/p2_invariante.log` cierra con `escrito: … (7352 bytes)`; terminal
`RC_CORRIDA=0` a `2026-10-13T03:02:18Z`. Veredicto del instrumento, tal cual:
`veredicto_M1_colocal = "ROJO"` · `veredicto_M2_invariante = "ROJO"`.

### 7.a V3 — fidelidad de la replica: PASA, bit a bit

`V3_fidelidad_replica.veredicto = "REPRODUCE"` · `peor_diferencia_abs = 0.0` ·
`diferencias_abs = {U0 0.0, U_fin 0.0, deriva_global 0.0, deriva_peor_par 0.0, deriva_por_par_max 0.0}`.
La corrida `chi3 = 0` reproduce el crudo del motor **digito a digito** (`U0 5.066059161232340e-04` ·
`U_fin 5.860746588598202e-04` · `deriva_global 1.5686501125907726e-01` ·
`deriva_peor_par 1.1693477574005584e-01`) ⇒ la trayectoria es el MISMO objeto y toda diferencia
entre M1 y M2 es **del metro**, no de la corrida. (Exacto porque los bytes son identicos; una
diferencia de `0.0` en coma flotante reproducida no es una coincidencia.)

### 7.b V4 — dominio del metro nuevo: PASA, exacto

`V4_reduccion_TE_cero = {max_Ex 0.0, max_Ey 0.0, max_Hz 0.0, veredicto "CERO_EXACTO"}` en las **6**
muestras (`extremos_por_muestra`). El objeto nunca sale del subespacio TE ⇒ los pares que M2 omite
son exactamente cero: no hay objeto faltante.

### 7.c V2 — el metro puede moverse: PASA en direccion

`V2_metro_puede_moverse = true`. Con `chi3 = 1.0` la deriva global de M2 pasa de
`3.204237419178968e-03` a `5.317677312151048e-03`, y `U1_colocal(k=0)` pasa de
`5.066059161232e-04` a `5.069481155317e-04` (contribucion Kerr en `k=0`, coherente con
`0.25 eps0 chi3 |E|^4 dx dy`). M2 no es ciego: se mueve con el objeto.

### 7.d V1 — el invariante NO se conserva: FALLA

`V1_invariante_se_conserva = false`. Crudo:
`M2_invariante.deriva_peor_par = 1.4928755491749235e-01` ·
`M2_invariante.deriva_global_ancla0 = 3.204237419178968e-03` ·
`M2_invariante.deriva_global_ancla_cascara = 7.561619079411264e-02` — los tres muy por encima del
`1e-09` sellado. **La forma bilineal intercalada, tal como se escribio, NO es plana en esta caja.**
Relacion medida entre metros (mismo objeto, misma trayectoria): la deriva global de M2
(`3.204e-03`) es **~49x** menor que la de M1 (`1.5687e-01`) ⇒ el invariante **es mucho mejor**, no
es suficiente.

### 7.e DEFECTO DE UNIDAD del metro nuevo (medido en el codigo, no argumentado)

`control_energia_invariante._invariante` calcula

```
0.5 * M.EPS0 * sum(|E|^2)  +  0.5 * M.MU0 * suma_emparejada(Hm, F)
```

**sin** el factor de area de celda, mientras que `propagador_2d_te.energia` multiplica por
`DX * DY = 0.0025`. Los dos metros estan en **unidades distintas** y su cociente es constante:
`defecto_metro_max_rel = 9.975e-01 = 1 - DX*DY` exacto (`1 - 0.0025 = 0.9975`). **Prueba numerica
en `k = 0`**, donde `H = 0` ⇒ el termino cruzado se anula:
`DX*DY * U2_k0 = 0.0025 * 2.026423664493e-01 = 5.066059161232e-04 = U1_colocal(k=0)` hasta el
ultimo digito impreso. En `k = 80` la diferencia que queda (`U1 5.658457653137e-04` contra
`DX*DY*U2 4.725005128e-04`) **si** es el efecto real del termino cruzado `H^{n-1/2} . H^{n+1/2}`.
⇒ El defecto `9.975e-01` **no es fisica: es la unidad**. Regla: un metro escrito en unidades
distintas de su referencia produce un cociente constante que se disfraza de efecto sistematico.

### 7.f Lo que el §7.e NO salva

Re-hecha la comparacion en **unidades parejas** (multiplicando `U2` por `DX * DY`), **M2 sigue
fuera del `1e-9`**. El defecto de unidad **no** explica el ROJO: lo que hace es retirar una cifra
(`9.975e-01`) que parecia objeto y era metro. Las dos causas que quedan van **declaradas, sin
adjudicar**: (a) el IC **fuera de la cascara** — una columna estatica de `Ez` sin `H` que par — y
la propia tabla del crudo lo muestra (`max|Ez|` cae de `4.5015815807855e-02` a
`7.639886787620385e-03` en `k = 80`: radiacion inmediata); (b) `pec_muros` aplicado **despues** de
`paso`, que recorta `Ez` de pared fuera del orden del esquema. Ninguna de las dos se corrige aqui.

### 7.g El propio instrumento declaro su reserva disparada

`disparador_reserva_barrido_dt = "CORRER (V1 fallo)"` — escrito por el instrumento, no por mi
despues. La reserva del §4 queda **disparada por su regla sellada**.

### 7.h Estado del ROJO del §1 (no se sustituye)

El ROJO del §1 **queda en el registro tal cual** (`deriva_global 1.5686501125907726e-01`). Lo que
esta adenda agrega es su **lectura separada**: la parte del ROJO que era **metro** (unidad,
`9.975e-01`) queda nombrada; la parte que es **objeto** (radiacion del IC fuera de cascara y
recorte PEC) queda **abierta**. No se cambia el veredicto del motor: `1e-9` sigue sellado.

## 8. Cierre

Pieza de clase bootstrap: identidad por **igualdad de blob**. Se escribio **antes** del instrumento
(§0) y se adjudica **despues** de su crudo (§7), con los dos veredictos juntos.

HUELLA DE LA FILA ORDENADA DEL §7: `V1_FALLO_ADJUDICADO`. Medida **ausente** por medicion propia
(`grep -cF` = 0, `2026-10-13T03:11:38Z`) sobre el blob previo
`0a02ccf39d843c956ad32065c9071fb11c304d05` (109 l) ⇒ no hubo colision. El pre-vuelo A2.1 de este
append volvio a dar `RC=13` (`ESTADO SUCIO`, `2026-10-13T03:12:39Z`, blob previo
`c0d1088d02f313e63bc445464810fd9407df8579`, 195 l): es el **defecto de dominio ya declarado** del
gate sobre objetivos no rastreados (`??`), no una colision.

## 9. Adjudicacion de la reserva del §4 (barrido dt), posterior al cierre del §8

Corrida del instrumento `control_energia_invariante.py --barrido-dt`: **`RC_BARRIDO=0`**,
`T_UTC_CIERRE_BARRIDO = 2026-10-13T03:45:27Z`. Crudo `data/control_energia_barrido_dt.json`
(6718 B, `T_UTC = 2026-10-13T03:13:22Z`), log `data/logs/p2_barrido_dt.log` (2919 B).

### 9.a Adjudicacion por la regla sellada (no por argumento)

Regla del §4: `O(dt^2) DEL METRO` si `deriva_M2_cfl070 / deriva_M2_cfl035 > 3.0`; si no,
`DEL OBJETO`. Crudo:

| brazo | cfl | pasos | dt | `M2_invariante.deriva_global_ancla0` | `M1_colocal.deriva_global_ancla0` | `segundos` |
|---|---|---|---|---|---|---|
| A | 0.70 | 400 | 0.02474873734152916 | 3.204237419178968e-03 | 1.5686501125907726e-01 | 861.0 |
| B | 0.35 | 800 | 0.01237436867076458 | 2.240129388002310e-02 | 2.221259463092684e-02 | 1064.4 |

`razon = 0.14303805112062856`, que **no** supera `3.0` ⇒ `lectura = "DEL OBJETO"`. La reserva del
§4 queda **adjudicada por su propia regla**: no se baja el umbral, no se re-corre con otra regla.

### 9.b La direccion refuta la hipotesis `O(dt^2)` del metro

Refinar `dt` por 2 **no** redujo la deriva global de M2: la **subio** de
`3.204237419178968e-03` a `2.240129388002310e-02` (**factor 6.99**). Un defecto de metro
`O(dt^2)` tendria que haber **bajado** por ~4. Se declara la direccion; **no** se adjudica su causa.

### 9.c Lo que si quedo medido: lo que depende de `dt` es el desacuerdo ENTRE metros

| brazo | `M1 / M2` | discrepancia relativa |
|---|---|---|
| A (cfl 0.70) | 48.955 | 4.7955e+01 |
| B (cfl 0.35) | 0.99158 | 8.4948e-03 |

A `cfl = 0.35` los **dos metros coinciden al 0.85 %** (diferencia absoluta
`1.8869924909626e-04`); a `cfl = 0.70` difieren por un factor **49**. Es decir: lo que se mueve al
refinar `dt` es **el desacuerdo del metro colocal**, mientras que el residuo que queda en el `dt`
fino es **casi independiente del metro** ⇒ **coherente** con la lectura `DEL OBJETO` (el IC fuera de
cascara del §7.f), **sin** adjudicar su magnitud. El umbral `1e-9` **no se toca**: los **cuatro**
veredictos del barrido siguen `ROJO`.

### 9.d El defecto de unidad del §7.e, ahora con control de `dt`

`defecto_metro_max_rel = 0.9975` en **los dos** brazos: valor **identico** bajo un cambio de `dt`
por 2. Un efecto de discretizacion se habria movido con `dt`; un **factor de unidad adimensional**
(`1 - DX*DY`) **no**. Es un segundo test, **independiente** del algebra del §7.e, y apunta al mismo
defecto de unidad.

### 9.e Fidelidad del arranque entre corridas

`U2_invariante` en `k = 0` vale `0.20264236644929357` y `U1_colocal` en `k = 0` vale
`5.06605916123234e-04` en los **tres** crudos (adenda invariante y los dos brazos del barrido) ⇒ los
brazos arrancan del **mismo objeto**. `V4` se replica en los dos brazos
(`max_Ex = max_Ey = max_Hz = 0.0` exacto en las 6 muestras) y `guarda_disparada_en = null`
(chi3 = 0: la guarda del §5 no tiene que disparar).

### 9.f Contencion medida durante el barrido (declarado, no corregido)

Las dos corridas P2 pesadas seguian en vuelo mientras corria el barrido. Medido
`2026-10-13T04:01:56Z`: memoria total 8 GiB, **swap en uso 4910.19 MB de 6144 MB**, `%CPU` 62-65 %,
`RSS` ~690-720 MB por proceso, `etime` 01:49:42. Los tiempos de pared del barrido (`861.0` s y
`1064.4` s para el mismo numero de operaciones por paso) se declaran **bajo esa contencion**, no
como coste limpio del instrumento.

HUELLA DE LA FILA ORDENADA DEL §9: `RESERVA_BARRIDO_DT_ADJUDICADA`. Medida **ausente** por medicion
propia (`grep -cF` = 0, `2026-10-13T04:02:56Z`) sobre el blob previo
`294c2a0db947794e498aa6926a0660258b25db9c` (202 l) ⇒ no hubo colision. El pre-vuelo A2.1 de este
append dio `RC=13` (`ESTADO SUCIO`, `2026-10-13T04:02:18Z`): **defecto de dominio ya declarado** del
gate sobre objetivos no rastreados (`??`), no una colision.

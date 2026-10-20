# optica-kerr-2d — solitón espacial Kerr 2D TE: el objeto falla en ROJO, el instrumento se exonera

> **EN —** 2D TE Kerr (1+1)D propagation. The A1 criterion is **ROJO** for the object (13.11 % vs a
> sealed 0.03) — and the falsifier A2 **passes on both sides**, which exonerates the instrument: with
> χ³ = 0 the beam diffracts 19.06 %, so the solver cannot confine by itself. Three thresholds were
> sealed before the first number; **none of them moved**.

## Por qué este repositorio vale

Un resultado negativo sólo vale si puedes demostrar que **tu metro** no lo fabricó. Aquí el ciclo
publica el rojo del objeto **y** el acta que exculpa al instrumento, con el control lineal medido en
la misma corrida.

## Umbrales sellados (no se movieron)

| criterio | umbral | dónde se selló |
|---|---|---|
| `A1` | `0.03` | `PREREGISTRO_SOLITON_ESPACIAL_KERR_20261012.md` §8 |
| `A2` | `0.02` y `0.03` (dos lados) | `PREREGISTRO_ADENDA_P2_ANALISIS_20261013.md` |
| control de energía | `1e-9` | CLI del motor + addenda de invariante |

## Veredictos

### A1 — ROJO

El objeto falla el criterio: **13.11 %** contra un umbral sellado de **0.03**.

### A2 — FALSADOR DEL INSTRUMENTO: **PASA EN LOS DOS LADOS**

- Con `χ³ = 0` el motor reproduce la ley de segundo momento del pre-registro 4 al **0.457 %** — la
  misma cifra sellada de `P1b` (`data/nulo_lineal_sech_fdtd.json`, `residuo_max = 4.5680e-03`) ⇒
  **`P1b` se reproduce con este motor**.
- Con `χ³ = 0` el haz difracta **19.06 %** ⇒ **el motor NO confina por sí mismo**: no existe
  confinamiento espurio capaz de fabricar el resultado del objeto.
- Declaración de dominio del umbral: el control lineal **falla** A1 (19.06 % = **6.35×** el umbral).
  Eso **no** es defecto de dominio — un nulo que pasara el criterio no discriminaría nada. Lo que
  adjudica es que **el objeto también lo falla** (13.11 %).

**Consecuencia: el instrumento queda exonerado.**

### Control de energía — ROJO, citado tal cual

`data/propagador_control_energia.json`: `veredicto = "ROJO"`, `deriva_global = 0.15686501125907726`,
`deriva_peor_par = 0.11693477574005584`, `umbral = 1e-09`, `χ³ = 0` en caja PEC cerrada, 400 pasos
libres. El ROJO **no se sustituye** por el verde de un metro nuevo: los dos se imprimen, el umbral
`1e-9` se mantiene y su **defecto de dominio se declara**.

### Reserva del barrido `dt` — veredicto sellado con su límite declarado

`razon = 0.14303805112062856` (< 3) ⇒ `lectura = "DEL OBJETO"`. Se declara su límite: al afinar `dt`
la deriva **subió ×6.99** (`3.2042e-03 → 2.2401e-02`), dirección **contraria** a `O(dt²)`, y `M1/M2`
vale **48.955** en A frente a **0.99158** en B ⇒ el cociente tiene **bajo poder discriminativo**
porque el término constante domina. La lectura se mantiene **porque es lo que la regla sellada
devuelve**, no porque discrimine bien.

## Identidad del ciclo

```
commit      3da7b009510e7ee782f16edacfaf8a80c24a976d   (15 archivos)
motor       propagador_2d_te.py  blob c103ef6c218414a5e1980a30aa24489b938de557
nulo        nulo_lineal.py       blob 69f94564db2e61891dda59a9ef666f0c856d8587
manifiesto  MANIFIESTO.txt       blob d218de6b25c5c186e75ae056fdfe79503b60c8af
preregistro (P2)                 blob 45fa6e96b707bd5c780cb3b9e160ac94a3be2a91
git status --porcelain -uall  -> vacio (SUCIOS = 0)
T_UTC_CIERRE 2026-10-13T05:37:21Z
```

## Mapa

```
propagador_2d_te.py            motor de propagación TE (objeto · nulo · control de energía · barrido dt)
nulo_lineal.py                 el control lineal del instrumento
control_energia_invariante.py  invariantes V1–V4 del ciclo
data/                          crudos del ciclo (objeto, nulo, control, barrido, logs)
MANIFIESTO.txt                 manifiesto del ciclo
PREREGISTRO_*                  sellos (P2 + dos addendas de análisis e invariante)
ACTA_P2_*                      el acta de cierre
```

## Reproducir

```sh
python3 -B propagador_2d_te.py --correr            # objeto
python3 -B propagador_2d_te.py --nulo-lineal       # falsador (χ³ = 0)
python3 -B propagador_2d_te.py --control-energia   # control PEC
python3 -B control_energia_invariante.py --correr  # V1–V4
```

Corridas registradas: objeto `8016.37 s`, nulo `8013.47 s`, invariante `816.13 s` (rama `χ³ = 1`),
medidas en `numpy 2.4.6`.

## Límites declarados

- **A1 es ROJO** y el acta **no** lo convierte en verde.
- **El control de energía es ROJO** con umbral `1e-9`; se imprime con su deriva y su dominio.
- La causa candidata de §11 **no se adjudica**: no se recalibra la constante sellada ni se ejecutan
  `P3`, `P4`, `control_cfl` ni el observador de THG en este ciclo.
- El `.gitignore` (`__pycache__/`, `*.pyc`) es el único acto fuera de "acta y crudos", declarado en
  el acta: existe para que "árbol limpio" sea un **estado** y no una foto.

## Licencia y citación

MIT — ver [`LICENSE`](LICENSE).

**Parte del archivo de instrumentos de [alexisromtz-lab](https://github.com/alexisromtz-lab).**

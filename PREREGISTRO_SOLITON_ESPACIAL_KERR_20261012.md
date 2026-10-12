# PRE-REGISTRO METROLÓGICO: SOLITÓN ESPACIAL KERR 2D TE (1+1)D

T_UTC_VENTANA = 2026-10-12T07:08:36Z

UNIVERSO DECLARADO: esta pieza (el pre-registro) + el blob base congelado `sim/maxwell2d.py` (sha16 `1db75ea7b0b8cba4` · blob git `b3fc082245cfc5c33b3e275f966cfb16b04aa2e2` · HEAD `f213af6` · limpio) + el árbol nuevo `~/optica-kerr-2d`. MOTOR = `git hash-object` · `shasum -a 256` · `python3 -B` (hashlib). UNIDAD = línea / byte / cabeza / blob. VENTANA = reloj UTC de la línea T_UTC_VENTANA.

REGLA DURA: todo umbral de esta pieza queda SELLADO **antes** de la primera cifra. Mover un umbral después de ver la salida es familia (a): no se mueve, se declara.

## 0. La orden viaja con su destino (tupla A2.1)

- `TARGET` = `~/optica-kerr-2d/PREREGISTRO_SOLITON_ESPACIAL_KERR_20261012.md`
- `BLOB_PRE` = `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` (blob vacío de git = semilla)
- `LINEAS_PRE` = `0`
- `HUELLA` = `# PRE-REGISTRO METROLÓGICO: SOLITÓN ESPACIAL KERR 2D TE (1+1)D`

Pre-vuelo corrido **antes** de escribir; su RC se imprime en el cierre (§10), no aquí.

## 1. Objeto declarado

Solitón espacial Kerr en 2D TE con geometría **(1+1)D**: propagación longitudinal en $x$, confinamiento transversal en $y$, campo $E_z$, sin variación en $z$.

**No es (2+1)D.** En (1+1)D transversal **no hay colapso y no hay potencia crítica**: $P_{\mathrm{cr}} = \lambda^2/(2\pi n_0 n_2)$ es el umbral del colapso masivo de (2+1)D y **no aplica a este objeto**. Lo que existe es una **familia continua de un parámetro**, sin umbral.

Asentado por el dueño (12-Oct-2026): «solitón temporal» y «solitón espacial» nombran **dos objetos y dos motores distintos**; esta pieza gobierna **sólo** el espacial.

## 2. Base congelada — y la razón real del aislamiento

- Motor heredado: `sfqed-paper/sim/maxwell2d.py` — 715 l · 30 759 B · sha16 `1db75ea7b0b8cba4` · blob git `b3fc082245cfc5c33b3e275f966cfb16b04aa2e2` · HEAD `f213af6` · **limpio** (`dirty = 0`, medido 12-Oct-2026 07:07:48Z).
- Razón declarada del aislamiento: **congelar el blob limpio** — **no** «no reabrir estados». `sfqed-paper` tiene **89** entradas sucias (**122** con `-uall`) y `sim/maxwell2d_nl.py` es una de ellas (`dirty = 1`): el stub `constitutivo_no_implementado()` vive **dentro de un archivo ya modificado**.
- Regla: en `~/optica-kerr-2d` el motor se **copia**; `sfqed-paper` **no se edita** (ni `maxwell2d.py` ni `maxwell2d_nl.py`).
- Enganches portados (línea en la base): `mascara_esponja():150` · `paso(F,dt,mascara):163` · `energia(F):179` · `envolvente(t):187` · `perfiles():194` · `inyectar(...):215` · `correr(...):283` · `control_energia(...):514` · `control_cfl():642`.
- Constantes heredadas: `CFL_2D = 0.70` (la base declara que 0.90 viola von Neumann en 2D, límite $1/\sqrt2 = 0.7071068$) · `ESPONJA_CELDAS = 60`.

## 3. Familia de equilibrio — CONGELADA

Perfil transversal inyectado (real, par, frente de onda plano):

$$$E_z(y,0) = E_0\operatorname{sech}(y/w_0).$$$

Relación ordenada (casa del dueño, 12-Oct-2026):

$$$E_0^2w_0^2 = \frac{2}{(\omega/c)^2\chi^{(3)}}.$$$

**Verificación de consistencia (derivada aquí, no importada):** con $\varepsilon_{bg}=1$ y $k_0=\omega/c$, la NLSE paraxial $2ik_0E_x + E_{yy} + k_0^2\chi^{(3)}|E|^2E = 0$ admite $E_0\operatorname{sech}(y/w_0)e^{i\gamma x}$ con $\gamma = 1/(2k_0w_0^2)$ y **exactamente** $E_0^2w_0^2 = 2/(k_0^2\chi^{(3)})$, que es la relación ordenada. La constante `2` no es un ajuste: es el coeficiente de $s^3$ en $s'' = s - 2s^3$.

**Consecuencia derivada** (fija la cota del §5; es el resultado no obvio de este ciclo):

$$$\Delta\varepsilon_{\mathrm{NL}} \equiv \chi^{(3)}|E_0|^2 = \frac{2}{(k_0w_0)^2}.$$$

Es decir: **la perturbación dieléctrica del solitón no depende de $\chi^{(3)}$** — sólo de la cintura y de la longitud de onda. Subir $\chi^{(3)}$ no sube $\Delta\varepsilon_{\mathrm{NL}}$: baja $E_0$ en la misma proporción.

Unidades declaradas: $c=1$ · $\lambda=1$ · $\omega=2\pi$ · $k_0=2\pi$ (toda longitud en longitudes de onda).

Elección sellada: $w_0 = 5\lambda = 5$ ⇒ $z_R = \pi w_0^2/\lambda = 25\pi = 78.5398163$ ⇒ $\Delta\varepsilon_{\mathrm{NL}} = 2/(10\pi)^2 = 2.0264236\times10^{-3}$. Con $\chi^{(3)}=1$: $E_0 = \sqrt{2.0264236\times10^{-3}} = 4.501582\times10^{-2}$.

## 4. Control nulo lineal — el metro del propagador

Con $\chi^{(3)}=0$ el medio es lineal. **Declaración de diferencia:** la ley de Rayleigh $w(x) = w_0\sqrt{1+(x/z_R)^2}$ es exacta para el perfil **gaussiano**; el perfil ordenado es **sech**, y un sech no es gaussiano (su $M^2>1$). Para no introducir un $M^2$ ajustado a posteriori, el nulo se compara contra la **ley exacta de segundo momento** (frente plano y campo real par ⇒ el término lineal en $x$ se anula):

$$$\sigma_y^2(x) = \sigma_y^2(0) + \frac{x^2}{k_0^2}\cdot\frac{\int|\partial_yE_0|^2\,\mathrm{d}y}{\int|E_0|^2\,\mathrm{d}y},\qquad \sigma_y(x) = \left[\frac{\int (y-\bar y)^2|E_z|^2\,\mathrm{d}y}{\int |E_z|^2\,\mathrm{d}y}\right]^{1/2}.$$$

Para $E_0\operatorname{sech}(y/w_0)$: $\int|\partial_yE_0|^2/\int|E_0|^2 = 1/(3w_0^2)$ y $\sigma_y(0) = \pi w_0/(2\sqrt3) = 0.9068997\,w_0 = 4.5344985$ ⇒

$$$\sigma_y(x) = \sqrt{\frac{\pi^2w_0^2}{12} + \frac{x^2}{3k_0^2w_0^2}} = \sqrt{20.561676 + 3.3774\times10^{-4}x^2}.$$$

En $x = 2z_R = 157.0796327$: $\sigma_y = 5.375407$ (es $1.18545\,\sigma_y(0)$).

**VENTANA:** $x\in[0,\,2z_R] = [0,\,157.0796327]$.

**TOLERANCIA SELLADA:** $\max_{x}\left|\sigma_y^{\text{med}}(x)/\sigma_y^{\text{ley}}(x) - 1\right| \le 0.02$ (2 %).

**Presupuesto de error declarado a priori** (declarado, no medido): dispersión Yee de 2º orden con $dy = \lambda/20$ ⇒ $k_0dy = 0.3141593$, error por longitud de onda $\approx (k_0dy)^2/24 = 4.1\times10^{-3}$ (0.41 %), atenuado por la fracción del ancho que depende de $x$ ⇒ 0.23 %; absorción de cola en la esponja 0.1 %; corrección no paraxial $(1/(k_0w_0))^2 = 1.01\times10^{-3}$ (0.10 %) ⇒ total 0.5 %, umbral 2 % (margen ×4).

**Control positivo del metro:** el mismo nulo con perfil **gaussiano** $E_z = E_0\exp(-y^2/w_0^2)$ debe reproducir la ley de Rayleigh en su forma exacta $\sigma_y(x) = \sigma_y(0)\sqrt{1+(x/z_R^{\sigma})^2}$, con $\sigma_y(0) = w_0/2$ y $z_R^{\sigma} = 2k_0\sigma_y(0)^2$. Si el gaussiano no cierra, el metro está roto y **no se juzga el sech**.

Regla: **el nulo corre primero.**

## 5. Modo de fallo declarado (esquema explícito, sin sub-stepping)

Medido en el corpus: predictor-corrector · sub-stepping · RK4 · Crank-Nicolson = **0** ocurrencias; el bucle de `paso()` es **leapfrog explícito**.

Cota declarada (orden del dueño): $\Delta\varepsilon_{\mathrm{NL}} \le 0.1$ relativa a $\varepsilon_{bg}=1$.

Con la relación del §3 la cota **no es libre**: $2/(k_0w_0)^2 \le 0.1 \iff k_0w_0 \ge \sqrt{20} \iff w_0 \ge \sqrt{20}/(2\pi) = 0.7117639\,\lambda$.

Con la elección $w_0 = 5\lambda$: $\Delta\varepsilon_{\mathrm{NL}}/0.1 = 2.0264236\times10^{-2}$ ⇒ se está **×49.3 por debajo** de la cota.

Regla: si una corrida futura exige $w_0 < 0.7117639\,\lambda$, **no se fuerza convergencia espuria**: se declara **FALLO DEL ESQUEMA** y se cierra el paso.

## 6. Desviación física declarada (no es fallo): tercer armónico

El motor resuelve **Maxwell completo**, no la envolvente paraxial. Con $\chi^{(3)}$ real, $\chi^{(3)}(E\cdot E)E$ radia a $3\omega$ (THG), efecto **ausente** de la NLSE que da la relación del §3.

Cota declarada a priori por escalamiento (**no medida**): conversión $O\!\left((\Delta\varepsilon_{\mathrm{NL}})^2\right) \approx 4.1\times10^{-6}$ para la elección del §3.

Se declara como **observable co-medido** (energía en $3\omega$ por FFT de $E_z$ sobre el eje), **no** como fallo del propagador.

## 7. Parámetros del propagador (sellados)

| parámetro | valor | casa |
|---|---|---|
| $c$, $\lambda$, $\omega$, $k_0$ | $1$, $1$, $2\pi$, $2\pi$ | unidades declaradas §3 |
| $w_0$, $z_R$ | $5$, $25\pi = 78.5398163$ | elección §3 |
| $\chi^{(3)}$, $E_0$ | $1$, $4.501582\times10^{-2}$ | relación §3 |
| $dy = dx$ | $\lambda/20 = 0.05$ | **eligida** (la base declara $\lambda/40$ para su caso Schwinger; aquí se justifica en el presupuesto del §4) |
| $L_y$, $N_y$ | $20w_0 = 100$, $2000$ | elegida: la esponja (3 $\lambda$) recorta ~0.1 % de la energía del haz difractado a $2z_R$ |
| $L_x$, $N_x$ | $2z_R + 2\times3 = 163.0796327$, $3262$ | ventana §4 + esponja |
| esponja | 60 celdas por borde | **heredada** (`ESPONJA_CELDAS = 60`) |
| $dt$ | $CFL_2D\,dx/(c\sqrt2) = 2.4748737\times10^{-2}$ | **heredada** (`CFL_2D = 0.70`) |
| pasos | $\lceil L_x/dt \rceil = 6590$ | derivado |

## 8. Predicciones falsables y criterios de cierre

- **P1a (metro, control positivo):** el nulo gaussiano cierra contra la ley de Rayleigh en $\le 2\%$. Si falla, se repara el propagador.
- **P1b (metro, objeto):** el nulo sech cierra contra la ley de segundo momento del §4 en $\le 2\%$.
- **P2 (objeto):** con $\chi^{(3)}$ y $E_0$ del §3, $\max_{x\in[0,2z_R]}|\sigma_y(x)/\sigma_y(0) - 1| \le 0.03$ (3 %). Si ensancha más, **la relación congelada no sostiene el haz** y se declara; no se recalibra la constante.
- **P3 (dominio):** en el borde de la cota ($w_0 = 0.7117639\,\lambda \Rightarrow \Delta\varepsilon_{\mathrm{NL}} = 0.1$) el esquema **no** explota: `control_energia` y `control_cfl` OK. Es el **control positivo del modo de fallo**.
- **P4 (familia):** dos cinturas distintas ($3\lambda$ y $5\lambda$), cada una con su $E_0$ de la relación, deben **ambas** sostener su propio ancho ⇒ lo sostenido es la **familia**, no un punto afinado. ($\Delta\varepsilon_{\mathrm{NL}}$ a $3\lambda$: $5.6290\times10^{-3}$, aún ×17.8 bajo la cota.)

## 9. Namespace de I/O

Todo sumidero se restringe a `~/optica-kerr-2d/data/`. Los **8** sitios de I/O del motor base (`open` · `savetxt` · `to_csv` · `np.save` · `write_text` · `json.dump`) se reescriben a esa raíz. `sfqed-paper/sim/data/` **no se escribe**.

## 10. Sello del cierre (medido fuera, no impreso aquí)

Una identidad impresa **dentro** de la pieza describe su versión **anterior** ⇒ el sha16, las líneas y las cabezas de esta pieza se miden **en la terminal** y se imprimen en el cierre del ciclo, no aquí.

## 11. ERRATA (declarada, no parcheada)

T_UTC_ERRATA = 2026-10-12T07:15:27Z

Corrección **registrada como apéndice**, no parcheada en el cuerpo: la pieza vieja no se edita, recibe apéndices.

**11.a — Cuatro literales con precisión truncada** (cifra impresa sin el dígito que el comando da). Medidos con `python3 -B` / numpy sobre el mismo objeto ($k_0 = 2\pi$, $w_0 = 5$, $\lambda = 1$):

| casa | literal impreso | valor medido | comando |
|---|---|---|---|
| §3, §5 y P3 | $0.7117639$ | **$0.7117625$** | `sqrt(20)/(2*pi)` |
| §3 | $2.0264236\times10^{-3}$ | **$2.0264237\times10^{-3}$** | `2/(10*pi)**2` |
| §4 | $4.5344985$ | **$4.5344984$** | `pi*w0/(2*sqrt(3))` |
| §4 | $5.375407$ (y su razón $1.18545$) | **$5.375408$** | `sqrt(pi**2*w0**2/12 + (2*zR)**2/(3*k0**2*w0**2))` |

**Ningún veredicto cambia:** el margen del §5 queda en $2.0264237\times10^{-2}$ (×49.348) y $w_0^{\min} = 0.7117625\,\lambda$ es **más** holgado bajo $w_0 = 5\lambda$, no menos.

**11.b — La ley del §4 quedó VERIFICADA, y se declara hasta dónde.** Propagador paraxial por FFT independiente (numpy, $N = 2^{20}$, $dy = 0.01$, 5 puntos por perfil):

- sech contra su ley de segundo momento: desviación máxima **$2.220\times10^{-16}$**;
- gaussiano contra Rayleigh: desviación máxima **$2.220\times10^{-16}$**.

⇒ **P1a y P1b caen DENTRO del umbral sellado (2 %) con 14 órdenes de margen — pero esto mide la capa ANALÍTICA, no el metro.** El FDTD todavía no existe: el control dice que la **ley está bien escrita**, no que `paso()` la reproduzca. La verificación del metro sigue siendo P1a/P1b sobre FDTD.

**11.c — El coeficiente del gradiente, con su control.** $\int|\partial_yE_0|^2/\int|E_0|^2 = 1/(3w_0^2)$: medido numéricamente $3.377366\times10^{-4}$ contra analítico $3.377373\times10^{-4}$ (difieren en el 6º dígito por el gradiente discreto a $dy = 0.01$; el literal del §4, $3.3774\times10^{-4}$, es el analítico).

**11.d — Una cifra, dos unidades declaradas.** El recuento del signo monetario en esta pieza: **240 ocurrencias** (carácter, `str.count`) vs **39 líneas** (`grep -c` cuenta líneas, no ocurrencias). Ninguna es falsa; viajan con su unidad.

**11.e — La cifra de esta pieza expira al escribir este apéndice.** 126 líneas · 10 241 B · sha16 $d9772bc6697b8939$ era verdad **antes** de escribir §11; el cierre imprime el par nuevo.

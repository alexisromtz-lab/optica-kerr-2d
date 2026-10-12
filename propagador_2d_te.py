#!/usr/bin/env python3
# SOLVER 2D TE CON TERMINO CONSTITUTIVO KERR LOCAL
"""(1+1)D TE: soliton espacial Kerr. Propaga en x, confina en y, campo E_z.

OBJETO
  E_z(y, 0) = E0 sech(y / w0),  w0 = 5 lambda,  E0 = 4.5015816e-2,
  chi3 = 1,  Delta eps_NL = chi3 E0^2 = 2.0264237e-3 <= 0.1 (guarda del §5).
  Un parametro continuo (w0); NO hay colapso ni P_cr: la familia existe para
  todo w0 y la cota Delta eps_NL <= 0.1 acota w0 >= 0.7117625 lambda.

UNIDADES NATURALES (declaradas): c = lambda = 1, omega = k0 = 2 pi,
eps0 = mu0 = 1, chi3 = 1. NO se importa sim/params.py: sus constantes SI no
entran en ninguna ecuacion de este objeto (el UNIVERSO lo declara). Las dos
constantes SI que se transcriben (C_SI, EPS0_SI) son documentales y NO se usan.

ESQUEMA
  Yee 2D3V salto de rana. Con chi3 = 0 el denominador vale EXACTAMENTE 1.0 y
  dividir por 1.0 es exacto en IEEE, o sea que la via lineal no recibe ni un
  bit de ruido del termino no lineal. Eso NO dice que el paso sea identico al
  de la base: se comparten los hooks de derivada, no la aritmetica.
  Con chi3 != 0 el termino constitutivo D = eps0 (1 + chi3 |E|^2) E se trata
  EXPLICITAMENTE a primer orden:  E <- E + dt (nabla x H) / (1 + chi3 |E|^2).
  El §5 declara el modo de fallo con guarda (RuntimeError) en vez de forzar
  convergencia espuria.

E/S
  §9 del pre-registro: TODO lo que este archivo escribe cae en ./data/.
  NO escribe nada dentro de sfqed-paper/ (esa casa es de solo lectura aqui).
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
DATA = AQUI / "data"                 # §9: UNICO sumidero de esta pieza
DATA.mkdir(parents=True, exist_ok=True)

# --- casa de las constantes SI: sfqed-paper/sim/params.py (133 l, 5 343 B,
#     sha256-16 9983b3d25a68f032). Se TRANSCRIBEN dos, solo como referencia
#     documental: el objeto vive en unidades naturales y NO las usa.
C_SI = 299792458.0                   # m/s (exacta)
EPS0_SI = 8.8541878128e-12           # F/m (CODATA 2018)

# --- constantes del objeto (§3 del pre-registro), unidades naturales --------
LAMBDA = 1.0
C = 1.0
EPS0 = 1.0
MU0 = 1.0                            # eps0 mu0 c^2 = 1
K0 = 2.0 * math.pi
OMEGA = K0
PERIODO = 2.0 * math.pi / OMEGA      # = 1
W0 = 5.0 * LAMBDA
Z_R = math.pi * W0 ** 2 / LAMBDA     # 25 pi = 78.53981633974483
CHI3_SELLADO = 1.0
CHI3 = CHI3_SELLADO                  # VIVO: lo mueve correr() para el nulo
E0 = math.sqrt(2.0 / (K0 * W0) ** 2)  # 0.045015815807855304
DEPS_NL = CHI3_SELLADO * E0 ** 2      # 2.0264236728467556e-3

# --- modo de fallo (§5): cota dura, NO se fuerza convergencia --------------
DEPS_NL_MAX = 0.1
W0_MIN = math.sqrt(20.0) / K0         # 0.7117625434171772 lambda
GUARDA_CADA = 20                      # [ELEGIDO] muestreo de la guarda

# --- numerica SELLADA (§7); nada de aqui se mueve tras ver salida ----------
DX_OVER_LAMBDA = 0.05                 # [ELEGIDO] dy = dx = lambda/20
CFL_2D = 0.70                         # heredada; < 1/sqrt(2) = 0.7071068
ESPONJA_CELDAS = 60                   # heredada
ALFA_ESPONJA = 0.10                   # heredada
NX = 3262                             # ceil(L_x / dx), L_x = 2 z_R + 2*3
NY = 2000                             # L_y = 20 w0 = 100
DX = LAMBDA * DX_OVER_LAMBDA
DY = DX
DT = CFL_2D * DX / (C * math.sqrt(2.0))   # 0.02474873734152916
LX = NX * DX
LY = NY * DY
JC = NY // 2
I_SRC = ESPONJA_CELDAS                # columna fuente: x = 0
MARGEN_FUENTE_CELDAS = 20             # [ELEGIDO] halo de 1 lambda
VENTANA_I0 = I_SRC + MARGEN_FUENTE_CELDAS   # 80
VENTANA_I1 = NX - 1 - ESPONJA_CELDAS        # 3201
T_RAMPA = 3.0 * PERIODO               # [ELEGIDO] rampa CW de coseno alzado
PASOS_TRANSITO = int(math.ceil((2.0 * Z_R + 2.0 * 3.0) / DT))   # 6590
PASOS_ASENTAR = int(round(10.0 * PERIODO / DT))                 # 404
PASOS = PASOS_TRANSITO + PASOS_ASENTAR                          # 6994
DIAG_CADA = 20
N_AVG = int(round(3.0 * PERIODO / DT))                          # 121
CFL_PRE = 0.9                         # heredada del protocolo (control)
SIG0_SECH = math.pi * W0 / (2.0 * math.sqrt(3.0))   # 4.534498410585544

COMPONENTES = ("Ex", "Ey", "Ez", "Hx", "Hy", "Hz")

UNIVERSO = (
    "optica-kerr-2d | (1+1)D TE: propaga en x, confina en y, campo Ez | "
    "unidades naturales c=lambda=1, omega=k0=2 pi, eps0=mu0=1 | "
    "w0=5, E0=4.5015816e-2, chi3=1, Delta eps_NL=2.0264237e-3 <= 0.1 | "
    "malla sellada dx=dy=0.05 (NX=3262, NY=2000), esponja 60 celdas alfa=0.10, "
    "dt = CFL_2D dx/(c sqrt2) = 2.4748737342e-2 con CFL=0.70 < 1/sqrt2=0.7071068 | "
    "fuente CW en la columna 60 con rampa de 3 periodos | pasos = 6590 transito "
    "+ 404 asentamiento = 6994 | MOTOR = python3 -B + numpy | UNIDAD = celda/linea"
)

_PASO_N = [0]


def paso(F, dt, mascara):
    """Un paso de Yee 2D3V; el termino Kerr entra como eps_efectivo LOCAL.

    eps_efectivo = eps0 (1 + chi3 |E|^2),  |E|^2 = Ex^2 + Ey^2 + Ez^2.
      Hz = Hz - dt (ddx_f(Ey) - ddy_f(Ex)) / mu0
      Hx = Hx - dt ddy_f(Ez) / mu0
      Hy = Hy + dt ddx_f(Ez) / mu0
      Ez = Ez + dt (ddx(Hy) - ddy(Hx)) / (eps0 (1 + chi3 |E|^2))
      Ex = Ex + dt ddy(Hz) / (eps0 (1 + chi3 |E|^2))
      Ey = Ey - dt ddx(Hz) / (eps0 (1 + chi3 |E|^2))

    Con chi3 = 0 el denominador vale EXACTAMENTE 1.0 y no perturba la via
    lineal ni un bit. Con chi3 != 0 el tratamiento es explicito a primer orden:
    DECLARADO, no corregido.
    Las asignaciones son F[c] = F[c] + ... (objeto NUEVO, NUNCA +=): el
    diagnostico de correr() guarda referencias a campos de pasos anteriores y
    un += los mutaria en silencio.
    La guarda del §5 no negocia: si chi3 max|E|^2 supera DEPS_NL_MAX se levanta
    RuntimeError en vez de dejar correr un regimen que el pre-registro no cubre.
    """
    _PASO_N[0] += 1
    e2 = F["Ex"] ** 2 + F["Ey"] ** 2 + F["Ez"] ** 2
    if _PASO_N[0] % GUARDA_CADA == 0:
        deps = CHI3 * float(e2.max())
        if deps > DEPS_NL_MAX:
            raise RuntimeError(
                "FALLO DEL ESQUEMA (§5): chi3 max|E|^2 = %.6g > %.6g en el paso %d"
                % (deps, DEPS_NL_MAX, _PASO_N[0]))
    inv = 1.0 / (1.0 + CHI3 * e2)

    F["Hz"] = F["Hz"] - dt * (ddx_f(F["Ey"]) - ddy_f(F["Ex"])) / MU0
    F["Hx"] = F["Hx"] - dt * ddy_f(F["Ez"]) / MU0
    F["Hy"] = F["Hy"] + dt * ddx_f(F["Ez"]) / MU0

    F["Ez"] = F["Ez"] + dt * (ddx(F["Hy"]) - ddy(F["Hx"])) * inv / EPS0
    F["Ex"] = F["Ex"] + dt * ddy(F["Hz"]) * inv / EPS0
    F["Ey"] = F["Ey"] - dt * ddx(F["Hz"]) * inv / EPS0

    if mascara is not None:
        for c in COMPONENTES:
            F[c] = F[c] * mascara
    return F

def ddx(F):
    g = np.zeros_like(F)
    g[1:, :] = (F[1:, :] - F[:-1, :]) / DX
    return g


def ddy(F):
    g = np.zeros_like(F)
    g[:, 1:] = (F[:, 1:] - F[:, :-1]) / DX
    return g


def ddx_f(F):
    g = np.zeros_like(F)
    g[:-1, :] = (F[1:, :] - F[:-1, :]) / DX
    return g


def ddy_f(F):
    g = np.zeros_like(F)
    g[:, :-1] = (F[:, 1:] - F[:, :-1]) / DX
    return g


def campos_vacios():
    z = lambda: np.zeros((NX, NY), dtype=np.float64)
    return {"Ex": z(), "Ey": z(), "Ez": z(), "Hx": z(), "Hy": z(), "Hz": z()}


def mascara_esponja():
    m = np.ones((NX, NY))
    for eje, n in ((0, NX), (1, NY)):
        idx = np.arange(n)
        borde = np.maximum(
            np.clip(ESPONJA_CELDAS - idx, 0, ESPONJA_CELDAS),
            np.clip(idx - (n - 1 - ESPONJA_CELDAS), 0, ESPONJA_CELDAS),
        ) / ESPONJA_CELDAS
        s = 1.0 - ALFA_ESPONJA * borde ** 2
        m *= s.reshape((-1, 1) if eje == 0 else (1, -1))
    return m


# =========================================================== energia / fuente
def energia(F):
    """U = suma[ (1/2)(eps0 |E|^2 + |B|^2/mu0) + (1/4) eps0 chi3 |E|^4 ] dx dy.

    Con D = eps0 (1 + chi3 |E|^2) E se tiene (1/2) E.D = (1/2) eps0 |E|^2 +
    (1/2) eps0 chi3 |E|^4 y la energia del medio se escribe con el factor 1/4.
    El termino de Kerr se DECLARA; no se ajusta para forzar conservacion (con
    chi3 != 0 este esquema explicito no es exactamente conservativo).
    """
    e2 = F["Ex"] ** 2 + F["Ey"] ** 2 + F["Ez"] ** 2
    b2 = MU0 ** 2 * (F["Hx"] ** 2 + F["Hy"] ** 2 + F["Hz"] ** 2)
    u = 0.5 * (EPS0 * e2 + b2 / MU0) + 0.25 * EPS0 * CHI3 * e2 * e2
    return float(np.sum(u) * DX * DY)


def envolvente(t):
    """[ELEGIDO, declarado §5.2] rampa de coseno alzado y despues CW."""
    if t <= 0.0:
        return 0.0
    if t < T_RAMPA:
        return 0.5 * (1.0 - math.cos(math.pi * t / T_RAMPA))
    return 1.0


def perfiles():
    """Frente PLANO: una sola curvatura, la identidad.

    La base (sfqed-paper) necesitaba DOS fases por sentido para CONVERGER al
    foco. Aqui el objeto no converge a nada: el frente es plano y la difraccion
    hace el trabajo. Se declara que esta pieza NO porta esa maquinaria.
    """
    y = (np.arange(NY) - JC) * DX
    g = E0 / np.cosh(y / W0)
    return g, {I_SRC: np.zeros(NY)}


def terminos_de(perfil="objeto"):
    """Fuente de UNA columna, polarizacion Ez, fase cero."""
    if perfil not in ("objeto", "gauss"):
        raise SystemExit("perfil desconocido: %r (use objeto o gauss)" % (perfil,))
    return [(I_SRC, (1.0, 1.0), 0.0)], perfil


def inyectar(F, t, terminos, g, fases, duro=True):
    """CW con rampa: E_z(col) = envolvente(t) g(y) cos(omega t)."""
    amp = envolvente(t)
    if amp <= 0.0:
        return
    for col, (ty, tz), desfase in terminos:
        F["Ez"][col, :] = amp * g * math.cos(OMEGA * t + desfase)


def modulo_E(F):
    """|E| celda a celda (no usa H): diagnostico de pico, no de energia."""
    return np.sqrt(F["Ex"] ** 2 + F["Ey"] ** 2 + F["Ez"] ** 2)


# ============================================================ metros del objeto
def segundo_momento(y, I):
    """sigma_y = sqrt(<y^2> - <y>^2). El origen y queda cancelado."""
    S0 = float(I.sum())
    if S0 <= 0.0:
        raise RuntimeError("intensidad nula: no hay nada que medir")
    S1 = float((y * I).sum())
    S2 = float((y * y * I).sum())
    return math.sqrt(max(S2 / S0 - (S1 / S0) ** 2, 0.0))


def ley_segundo_momento(x):
    """§4: sigma_y(x)^2 = (pi w0 / (2 sqrt 3))^2 + x^2 / (3 k0^2 w0^2)."""
    return np.sqrt(SIG0_SECH ** 2 + np.asarray(x, dtype=float) ** 2
                   / (3.0 * K0 ** 2 * W0 ** 2))


def medida_ancho(I):
    """sigma_y(x) sobre la ventana sellada, mas S0 = int I dy como invariante.

    La cuadratura I = E_z^2 + (dE_z/dt / omega)^2 con el operador centrado
    corregido por sin(omega dt)/(omega dt) es EXACTA para una CW pura: sin esa
    correccion la derivada lleva 8.9 grados de retraso (omega dt = 0.1555) y
    sigma_y se contaminaria en el rango 0.3 a 0.8 por ciento.
    """
    y = (np.arange(NY) - JC) * DX
    cols = np.arange(VENTANA_I0, VENTANA_I1 + 1)
    II = I[cols, :]
    S0 = II.sum(axis=1)
    S1 = (II * y[None, :]).sum(axis=1)
    S2 = (II * (y ** 2)[None, :]).sum(axis=1)
    sig = np.sqrt(np.maximum(S2 / S0 - (S1 / S0) ** 2, 0.0))
    x = (cols - I_SRC) * DX
    return x, sig, S0


def correr(chi3=None, pasos=None, verbose=True):
    """Corre el objeto y devuelve el perfil de ancho y los invariantes.

    chi3 = None usa el valor SELLADO 1.0; se puede pasar 0.0 para correr el
    MISMO propagador en medio lineal y contrastarlo con nulo_lineal.py (que es
    el nulo INDEPENDIENTE, con kernel propio).
    """
    global CHI3
    previo = CHI3
    CHI3 = CHI3_SELLADO if chi3 is None else float(chi3)
    try:
        pasos = PASOS if pasos is None else int(pasos)
        F = campos_vacios()
        masc = mascara_esponja()
        terminos, perfil = terminos_de("objeto")
        g, fases = perfiles()
        q = 2.0 * math.sin(OMEGA * DT) / OMEGA
        Iacc = None
        n_acc = 0
        a1 = None
        a2 = None
        k_desde = pasos - N_AVG
        hist = []
        t0 = time.time()
        for k in range(pasos):
            t = (k + 0.5) * DT
            inyectar(F, t, terminos, g, fases, duro=True)
            paso(F, DT, masc)
            Ezn = F["Ez"]
            if a2 is not None and k >= k_desde:
                if Iacc is None:
                    Iacc = np.zeros_like(Ezn)
                der = (Ezn - a2) / q
                Iacc += a1 * a1 + der * der
                n_acc += 1
            a2 = a1
            a1 = Ezn
            if k % DIAG_CADA == 0:
                hist.append([t, energia(F)])
            if verbose and (k + 1) % 1000 == 0:
                print("    paso %5d/%d  t=%.3f  %.1f s" % (k + 1, pasos, t, time.time() - t0))
        I = Iacc / max(n_acc, 1)
        x, sig, S0 = medida_ancho(I)
        m = x >= 1.0 * LAMBDA
        sig0 = float(sig[0])
        res_plano = float(np.abs(sig[m] / sig0 - 1.0).max())
        ley = ley_segundo_momento(x)
        res_ley = float(np.abs(sig[m] / ley[m] - 1.0).max())
        fuga = float(np.abs(S0 / S0[0] - 1.0).max())
        pico_fin = float(np.abs(F["Ez"][VENTANA_I0:]).max())
        r = {"chi3": CHI3, "pasos": pasos, "dt": DT, "dx": DX, "NX": NX, "NY": NY,
             "I_SRC": I_SRC, "n_acc": n_acc, "pico_Ez_final": pico_fin,
             "sigma_y0_medido": sig0, "sigma_y0_ley": SIG0_SECH,
             "residuo_ley_segundo_momento": res_ley,
             "residuo_plano_max": res_plano,
             "S0_fuga_max_rel": fuga,
             "x": x.tolist(), "sigma_y": sig.tolist(), "ley": ley.tolist(),
             "hist_energia": hist[:20],
             "ventana_juzgada": [1.0 * LAMBDA, float(x[-1])],
             "segundos": time.time() - t0}
        if verbose:
            print("  sigma_y(0) medido = %.10f   ley(0) = %.10f" % (sig0, SIG0_SECH))
            print("  residuo max |sigma/ley - 1| = %.4e   (ley del §4)"
                  % res_ley)
            print("  residuo max |sigma/sigma0 - 1| = %.4e   (criterio P2, 0.03)"
                  % res_plano)
            print("  fuga de S0 = int I dy: %.4e   pico |Ez| final = %.6g"
                  % (fuga, pico_fin))
        return r
    finally:
        CHI3 = previo


# ================================================================ controles
def pec_muros(F):
    """PEC en las cuatro paredes (modo TE): la E_z tangencial se anula."""
    F["Ez"][0, :] = 0.0
    F["Ez"][NX - 1, :] = 0.0
    F["Ez"][:, 0] = 0.0
    F["Ez"][:, NY - 1] = 0.0


def control_energia(pasos_libres=400, verbose=True):
    """Caja CERRADA (PEC, sin esponja) y sin fuente: la energia no debe derivar.

    Se corre con chi3 = 0 porque es ahi donde el umbral sellado 1e-9 aplica:
    con chi3 = 1 el esquema explicito NO es exactamente conservativo y este
    control lo declara (no lo esconde moviendo el umbral).
    U0 se ancla en el PRIMER paso de evolucion LIBRE, con la fuente apagada.
    Se miden CINCO emparejamientos temporales y se reporta el peor.
    """
    global CHI3
    previo = CHI3
    CHI3 = 0.0
    try:
        F = campos_vacios()
        g, _ = perfiles()
        F["Ez"][I_SRC, :] = g
        h = max(1, pasos_libres // 5)
        U = []
        for k in range(pasos_libres + 1):
            if k > 0:
                paso(F, DT, None)
                pec_muros(F)
            if k % h == 0:
                U.append(energia(F))
        U0 = U[0]
        deriva_par = [abs(b / a - 1.0) for a, b in zip(U[:-1], U[1:])]
        deriva_glob = abs(U[-1] / U0 - 1.0)
        peor = max(deriva_par)
        out = {"chi3": 0.0, "pasos_libres": pasos_libres, "pares": 5,
               "U0": U0, "U_fin": U[-1], "deriva_global": deriva_glob,
               "deriva_peor_par": peor, "deriva_por_par": deriva_par,
               "umbral": 1e-9,
               "veredicto": "OK" if peor <= 1e-9 and deriva_glob <= 1e-9 else "ROJO"}
        if verbose:
            print("  control de energia: deriva global %.4e  peor par %.4e  (umbral 1e-9)"
                  % (deriva_glob, peor))
            print("  veredicto: %s" % out["veredicto"])
        return out
    finally:
        CHI3 = previo


def control_cfl(pasos=400, verbose=True):
    """El CFL pre-registrado (0.90, inestable en 2D) contra el limite de von
    Neumann: dt <= dx/(c sqrt 2), o sea CFL <= 0.7071068."""
    if verbose:
        print("  von Neumann en 2D: CFL <= %.7f" % (1.0 / math.sqrt(2.0)))
    out = {}
    for cfl in (CFL_PRE, CFL_2D):
        dt = cfl * DX / C
        F = campos_vacios()
        g, fases = perfiles()
        terminos, _ = terminos_de("objeto")
        picos = []
        estallo = None
        for k in range(pasos):
            t = (k + 0.5) * dt
            inyectar(F, t, terminos, g, fases, duro=True)
            try:
                paso(F, dt, mascara_esponja())
            except RuntimeError:
                estallo = k
                break
            picos.append(float(np.abs(F["Ez"]).max()))
        crec = picos[-1] / max(picos[0], 1e-300)
        out["%.2f" % cfl] = {"dt": dt, "E_pico_final": picos[-1],
                             "crecimiento": crec, "pasos_corridos": len(picos),
                             "guarda_disparada_en": estallo}
        if verbose:
            print("  cfl = %.2f: |Ez| al paso %d = %.6g (crecimiento %.3e)%s"
                  % (cfl, len(picos), picos[-1], crec,
                     "" if estallo is None else "  GUARDA DISPARADA en %d" % estallo))
    return out


def main() -> int:
    args = sys.argv[1:]
    t_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print("T_UTC_INICIO = %s" % t_utc)
    print("UNIVERSO DECLARADO: %s" % UNIVERSO)
    print("MOTOR = python3 -B + numpy %s ; UNIDAD = celda / linea / byte" % np.__version__)

    def guardar(nombre, carga):
        destino = DATA / ("propagador_%s.json" % nombre)
        destino.write_text(json.dumps(carga, indent=1, ensure_ascii=False),
                           encoding="utf-8")
        print("escrito: %s" % destino)

    if "--control-cfl" in args:
        r = control_cfl()
        guardar("control_cfl", {"T_UTC": t_utc, "UNIVERSO": UNIVERSO, "medido": r})
        return 0
    if "--control-energia" in args:
        r = control_energia()
        guardar("control_energia", {"T_UTC": t_utc, "UNIVERSO": UNIVERSO, "medido": r})
        return 0
    if "--nulo-lineal" in args:
        r = correr(chi3=0.0)
        guardar("nulo_lineal", {"T_UTC": t_utc, "UNIVERSO": UNIVERSO, "medido": r})
        return 0
    if "--correr" in args:
        r = correr()
        guardar("objeto", {"T_UTC": t_utc, "UNIVERSO": UNIVERSO, "medido": r})
        return 0
    print("uso: propagador_2d_te.py [--correr | --nulo-lineal | --control-energia"
          " | --control-cfl] [--pasos N]")
    print("  por defecto NO corre nada: los 6994 pasos se piden explicitamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

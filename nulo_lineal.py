#!/usr/bin/env python3
# EXPERIMENTO P1A: NULO DIFRACTIVO LINEAL CHI3=0 (SEGUNDO MOMENTO)
"""nulo_lineal.py -- P1a/P1b: el nulo DIFRACTIVO LINEAL (chi3 = 0) medido por el
SEGUNDO MOMENTO transversal, contra la ley cerrada del pre-registro §4 y §8.

UNIVERSO DECLARADO (se imprime en cada corrida, ANTES de toda cifra):
  unidades naturales: c = lambda = 1, omega = k0 = 2 pi, eps0 = mu0 = 1;
  perfil inyectado  E_z(y, 0) = E0 sech(y / w0)          (objeto, P1b)
                    E_z(y, 0) = E0 exp(-(y / w0)^2)      (control positivo, P1a)
  con w0 = 5 lambda y E0 = 0.045015815807855304 (constantes del §3);
  chi3 = 0: medio LINEAL, sin termino constitutivo;
  malla SELLADA §7: dx = dy = lambda/20 = 0.05, N_y = 2000 (L_y = 20 w0 = 100),
  N_x = 3262 (L_x = 2 z_R + 2*3 = 163.07963267948966), esponja 60 celdas por
  borde con alfa = 0.10, dt = CFL dx / (c sqrt 2) = 0.02474873734152916 con
  CFL = 0.70 < 1/sqrt(2) = 0.7071068;
  fuente CW con rampa de coseno alzado de 3 periodos en la columna 60;
  MOTOR = python3 -B + numpy; UNIDAD = celda / linea / byte.

DOS INSTRUMENTOS, declarados, y no son el mismo metro:
  A  ESPECTRO ANGULAR PARAXIAL por FFT (n = 2**20, dy = 0.01):
     psi(x) = IFFT[ exp(-i ky^2 x / (2 k0)) FFT[psi0] ].
     Es EXACTO para el modelo paraxial: dice que la LEY esta bien escrita, NO
     que un esquema de diferencias finitas la reproduzca. Es la capa analitica.
  B  YEE 2D TE (E_z, H_x, H_y) con chi3 = 0 sobre la malla SELLADA: ESTE ES EL
     METRO. La envolvente se extrae por CUADRATURA CENTRADA EXACTA EN MALLA,
       I = E_z(t)^2 + (dE_z/dt / omega)^2 = A^2
     valida para una CW pura; el operador de diferencia se corrige por
     sin(omega dt)/(omega dt) para que la cuadratura sea EXACTA, no aproximada.
  El kernel TE del instrumento B se escribe AQUI y NO se importa del propagador:
  un nulo que comparte codigo con el objeto que juzga no es un nulo.

USO:
    python3 -B nulo_lineal.py                          # controles + instrumento A
    python3 -B nulo_lineal.py --fdtd --perfil sech     # + instrumento B (~9 min)
    python3 -B nulo_lineal.py --fdtd --perfil gauss
    python3 -B nulo_lineal.py --json
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

# --- constantes del objeto (§3 y §7 del pre-registro) -----------------------
LAMBDA = 1.0
C = 1.0
EPS0 = 1.0
MU0 = 1.0
K0 = 2.0 * math.pi
OMEGA = K0
PERIODO = 2.0 * math.pi / OMEGA
W0 = 5.0 * LAMBDA
Z_R = math.pi * W0 ** 2 / LAMBDA
E0 = math.sqrt(2.0 / (K0 * W0) ** 2)
X_FIN = 2.0 * Z_R

DX = 0.05
CFL_2D = 0.70
DT = CFL_2D * DX / (C * math.sqrt(2.0))
ESPONJA = 60
ALFA = 0.10
NX = 3262
NY = 2000
JC = NY // 2
I_SRC = ESPONJA                      # columna fuente: x = 0
I_MIN = I_SRC + 20                   # 1 lambda de halo (frente plano)
I_MAX = NX - 1 - ESPONJA             # 3201, ultima columna limpia
X_JUEZ = 1.0 * LAMBDA                # ventana JUZGADA: x >= 1 lambda (declarada)
T_RAMPA = 3.0 * PERIODO
PASOS_TRANSITO = int(math.ceil((2.0 * Z_R + 2.0 * 3.0) / DT))     # 6590 (§7)
PASOS_ASENTAR = int(round(10.0 * PERIODO / DT))                   # 404
PASOS = PASOS_TRANSITO + PASOS_ASENTAR                            # 6994
N_AVG = int(round(3.0 * PERIODO / DT))                            # 121
UMBRAL = 0.02                        # §4 y §8: 2 %, NO se mueve tras ver salida

# --- ley cerrada del §4, sin parametros libres ------------------------------
SIG0_SECH = math.pi * W0 / (2.0 * math.sqrt(3.0))      # 4.534498410585544
COEF_SECH = 1.0 / (3.0 * K0 ** 2 * W0 ** 2)            # 3.3773727881e-4
SIG0_GAUSS = W0 / 2.0                                  # 2.5
ZR_GAUSS = 2.0 * K0 * SIG0_GAUSS ** 2                  # k0 w0^2 / 2 = 25 pi


def ley_segundo_momento(x):
    """sigma_y(x)^2 = sigma_y(0)^2 + x^2 / (3 k0^2 w0^2). Identidad, no ajuste."""
    return np.sqrt(SIG0_SECH ** 2 + COEF_SECH * np.asarray(x, dtype=float) ** 2)


def ley_rayleigh_sigma(x):
    """sigma_y(x) = sigma_y(0) sqrt(1 + (x / z_R^sigma)^2), z_R^sigma = k0 w0^2/2."""
    return SIG0_GAUSS * np.sqrt(1.0 + (np.asarray(x, dtype=float) / ZR_GAUSS) ** 2)


def segundo_momento(y, I):
    """sigma_y = sqrt(<y^2> - <y>^2). El punto de referencia se cancela."""
    S0 = float(I.sum())
    if S0 <= 0.0:
        raise RuntimeError("intensidad nula: no hay nada que medir")
    S1 = float((y * I).sum())
    S2 = float((y * y * I).sum())
    return math.sqrt(max(S2 / S0 - (S1 / S0) ** 2, 0.0))


def perfil(y, clase):
    """Perfil transversal sellado. En el instrumento A la malla sintetica es
    enorme (2**20 muestras a dy=0.01) y cosh(y/w0) DESBORDA; el desborde no
    cambia el resultado (inf -> E0/inf = 0.0, que es el limite correcto) pero
    imprime un aviso en el crudo, asi que se declara con errstate en vez de
    dejar que el aviso viaje como si fuera un hallazgo.
    """
    if clase == "gauss":
        return E0 * np.exp(-(y / W0) ** 2)
    if clase == "sech":
        with np.errstate(over="ignore"):
            return E0 / np.cosh(y / W0)
    raise SystemExit("perfil desconocido: %r (use sech o gauss)" % (clase,))


def envolvente(t):
    """[ELEGIDO, declarado] rampa de coseno alzado de 3 periodos y luego CW."""
    if t <= 0.0:
        return 0.0
    if t < T_RAMPA:
        return 0.5 * (1.0 - math.cos(math.pi * t / T_RAMPA))
    return 1.0


# ============================================================================
# INSTRUMENTO A: espectro angular paraxial por FFT (capa analitica)
# ============================================================================
def instrumento_espectral(clase, n=1 << 20, dy=0.01, nmuestras=41, verbose=True):
    y = (np.arange(n) - n // 2) * dy
    psi0 = perfil(y, clase)
    ky = 2.0 * math.pi * np.fft.fftfreq(n, d=dy)
    P0 = np.fft.fft(psi0)
    xs = np.linspace(0.0, X_FIN, nmuestras)
    sig = []
    for x in xs:
        psi = np.fft.ifft(P0 * np.exp(-1j * (ky ** 2) * x / (2.0 * K0)))
        sig.append(segundo_momento(y, np.abs(psi) ** 2))
    sig = np.asarray(sig, dtype=float)
    ley = ley_rayleigh_sigma(xs) if clase == "gauss" else ley_segundo_momento(xs)
    rel = sig / ley - 1.0
    m = xs >= X_JUEZ
    res = float(np.abs(rel[m]).max())
    where = float(xs[m][int(np.argmax(np.abs(rel[m])))])
    if verbose:
        print("  [A] espectral n=2**%d dy=%.4g  sigma_y(0)=%.10f  ley(0)=%.10f"
              % (int(math.log2(n)), dy, sig[0], ley[0]))
        print("  [A] residuo max |sigma_med/ley - 1| = %.4e en x = %.4f  (umbral %.3g)"
              % (res, where, UMBRAL))
    return {"instrumento": "espectral_fft_paraxial", "perfil": clase,
            "n": n, "dy": dy, "x": xs.tolist(), "sigma_y": sig.tolist(),
            "ley": ley.tolist(), "residuo_max": res, "residuo_en_x": where,
            "ventana_juzgada": [X_JUEZ, X_FIN], "umbral": UMBRAL,
            "veredicto": "OK" if res <= UMBRAL else "ROJO"}


# ============================================================================
# INSTRUMENTO B: Yee 2D TE sobre la malla sellada (EL METRO)
# ============================================================================
def _ddx(F):
    g = np.zeros_like(F)
    g[1:, :] = (F[1:, :] - F[:-1, :]) / DX
    return g


def _ddy(F):
    g = np.zeros_like(F)
    g[:, 1:] = (F[:, 1:] - F[:, :-1]) / DX
    return g


def _ddx_f(F):
    g = np.zeros_like(F)
    g[:-1, :] = (F[1:, :] - F[:-1, :]) / DX
    return g


def _ddy_f(F):
    g = np.zeros_like(F)
    g[:, :-1] = (F[:, 1:] - F[:, :-1]) / DX
    return g


def _mascara():
    m = np.ones((NX, NY))
    for eje, n in ((0, NX), (1, NY)):
        idx = np.arange(n)
        borde = np.maximum(np.clip(ESPONJA - idx, 0, ESPONJA),
                           np.clip(idx - (n - 1 - ESPONJA), 0, ESPONJA)) / float(ESPONJA)
        s = 1.0 - ALFA * borde ** 2
        m = m * (s.reshape((-1, 1)) if eje == 0 else s.reshape((1, -1)))
    return m


def _paso(F, dt, masc):
    """Un paso de Yee TE: H en t+dt/2 con E viejo, E en t+dt con H nuevo."""
    Ez, Hx, Hy = F["Ez"], F["Hx"], F["Hy"]
    Hx = Hx - (dt / MU0) * _ddy_f(Ez)
    Hy = Hy + (dt / MU0) * _ddx_f(Ez)
    Ez = Ez + (dt / EPS0) * (_ddx(Hy) - _ddy(Hx))
    if masc is not None:
        Hx = Hx * masc
        Hy = Hy * masc
        Ez = Ez * masc
    F["Ez"], F["Hx"], F["Hy"] = Ez, Hx, Hy


def instrumento_fdtd(clase="sech", pasos=None, verbose=True):
    pasos = PASOS if pasos is None else int(pasos)
    y = (np.arange(NY) - JC) * DX
    g = perfil(y, clase)                            # amplitud E0 del §3
    masc = _mascara()
    F = {"Ez": np.zeros((NX, NY)), "Hx": np.zeros((NX, NY)), "Hy": np.zeros((NX, NY))}
    q = 2.0 * math.sin(OMEGA * DT) / OMEGA          # cuadratura EXACTA en malla
    Iacc = np.zeros((NX, NY))
    n_acc = 0
    a1 = None
    a2 = None
    k_desde = pasos - N_AVG
    t0 = time.time()
    for k in range(pasos):
        t = (k + 0.5) * DT
        F["Ez"][I_SRC, :] = envolvente(t) * g * math.cos(OMEGA * t)
        _paso(F, DT, masc)
        Ezn = F["Ez"]
        if a2 is not None and k >= k_desde:
            # derivada CENTRADA en t_{k-1}: (E_k - E_{k-2}) / q, q = 2 sin(w dt)/w
            der = (Ezn - a2) / q
            Iacc += a1 * a1 + der * der
            n_acc += 1
        a2 = a1
        a1 = Ezn
        if verbose and (k + 1) % 1000 == 0:
            print("    [B] paso %5d/%d  t=%.3f  %.1f s"
                  % (k + 1, pasos, (k + 1) * DT, time.time() - t0))
    I = Iacc / max(n_acc, 1)
    cols = np.arange(I_MIN, I_MAX + 1)
    II = I[cols, :]
    x = (cols - I_SRC) * DX
    S0 = II.sum(axis=1)
    S1 = (II * y[None, :]).sum(axis=1)
    S2 = (II * (y ** 2)[None, :]).sum(axis=1)
    # GUARDA DE ESTACION CIEGA: donde el frente todavia no llego S0 = 0 y
    # S2/S0 es 0/0 -> nan, y donde llego apenas queda ruido de redondeo cuyo
    # sigma es basura. El reparto NO es un umbral elegido al ver la salida: es
    # el cono de luz del esquema. La fuente vive en la columna I_SRC y en
    # unidades naturales la senal avanza a c = 1, asi que la estacion a
    # distancia x tiene senal solo si x <= c * pasos * dt. Lo que queda fuera
    # se marca NO MEDIDO, se excluye del maximo y se declara: no_medido > 0 no
    # puede resolverse en un "OK" a secas.
    x_frente = pasos * DT
    alcanzado = x <= x_frente
    vivo = alcanzado & (S0 > 0.0)
    sig = np.zeros(S0.shape)
    sig[vivo] = np.sqrt(np.maximum(
        S2[vivo] / S0[vivo] - (S1[vivo] / S0[vivo]) ** 2, 0.0))
    ley = ley_rayleigh_sigma(x) if clase == "gauss" else ley_segundo_momento(x)
    rel = sig / ley - 1.0
    m = vivo & (x >= X_JUEZ)
    no_medido = int((~vivo).sum())
    no_alcanzado = int((~alcanzado).sum())
    if not bool(m.any()):
        raise SystemExit("ROJO: ninguna estacion medida en la ventana juzgada")
    res = float(np.abs(rel[m]).max())
    where = float(x[m][int(np.argmax(np.abs(rel[m])))])
    # invariante declarado: S0 = int I dy debe ser constante a lo largo de x
    der_s0 = float(np.abs(S0[vivo] / S0[0] - 1.0).max())
    veredicto = "OK" if res <= UMBRAL else "ROJO"
    if no_medido:
        veredicto = "ROJO" if res > UMBRAL else "PARCIAL"
    if verbose:
        print("  [B] sigma_y(x=%.3f)=%.10f  ley=%.10f  S0/S0(0) max=%.4e"
              % (x[0], sig[0], ley[0], der_s0))
        print("  [B] residuo max |sigma_med/ley - 1| = %.4e en x = %.4f  (umbral %.3g)"
              % (res, where, UMBRAL))
        print("  [B] frente causal x <= %.4f ; medidas=%d  no_medido=%d (fuera del cono %d)"
              % (x_frente, int(vivo.sum()), no_medido, no_alcanzado))
        print("  [B] n_acc=%d  pasos=%d  t_fin=%.4f  %.1f s"
              % (n_acc, pasos, pasos * DT, time.time() - t0))
    return {"instrumento": "yee_te_2d_malla_sellada", "perfil": clase,
            "pasos": pasos, "dt": DT, "dx": DX, "NX": NX, "NY": NY,
            "I_SRC": I_SRC, "I_MIN": I_MIN, "I_MAX": I_MAX, "n_acc": n_acc,
            "x": x.tolist(), "sigma_y": sig.tolist(), "ley": ley.tolist(),
            "x_frente_causal": x_frente,
            "estaciones_medidas": int(vivo.sum()), "no_medido": no_medido,
            "fuera_del_cono": no_alcanzado,
            "S0_invariante_max_rel": der_s0,
            "residuo_max": res, "residuo_en_x": where,
            "ventana_juzgada": [X_JUEZ, float(x[vivo][-1]) if bool(vivo.any()) else X_JUEZ],
            "umbral": UMBRAL,
            "veredicto": veredicto}


# ============================================================================
def control_discreto(verbose=True):
    """Control P1b: el perfil SELLADO, discretizado en dy = 0.05, contra la ley(0).

    Un residuo grande aqui seria del METRO (la malla), no del objeto.
    """
    y = (np.arange(NY) - JC) * DX
    out = {}
    for clase in ("sech", "gauss"):
        g = perfil(y, clase)
        s = segundo_momento(y, g * g)
        ley0 = SIG0_GAUSS if clase == "gauss" else SIG0_SECH
        out[clase] = {"sigma_discreto": s, "sigma_ley0": ley0,
                      "rel": s / ley0 - 1.0}
        if verbose:
            print("  [control] %-5s sigma_y(0) discreto = %.10f  ley(0) = %.10f  rel = %+.3e"
                  % (clase, s, ley0, s / ley0 - 1.0))
    return out


def main(argv):
    t_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print("T_UTC_INICIO = %s" % t_utc)
    print("UNIVERSO DECLARADO: %s" % (AQUI / "nulo_lineal.py"))
    print("  unidades naturales c=lambda=1, omega=k0=2pi, eps0=mu0=1; chi3=0 (medio lineal)")
    print("  malla sellada: dx=dy=%.4g  NX=%d  NY=%d  dt=%.12g  esponja=%d celdas alfa=%.2f"
          % (DX, NX, NY, DT, ESPONJA, ALFA))
    print("  fuente CW en columna %d, rampa %.4g; estaciones %d..%d (x=%.4g..%.4g)"
          % (I_SRC, T_RAMPA, I_MIN, I_MAX, (I_MIN - I_SRC) * DX, (I_MAX - I_SRC) * DX))
    print("  MOTOR = python3 -B + numpy %s ; UNIDAD = celda / linea / byte" % np.__version__)

    fdtd = "--fdtd" in argv
    guardar = "--json" in argv
    clase = "sech"
    pasos = None
    for i, a in enumerate(argv):
        if a == "--perfil" and i + 1 < len(argv):
            clase = argv[i + 1]
        elif a.startswith("--perfil="):
            clase = a.split("=", 1)[1]
        elif a == "--pasos" and i + 1 < len(argv):
            pasos = int(argv[i + 1])
        elif a.startswith("--pasos="):
            pasos = int(a.split("=", 1)[1])

    print("PERFIL = %s%s" % (clase, "" if pasos is None else "  (pasos=%d)" % pasos))
    resultados = {"T_UTC_inicio": t_utc, "perfil": clase,
                  "universo": {"c": 1.0, "lambda": 1.0, "omega": OMEGA, "k0": K0,
                               "eps0": 1.0, "mu0": 1.0, "chi3": 0.0,
                               "w0": W0, "E0": E0, "dx": DX, "dt": DT,
                               "NX": NX, "NY": NY, "I_SRC": I_SRC,
                               "X_JUEZ": X_JUEZ, "umbral": UMBRAL}}

    print("--- control discreto (el metro, no el objeto) ---")
    resultados["control_discreto"] = control_discreto()

    print("--- instrumento A: espectro angular PARAXIAL (capa analitica) ---")
    rA = instrumento_espectral(clase)
    resultados["A_espectral"] = rA

    if fdtd:
        print("--- instrumento B: YEE 2D TE sobre la malla SELLADA (el metro) ---")
        rB = instrumento_fdtd(clase, pasos=pasos)
        resultados["B_fdtd"] = rB

    veredictos = [rA["veredicto"]]
    if fdtd:
        veredictos.append(resultados["B_fdtd"]["veredicto"])
    rojo = any(v != "OK" for v in veredictos)
    print("P1%s %s: %s" % ("a" if clase == "gauss" else "b", clase.upper(),
                           "OK" if not rojo else "ROJO"))

    if guardar:
        etiqueta = "%s_%s" % (clase, "fdtd" if fdtd else "espectral")
        destino = DATA / ("nulo_lineal_%s.json" % etiqueta)
        destino.write_text(json.dumps(resultados, indent=1, ensure_ascii=False),
                           encoding="utf-8")
        print("escrito: %s" % destino)
    return 1 if rojo else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

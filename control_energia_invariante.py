#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""control_energia_invariante.py — METRO NUEVO para el control de energia.

NO edita el motor: lo IMPORTA. `propagador_2d_te.py` queda intacto y sigue
siendo el testigo de control de P1 (blob c103ef6c218414a5e1980a30aa24489b938de557).

Separa dos objetos que el control sellado confunde:

  M1 = energia COLOCAL: el metro del motor (propagador_2d_te.energia). Suma
       (1/2)(eps0 |E|^2 + |B|^2/mu0) en la MISMA rejilla y al MISMO indice
       temporal. Pero el esquema es una saltarina entrecruzada: E vive en
       pasos enteros (E^n) y H en semienteros (H^{n+1/2}). Sumar cuadrado a
       cuadrado los mezcla con defecto O((omega dt)^2).

  M2 = invariante de saltarina: la forma BILINEAL intercalada en H
       U^n = (1/2) eps0 sum |E^n|^2 + (1/2) mu0 sum H^{n-1/2} . H^{n+1/2}
       que el esquema lineal (chi3 = 0) conserva EXACTAMENTE, porque
       C^T = -C (skew-adjunto) con PEC:
         H^{n+3/2} - H^{n-1/2} = -(dt/mu0) C (E^n + E^{n+1})
         |E^{n+1}|^2 - |E^n|^2 = (dt/eps0) (E^{n+1}+E^n) . C^T H^{n+1/2}
         dU = (1/2)dt (E^{n+1}+E^n).C^T H^{n+1/2}
              - (1/2)dt H^{n+1/2}.C(E^{n+1}+E^n) = 0    [u.Cv = -v.Cu]

PROTOCOLO: identico al de control_energia() del motor (misma malla, mismo IC,
400 pasos, PEC, sin esponja, sin fuente, chi3 = 0, muestreo en
k = 0,80,...,400) para que los DOS metros midan LA MISMA trayectoria.

Predicciones selladas (V1..V4 + reserva) en
PREREGISTRO_ADENDA_P2_INVARIANTE_20261013.md, escritas ANTES de esta corrida.
"""

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

import propagador_2d_te as M

AQUI = Path(__file__).resolve().parent
DATA = AQUI / "data"
COMPONENTES_H = ("Hx", "Hy", "Hz")
UMBRAL_SELLADO = 1e-9  # el del motor: NO se baja, se le mide el dominio

# crudo del motor leido el 2026-10-13T02:12:15Z (data/propagador_control_energia.json)
CRUDO_MOTOR = {"U0": 0.000506605916123234,
               "U_fin": 0.0005860746588598202,
               "deriva_global": 0.15686501125907726,
               "deriva_peor_par": 0.11693477574005584,
               "deriva_por_par": [0.11693477574005584, 0.06943300755272275,
                                  0.06207741888182505, 0.007474479289240721,
                                  0.02494425034993153],
               "umbral": 1e-9}


def _suma_emparejada(Ha, Hb):
    """sum_c Hc[k-1/2] * Hc[k+1/2] sobre la rejilla colocal del motor."""
    s = 0.0
    for c in COMPONENTES_H:
        s += float(np.sum(Ha[c] * Hb[c]))
    return s


def _invariante(F, Hm):
    """M2: (1/2) eps0 sum|E|^2 + (1/2) mu0 sum H^{k-1/2}.H^{k+1/2}."""
    e2 = F["Ex"] ** 2 + F["Ey"] ** 2 + F["Ez"] ** 2
    return (0.5 * M.EPS0 * float(np.sum(e2))
            + 0.5 * M.MU0 * _suma_emparejada(Hm, F))


def _extremos(F):
    return {"max_Ex": float(np.abs(F["Ex"]).max()),
            "max_Ey": float(np.abs(F["Ey"]).max()),
            "max_Ez": float(np.abs(F["Ez"]).max()),
            "max_Hx": float(np.abs(F["Hx"]).max()),
            "max_Hy": float(np.abs(F["Hy"]).max()),
            "max_Hz": float(np.abs(F["Hz"]).max())}


def _derivas(U):
    pares = [abs(b / a - 1.0) for a, b in zip(U[:-1], U[1:])]
    return {"deriva_por_par": pares, "deriva_peor_par": max(pares),
            "deriva_global_ancla0": abs(U[-1] / U[0] - 1.0),
            "deriva_global_ancla_cascara": abs(U[-1] / U[1] - 1.0)}


def corrida(chi3, pasos_libres=400, dt=None, verbose=True):
    """Replica EXACTA del protocolo de control_energia(), con los dos metros.

    dt = None usa M.DT (CFL 0.70). dt distinto = barrido de reserva (§4).
    """
    dt = M.DT if dt is None else float(dt)
    previo = M.CHI3
    M.CHI3 = float(chi3)
    t0 = time.time()
    try:
        F = M.campos_vacios()
        g, _ = M.perfiles()
        F["Ez"][M.I_SRC, :] = g
        h = max(1, pasos_libres // 5)
        ks, U1, U2, ext = [], [], [], []
        guarda_en = None
        for k in range(pasos_libres + 1):
            Hm = {c: F[c].copy() for c in COMPONENTES_H}
            if k > 0:
                try:
                    M.paso(F, dt, None)
                except RuntimeError as e:
                    guarda_en = k
                    if verbose:
                        print("  GUARDA DISPARADA en k=%d: %s" % (k, e), flush=True)
                    break
                M.pec_muros(F)
            if k % h == 0:
                ks.append(k)
                U1.append(M.energia(F))
                U2.append(_invariante(F, Hm))
                ext.append(_extremos(F))
                if verbose:
                    print("  k=%4d  U1_colocal=%.12e  U2_invariante=%.12e"
                          "  defecto_rel=%.3e" % (k, U1[-1], U2[-1],
                                                 abs(U1[-1] / U2[-1] - 1.0)),
                          flush=True)
            if verbose and (k % 100 == 0):
                print("    ... paso %d/%d  t_fis=%.3f  %.1f s"
                      % (k, pasos_libres, k * dt, time.time() - t0), flush=True)
        d1, d2 = _derivas(U1), _derivas(U2)
        out = {"chi3": float(chi3), "pasos_libres": pasos_libres, "h": h,
               "dt": dt, "cfl": dt * M.C / M.DX,
               "muestras_k": ks,
               "U1_colocal": U1, "U2_invariante": U2,
               "M1_colocal": d1, "M2_invariante": d2,
               "defecto_metro_max_rel": max(abs(a / b - 1.0)
                                            for a, b in zip(U1, U2)),
               "extremos_por_muestra": ext,
               "extremos_final": ext[-1],
               "guarda_disparada_en": guarda_en,
               "umbral_sellado": UMBRAL_SELLADO,
               "veredicto_M1_colocal": _veredicto(d1),
               "veredicto_M2_invariante": _veredicto(d2),
               "omega_dt": M.OMEGA * dt, "omega_dt_cuadrado": (M.OMEGA * dt) ** 2,
               "segundos": time.time() - t0}
        return out
    finally:
        M.CHI3 = previo


def _veredicto(d):
    ok = (d["deriva_peor_par"] <= UMBRAL_SELLADO
          and d["deriva_global_ancla0"] <= UMBRAL_SELLADO)
    return "OK" if ok else "ROJO"


def fidelidad_V3(chi3_cero):
    """V3: mi corrida chi3=0 debe reproducir el crudo del motor digito a digito."""
    dif = {"U0": abs(chi3_cero["U1_colocal"][0] - CRUDO_MOTOR["U0"]),
           "U_fin": abs(chi3_cero["U1_colocal"][-1] - CRUDO_MOTOR["U_fin"]),
           "deriva_global": abs(chi3_cero["M1_colocal"]["deriva_global_ancla0"]
                                - CRUDO_MOTOR["deriva_global"]),
           "deriva_peor_par": abs(chi3_cero["M1_colocal"]["deriva_peor_par"]
                                  - CRUDO_MOTOR["deriva_peor_par"]),
           "deriva_por_par_max": max(abs(a - b) for a, b in zip(
               chi3_cero["M1_colocal"]["deriva_por_par"],
               CRUDO_MOTOR["deriva_por_par"]))}
    peor = max(dif.values())
    return {"CRUDO_MOTOR": CRUDO_MOTOR, "diferencias_abs": dif,
            "peor_diferencia_abs": peor,
            "veredicto": "REPRODUCE" if peor == 0.0 else
                         ("REPRODUCE_A_REDONDEO" if peor <= 1e-15 else "DIVERGE")}


def main() -> int:
    args = sys.argv[1:]
    t_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print("T_UTC_INICIO = %s" % t_utc)
    print("UNIVERSO DECLARADO: %s" % M.UNIVERSO)
    print("MOTOR = python3 -B + numpy %s ; UNIDAD = celda / linea / byte"
          % np.__version__)
    print("METRO NUEVO = invariante de saltarina (bilineal intercalado en H)")

    def guardar(nombre, carga):
        destino = DATA / (nombre + ".json")
        destino.write_text(json.dumps(carga, indent=1, ensure_ascii=False),
                           encoding="utf-8")
        print("escrito: %s (%d bytes)"
              % (destino, destino.stat().st_size), flush=True)

    if "--barrido-dt" not in args and "--correr" not in args:
        print("uso: control_energia_invariante.py --correr | --barrido-dt")
        print("  --correr      : chi3=0 (V1,V3,V4) y chi3=1 (V2)")
        print("  --barrido-dt  : RESERVA del §4, solo si V1 falla")
        return 0

    salida = {"T_UTC": t_utc, "UNIVERSO": M.UNIVERSO,
              "MOTOR": "python3 -B + numpy %s" % np.__version__,
              "protocolo": {"replica_de": "propagador_2d_te.control_energia",
                            "malla": {"NX": M.NX, "NY": M.NY, "DX": M.DX,
                                      "DT": M.DT, "I_SRC": M.I_SRC},
                            "muestreo": "k % (pasos_libres//5) == 0",
                            "sesion": "PREREGISTRO_ADENDA_P2_INVARIANTE_20261013.md"},
              "corridas": {}}

    if "--correr" in args:
        c0 = corrida(0.0)
        salida["corridas"]["chi3=0.00"] = c0
        salida["V3_fidelidad_replica"] = fidelidad_V3(c0)
        print("  V3 fidelidad: %s (peor dif abs %.3e)"
              % (salida["V3_fidelidad_replica"]["veredicto"],
                 salida["V3_fidelidad_replica"]["peor_diferencia_abs"]), flush=True)
        c1 = corrida(1.0)
        salida["corridas"]["chi3=1.00"] = c1
        # V1 / V2 / V4 explicitos
        salida["V1_invariante_se_conserva"] = (
            c0["veredicto_M2_invariante"] == "OK")
        salida["V2_metro_puede_moverse"] = (
            c1["M2_invariante"]["deriva_global_ancla0"] > UMBRAL_SELLADO
            or c1["M2_invariante"]["deriva_peor_par"] > UMBRAL_SELLADO)
        salida["V4_reduccion_TE_cero"] = {
            "max_Ex": c0["extremos_final"]["max_Ex"],
            "max_Ey": c0["extremos_final"]["max_Ey"],
            "max_Hz": c0["extremos_final"]["max_Hz"],
            "veredicto": "CERO_EXACTO" if (c0["extremos_final"]["max_Ex"] == 0.0
                                           and c0["extremos_final"]["max_Ey"] == 0.0
                                           and c0["extremos_final"]["max_Hz"] == 0.0)
                         else "NO_CERO"}
        salida["disparador_reserva_barrido_dt"] = (
            "CORRER (V1 fallo)" if not salida["V1_invariante_se_conserva"]
            else "NO CORRER (V1 se cumplio)")
        guardar("control_energia_invariante", salida)
        return 0

    if "--barrido-dt" in args:
        d2 = 0.5 * M.DT
        a = corrida(0.0, pasos_libres=400, dt=M.DT)
        b = corrida(0.0, pasos_libres=800, dt=d2)
        salida["corridas"]["cfl=0.70_400pasos"] = a
        salida["corridas"]["cfl=0.35_800pasos"] = b
        ra = a["M2_invariante"]["deriva_global_ancla0"]
        rb = b["M2_invariante"]["deriva_global_ancla0"]
        salida["barrido_dt"] = {"deriva_M2_cfl070": ra, "deriva_M2_cfl035": rb,
                                "razon": (ra / rb) if rb > 0 else None,
                                "lectura": ("O(dt^2) DEL METRO" if rb > 0
                                            and ra / rb > 3.0 else "DEL OBJETO")}
        guardar("control_energia_barrido_dt", salida)
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# HUELLA-EJECUTOR-CONTROL-ENERGIA-OPTICA-20261021
"""Ejecutor directo del metro de energia, con una corrida reducida."""

from __future__ import annotations

import math
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import control_energia_invariante as instrumento  # noqa: E402
import propagador_2d_te as motor  # noqa: E402


def test_corrida_reducida_devuelve_metricas_derivadas_y_restaura_chi3():
    chi3_previo = motor.CHI3
    resultado = instrumento.corrida(0.0, pasos_libres=40, verbose=False)

    assert motor.CHI3 == chi3_previo
    assert resultado["chi3"] == 0.0
    assert resultado["pasos_libres"] == 40
    assert resultado["muestras_k"] == [0, 8, 16, 24, 32, 40]
    assert resultado["guarda_disparada_en"] is None

    u1 = resultado["U1_colocal"]
    u2 = resultado["U2_invariante"]
    assert len(u1) == len(u2) == len(resultado["muestras_k"])
    assert all(math.isfinite(valor) for valor in (*u1, *u2))
    assert all(valor > 0.0 for valor in (*u1, *u2))
    defecto = max(abs(a / b - 1.0) for a, b in zip(u1, u2))
    assert resultado["defecto_metro_max_rel"] == defecto
    assert len(resultado["M1_colocal"]["deriva_por_par"]) == 5
    assert len(resultado["M2_invariante"]["deriva_por_par"]) == 5


def test_runtimeerror_del_paso_se_reporta_y_chi3_se_restaura(monkeypatch):
    llamadas = 0
    chi3_previo = motor.CHI3

    def paso_controlado(campos, dt, mascara):
        nonlocal llamadas
        llamadas += 1
        if llamadas == 9:
            raise RuntimeError("guarda de prueba")
        return campos

    monkeypatch.setattr(motor, "paso", paso_controlado)
    resultado = instrumento.corrida(1.0, pasos_libres=40, verbose=False)

    assert resultado["guarda_disparada_en"] == 9
    assert resultado["muestras_k"] == [0, 8]
    assert motor.CHI3 == chi3_previo

# HUELLA-EJECUTOR-PROPAGADOR-TE-OPTICA-20261021
"""Ejecutor directo de los contratos locales del paso Yee TE."""

from __future__ import annotations

import math

import numpy as np
import pytest

import propagador_2d_te as motor


@pytest.fixture(autouse=True)
def estado_limpio():
    chi3_previo = motor.CHI3
    motor.CHI3 = 0.0
    motor._PASO_N[0] = 0
    yield
    motor.CHI3 = chi3_previo
    motor._PASO_N[0] = 0


def test_paso_aplica_el_stencil_yee_con_signo_y_magnitud():
    dt = 0.01
    campos = {nombre: np.zeros((5, 5)) for nombre in motor.COMPONENTES}
    campos["Ez"][1, 2] = 1.0

    resultado = motor.paso(campos, dt, None)

    assert resultado is campos
    assert math.isclose(campos["Hx"][1, 2], dt / motor.DX, abs_tol=1e-12)
    assert math.isclose(campos["Hy"][1, 2], -dt / motor.DX, abs_tol=1e-12)
    esperado_ez = 1.0 - 3.0 * (dt / motor.DX) ** 2
    assert math.isclose(campos["Ez"][1, 2], esperado_ez, abs_tol=1e-12)


def test_perfil_no_declarado_falla_con_systemexit_textual():
    with pytest.raises(SystemExit) as salida:
        motor.terminos_de("perfil-no-declarado")

    assert isinstance(salida.value.code, str)
    assert "perfil desconocido" in salida.value.code


def test_guarda_kerr_dispara_en_el_paso_declarado():
    motor.CHI3 = 1.0
    campos = {nombre: np.zeros((5, 5)) for nombre in motor.COMPONENTES}
    campos["Ez"][:] = 1.0

    with pytest.raises(RuntimeError, match="FALLO DEL ESQUEMA"):
        for _ in range(motor.GUARDA_CADA):
            motor.paso(campos, 0.01, None)

    assert motor._PASO_N[0] == motor.GUARDA_CADA

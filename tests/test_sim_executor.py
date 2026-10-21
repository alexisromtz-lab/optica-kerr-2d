# HUELLA-EJECUTOR-SIM-OPTICA-20261020
"""Ejecutor del instrumento — optica-kerr-2d.

`nulo_lineal.py` importa numpy y produce el nulo lineal (control negativo de la
casa Kerr) que el pre-registro y el README publican, pero hasta hoy ningun test
ni paso del aparato lo abria: el censo `censo_numpy_dependencia_20261020.py` lo
clasifico `SIN_EJECUTOR` (3 portadores, 0 ejecutados). Un import que nadie
ejecuta no puede fallar, y por tanto no era una dependencia: era una suposicion.

Este test corre el instrumento por su propia puerta (`main`, en proceso) y
**asierte sobre su salida**: el residuo del instrumento A contra el umbral que
el propio instrumento imprime, y la version de numpy que la cabecera declara
contra la que de verdad esta cargada.

Falsador declarado (lo que hace rojo a este test):

  1. numpy ausente -> `import nulo_lineal` levanta `ModuleNotFoundError` en la
     coleccion: el test no puede ni empezar.
  2. el residuo maximo supera el umbral impreso -> cae el test del residuo
     (y con el, el veredicto `P1b SECH: OK` deja de estar sostenido).
  3. la cabecera `MOTOR = ... numpy X.Y.Z` deja de coincidir con el numpy
     cargado -> cae el test de la cabecera: la prosa del instrumento no puede
     contradecir su aparato.
  4. numpy 1.x activo -> cae el mismo test: el manifiesto declara 2.0.
"""

from __future__ import annotations

import contextlib
import io
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import nulo_lineal as instrumento  # noqa: E402

RE_RESIDUO = re.compile(
    r"^\s*\[A\] residuo max \|sigma_med/ley - 1\| = ([0-9.eE+-]+) en x = "
    r"([0-9.]+)\s+\(umbral ([0-9.eE+-]+)\)\s*$"
)
RE_MOTOR = re.compile(r"^\s*MOTOR = python3 -B \+ numpy (\S+) ;")


def _salida():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = instrumento.main([])
    return rc, buf.getvalue().splitlines()


def test_el_instrumento_corre_y_sella_su_veredicto():
    rc, lineas = _salida()
    assert rc == 0, rc
    assert lineas, "el instrumento no imprimio nada"
    assert "P1b SECH: OK" in lineas, lineas[-3:]


def test_el_residuo_del_instrumento_a_cumple_su_umbral():
    _, lineas = _salida()
    hallados = [RE_RESIDUO.match(l) for l in lineas]
    hallados = [m for m in hallados if m]
    assert hallados, [l for l in lineas if "residuo" in l]
    residuo, x, umbral = (float(g) for g in hallados[-1].groups())
    assert umbral > 0.0, umbral
    assert residuo >= 0.0, residuo
    assert residuo <= umbral, (residuo, umbral, x)


def test_la_cabecera_no_miente_sobre_su_motor():
    """La version que imprime el instrumento es la que tiene cargada."""
    _, lineas = _salida()
    hallados = [RE_MOTOR.match(l) for l in lineas]
    hallados = [m for m in hallados if m]
    assert hallados, [l for l in lineas if "MOTOR" in l]
    version_cabecera = hallados[0].group(1)
    version_cargada = instrumento.np.__version__
    assert version_cabecera == version_cargada, (version_cabecera, version_cargada)


def test_numpy_cargado_cumple_el_piso_declarado():
    version = instrumento.np.__version__
    assert re.fullmatch(r"\d+\.\d+\.\d+.*", version), version
    assert int(version.split(".")[0]) >= 2, version

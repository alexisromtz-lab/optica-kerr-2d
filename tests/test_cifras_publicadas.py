# HUELLA-OPTICA-KERR-TEST-CIFRAS-20261020
"""El README de este repositorio promete que cada cifra tiene portador.

Este test hace exigible esa promesa en cada push. No mide fisica: mide
procedencia. Los falsadores, uno por cada forma de mentir de una cifra:

  1. una cifra publicada con seis o mas decimales cuyo valor no esta en
     ningun crudo commiteado;
  2. una figura de prosa (13.11 %, 19.06 %) que no sea el redondeo fiel de
     la hoja que la respalda;
  3. un umbral sellado que se mueva de sitio o desaparezca del pre-registro;
  4. una celda roja que alguien borre del README para dejar solo lo verde.

No hay red, no hay tolerancias elegidas a mano: la tolerancia de cada cifra es
la de su propio redondeo (media unidad del ultimo digito publicado).
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CRUDOS = sorted((RAIZ / "data").glob("*.json"))
README = RAIZ / "README.md"
PREREGISTRO = RAIZ / "PREREGISTRO_SOLITON_ESPACIAL_KERR_20261012.md"

# Una cifra "publicada" es la que se escribe con seis decimales o mas: las de
# menos digitos son redondeos de prosa y reclaman portador por otra via.
PATRON_CIFRA = re.compile(r"-?\d+\.\d{6,}(?:[eE][-+]?\d+)?")
# Cifras de prosa: dos o mas decimales, con o sin exponente.
PATRON_PROSA = re.compile(r"-?\d+\.\d{2,}(?:[eE][-+]?\d+)?")

UMBRAL_A1 = 0.03


def _cargar_crudos() -> list[tuple[str, object]]:
    """Devuelve (nombre, objeto). Un crudo ilegible es un rojo, no un olvido."""
    cargados = []
    for ruta in CRUDOS:
        try:
            cargados.append((ruta.name, json.loads(ruta.read_text(encoding="utf-8"))))
        except json.JSONDecodeError as exc:  # fail-closed
            raise AssertionError(f"crudo ilegible: {ruta.name}: {exc}") from exc
    return cargados


def _hojas_numericas(objeto: object):
    if isinstance(objeto, dict):
        for valor in objeto.values():
            yield from _hojas_numericas(valor)
    elif isinstance(objeto, list):
        for valor in objeto:
            yield from _hojas_numericas(valor)
    elif isinstance(objeto, (int, float)) and not isinstance(objeto, bool):
        if math.isfinite(objeto):
            yield objeto


def _quantum(literal: str) -> float:
    """Media unidad del ultimo digito publicado (la tolerancia de su redondeo)."""
    m = re.fullmatch(r"(\d+)\.(\d+)(?:[eE]([-+]?\d+))?", literal.lstrip("-"))
    assert m, f"literal no reconocido: {literal}"
    decimales = len(m.group(2))
    exponente = int(m.group(3) or 0)
    return 0.5 * 10.0 ** (exponente - decimales)


def _leer_crudo(nombre: str) -> dict:
    return json.loads((RAIZ / "data" / nombre).read_text(encoding="utf-8"))


def _residuo_plano(nombre: str) -> float:
    """El dato que sostiene A1/A2: el residuo de plano maximo del propagador."""
    medido = _leer_crudo(nombre)["medido"]
    valor = medido["residuo_plano_max"]
    assert isinstance(valor, float) and math.isfinite(valor), f"{nombre}: residuo ilegible"
    return valor


def _texto_readme() -> str:
    return README.read_text(encoding="utf-8")


def test_el_readme_publica_cifras():
    """Un README vaciado no puede pasar este test por vacuidad."""
    cifras = set(PATRON_PROSA.findall(_texto_readme()))
    assert len(cifras) >= 8, f"el README perdio sus cifras: solo quedan {sorted(cifras)}"


def test_toda_cifra_de_seis_decimales_tiene_portador():
    crudos = _cargar_crudos()
    assert crudos, "no hay crudos: sin portadores no hay auditoria"
    hojas = [valor for _, objeto in crudos for valor in _hojas_numericas(objeto)]
    textos = [(RAIZ / "data" / nombre).read_text(encoding="utf-8") for nombre, _ in crudos]

    huerfanas = []
    for literal in sorted(set(PATRON_CIFRA.findall(_texto_readme()))):
        publicado = float(literal)
        tolerancia = _quantum(literal)
        en_hoja = any(abs(valor - publicado) <= tolerancia for valor in hojas)
        en_texto = any(literal in texto for texto in textos)
        if not (en_hoja or en_texto):
            huerfanas.append(literal)

    assert not huerfanas, f"cifras publicadas sin crudo que las respalde: {huerfanas}"


def test_a1_rojo_es_el_redondeo_fiel_de_su_crudo():
    """13.11 % no es prosa: es el redondeo de la hoja del objeto."""
    medido = 100.0 * _residuo_plano("propagador_objeto.json")
    publicado = 13.11
    assert abs(medido - publicado) <= 0.5 * 10.0 ** -2, f"publicado {publicado}, medido {medido!r}"
    assert "13.11" in _texto_readme(), "el README dejo de publicar el ROJO del objeto"


def test_a2_nulo_difracta_y_lo_dice_el_crudo():
    """19.06 % y su cociente 6.35x contra el umbral sellado."""
    residuo = _residuo_plano("propagador_nulo_lineal.json")
    medido = 100.0 * residuo
    assert abs(medido - 19.06) <= 0.5 * 10.0 ** -2, f"publicado 19.06, medido {medido!r}"
    razon = residuo / UMBRAL_A1
    assert abs(razon - 6.35) <= 0.5 * 10.0 ** -2, f"publicado 6.35x, medido {razon!r}"
    assert "19.06" in _texto_readme(), "el README dejo de publicar la difraccion del nulo"


def test_el_umbral_sellado_sigue_en_su_preregistro():
    """El umbral no vive en el README: vive donde se sello."""
    sello = PREREGISTRO.read_text(encoding="utf-8")
    assert "0.03" in sello, "el pre-registro perdio el umbral A1"
    assert PREREGISTRO.name in _texto_readme(), "el README dejo de citar donde se sello el umbral"


def test_el_readme_conserva_los_rojos():
    """Quitar lo rojo del escaparate es el unico cambio que este repo no admite."""
    texto = _texto_readme()
    for marca in ("ROJO", "13.11", "19.06"):
        assert marca in texto, f"el README dejo de declarar {marca}"
    assert texto.count("ROJO") >= 2, "el README conserva un solo rojo: se perdio el otro"
    # Control negativo: la cifra falsa que circulo en un repo hermano no tiene
    # portador aqui, asi que si aparece es un error de procedencia.
    assert "-44.94" not in texto, "el README importo una cifra sin portador en este instrumento"

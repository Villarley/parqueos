import os
import sys
import json
from datetime import datetime

# Agrega la carpeta raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import modulo_parqueo as mp
from src import modulo_utiles as mu

# Rutas temporales para pruebas
TEST_ESPACIOS = "data/test_pc_espacios.json"
TEST_ALQUILERES = "data/test_pc_alquileres.json"
TEST_CONFIG = "data/test_pc_configuracion.json"

# Reasignar rutas en el módulo a las de prueba
mp.ESPACIOS_PATH = TEST_ESPACIOS
mp.ALQUILERES_PATH = TEST_ALQUILERES
mp.CONFIG_PATH = TEST_CONFIG

# Setup: reinicia los archivos
def setup_function():
    mu.escribir_json(TEST_ESPACIOS, [
        {"id": "A1", "estado": "libre"},
        {"id": "B1", "estado": "ocupado"}
    ])
    mu.escribir_json(TEST_ALQUILERES, [])
    mu.escribir_json(TEST_CONFIG, {
        "tarifa": 1.5,
        "tiempo_minimo": 30
    })

# Teardown: limpia al final
def teardown_module(module):
    for f in [TEST_ESPACIOS, TEST_ALQUILERES, TEST_CONFIG]:
        if os.path.exists(f):
            os.remove(f)

# -------------------------------
# TESTS
# -------------------------------

def test_obtener_espacios_disponibles():
    disponibles = mp.obtener_espacios_disponibles()
    assert len(disponibles) == 1
    assert disponibles[0]["id"] == "A1"

def test_alquilar_espacio_exitoso():
    resultado = mp.alquilar_espacio("user@test.com", "A1", 60)
    assert resultado is True

    alquileres = mu.leer_json(TEST_ALQUILERES)
    assert len(alquileres) == 1
    assert alquileres[0]["usuario"] == "user@test.com"

    espacios = mu.leer_json(TEST_ESPACIOS)
    assert espacios[0]["estado"] == "ocupado"

def test_alquilar_falla_espacio_ocupado():
    resultado = mp.alquilar_espacio("user@test.com", "B1", 60)
    assert resultado is False

def test_agregar_tiempo_alquiler():
    # Simula un alquiler activo
    mp.alquilar_espacio("otro@correo.com", "A1", 60)
    alquileres = mu.leer_json(TEST_ALQUILERES)
    id_alq = alquileres[0]["id"]

    resultado = mp.agregar_tiempo_alquiler(id_alq, 30)
    assert resultado is True

    alquileres = mu.leer_json(TEST_ALQUILERES)
    assert alquileres[0]["costo_total"] > 1.5  # aumentó

def test_liberar_espacio():
    mp.alquilar_espacio("usuario@correo.com", "A1", 60)
    alquileres = mu.leer_json(TEST_ALQUILERES)
    id_alq = alquileres[0]["id"]

    resultado = mp.liberar_espacio(id_alq)
    assert resultado is True

    alquileres = mu.leer_json(TEST_ALQUILERES)
    assert alquileres[0]["estado"] == "finalizado"

    espacios = mu.leer_json(TEST_ESPACIOS)
    assert espacios[0]["estado"] == "libre"

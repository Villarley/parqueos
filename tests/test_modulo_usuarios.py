# tests/test_modulo_usuarios.py

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import modulo_usuarios as mu

# Usamos archivo de prueba temporal
TEST_JSON = "data/test_pc_usuarios.json"
mu.USUARIOS_PATH = TEST_JSON

# Simular envío de correo para no enviar en realidad
def fake_enviar_correo(destino, asunto, cuerpo):
    print(f"[SIMULADO] Correo a {destino}: {asunto}")

mu.mu.enviar_correo = fake_enviar_correo

# Setup antes de cada test
def setup_function():
    with open(TEST_JSON, 'w', encoding='utf-8') as f:
        json.dump([], f)

# Teardown al final
def teardown_module(module):
    if os.path.exists(TEST_JSON):
        os.remove(TEST_JSON)

# ------------------------
# TESTS
# ------------------------

def test_registrar_usuario_exitoso():
    assert mu.registrar_usuario(
        correo="test@correo.com",
        contrasena="Password123",
        nombre="Usuario Prueba",
        telefono="0999999999",
        placa="XYZ123"
    ) is True

def test_registro_usuario_duplicado():
    mu.registrar_usuario("duplicado@correo.com", "Clave123", "Uno", "0987654321", "AAA111")
    assert mu.registrar_usuario("duplicado@correo.com", "OtraClave123", "Dos", "0987654321", "BBB222") is False

def test_login_correcto():
    mu.registrar_usuario("login@correo.com", "Correcta123", "Login User", "0998887777", "LOGIN1")
    user = mu.autenticar_usuario("login@correo.com", "Correcta123")
    assert user is not None
    assert user["nombre"] == "Login User"

def test_login_incorrecto():
    mu.registrar_usuario("noentra@correo.com", "ClaveSegura123", "Error", "0991234567", "FAIL1")
    assert mu.autenticar_usuario("noentra@correo.com", "ContraseñaIncorrecta") is None

def test_recuperar_contrasena_simulada():
    mu.registrar_usuario("recuperar@correo.com", "Clave123", "Recuperar", "0991112222", "RECUP1")
    assert mu.enviar_recordatorio_contrasena("recuperar@correo.com") is True

def test_recuperar_contrasena_usuario_inexistente():
    assert mu.enviar_recordatorio_contrasena("inexistente@correo.com") is False

# tests/test_modulo_utiles.py

import sys
import os

# Agrega la carpeta src al path de imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import modulo_utiles as mu

def test_validar_correo():
    assert mu.validar_correo("correo@ejemplo.com") is True
    assert mu.validar_correo("correo-invalido") is False

def test_validar_contrasena():
    assert mu.validar_contrasena("ClaveSegura123") is True
    assert mu.validar_contrasena("123") is False

def test_validar_telefono():
    assert mu.validar_telefono("0987654321") is True
    assert mu.validar_telefono("abcd123456") is False

def test_fecha_hora_actual():
    resultado = mu.fecha_hora_actual()
    assert isinstance(resultado, str)
    assert len(resultado) == 16

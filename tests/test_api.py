import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_inicio():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["mensaje"] == "NetAdmin API funcionando correctamente"


def test_crear_dispositivo():
    dispositivo = {
        "ip": "10.0.0.1",
        "hostname": "router-test",
        "mac": "00:AA:BB:CC:DD:EE",
        "tipo": "router",
        "sistema": "Cisco IOS",
        "estado": "activo"
    }

    response = client.post("/dispositivos", json=dispositivo)

    assert response.status_code in [201, 400]


def test_listar_dispositivos():
    response = client.get("/dispositivos")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_dispositivo_no_encontrado():
    response = client.get("/dispositivos/255.255.255.255")

    assert response.status_code == 404


def test_exportar_inventario():
    response = client.get("/exportar")

    assert response.status_code == 200
    assert response.json()["mensaje"] == "Inventario exportado correctamente"
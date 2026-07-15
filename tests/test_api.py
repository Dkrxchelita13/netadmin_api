import os
import sys
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


def registrar_usuario_prueba(client, rol):
    username = f"{rol}_{uuid4().hex[:10]}"
    password = "PasswordPrueba123"

    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "rol": rol
        }
    )

    assert response.status_code == 201

    return {
        "username": username,
        "password": password
    }


def iniciar_sesion_prueba(client, credenciales):
    response = client.post(
        "/auth/login",
        json=credenciales
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture(scope="session")
def admin_headers(client):
    credenciales = registrar_usuario_prueba(
        client,
        rol="admin"
    )

    return iniciar_sesion_prueba(
        client,
        credenciales
    )


@pytest.fixture(scope="session")
def consulta_headers(client):
    credenciales = registrar_usuario_prueba(
        client,
        rol="consulta"
    )

    return iniciar_sesion_prueba(
        client,
        credenciales
    )


def generar_ip_prueba():
    numero = uuid4().int

    tercer_octeto = (numero % 200) + 1
    cuarto_octeto = ((numero >> 8) % 200) + 1

    return f"10.250.{tercer_octeto}.{cuarto_octeto}"


def test_inicio(client):
    response = client.get("/")

    assert response.status_code == 200
    assert (
        response.json()["mensaje"]
        == "NetAdmin API funcionando correctamente"
    )


def test_endpoint_protegido_sin_token(client):
    response = client.get("/dispositivos")

    assert response.status_code == 401
    assert response.json()["detail"] == "Token requerido"


def test_endpoint_con_token_invalido(client):
    response = client.get(
        "/dispositivos",
        headers={
            "Authorization": "Bearer token-invalido"
        }
    )

    assert response.status_code == 401


def test_auth_me(client, admin_headers):
    response = client.get(
        "/auth/me",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()["rol"] == "admin"
    assert "username" in response.json()


def test_usuario_consulta_puede_listar(
    client,
    consulta_headers
):
    response = client.get(
        "/dispositivos",
        headers=consulta_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_usuario_consulta_no_puede_crear(
    client,
    consulta_headers
):
    dispositivo = {
        "ip": generar_ip_prueba(),
        "hostname": "equipo-sin-permiso",
        "mac": "00:11:22:33:44:55",
        "tipo": "switch",
        "sistema": "Cisco IOS",
        "estado": "activo"
    }

    response = client.post(
        "/dispositivos",
        json=dispositivo,
        headers=consulta_headers
    )

    assert response.status_code == 403
    assert (
        response.json()["detail"]
        == "No tienes permisos suficientes"
    )


def test_crud_dispositivo_admin(
    client,
    admin_headers
):
    ip_prueba = generar_ip_prueba()

    dispositivo = {
        "ip": ip_prueba,
        "hostname": "router-test",
        "mac": "00:AA:BB:CC:DD:EE",
        "tipo": "router",
        "sistema": "Cisco IOS",
        "estado": "activo"
    }

    response_crear = client.post(
        "/dispositivos",
        json=dispositivo,
        headers=admin_headers
    )

    assert response_crear.status_code == 201
    assert (
        response_crear.json()["dispositivo"]["ip"]
        == ip_prueba
    )

    response_consultar = client.get(
        f"/dispositivos/{ip_prueba}",
        headers=admin_headers
    )

    assert response_consultar.status_code == 200
    assert response_consultar.json()["ip"] == ip_prueba

    dispositivo_actualizado = {
        "ip": ip_prueba,
        "hostname": "router-actualizado",
        "mac": "00:AA:BB:CC:DD:EE",
        "tipo": "router",
        "sistema": "Cisco IOS XE",
        "estado": "activo"
    }

    response_actualizar = client.put(
        f"/dispositivos/{ip_prueba}",
        json=dispositivo_actualizado,
        headers=admin_headers
    )

    assert response_actualizar.status_code == 200
    assert (
        response_actualizar.json()
        ["dispositivo"]["hostname"]
        == "router-actualizado"
    )

    response_eliminar = client.delete(
        f"/dispositivos/{ip_prueba}",
        headers=admin_headers
    )

    assert response_eliminar.status_code == 200

    response_final = client.get(
        f"/dispositivos/{ip_prueba}",
        headers=admin_headers
    )

    assert response_final.status_code == 404


def test_dispositivo_no_encontrado(
    client,
    admin_headers
):
    response = client.get(
        "/dispositivos/255.255.255.255",
        headers=admin_headers
    )

    assert response.status_code == 404


def test_exportar_inventario(
    client,
    admin_headers
):
    response = client.get(
        "/exportar",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert (
        response.json()["mensaje"]
        == "Inventario exportado correctamente"
    )


def test_historial_admin(
    client,
    admin_headers
):
    response = client.get(
        "/historial",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_comando_red_simulado(
    client,
    admin_headers
):
    datos = {
        "ip": "192.168.163.10",
        "username": "admin",
        "password": "cisco",
        "secret": "class",
        "device_type": "simulador_cisco",
        "comando": "show ip interface brief"
    }

    response = client.post(
        "/red/comando",
        json=datos,
        headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()["ip"] == "192.168.163.10"
    assert "GigabitEthernet0/0" in response.json()["salida"]
def test_configurar_escaneo_automatico_con_token_admin(
    client,
    admin_headers
):
    response = client.post(
        "/escaneo/automatico/configurar",
        json={
            "red": "192.168.163.0/28",
            "intervalo_minutos": 5,
            "activo": False
        },
        headers=admin_headers
    )

    assert response.status_code == 200
    assert (
        response.json()["configuracion"]["red"]
        == "192.168.163.0/28"
    )


def test_estado_escaneo_automatico_con_token(
    client,
    admin_headers
):
    response = client.get(
        "/escaneo/automatico/estado",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert "red" in response.json()


def test_historial_escaneo_automatico_con_token_admin(
    client,
    admin_headers
):
    response = client.get(
        "/escaneo/automatico/historial",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
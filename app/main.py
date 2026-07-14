from fastapi import FastAPI, HTTPException

from app.modelos import Dispositivo, ComandoRed, ComandoLinux
from app.inventario import (
    agregar_dispositivo,
    listar_dispositivos,
    buscar_dispositivo,
    actualizar_dispositivo,
    eliminar_dispositivo,
    listar_historial
)
from app.escaner import escanear_red
from app.exportador import exportar_json, exportar_yaml, exportar_xml
from app.netmiko_admin import ejecutar_comando_red
from app.paramiko_admin import ejecutar_comando_linux
from app.database import init_db


app = FastAPI(
    title="NetAdmin API",
    description="Sistema automatizado de inventario y administración de red",
    version="2.0"
)


@app.on_event("startup")
def iniciar_base_datos():
    init_db()


@app.get("/")
def inicio():
    return {
        "mensaje": "NetAdmin API funcionando correctamente",
        "version": "2.0"
    }


@app.get("/dispositivos")
def obtener_dispositivos():
    return listar_dispositivos()


@app.get("/dispositivos/{ip}")
def obtener_dispositivo(ip: str):
    dispositivo = buscar_dispositivo(ip)

    if dispositivo is None:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return dispositivo


@app.post("/dispositivos", status_code=201)
def crear_dispositivo(dispositivo: Dispositivo):
    existente = buscar_dispositivo(dispositivo.ip)

    if existente:
        raise HTTPException(
            status_code=400,
            detail="La IP ya existe en el inventario"
        )

    nuevo_dispositivo = agregar_dispositivo(dispositivo)

    return {
        "mensaje": "Dispositivo agregado correctamente",
        "dispositivo": nuevo_dispositivo
    }


@app.put("/dispositivos/{ip}")
def modificar_dispositivo(ip: str, dispositivo: Dispositivo):
    actualizado = actualizar_dispositivo(ip, dispositivo)

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return {
        "mensaje": "Dispositivo actualizado correctamente",
        "dispositivo": actualizado
    }


@app.delete("/dispositivos/{ip}")
def borrar_dispositivo(ip: str):
    eliminado = eliminar_dispositivo(ip)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return {
        "mensaje": "Dispositivo eliminado correctamente"
    }


@app.post("/escanear")
def escanear(red: str):
    resultado = escanear_red(red)

    dispositivos_agregados = []

    for dispositivo in resultado:
        existente = buscar_dispositivo(dispositivo["ip"])

        if not existente:
            nuevo_dispositivo = Dispositivo(**dispositivo)
            agregado = agregar_dispositivo(nuevo_dispositivo)
            dispositivos_agregados.append(agregado)

    return {
        "red": red,
        "equipos_detectados": len(resultado),
        "equipos_agregados": len(dispositivos_agregados),
        "dispositivos": resultado
    }


@app.get("/historial")
def obtener_historial():
    return listar_historial()


@app.get("/exportar")
def exportar():
    datos = listar_dispositivos()

    exportar_json(datos)
    exportar_yaml(datos)
    exportar_xml({"dispositivos": datos})

    return {
        "mensaje": "Inventario exportado correctamente",
        "formatos": [
            "JSON",
            "YAML",
            "XML"
        ],
        "archivos": [
            "data/inventario.json",
            "data/inventario.yaml",
            "data/inventario.xml"
        ]
    }


@app.post("/red/comando")
def comando_equipo_red(datos: ComandoRed):
    try:
        salida = ejecutar_comando_red(
            datos.ip,
            datos.username,
            datos.password,
            datos.secret,
            datos.device_type,
            datos.comando
        )

        return {
            "ip": datos.ip,
            "comando": datos.comando,
            "salida": salida
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/linux/comando")
def comando_linux(datos: ComandoLinux):
    try:
        salida = ejecutar_comando_linux(
            datos.ip,
            datos.username,
            datos.password,
            datos.comando
        )

        return {
            "ip": datos.ip,
            "comando": datos.comando,
            "salida": salida
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
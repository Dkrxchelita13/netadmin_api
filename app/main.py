from fastapi import FastAPI, HTTPException, Depends

from app.modelos import (
    Dispositivo,
    ComandoRed,
    ComandoLinux,
    UsuarioRegistro,
    UsuarioLogin
)
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
from app.auth import (
    crear_usuario,
    iniciar_sesion,
    obtener_usuario_actual,
    requiere_admin
)


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


# =========================================================
# AUTENTICACIÓN
# =========================================================

@app.post("/auth/register", status_code=201)
def registrar_usuario(usuario: UsuarioRegistro):
    return crear_usuario(
        username=usuario.username,
        password=usuario.password,
        rol=usuario.rol
    )


@app.post("/auth/login")
def login(usuario: UsuarioLogin):
    return iniciar_sesion(
        username=usuario.username,
        password=usuario.password
    )


@app.get("/auth/me")
def obtener_mi_usuario(
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    return {
        "username": usuario_actual["username"],
        "rol": usuario_actual["rol"]
    }


# =========================================================
# INVENTARIO
# =========================================================

@app.get("/dispositivos")
def obtener_dispositivos(
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    return listar_dispositivos()


@app.get("/dispositivos/{ip}")
def obtener_dispositivo(
    ip: str,
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    dispositivo = buscar_dispositivo(ip)

    if not dispositivo:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return dispositivo


@app.post("/dispositivos", status_code=201)
def crear_dispositivo(
    dispositivo: Dispositivo,
    usuario_actual: dict = Depends(requiere_admin)
):
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
def modificar_dispositivo(
    ip: str,
    dispositivo: Dispositivo,
    usuario_actual: dict = Depends(requiere_admin)
):
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
def borrar_dispositivo(
    ip: str,
    usuario_actual: dict = Depends(requiere_admin)
):
    eliminado = eliminar_dispositivo(ip)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return {
        "mensaje": "Dispositivo eliminado correctamente"
    }


# =========================================================
# ESCANEO
# =========================================================

@app.post("/escanear")
def escanear(
    red: str,
    usuario_actual: dict = Depends(requiere_admin)
):
    resultado = escanear_red(red)

    for dispositivo in resultado:
        existente = buscar_dispositivo(dispositivo["ip"])

        if not existente:
            agregar_dispositivo(dispositivo)

    return {
        "red": red,
        "equipos_detectados": len(resultado),
        "dispositivos": resultado
    }


# =========================================================
# HISTORIAL
# =========================================================

@app.get("/historial")
def obtener_historial(
    usuario_actual: dict = Depends(requiere_admin)
):
    return listar_historial()


# =========================================================
# EXPORTACIÓN
# =========================================================

@app.get("/exportar")
def exportar(
    usuario_actual: dict = Depends(requiere_admin)
):
    datos = listar_dispositivos()

    exportar_json(datos)
    exportar_yaml(datos)
    exportar_xml({"dispositivos": datos})

    return {
        "mensaje": "Inventario exportado correctamente",
        "formatos": ["JSON", "YAML", "XML"],
        "archivos": [
            "data/inventario.json",
            "data/inventario.yaml",
            "data/inventario.xml"
        ]
    }


# =========================================================
# ADMINISTRACIÓN DE EQUIPOS DE RED
# =========================================================

@app.post("/red/comando")
def comando_red(
    datos: ComandoRed,
    usuario_actual: dict = Depends(requiere_admin)
):
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


# =========================================================
# ADMINISTRACIÓN DE EQUIPOS LINUX
# =========================================================

@app.post("/linux/comando")
def comando_linux(
    datos: ComandoLinux,
    usuario_actual: dict = Depends(requiere_admin)
):
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
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.auth import (
    crear_usuario,
    iniciar_sesion,
    obtener_usuario_actual,
    requiere_admin
)
from app.auditoria import (
    listar_auditoria,
    listar_auditoria_por_ip,
    registrar_evento_auditoria
)
from app.database import init_db
from app.dashboard import router as dashboard_router
from app.escaner import escanear_red
from app.escaneo_automatico import (
    configurar_escaneo_automatico,
    ejecutar_escaneo_automatico,
    iniciar_scheduler,
    listar_historial_escaneos,
    obtener_configuracion_escaneo
)
from app.exportador import (
    exportar_json,
    exportar_xml,
    exportar_yaml
)
from app.inventario import (
    actualizar_dispositivo,
    agregar_dispositivo,
    buscar_dispositivo,
    eliminar_dispositivo,
    listar_dispositivos,
    listar_historial
)
from app.modelos import (
    ComandoLinux,
    ComandoRed,
    ConfiguracionEscaneoAutomatico,
    Dispositivo,
    UsuarioLogin,
    UsuarioRegistro
)
from app.netmiko_admin import ejecutar_comando_red
from app.paramiko_admin import ejecutar_comando_linux

from app.reportes_pdf import generar_reporte_pdf
# =========================================================
# INICIO Y CIERRE DE LA APLICACIÓN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    iniciar_scheduler()

    yield


app = FastAPI(
    title="NetAdmin API",
    description="Sistema automatizado de inventario y administración de red",
    version="2.0",
    lifespan=lifespan
)

app.include_router(dashboard_router)


# =========================================================
# ENDPOINT PRINCIPAL
# =========================================================

@app.get("/")
def inicio():
    return {
        "mensaje": "NetAdmin API funcionando correctamente",
        "version": "2.0",
        "dashboard": "/dashboard",
        "documentacion": "/docs"
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

    if dispositivo is None:
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
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="inventario",
            accion="CREAR",
            ip=dispositivo.ip,
            descripcion="Intento de registrar una IP duplicada",
            datos_nuevos=dispositivo.model_dump(),
            resultado="ERROR"
        )

        raise HTTPException(
            status_code=400,
            detail="La IP ya existe en el inventario"
        )

    nuevo_dispositivo = agregar_dispositivo(dispositivo)

    registrar_evento_auditoria(
        usuario=usuario_actual["username"],
        rol=usuario_actual["rol"],
        modulo="inventario",
        accion="CREAR",
        ip=dispositivo.ip,
        descripcion="Dispositivo agregado al inventario",
        datos_nuevos=nuevo_dispositivo,
        resultado="OK"
    )

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
    datos_anteriores = buscar_dispositivo(ip)

    actualizado = actualizar_dispositivo(
        ip,
        dispositivo
    )

    if not actualizado:
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="inventario",
            accion="ACTUALIZAR",
            ip=ip,
            descripcion="Intento de actualizar un dispositivo inexistente",
            datos_nuevos=dispositivo.model_dump(),
            resultado="ERROR"
        )

        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    registrar_evento_auditoria(
        usuario=usuario_actual["username"],
        rol=usuario_actual["rol"],
        modulo="inventario",
        accion="ACTUALIZAR",
        ip=ip,
        descripcion="Dispositivo actualizado correctamente",
        datos_anteriores=datos_anteriores,
        datos_nuevos=actualizado,
        resultado="OK"
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
    datos_anteriores = buscar_dispositivo(ip)

    eliminado = eliminar_dispositivo(ip)

    if not eliminado:
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="inventario",
            accion="ELIMINAR",
            ip=ip,
            descripcion="Intento de eliminar un dispositivo inexistente",
            resultado="ERROR"
        )

        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    registrar_evento_auditoria(
        usuario=usuario_actual["username"],
        rol=usuario_actual["rol"],
        modulo="inventario",
        accion="ELIMINAR",
        ip=ip,
        descripcion="Dispositivo eliminado del inventario",
        datos_anteriores=datos_anteriores,
        resultado="OK"
    )

    return {
        "mensaje": "Dispositivo eliminado correctamente"
    }


# =========================================================
# ESCANEO MANUAL
# =========================================================

@app.post("/escanear")
def escanear(
    red: str,
    usuario_actual: dict = Depends(requiere_admin)
):
    try:
        resultado = escanear_red(red)
        dispositivos_agregados = []

        for dispositivo in resultado:
            existente = buscar_dispositivo(
                dispositivo["ip"]
            )

            if not existente:
                nuevo_dispositivo = Dispositivo(
                    **dispositivo
                )

                agregado = agregar_dispositivo(
                    nuevo_dispositivo
                )

                dispositivos_agregados.append(
                    agregado
                )

        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="escaneo",
            accion="ESCANEAR_RED",
            descripcion=f"Escaneo manual ejecutado sobre la red {red}",
            datos_nuevos={
                "red": red,
                "equipos_detectados": len(resultado),
                "equipos_agregados": len(dispositivos_agregados)
            },
            resultado="OK"
        )

        return {
            "red": red,
            "equipos_detectados": len(resultado),
            "equipos_agregados": len(dispositivos_agregados),
            "dispositivos": resultado
        }

    except Exception as error:
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="escaneo",
            accion="ESCANEAR_RED",
            descripcion=str(error),
            datos_nuevos={
                "red": red
            },
            resultado="ERROR"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# ESCANEO AUTOMÁTICO
# =========================================================

@app.post("/escaneo/automatico/configurar")
def configurar_escaneo(
    configuracion: ConfiguracionEscaneoAutomatico,
    usuario_actual: dict = Depends(requiere_admin)
):
    try:
        resultado = configurar_escaneo_automatico(
            red=configuracion.red,
            intervalo_minutos=configuracion.intervalo_minutos,
            activo=configuracion.activo
        )

        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="escaneo_automatico",
            accion="CONFIGURAR",
            descripcion="Configuración de escaneo automático actualizada",
            datos_nuevos=configuracion.model_dump(),
            resultado="OK"
        )

        return resultado

    except ValueError as error:
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="escaneo_automatico",
            accion="CONFIGURAR",
            descripcion=str(error),
            datos_nuevos=configuracion.model_dump(),
            resultado="ERROR"
        )

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.get("/escaneo/automatico/estado")
def estado_escaneo_automatico(
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    return obtener_configuracion_escaneo()


@app.post("/escaneo/automatico/ejecutar")
def ejecutar_escaneo_manual_automatico(
    usuario_actual: dict = Depends(requiere_admin)
):
    try:
        resultado = ejecutar_escaneo_automatico()

        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="escaneo_automatico",
            accion="EJECUTAR",
            descripcion="Escaneo automático ejecutado manualmente",
            datos_nuevos=resultado,
            resultado="OK"
        )

        return resultado

    except Exception as error:
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="escaneo_automatico",
            accion="EJECUTAR",
            descripcion=str(error),
            resultado="ERROR"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/escaneo/automatico/historial")
def historial_escaneo_automatico(
    usuario_actual: dict = Depends(requiere_admin)
):
    return listar_historial_escaneos()


# =========================================================
# HISTORIAL Y AUDITORÍA
# =========================================================

@app.get("/historial")
def obtener_historial(
    usuario_actual: dict = Depends(requiere_admin)
):
    return listar_historial()


@app.get("/auditoria")
def obtener_auditoria(
    usuario_actual: dict = Depends(requiere_admin)
):
    return listar_auditoria()


@app.get("/auditoria/{ip}")
def obtener_auditoria_por_ip(
    ip: str,
    usuario_actual: dict = Depends(requiere_admin)
):
    return listar_auditoria_por_ip(ip)

@app.get("/reporte/pdf")
def descargar_reporte_pdf(usuario_actual: dict = Depends(requiere_admin)):
    try:
        ruta_pdf = generar_reporte_pdf()

        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="reportes",
            accion="GENERAR_PDF",
            descripcion="Reporte PDF generado automaticamente desde la API",
            datos_nuevos={
                "archivo": ruta_pdf
            },
            resultado="OK"
        )

        return FileResponse(
            path=ruta_pdf,
            media_type="application/pdf",
            filename="reporte_netadmin.pdf"
        )

    except Exception as error:
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="reportes",
            accion="GENERAR_PDF",
            descripcion=str(error),
            resultado="ERROR"
        )

        raise HTTPException(status_code=500, detail=str(error))
# =========================================================
# EXPORTACIÓN
# =========================================================

@app.get("/exportar")
def exportar(
    usuario_actual: dict = Depends(requiere_admin)
):
    try:
        datos = listar_dispositivos()

        exportar_json(datos)
        exportar_yaml(datos)
        exportar_xml({
            "dispositivos": datos
        })

        archivos = [
            "data/inventario.json",
            "data/inventario.yaml",
            "data/inventario.xml"
        ]

        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="exportacion",
            accion="EXPORTAR",
            descripcion="Inventario exportado en JSON, YAML y XML",
            datos_nuevos={
                "formatos": [
                    "JSON",
                    "YAML",
                    "XML"
                ],
                "archivos": archivos
            },
            resultado="OK"
        )

        return {
            "mensaje": "Inventario exportado correctamente",
            "formatos": [
                "JSON",
                "YAML",
                "XML"
            ],
            "archivos": archivos
        }

    except Exception as error:
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="exportacion",
            accion="EXPORTAR",
            descripcion=str(error),
            resultado="ERROR"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


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

        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="netmiko",
            accion="EJECUTAR_COMANDO",
            ip=datos.ip,
            descripcion=f"Comando ejecutado: {datos.comando}",
            datos_nuevos={
                "device_type": datos.device_type,
                "comando": datos.comando
            },
            resultado="OK"
        )

        return {
            "ip": datos.ip,
            "comando": datos.comando,
            "salida": salida
        }

    except Exception as error:
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="netmiko",
            accion="EJECUTAR_COMANDO",
            ip=datos.ip,
            descripcion=str(error),
            datos_nuevos={
                "device_type": datos.device_type,
                "comando": datos.comando
            },
            resultado="ERROR"
        )

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

        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="paramiko",
            accion="EJECUTAR_COMANDO",
            ip=datos.ip,
            descripcion=f"Comando ejecutado: {datos.comando}",
            datos_nuevos={
                "comando": datos.comando
            },
            resultado="OK"
        )

        return {
            "ip": datos.ip,
            "comando": datos.comando,
            "salida": salida
        }

    except Exception as error:
        registrar_evento_auditoria(
            usuario=usuario_actual["username"],
            rol=usuario_actual["rol"],
            modulo="paramiko",
            accion="EJECUTAR_COMANDO",
            ip=datos.ip,
            descripcion=str(error),
            datos_nuevos={
                "comando": datos.comando
            },
            resultado="ERROR"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
import threading
import time
from datetime import datetime, timedelta

from app.database import get_connection
from app.escaner import escanear_red
from app.inventario import agregar_dispositivo, buscar_dispositivo
from app.modelos import Dispositivo


_scheduler_iniciado = False


def fecha_actual():
    return datetime.now().isoformat(sep=" ", timespec="seconds")


def convertir_activo(valor):
    return bool(valor)


def obtener_configuracion_escaneo():
    with get_connection() as connection:
        fila = connection.execute(
            """
            SELECT id, red, intervalo_minutos, activo, ultima_ejecucion, proxima_ejecucion
            FROM configuracion_escaneo
            WHERE id = 1
            """
        ).fetchone()

    configuracion = dict(fila)
    configuracion["activo"] = convertir_activo(configuracion["activo"])

    return configuracion


def actualizar_proxima_ejecucion(intervalo_minutos):
    return (datetime.now() + timedelta(minutes=intervalo_minutos)).isoformat(
        sep=" ",
        timespec="seconds"
    )


def configurar_escaneo_automatico(red, intervalo_minutos, activo):
    if intervalo_minutos < 1:
        raise ValueError("El intervalo debe ser mínimo de 1 minuto.")

    proxima_ejecucion = actualizar_proxima_ejecucion(intervalo_minutos) if activo else None

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE configuracion_escaneo
            SET red = ?,
                intervalo_minutos = ?,
                activo = ?,
                proxima_ejecucion = ?
            WHERE id = 1
            """,
            (
                red,
                intervalo_minutos,
                1 if activo else 0,
                proxima_ejecucion,
            ),
        )
        connection.commit()

    return {
        "mensaje": "Configuración de escaneo automático actualizada",
        "configuracion": obtener_configuracion_escaneo()
    }


def registrar_historial_escaneo(red, equipos_detectados, nuevos_agregados, estado, detalle=None):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO historial_escaneos (
                red,
                equipos_detectados,
                nuevos_agregados,
                estado,
                detalle,
                fecha
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                red,
                equipos_detectados,
                nuevos_agregados,
                estado,
                detalle,
                fecha_actual(),
            ),
        )
        connection.commit()


def listar_historial_escaneos():
    with get_connection() as connection:
        filas = connection.execute(
            """
            SELECT id, red, equipos_detectados, nuevos_agregados, estado, detalle, fecha
            FROM historial_escaneos
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(fila) for fila in filas]


def ejecutar_escaneo_automatico():
    configuracion = obtener_configuracion_escaneo()
    red = configuracion["red"]
    intervalo_minutos = configuracion["intervalo_minutos"]

    try:
        dispositivos_detectados = escanear_red(red)
        nuevos_agregados = 0

        for dispositivo in dispositivos_detectados:
            existente = buscar_dispositivo(dispositivo["ip"])

            if not existente:
                agregar_dispositivo(Dispositivo(**dispositivo))
                nuevos_agregados += 1

        ultima_ejecucion = fecha_actual()
        proxima_ejecucion = actualizar_proxima_ejecucion(intervalo_minutos)

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE configuracion_escaneo
                SET ultima_ejecucion = ?,
                    proxima_ejecucion = ?
                WHERE id = 1
                """,
                (
                    ultima_ejecucion,
                    proxima_ejecucion,
                ),
            )
            connection.commit()

        registrar_historial_escaneo(
            red=red,
            equipos_detectados=len(dispositivos_detectados),
            nuevos_agregados=nuevos_agregados,
            estado="OK",
            detalle="Escaneo ejecutado correctamente"
        )

        return {
            "mensaje": "Escaneo automático ejecutado correctamente",
            "red": red,
            "equipos_detectados": len(dispositivos_detectados),
            "nuevos_agregados": nuevos_agregados,
            "dispositivos": dispositivos_detectados
        }

    except Exception as error:
        registrar_historial_escaneo(
            red=red,
            equipos_detectados=0,
            nuevos_agregados=0,
            estado="ERROR",
            detalle=str(error)
        )

        raise error


def ciclo_scheduler():
    while True:
        try:
            configuracion = obtener_configuracion_escaneo()

            if configuracion["activo"]:
                proxima = configuracion["proxima_ejecucion"]

                if not proxima:
                    ejecutar_escaneo_automatico()

                else:
                    proxima_fecha = datetime.fromisoformat(proxima)

                    if datetime.now() >= proxima_fecha:
                        ejecutar_escaneo_automatico()

        except Exception:
            pass

        time.sleep(10)


def iniciar_scheduler():
    global _scheduler_iniciado

    if _scheduler_iniciado:
        return

    hilo = threading.Thread(target=ciclo_scheduler, daemon=True)
    hilo.start()

    _scheduler_iniciado = True
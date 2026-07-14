import json
from app.database import get_connection


def convertir_a_diccionario(dispositivo):
    if hasattr(dispositivo, "model_dump"):
        return dispositivo.model_dump()

    if hasattr(dispositivo, "dict"):
        return dispositivo.dict()

    return dict(dispositivo)


def registrar_historial(accion, ip, datos_anteriores=None, datos_nuevos=None):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO historial_cambios (
                accion,
                ip,
                datos_anteriores,
                datos_nuevos
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                accion,
                ip,
                json.dumps(datos_anteriores, ensure_ascii=False) if datos_anteriores else None,
                json.dumps(datos_nuevos, ensure_ascii=False) if datos_nuevos else None,
            ),
        )
        connection.commit()


def agregar_dispositivo(dispositivo):
    datos = convertir_a_diccionario(dispositivo)

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO dispositivos (
                ip,
                hostname,
                mac,
                tipo,
                sistema,
                estado
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datos["ip"],
                datos.get("hostname", "desconocido"),
                datos.get("mac", "desconocida"),
                datos.get("tipo", "desconocido"),
                datos.get("sistema", "desconocido"),
                datos.get("estado", "activo"),
            ),
        )
        connection.commit()

    registrar_historial("CREAR", datos["ip"], None, datos)

    return datos


def listar_dispositivos():
    with get_connection() as connection:
        filas = connection.execute(
            """
            SELECT ip, hostname, mac, tipo, sistema, estado
            FROM dispositivos
            ORDER BY ip
            """
        ).fetchall()

    return [dict(fila) for fila in filas]


def buscar_dispositivo(ip):
    with get_connection() as connection:
        fila = connection.execute(
            """
            SELECT ip, hostname, mac, tipo, sistema, estado
            FROM dispositivos
            WHERE ip = ?
            """,
            (ip,),
        ).fetchone()

    if fila:
        return dict(fila)

    return None


def actualizar_dispositivo(ip, dispositivo):
    datos_nuevos = convertir_a_diccionario(dispositivo)
    datos_anteriores = buscar_dispositivo(ip)

    if not datos_anteriores:
        return None

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE dispositivos
            SET hostname = ?,
                mac = ?,
                tipo = ?,
                sistema = ?,
                estado = ?
            WHERE ip = ?
            """,
            (
                datos_nuevos.get("hostname", "desconocido"),
                datos_nuevos.get("mac", "desconocida"),
                datos_nuevos.get("tipo", "desconocido"),
                datos_nuevos.get("sistema", "desconocido"),
                datos_nuevos.get("estado", "activo"),
                ip,
            ),
        )
        connection.commit()

    dispositivo_actualizado = buscar_dispositivo(ip)
    registrar_historial("ACTUALIZAR", ip, datos_anteriores, dispositivo_actualizado)

    return dispositivo_actualizado


def eliminar_dispositivo(ip):
    datos_anteriores = buscar_dispositivo(ip)

    if not datos_anteriores:
        return False

    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM dispositivos
            WHERE ip = ?
            """,
            (ip,),
        )
        connection.commit()

    registrar_historial("ELIMINAR", ip, datos_anteriores, None)

    return True


def listar_historial():
    with get_connection() as connection:
        filas = connection.execute(
            """
            SELECT id, accion, ip, datos_anteriores, datos_nuevos, fecha
            FROM historial_cambios
            ORDER BY id DESC
            """
        ).fetchall()

    historial = []

    for fila in filas:
        registro = dict(fila)

        if registro["datos_anteriores"]:
            registro["datos_anteriores"] = json.loads(registro["datos_anteriores"])

        if registro["datos_nuevos"]:
            registro["datos_nuevos"] = json.loads(registro["datos_nuevos"])

        historial.append(registro)

    return historial
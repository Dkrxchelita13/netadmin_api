import json

from app.database import get_connection


def convertir_json(datos):
    if datos is None:
        return None

    return json.dumps(datos, ensure_ascii=False)


def registrar_evento_auditoria(
    usuario: str | None,
    rol: str | None,
    modulo: str,
    accion: str,
    resultado: str,
    ip: str | None = None,
    descripcion: str | None = None,
    datos_anteriores=None,
    datos_nuevos=None
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO auditoria_eventos (
                usuario,
                rol,
                modulo,
                accion,
                ip,
                descripcion,
                datos_anteriores,
                datos_nuevos,
                resultado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                usuario,
                rol,
                modulo,
                accion,
                ip,
                descripcion,
                convertir_json(datos_anteriores),
                convertir_json(datos_nuevos),
                resultado
            )
        )
        connection.commit()


def listar_auditoria():
    with get_connection() as connection:
        filas = connection.execute(
            """
            SELECT id, usuario, rol, modulo, accion, ip, descripcion,
                   datos_anteriores, datos_nuevos, resultado, fecha
            FROM auditoria_eventos
            ORDER BY id DESC
            """
        ).fetchall()

    eventos = []

    for fila in filas:
        evento = dict(fila)

        if evento["datos_anteriores"]:
            evento["datos_anteriores"] = json.loads(evento["datos_anteriores"])

        if evento["datos_nuevos"]:
            evento["datos_nuevos"] = json.loads(evento["datos_nuevos"])

        eventos.append(evento)

    return eventos


def listar_auditoria_por_ip(ip: str):
    with get_connection() as connection:
        filas = connection.execute(
            """
            SELECT id, usuario, rol, modulo, accion, ip, descripcion,
                   datos_anteriores, datos_nuevos, resultado, fecha
            FROM auditoria_eventos
            WHERE ip = ?
            ORDER BY id DESC
            """,
            (ip,)
        ).fetchall()

    eventos = []

    for fila in filas:
        evento = dict(fila)

        if evento["datos_anteriores"]:
            evento["datos_anteriores"] = json.loads(evento["datos_anteriores"])

        if evento["datos_nuevos"]:
            evento["datos_nuevos"] = json.loads(evento["datos_nuevos"])

        eventos.append(evento)

    return eventos
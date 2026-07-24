import difflib
import hashlib
import re

from app.database import get_connection


def sanitizar_configuracion(configuracion: str) -> str:
    """
    Oculta valores sensibles antes de guardar o mostrar configuraciones.
    """
    lineas_sanitizadas = []

    for linea in configuracion.splitlines():
        linea = re.sub(r"(password\s+)(.+)", r"\1********", linea, flags=re.IGNORECASE)
        linea = re.sub(r"(secret\s+)(.+)", r"\1********", linea, flags=re.IGNORECASE)
        linea = re.sub(r"(community\s+)(.+)", r"\1********", linea, flags=re.IGNORECASE)
        linea = re.sub(r"(key\s+)(.+)", r"\1********", linea, flags=re.IGNORECASE)

        lineas_sanitizadas.append(linea)

    return "\n".join(lineas_sanitizadas)


def calcular_hash(configuracion: str) -> str:
    return hashlib.sha256(configuracion.encode("utf-8")).hexdigest()


def guardar_configuracion(
    ip: str,
    comando: str,
    configuracion: str,
    usuario: str | None = None,
    rol: str | None = None
):
    configuracion_limpia = sanitizar_configuracion(configuracion)
    hash_configuracion = calcular_hash(configuracion_limpia)

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO configuraciones_dispositivos (
                ip,
                comando,
                configuracion,
                hash_sha256,
                usuario,
                rol
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ip,
                comando,
                configuracion_limpia,
                hash_configuracion,
                usuario,
                rol,
            ),
        )
        connection.commit()

        configuracion_id = cursor.lastrowid

    return obtener_configuracion_por_id(configuracion_id)


def obtener_configuracion_por_id(configuracion_id: int):
    with get_connection() as connection:
        fila = connection.execute(
            """
            SELECT id, ip, comando, configuracion, hash_sha256, usuario, rol, fecha
            FROM configuraciones_dispositivos
            WHERE id = ?
            """,
            (configuracion_id,),
        ).fetchone()

    if not fila:
        return None

    return dict(fila)


def listar_configuraciones_por_ip(ip: str):
    with get_connection() as connection:
        filas = connection.execute(
            """
            SELECT id, ip, comando, hash_sha256, usuario, rol, fecha
            FROM configuraciones_dispositivos
            WHERE ip = ?
            ORDER BY id DESC
            """,
            (ip,),
        ).fetchall()

    return [dict(fila) for fila in filas]


def obtener_ultimas_dos_configuraciones(ip: str):
    with get_connection() as connection:
        filas = connection.execute(
            """
            SELECT id, ip, comando, configuracion, hash_sha256, usuario, rol, fecha
            FROM configuraciones_dispositivos
            WHERE ip = ?
            ORDER BY id DESC
            LIMIT 2
            """,
            (ip,),
        ).fetchall()

    configuraciones = [dict(fila) for fila in filas]

    if len(configuraciones) < 2:
        return None, None

    actual = configuraciones[0]
    anterior = configuraciones[1]

    return anterior, actual


def comparar_textos_configuracion(config_anterior: str, config_actual: str):
    lineas_anteriores = config_anterior.splitlines()
    lineas_actuales = config_actual.splitlines()

    diff = list(
        difflib.unified_diff(
            lineas_anteriores,
            lineas_actuales,
            fromfile="configuracion_anterior",
            tofile="configuracion_actual",
            lineterm=""
        )
    )

    lineas_agregadas = [
        linea for linea in diff
        if linea.startswith("+") and not linea.startswith("+++")
    ]

    lineas_eliminadas = [
        linea for linea in diff
        if linea.startswith("-") and not linea.startswith("---")
    ]

    return {
        "hay_cambios": len(lineas_agregadas) > 0 or len(lineas_eliminadas) > 0,
        "lineas_agregadas": lineas_agregadas,
        "lineas_eliminadas": lineas_eliminadas,
        "diff": diff
    }


def comparar_ultimas_configuraciones(ip: str):
    anterior, actual = obtener_ultimas_dos_configuraciones(ip)

    if not anterior or not actual:
        return None

    comparacion = comparar_textos_configuracion(
        anterior["configuracion"],
        actual["configuracion"]
    )

    return {
        "ip": ip,
        "configuracion_anterior": {
            "id": anterior["id"],
            "fecha": anterior["fecha"],
            "hash_sha256": anterior["hash_sha256"],
            "comando": anterior["comando"]
        },
        "configuracion_actual": {
            "id": actual["id"],
            "fecha": actual["fecha"],
            "hash_sha256": actual["hash_sha256"],
            "comando": actual["comando"]
        },
        "hay_cambios": comparacion["hay_cambios"],
        "lineas_agregadas": comparacion["lineas_agregadas"],
        "lineas_eliminadas": comparacion["lineas_eliminadas"],
        "diff": comparacion["diff"]
    }
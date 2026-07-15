import hashlib
import secrets
import sqlite3

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database import get_connection


ROLES_VALIDOS = {"admin", "consulta"}

seguridad_bearer = HTTPBearer(auto_error=False)


def generar_hash_password(
    password: str,
    salt: str | None = None
):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        100000
    ).hex()

    return salt, password_hash


def verificar_password(
    password: str,
    salt: str,
    password_hash: str
) -> bool:
    _, hash_calculado = generar_hash_password(
        password,
        salt
    )

    return secrets.compare_digest(
        hash_calculado,
        password_hash
    )


def crear_usuario(
    username: str,
    password: str,
    rol: str = "consulta"
):
    username = username.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario es obligatorio"
        )

    if not password:
        raise HTTPException(
            status_code=400,
            detail="La contraseña es obligatoria"
        )

    if rol not in ROLES_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail="Rol no válido. Usa admin o consulta."
        )

    salt, password_hash = generar_hash_password(password)
    token = secrets.token_urlsafe(32)

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO usuarios (
                    username,
                    password_hash,
                    salt,
                    rol,
                    token
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    username,
                    password_hash,
                    salt,
                    rol,
                    token
                )
            )

            connection.commit()

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    return {
        "mensaje": "Usuario registrado correctamente",
        "username": username,
        "rol": rol,
        "access_token": token,
        "token_type": "bearer"
    }


def iniciar_sesion(
    username: str,
    password: str
):
    with get_connection() as connection:
        usuario = connection.execute(
            """
            SELECT
                id,
                username,
                password_hash,
                salt,
                rol
            FROM usuarios
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    usuario = dict(usuario)

    password_correcta = verificar_password(
        password,
        usuario["salt"],
        usuario["password_hash"]
    )

    if not password_correcta:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    nuevo_token = secrets.token_urlsafe(32)

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE usuarios
            SET token = ?
            WHERE id = ?
            """,
            (
                nuevo_token,
                usuario["id"]
            )
        )

        connection.commit()

    return {
        "mensaje": "Inicio de sesión correcto",
        "username": usuario["username"],
        "rol": usuario["rol"],
        "access_token": nuevo_token,
        "token_type": "bearer"
    }


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(
        seguridad_bearer
    )
):
    if credenciales is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token requerido",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if credenciales.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de token inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = credenciales.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token requerido",
            headers={"WWW-Authenticate": "Bearer"}
        )

    with get_connection() as connection:
        usuario = connection.execute(
            """
            SELECT
                id,
                username,
                rol,
                token
            FROM usuarios
            WHERE token = ?
            """,
            (token,)
        ).fetchone()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return dict(usuario)


def requiere_admin(
    usuario_actual: dict = Depends(
        obtener_usuario_actual
    )
):
    if usuario_actual["rol"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes"
        )

    return usuario_actual
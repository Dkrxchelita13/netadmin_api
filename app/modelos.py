from typing import Optional

from pydantic import BaseModel


class Dispositivo(BaseModel):
    ip: str
    hostname: Optional[str] = "desconocido"
    mac: Optional[str] = "desconocida"
    tipo: Optional[str] = "desconocido"
    sistema: Optional[str] = "desconocido"
    estado: Optional[str] = "activo"


class ComandoRed(BaseModel):
    ip: str
    username: str
    password: str
    secret: Optional[str] = ""
    device_type: str = "cisco_ios"
    comando: str


class ComandoLinux(BaseModel):
    ip: str
    username: str
    password: str
    comando: str


class UsuarioRegistro(BaseModel):
    username: str
    password: str
    rol: str = "consulta"


class UsuarioLogin(BaseModel):
    username: str
    password: str


class ConfiguracionEscaneoAutomatico(BaseModel):
    red: str = "192.168.163.0/28"
    intervalo_minutos: int = 30
    activo: bool = True


class CapturaConfiguracion(BaseModel):
    ip: str
    username: str
    password: str
    secret: Optional[str] = ""
    device_type: str = "simulador_cisco"
    comando: str = "show running-config"


class AlertaPrueba(BaseModel):
    asunto: str = "Prueba de alerta NetAdmin API"
    mensaje: str = (
        "Esta es una alerta de prueba generada "
        "desde NetAdmin API."
    )
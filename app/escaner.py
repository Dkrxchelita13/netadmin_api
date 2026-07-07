import ipaddress
import platform
import subprocess
import socket


def hacer_ping(ip: str) -> bool:
    sistema = platform.system().lower()

    if sistema == "windows":
        comando = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        comando = ["ping", "-c", "1", "-W", "1", ip]

    resultado = subprocess.run(
        comando,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return resultado.returncode == 0


def obtener_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "desconocido"


def clasificar_dispositivo(ip: str, hostname: str) -> str:
    hostname_lower = hostname.lower()

    if ip.endswith(".1"):
        return "router"
    elif "printer" in hostname_lower or "impresora" in hostname_lower:
        return "impresora"
    elif "ap" in hostname_lower or "access" in hostname_lower:
        return "AP"
    elif "server" in hostname_lower or "srv" in hostname_lower:
        return "servidor"
    elif "switch" in hostname_lower or "sw" in hostname_lower:
        return "switch"
    else:
        return "desconocido"


def escanear_red(red: str):
    dispositivos = []
    red_objeto = ipaddress.ip_network(red, strict=False)

    for ip in red_objeto.hosts():
        ip_texto = str(ip)

        if hacer_ping(ip_texto):
            hostname = obtener_hostname(ip_texto)
            tipo = clasificar_dispositivo(ip_texto, hostname)

            dispositivos.append({
                "ip": ip_texto,
                "hostname": hostname,
                "mac": "pendiente",
                "tipo": tipo,
                "sistema": "desconocido",
                "estado": "activo"
            })

    return dispositivos
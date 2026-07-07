from netmiko import ConnectHandler


def ejecutar_comando_red(ip, username, password, secret, device_type, comando):
    dispositivo = {
        "device_type": device_type,
        "host": ip,
        "username": username,
        "password": password,
        "secret": secret
    }

    conexion = ConnectHandler(**dispositivo)

    if secret:
        conexion.enable()

    salida = conexion.send_command(comando)
    conexion.disconnect()

    return salida
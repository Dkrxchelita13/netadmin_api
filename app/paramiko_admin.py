import paramiko


def ejecutar_comando_linux(ip, username, password, comando):
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    cliente.connect(
        hostname=ip,
        username=username,
        password=password,
        timeout=10
    )

    stdin, stdout, stderr = cliente.exec_command(comando)

    salida = stdout.read().decode()
    error = stderr.read().decode()

    cliente.close()

    if error:
        return error

    return salida
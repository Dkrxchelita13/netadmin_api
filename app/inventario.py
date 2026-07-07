inventario = []


def agregar_dispositivo(dispositivo):
    inventario.append(dispositivo)
    return dispositivo


def listar_dispositivos():
    return inventario


def buscar_dispositivo(ip):
    for dispositivo in inventario:
        if dispositivo["ip"] == ip:
            return dispositivo
    return None


def actualizar_dispositivo(ip, nuevos_datos):
    for index, dispositivo in enumerate(inventario):
        if dispositivo["ip"] == ip:
            inventario[index].update(nuevos_datos)
            return inventario[index]
    return None


def eliminar_dispositivo(ip):
    for dispositivo in inventario:
        if dispositivo["ip"] == ip:
            inventario.remove(dispositivo)
            return True
    return False
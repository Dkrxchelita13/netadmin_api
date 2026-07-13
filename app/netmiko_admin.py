from netmiko import ConnectHandler


def salida_switch_simulado(comando: str) -> str:
    comando = comando.strip().lower()

    if comando == "show ip interface brief":
        return """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.163.10  YES manual up                    up
GigabitEthernet0/1     unassigned      YES unset  administratively down down
Vlan1                  192.168.163.10  YES manual up                    up
"""

    if comando == "show version":
        return """
Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 15.2(2)E
Switch uptime is 2 hours, 15 minutes
System image file is "flash:c2960-lanbasek9-mz.152-2.E.bin"
Processor board ID FOC1234X0YZ
"""

    if comando == "show vlan brief":
        return """
VLAN Name                             Status    Ports
1    default                          active    Gi0/1, Gi0/2
10   Administracion                   active    Gi0/3
20   Usuarios                         active    Gi0/4
"""

    if comando == "show interfaces status":
        return """
Port      Name               Status       Vlan       Duplex  Speed Type
Gi0/1     Uplink             connected    trunk      a-full  a-1000 10/100/1000BaseTX
Gi0/2     PC-Admin           connected    10         a-full  a-100  10/100/1000BaseTX
Gi0/3     Usuario-1          connected    20         a-full  a-100  10/100/1000BaseTX
Gi0/4                        notconnect   20         auto    auto   10/100/1000BaseTX
"""

    if comando == "show running-config":
        return """
hostname SW-NETADMIN
!
interface vlan 1
 ip address 192.168.163.10 255.255.255.0
 no shutdown
!
username admin privilege 15 secret cisco
!
line vty 0 4
 login local
 transport input ssh
!
end
"""

    return f"Comando simulado no reconocido: {comando}"


def ejecutar_comando_red(ip, username, password, secret, device_type, comando):
    """
    Si device_type es 'simulador_cisco', se devuelve una salida simulada.
    Si device_type es 'cisco_ios', se intenta conexión real con Netmiko.
    """

    if device_type.lower() in ["simulador_cisco", "cisco_simulado"]:
        return salida_switch_simulado(comando)

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
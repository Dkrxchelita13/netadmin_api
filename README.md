# NetAdmin API

Sistema de inventario, monitoreo y administración básica de red desarrollado en Python con FastAPI.

## Objetivo

Desarrollar una API REST que permita registrar dispositivos de red, escanear una red local, administrar un inventario y exportar la información en formatos JSON, YAML y XML.

## Tecnologías utilizadas

- Python 3.12
- FastAPI
- Uvicorn
- PyYAML
- dicttoxml
- Netmiko
- Paramiko
- Pytest
- Postman
- Git y GitHub

## Estructura del proyecto

```txt
netadmin_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── modelos.py
│   ├── inventario.py
│   ├── escaner.py
│   ├── exportador.py
│   ├── netmiko_admin.py
│   └── paramiko_admin.py
│
├── data/
│   ├── inventario.json
│   ├── inventario.yaml
│   └── inventario.xml
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
├── README.md
└── .gitignore
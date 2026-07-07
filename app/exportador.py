import json
import os
import yaml
from dicttoxml import dicttoxml


def asegurar_carpeta_data():
    os.makedirs("data", exist_ok=True)


def exportar_json(datos, ruta="data/inventario.json"):
    asegurar_carpeta_data()

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def exportar_yaml(datos, ruta="data/inventario.yaml"):
    asegurar_carpeta_data()

    with open(ruta, "w", encoding="utf-8") as archivo:
        yaml.dump(datos, archivo, allow_unicode=True, sort_keys=False)


def exportar_xml(datos, ruta="data/inventario.xml"):
    asegurar_carpeta_data()

    xml = dicttoxml(datos, custom_root="inventario", attr_type=False)

    with open(ruta, "wb") as archivo:
        archivo.write(xml)
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from app.database import get_connection
from app.inventario import listar_dispositivos, listar_historial
from app.auditoria import listar_auditoria


BASE_DIR = Path(__file__).resolve().parent.parent
REPORTES_DIR = BASE_DIR / "data" / "reportes"


def consultar_tabla(query: str, parametros=()):
    try:
        with get_connection() as connection:
            filas = connection.execute(query, parametros).fetchall()

        return [dict(fila) for fila in filas]

    except Exception:
        return []


def obtener_historial_escaneos():
    return consultar_tabla(
        """
        SELECT id, red, equipos_detectados, nuevos_agregados, estado, fecha
        FROM historial_escaneos
        ORDER BY id DESC
        LIMIT 10
        """
    )


def obtener_configuraciones():
    return consultar_tabla(
        """
        SELECT id, ip, comando, hash_sha256, usuario, fecha
        FROM configuraciones_dispositivos
        ORDER BY id DESC
        LIMIT 10
        """
    )


def crear_tabla_pdf(encabezados, filas):
    datos = [encabezados]

    if not filas:
        datos.append(["Sin registros"] + [""] * (len(encabezados) - 1))
    else:
        datos.extend(filas)

    tabla = Table(datos, repeatRows=1)

    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12355b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
            ]
        )
    )

    return tabla


def agregar_titulo(elementos, texto, estilos):
    elementos.append(Paragraph(texto, estilos["Heading2"]))
    elementos.append(Spacer(1, 8))


def agregar_parrafo(elementos, texto, estilos):
    elementos.append(Paragraph(texto, estilos["BodyText"]))
    elementos.append(Spacer(1, 8))


def generar_reporte_pdf():
    REPORTES_DIR.mkdir(parents=True, exist_ok=True)

    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ruta_pdf = REPORTES_DIR / f"reporte_netadmin_{fecha_actual}.pdf"

    documento = SimpleDocTemplate(
        str(ruta_pdf),
        pagesize=letter,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("NetAdmin API", estilos["Title"]))
    elementos.append(Paragraph("Reporte automatico de inventario, monitoreo y administracion de red", estilos["Heading2"]))
    elementos.append(Spacer(1, 12))

    agregar_parrafo(
        elementos,
        f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        estilos
    )

    agregar_parrafo(
        elementos,
        "Este reporte fue generado automaticamente desde la API. Incluye informacion del inventario, historial de cambios, auditoria del sistema, escaneos automaticos y configuraciones capturadas.",
        estilos
    )

    dispositivos = listar_dispositivos()
    historial = listar_historial()
    auditoria = listar_auditoria()
    escaneos = obtener_historial_escaneos()
    configuraciones = obtener_configuraciones()

    total_dispositivos = len(dispositivos)
    total_activos = len([d for d in dispositivos if d.get("estado") == "activo"])
    total_routers = len([d for d in dispositivos if d.get("tipo", "").lower() == "router"])
    total_switches = len([d for d in dispositivos if d.get("tipo", "").lower() == "switch"])

    agregar_titulo(elementos, "1. Resumen general", estilos)

    resumen = [
        ["Indicador", "Valor"],
        ["Total de dispositivos", str(total_dispositivos)],
        ["Dispositivos activos", str(total_activos)],
        ["Routers", str(total_routers)],
        ["Switches", str(total_switches)],
        ["Eventos de auditoria", str(len(auditoria))],
        ["Escaneos registrados", str(len(escaneos))],
        ["Configuraciones capturadas", str(len(configuraciones))]
    ]

    tabla_resumen = Table(resumen)
    tabla_resumen.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12355b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]
        )
    )

    elementos.append(tabla_resumen)
    elementos.append(Spacer(1, 14))

    agregar_titulo(elementos, "2. Inventario de dispositivos", estilos)

    filas_dispositivos = [
        [
            d.get("ip", ""),
            d.get("hostname", ""),
            d.get("mac", ""),
            d.get("tipo", ""),
            d.get("sistema", ""),
            d.get("estado", "")
        ]
        for d in dispositivos[:20]
    ]

    elementos.append(
        crear_tabla_pdf(
            ["IP", "Hostname", "MAC", "Tipo", "Sistema", "Estado"],
            filas_dispositivos
        )
    )
    elementos.append(Spacer(1, 14))

    agregar_titulo(elementos, "3. Historial de cambios del inventario", estilos)

    filas_historial = [
        [
            str(h.get("id", "")),
            h.get("accion", ""),
            h.get("ip", ""),
            h.get("fecha", "")
        ]
        for h in historial[:10]
    ]

    elementos.append(
        crear_tabla_pdf(
            ["ID", "Accion", "IP", "Fecha"],
            filas_historial
        )
    )
    elementos.append(Spacer(1, 14))

    agregar_titulo(elementos, "4. Auditoria del sistema", estilos)

    filas_auditoria = [
        [
            str(a.get("id", "")),
            str(a.get("usuario", "")),
            str(a.get("modulo", "")),
            str(a.get("accion", "")),
            str(a.get("ip", "")),
            str(a.get("resultado", "")),
            str(a.get("fecha", ""))
        ]
        for a in auditoria[:10]
    ]

    elementos.append(
        crear_tabla_pdf(
            ["ID", "Usuario", "Modulo", "Accion", "IP", "Resultado", "Fecha"],
            filas_auditoria
        )
    )
    elementos.append(Spacer(1, 14))

    agregar_titulo(elementos, "5. Historial de escaneos automaticos", estilos)

    filas_escaneos = [
        [
            str(e.get("id", "")),
            e.get("red", ""),
            str(e.get("equipos_detectados", "")),
            str(e.get("nuevos_agregados", "")),
            e.get("estado", ""),
            e.get("fecha", "")
        ]
        for e in escaneos
    ]

    elementos.append(
        crear_tabla_pdf(
            ["ID", "Red", "Detectados", "Nuevos", "Estado", "Fecha"],
            filas_escaneos
        )
    )
    elementos.append(Spacer(1, 14))

    agregar_titulo(elementos, "6. Configuraciones capturadas", estilos)

    filas_configuraciones = [
        [
            str(c.get("id", "")),
            c.get("ip", ""),
            c.get("comando", ""),
            c.get("hash_sha256", "")[:16] + "...",
            str(c.get("usuario", "")),
            c.get("fecha", "")
        ]
        for c in configuraciones
    ]

    elementos.append(
        crear_tabla_pdf(
            ["ID", "IP", "Comando", "Hash SHA-256", "Usuario", "Fecha"],
            filas_configuraciones
        )
    )
    elementos.append(Spacer(1, 14))

    agregar_titulo(elementos, "7. Conclusiones del reporte", estilos)

    agregar_parrafo(
        elementos,
        "El sistema NetAdmin API cuenta con almacenamiento en SQLite, autenticacion por token, dashboard web, escaneo automatico, historial de cambios, auditoria, comparacion de configuraciones y generacion automatica de reportes PDF. Estas mejoras fortalecen el producto y permiten consultar informacion relevante del inventario de red de forma estructurada.",
        estilos
    )

    documento.build(elementos)

    return str(ruta_pdf)
from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(
    tags=["dashboard"]
)


@router.get("/dashboard", response_class=HTMLResponse)
def mostrar_dashboard():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>NetAdmin | Dashboard</title>

    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --primary-light: #eff6ff;
            --sidebar: #0f172a;
            --sidebar-hover: #1e293b;
            --background: #f1f5f9;
            --surface: #ffffff;
            --text: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --success: #16a34a;
            --success-bg: #f0fdf4;
            --warning: #d97706;
            --warning-bg: #fffbeb;
            --danger: #dc2626;
            --danger-bg: #fef2f2;
            --shadow: 0 8px 30px rgba(15, 23, 42, 0.08);
            --radius: 16px;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family:
                Inter,
                "Segoe UI",
                Arial,
                sans-serif;
            background: var(--background);
            color: var(--text);
        }

        button,
        input {
            font: inherit;
        }

        button {
            cursor: pointer;
        }

        /* =====================================================
           PANTALLA DE INICIO DE SESIÓN
        ===================================================== */

        .login-screen {
            min-height: 100vh;
            display: grid;
            grid-template-columns: 1.05fr 0.95fr;
            background: var(--surface);
        }

        .login-presentation {
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 55px;
            color: white;
            background:
                radial-gradient(
                    circle at top right,
                    rgba(59, 130, 246, 0.45),
                    transparent 38%
                ),
                linear-gradient(
                    145deg,
                    #0f172a 0%,
                    #172554 48%,
                    #1d4ed8 100%
                );
        }

        .login-presentation::after {
            content: "";
            position: absolute;
            width: 420px;
            height: 420px;
            right: -140px;
            bottom: -150px;
            border: 70px solid rgba(255, 255, 255, 0.05);
            border-radius: 50%;
        }

        .login-brand {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .brand-symbol {
            width: 46px;
            height: 46px;
            display: grid;
            place-items: center;
            flex-shrink: 0;
            border-radius: 14px;
            font-size: 20px;
            font-weight: 800;
            color: white;
            background: var(--primary);
            box-shadow: 0 10px 25px rgba(37, 99, 235, 0.35);
        }

        .login-brand strong {
            display: block;
            font-size: 20px;
        }

        .login-brand span {
            display: block;
            margin-top: 3px;
            font-size: 13px;
            color: #cbd5e1;
        }

        .presentation-content {
            position: relative;
            z-index: 1;
            max-width: 600px;
        }

        .presentation-content h1 {
            margin: 0 0 20px;
            font-size: clamp(38px, 5vw, 65px);
            line-height: 1.03;
            letter-spacing: -2px;
        }

        .presentation-content p {
            max-width: 530px;
            margin: 0;
            font-size: 18px;
            line-height: 1.7;
            color: #dbeafe;
        }

        .presentation-features {
            position: relative;
            z-index: 1;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }

        .feature-chip {
            padding: 10px 15px;
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 999px;
            font-size: 13px;
            color: #e2e8f0;
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(8px);
        }

        .login-panel {
            display: grid;
            place-items: center;
            padding: 35px;
            background: #f8fafc;
        }

        .login-card {
            width: min(440px, 100%);
            padding: 38px;
            border: 1px solid var(--border);
            border-radius: 24px;
            background: var(--surface);
            box-shadow: var(--shadow);
        }

        .login-card h2 {
            margin: 0 0 8px;
            font-size: 30px;
            letter-spacing: -0.7px;
        }

        .login-card > p {
            margin: 0 0 30px;
            line-height: 1.6;
            color: var(--text-muted);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
            font-weight: 650;
        }

        .form-control {
            width: 100%;
            height: 48px;
            padding: 0 14px;
            border: 1px solid var(--border);
            border-radius: 11px;
            outline: none;
            color: var(--text);
            background: white;
            transition: 0.2s ease;
        }

        .form-control:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
        }

        .btn {
            min-height: 44px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 0 18px;
            border: none;
            border-radius: 10px;
            font-weight: 700;
            transition:
                transform 0.15s ease,
                background 0.2s ease,
                opacity 0.2s ease;
        }

        .btn:hover {
            transform: translateY(-1px);
        }

        .btn:disabled {
            cursor: not-allowed;
            opacity: 0.6;
            transform: none;
        }

        .btn-primary {
            color: white;
            background: var(--primary);
        }

        .btn-primary:hover {
            background: var(--primary-dark);
        }

        .btn-secondary {
            color: var(--text);
            border: 1px solid var(--border);
            background: white;
        }

        .btn-secondary:hover {
            background: #f8fafc;
        }

        .btn-danger {
            color: var(--danger);
            border: 1px solid #fecaca;
            background: var(--danger-bg);
        }

        .btn-block {
            width: 100%;
        }

        /* =====================================================
           MENSAJES
        ===================================================== */

        .alert {
            display: none;
            align-items: flex-start;
            gap: 10px;
            margin-top: 18px;
            padding: 13px 15px;
            border: 1px solid transparent;
            border-radius: 11px;
            font-size: 14px;
            line-height: 1.5;
        }

        .alert.visible {
            display: flex;
        }

        .alert-success {
            color: #166534;
            border-color: #bbf7d0;
            background: var(--success-bg);
        }

        .alert-error {
            color: #991b1b;
            border-color: #fecaca;
            background: var(--danger-bg);
        }

        .alert-info {
            color: #1e40af;
            border-color: #bfdbfe;
            background: var(--primary-light);
        }

        /* =====================================================
           ESTRUCTURA PRINCIPAL
        ===================================================== */

        .app-shell {
            min-height: 100vh;
            display: none;
        }

        .app-shell.visible {
            display: grid;
            grid-template-columns: 260px minmax(0, 1fr);
        }

        .sidebar {
            position: fixed;
            inset: 0 auto 0 0;
            width: 260px;
            display: flex;
            flex-direction: column;
            padding: 24px 18px;
            color: white;
            background: var(--sidebar);
            z-index: 20;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 2px 8px 26px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.09);
        }

        .sidebar-brand strong {
            display: block;
            font-size: 18px;
        }

        .sidebar-brand span {
            display: block;
            margin-top: 3px;
            font-size: 12px;
            color: #94a3b8;
        }

        .nav-label {
            margin: 28px 10px 10px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1.4px;
            color: #64748b;
            text-transform: uppercase;
        }

        .sidebar-nav {
            display: flex;
            flex-direction: column;
            gap: 7px;
        }

        .nav-button {
            width: 100%;
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 13px;
            border: none;
            border-radius: 10px;
            text-align: left;
            color: #cbd5e1;
            background: transparent;
            transition: 0.2s ease;
        }

        .nav-button:hover {
            color: white;
            background: var(--sidebar-hover);
        }

        .nav-button.active {
            color: white;
            background: var(--primary);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
        }

        .nav-icon {
            width: 24px;
            text-align: center;
            font-size: 17px;
        }

        .sidebar-footer {
            margin-top: auto;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.09);
        }

        .user-card {
            padding: 13px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.06);
        }

        .user-card strong {
            display: block;
            font-size: 14px;
        }

        .user-card span {
            display: block;
            margin-top: 4px;
            font-size: 12px;
            color: #94a3b8;
            text-transform: capitalize;
        }

        .logout-button {
            width: 100%;
            margin-top: 10px;
            padding: 10px 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 9px;
            color: #cbd5e1;
            background: transparent;
        }

        .logout-button:hover {
            color: white;
            background: rgba(255, 255, 255, 0.08);
        }

        .main-area {
            grid-column: 2;
            min-width: 0;
        }

        .topbar {
            position: sticky;
            top: 0;
            z-index: 10;
            height: 76px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            padding: 0 32px;
            border-bottom: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(12px);
        }

        .topbar-title h1 {
            margin: 0;
            font-size: 21px;
            letter-spacing: -0.4px;
        }

        .topbar-title p {
            margin: 4px 0 0;
            font-size: 13px;
            color: var(--text-muted);
        }

        .api-status {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border: 1px solid #bbf7d0;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            color: #166534;
            background: var(--success-bg);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 0 4px rgba(22, 163, 74, 0.12);
        }

        .content {
            padding: 30px 32px 50px;
        }

        .view {
            display: none;
            animation: fadeIn 0.22s ease;
        }

        .view.active {
            display: block;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(4px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .page-heading {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 25px;
        }

        .page-heading h2 {
            margin: 0;
            font-size: 27px;
            letter-spacing: -0.6px;
        }

        .page-heading p {
            margin: 7px 0 0;
            color: var(--text-muted);
        }

        .action-group {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        /* =====================================================
           MÉTRICAS
        ===================================================== */

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 18px;
            margin-bottom: 22px;
        }

        .metric-card {
            position: relative;
            overflow: hidden;
            padding: 22px;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        }

        .metric-card::after {
            content: "";
            position: absolute;
            width: 90px;
            height: 90px;
            right: -32px;
            top: -35px;
            border-radius: 50%;
            background: var(--primary-light);
        }

        .metric-header {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
        }

        .metric-icon {
            width: 42px;
            height: 42px;
            display: grid;
            place-items: center;
            border-radius: 12px;
            font-weight: 800;
            color: var(--primary);
            background: var(--primary-light);
        }

        .metric-value {
            position: relative;
            z-index: 1;
            margin: 0;
            font-size: 35px;
            line-height: 1;
            letter-spacing: -1px;
        }

        .metric-label {
            position: relative;
            z-index: 1;
            margin: 8px 0 0;
            font-size: 13px;
            color: var(--text-muted);
        }

        /* =====================================================
           TARJETAS Y TABLAS
        ===================================================== */

        .dashboard-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.5fr) minmax(280px, 0.7fr);
            gap: 20px;
        }

        .card {
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04);
        }

        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 20px 22px;
            border-bottom: 1px solid var(--border);
        }

        .card-header h3 {
            margin: 0;
            font-size: 16px;
        }

        .card-header p {
            margin: 5px 0 0;
            font-size: 13px;
            color: var(--text-muted);
        }

        .card-body {
            padding: 22px;
        }

        .table-wrapper {
            width: 100%;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            white-space: nowrap;
        }

        th {
            padding: 13px 15px;
            border-bottom: 1px solid var(--border);
            text-align: left;
            font-size: 11px;
            letter-spacing: 0.6px;
            color: var(--text-muted);
            background: #f8fafc;
            text-transform: uppercase;
        }

        td {
            padding: 14px 15px;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
            color: #334155;
        }

        tbody tr:last-child td {
            border-bottom: none;
        }

        tbody tr:hover {
            background: #f8fafc;
        }

        .empty-state {
            padding: 38px 20px;
            text-align: center;
            color: var(--text-muted);
        }

        .empty-state strong {
            display: block;
            margin-bottom: 7px;
            color: var(--text);
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 9px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 750;
            text-transform: capitalize;
        }

        .badge-success {
            color: #166534;
            background: #dcfce7;
        }

        .badge-muted {
            color: #475569;
            background: #e2e8f0;
        }

        .badge-info {
            color: #1e40af;
            background: #dbeafe;
        }

        .badge-warning {
            color: #92400e;
            background: #fef3c7;
        }

        .badge-danger {
            color: #991b1b;
            background: #fee2e2;
        }

        .quick-actions {
            display: grid;
            gap: 12px;
        }

        .quick-action {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 15px;
            border: 1px solid var(--border);
            border-radius: 12px;
            color: var(--text);
            text-align: left;
            background: white;
            transition: 0.2s ease;
        }

        .quick-action:hover {
            border-color: #bfdbfe;
            background: var(--primary-light);
            transform: translateY(-1px);
        }

        .quick-action-icon {
            width: 40px;
            height: 40px;
            display: grid;
            place-items: center;
            flex-shrink: 0;
            border-radius: 11px;
            color: var(--primary);
            background: var(--primary-light);
        }

        .quick-action strong {
            display: block;
            margin-bottom: 3px;
            font-size: 13px;
        }

        .quick-action span {
            display: block;
            font-size: 11px;
            color: var(--text-muted);
        }

        .toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 18px;
        }

        .search-box {
            position: relative;
            width: min(360px, 100%);
        }

        .search-box input {
            width: 100%;
            height: 42px;
            padding: 0 14px 0 39px;
            border: 1px solid var(--border);
            border-radius: 10px;
            outline: none;
        }

        .search-box input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        .search-symbol {
            position: absolute;
            top: 50%;
            left: 14px;
            color: var(--text-muted);
            transform: translateY(-50%);
        }

        .export-panel {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 330px;
            gap: 22px;
        }

        .export-formats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }

        .format-card {
            padding: 25px 18px;
            border: 1px solid var(--border);
            border-radius: 14px;
            text-align: center;
            background: #f8fafc;
        }

        .format-icon {
            width: 52px;
            height: 52px;
            display: grid;
            place-items: center;
            margin: 0 auto 13px;
            border-radius: 14px;
            font-weight: 800;
            color: var(--primary);
            background: var(--primary-light);
        }

        .format-card strong {
            display: block;
            margin-bottom: 5px;
        }

        .format-card span {
            font-size: 12px;
            color: var(--text-muted);
        }

        .info-list {
            display: grid;
            gap: 15px;
        }

        .info-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
            padding-bottom: 13px;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
        }

        .info-row:last-child {
            padding-bottom: 0;
            border-bottom: none;
        }

        .info-row span:first-child {
            color: var(--text-muted);
        }

        .info-row strong {
            text-align: right;
        }

        .hidden {
            display: none !important;
        }

        /* =====================================================
           RESPONSIVE
        ===================================================== */

        @media (max-width: 1100px) {
            .metrics-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .dashboard-grid,
            .export-panel {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 820px) {
            .login-screen {
                grid-template-columns: 1fr;
            }

            .login-presentation {
                display: none;
            }

            .app-shell.visible {
                display: block;
            }

            .sidebar {
                position: static;
                width: 100%;
                padding: 16px;
            }

            .sidebar-brand {
                padding-bottom: 16px;
            }

            .nav-label {
                display: none;
            }

            .sidebar-nav {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                margin-top: 15px;
            }

            .nav-button {
                justify-content: center;
                padding: 10px;
            }

            .nav-button span:last-child {
                display: none;
            }

            .sidebar-footer {
                display: none;
            }

            .main-area {
                grid-column: auto;
            }

            .topbar {
                height: auto;
                padding: 17px 20px;
            }

            .content {
                padding: 22px 18px 40px;
            }
        }

        @media (max-width: 600px) {
            .metrics-grid {
                grid-template-columns: 1fr;
            }

            .export-formats {
                grid-template-columns: 1fr;
            }

            .page-heading {
                flex-direction: column;
            }

            .action-group {
                width: 100%;
            }

            .action-group .btn {
                flex: 1;
            }

            .api-status {
                display: none;
            }
        }
    </style>
</head>

<body>

<!-- =====================================================
     INICIO DE SESIÓN
===================================================== -->

<section id="loginScreen" class="login-screen">

    <div class="login-presentation">

        <div class="login-brand">
            <div class="brand-symbol">NA</div>

            <div>
                <strong>NetAdmin</strong>
                <span>Network Administration Platform</span>
            </div>
        </div>

        <div class="presentation-content">
            <h1>Administración de red en un solo lugar.</h1>

            <p>
                Consulta el inventario, supervisa los cambios y administra
                la información de tus dispositivos desde una interfaz segura
                y centralizada.
            </p>
        </div>

        <div class="presentation-features">
            <span class="feature-chip">Inventario centralizado</span>
            <span class="feature-chip">Autenticación Bearer</span>
            <span class="feature-chip">Historial de cambios</span>
            <span class="feature-chip">Exportación multiformato</span>
        </div>

    </div>

    <div class="login-panel">

        <form id="loginForm" class="login-card">

            <h2>Bienvenido</h2>

            <p>
                Ingresa tus credenciales para acceder al panel de
                administración.
            </p>

            <div class="form-group">
                <label for="username">Usuario</label>

                <input
                    class="form-control"
                    type="text"
                    id="username"
                    placeholder="Ingresa tu usuario"
                    autocomplete="username"
                    required
                >
            </div>

            <div class="form-group">
                <label for="password">Contraseña</label>

                <input
                    class="form-control"
                    type="password"
                    id="password"
                    placeholder="Ingresa tu contraseña"
                    autocomplete="current-password"
                    required
                >
            </div>

            <button
                id="loginButton"
                type="submit"
                class="btn btn-primary btn-block"
            >
                Iniciar sesión
            </button>

            <div id="loginAlert" class="alert"></div>

        </form>

    </div>

</section>


<!-- =====================================================
     APLICACIÓN
===================================================== -->

<div id="appShell" class="app-shell">

    <aside class="sidebar">

        <div class="sidebar-brand">
            <div class="brand-symbol">NA</div>

            <div>
                <strong>NetAdmin</strong>
                <span>Panel de administración</span>
            </div>
        </div>

        <div class="nav-label">Menú principal</div>

        <nav class="sidebar-nav">

            <button
                class="nav-button active"
                data-view="resumen"
                onclick="cambiarVista('resumen', this)"
            >
                <span class="nav-icon">▦</span>
                <span>Resumen</span>
            </button>

            <button
                class="nav-button"
                data-view="inventario"
                onclick="cambiarVista('inventario', this)"
            >
                <span class="nav-icon">◫</span>
                <span>Inventario</span>
            </button>

            <button
                class="nav-button admin-only"
                data-view="historial"
                onclick="cambiarVista('historial', this)"
            >
                <span class="nav-icon">↻</span>
                <span>Historial</span>
            </button>

            <button
                class="nav-button admin-only"
                data-view="exportacion"
                onclick="cambiarVista('exportacion', this)"
            >
                <span class="nav-icon">⇩</span>
                <span>Exportación</span>
            </button>

        </nav>

        <div class="sidebar-footer">

            <div class="user-card">
                <strong id="sidebarUsername">Usuario</strong>
                <span id="sidebarRole">Rol</span>
            </div>

            <button
                class="logout-button"
                onclick="cerrarSesion()"
            >
                Cerrar sesión
            </button>

        </div>

    </aside>


    <main class="main-area">

        <header class="topbar">

            <div class="topbar-title">
                <h1 id="topbarTitle">Resumen general</h1>
                <p id="topbarSubtitle">
                    Estado actual de la infraestructura registrada
                </p>
            </div>

            <div class="api-status">
                <span class="status-dot"></span>
                API conectada
            </div>

        </header>


        <div class="content">

            <div id="globalAlert" class="alert"></div>


            <!-- =============================================
                 VISTA: RESUMEN
            ============================================== -->

            <section id="view-resumen" class="view active">

                <div class="page-heading">

                    <div>
                        <h2>Resumen de infraestructura</h2>
                        <p>
                            Métricas generales del inventario de red.
                        </p>
                    </div>

                    <div class="action-group">
                        <button
                            class="btn btn-primary"
                            onclick="cargarResumen()"
                        >
                            Actualizar información
                        </button>
                    </div>

                </div>


                <div class="metrics-grid">

                    <article class="metric-card">
                        <div class="metric-header">
                            <div class="metric-icon">01</div>
                        </div>

                        <h3 id="totalDispositivos" class="metric-value">0</h3>
                        <p class="metric-label">Dispositivos registrados</p>
                    </article>

                    <article class="metric-card">
                        <div class="metric-header">
                            <div class="metric-icon">02</div>
                        </div>

                        <h3 id="totalActivos" class="metric-value">0</h3>
                        <p class="metric-label">Dispositivos activos</p>
                    </article>

                    <article class="metric-card">
                        <div class="metric-header">
                            <div class="metric-icon">03</div>
                        </div>

                        <h3 id="totalRouters" class="metric-value">0</h3>
                        <p class="metric-label">Routers identificados</p>
                    </article>

                    <article class="metric-card">
                        <div class="metric-header">
                            <div class="metric-icon">04</div>
                        </div>

                        <h3 id="totalSwitches" class="metric-value">0</h3>
                        <p class="metric-label">Switches identificados</p>
                    </article>

                </div>


                <div class="dashboard-grid">

                    <article class="card">

                        <div class="card-header">
                            <div>
                                <h3>Dispositivos recientes</h3>
                                <p>
                                    Últimos elementos consultados del inventario.
                                </p>
                            </div>

                            <button
                                class="btn btn-secondary"
                                onclick="cambiarVistaPorNombre('inventario')"
                            >
                                Ver inventario
                            </button>
                        </div>

                        <div class="table-wrapper">

                            <table>
                                <thead>
                                    <tr>
                                        <th>Dirección IP</th>
                                        <th>Hostname</th>
                                        <th>Tipo</th>
                                        <th>Estado</th>
                                    </tr>
                                </thead>

                                <tbody id="tablaResumen">
                                    <tr>
                                        <td colspan="4">
                                            <div class="empty-state">
                                                <strong>Sin información</strong>
                                                Actualiza el resumen para cargar
                                                el inventario.
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>

                        </div>

                    </article>


                    <article class="card">

                        <div class="card-header">
                            <div>
                                <h3>Acciones rápidas</h3>
                                <p>
                                    Accesos a las funciones principales.
                                </p>
                            </div>
                        </div>

                        <div class="card-body">

                            <div class="quick-actions">

                                <button
                                    class="quick-action"
                                    onclick="cambiarVistaPorNombre('inventario')"
                                >
                                    <span class="quick-action-icon">◫</span>

                                    <span>
                                        <strong>Consultar inventario</strong>
                                        <span>
                                            Visualizar todos los dispositivos
                                        </span>
                                    </span>
                                </button>

                                <button
                                    class="quick-action admin-only"
                                    onclick="cambiarVistaPorNombre('historial')"
                                >
                                    <span class="quick-action-icon">↻</span>

                                    <span>
                                        <strong>Revisar historial</strong>
                                        <span>
                                            Consultar cambios registrados
                                        </span>
                                    </span>
                                </button>

                                <button
                                    class="quick-action admin-only"
                                    onclick="cambiarVistaPorNombre('exportacion')"
                                >
                                    <span class="quick-action-icon">⇩</span>

                                    <span>
                                        <strong>Exportar datos</strong>
                                        <span>
                                            Generar archivos JSON, YAML y XML
                                        </span>
                                    </span>
                                </button>

                            </div>

                        </div>

                    </article>

                </div>

            </section>


            <!-- =============================================
                 VISTA: INVENTARIO
            ============================================== -->

            <section id="view-inventario" class="view">

                <div class="page-heading">

                    <div>
                        <h2>Inventario de dispositivos</h2>
                        <p>
                            Consulta de equipos registrados en la base de datos.
                        </p>
                    </div>

                    <div class="action-group">
                        <button
                            class="btn btn-primary"
                            onclick="cargarInventario()"
                        >
                            Actualizar inventario
                        </button>
                    </div>

                </div>


                <article class="card">

                    <div class="card-body">

                        <div class="toolbar">

                            <div class="search-box">
                                <span class="search-symbol">⌕</span>

                                <input
                                    type="text"
                                    id="buscarDispositivo"
                                    placeholder="Buscar por IP, hostname o tipo..."
                                    oninput="filtrarInventario()"
                                >
                            </div>

                            <span id="contadorInventario" class="badge badge-info">
                                0 dispositivos
                            </span>

                        </div>


                        <div class="table-wrapper">

                            <table>
                                <thead>
                                    <tr>
                                        <th>Dirección IP</th>
                                        <th>Hostname</th>
                                        <th>MAC</th>
                                        <th>Tipo</th>
                                        <th>Sistema</th>
                                        <th>Estado</th>
                                    </tr>
                                </thead>

                                <tbody id="tablaInventario">
                                    <tr>
                                        <td colspan="6">
                                            <div class="empty-state">
                                                <strong>
                                                    Inventario no cargado
                                                </strong>
                                                Presiona “Actualizar inventario”.
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>

                        </div>

                    </div>

                </article>

            </section>


            <!-- =============================================
                 VISTA: HISTORIAL
            ============================================== -->

            <section id="view-historial" class="view">

                <div class="page-heading">

                    <div>
                        <h2>Historial de cambios</h2>
                        <p>
                            Registro de altas, modificaciones y eliminaciones.
                        </p>
                    </div>

                    <div class="action-group">
                        <button
                            class="btn btn-primary"
                            onclick="cargarHistorial()"
                        >
                            Actualizar historial
                        </button>
                    </div>

                </div>


                <article class="card">

                    <div class="card-body">

                        <div class="toolbar">

                            <div class="search-box">
                                <span class="search-symbol">⌕</span>

                                <input
                                    type="text"
                                    id="buscarHistorial"
                                    placeholder="Buscar por acción o dirección IP..."
                                    oninput="filtrarHistorial()"
                                >
                            </div>

                            <span id="contadorHistorial" class="badge badge-info">
                                0 registros
                            </span>

                        </div>


                        <div class="table-wrapper">

                            <table>
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Acción</th>
                                        <th>Dirección IP</th>
                                        <th>Fecha</th>
                                    </tr>
                                </thead>

                                <tbody id="tablaHistorial">
                                    <tr>
                                        <td colspan="4">
                                            <div class="empty-state">
                                                <strong>
                                                    Historial no cargado
                                                </strong>
                                                Presiona “Actualizar historial”.
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>

                        </div>

                    </div>

                </article>

            </section>


            <!-- =============================================
                 VISTA: EXPORTACIÓN
            ============================================== -->

            <section id="view-exportacion" class="view">

                <div class="page-heading">

                    <div>
                        <h2>Exportación de inventario</h2>
                        <p>
                            Genera respaldos del inventario en distintos
                            formatos.
                        </p>
                    </div>

                </div>


                <div class="export-panel">

                    <article class="card">

                        <div class="card-header">
                            <div>
                                <h3>Formatos disponibles</h3>
                                <p>
                                    La operación genera los tres archivos
                                    simultáneamente.
                                </p>
                            </div>
                        </div>

                        <div class="card-body">

                            <div class="export-formats">

                                <div class="format-card">
                                    <div class="format-icon">{ }</div>
                                    <strong>JSON</strong>
                                    <span>Intercambio estructurado</span>
                                </div>

                                <div class="format-card">
                                    <div class="format-icon">YML</div>
                                    <strong>YAML</strong>
                                    <span>Configuración legible</span>
                                </div>

                                <div class="format-card">
                                    <div class="format-icon">&lt;/&gt;</div>
                                    <strong>XML</strong>
                                    <span>Compatibilidad empresarial</span>
                                </div>

                            </div>

                            <button
                                id="exportButton"
                                class="btn btn-primary btn-block"
                                style="margin-top: 22px;"
                                onclick="exportarInventario()"
                            >
                                Generar archivos de exportación
                            </button>

                        </div>

                    </article>


                    <article class="card">

                        <div class="card-header">
                            <div>
                                <h3>Detalles de exportación</h3>
                                <p>Ubicación de los archivos generados.</p>
                            </div>
                        </div>

                        <div class="card-body">

                            <div class="info-list">

                                <div class="info-row">
                                    <span>Archivo JSON</span>
                                    <strong>data/inventario.json</strong>
                                </div>

                                <div class="info-row">
                                    <span>Archivo YAML</span>
                                    <strong>data/inventario.yaml</strong>
                                </div>

                                <div class="info-row">
                                    <span>Archivo XML</span>
                                    <strong>data/inventario.xml</strong>
                                </div>

                                <div class="info-row">
                                    <span>Última operación</span>
                                    <strong id="ultimaExportacion">
                                        Sin ejecutar
                                    </strong>
                                </div>

                            </div>

                        </div>

                    </article>

                </div>

            </section>

        </div>

    </main>

</div>


<script>
    let dispositivos = [];
    let historial = [];
    let usuarioActual = null;


    function obtenerToken() {
        return localStorage.getItem("netadmin_token");
    }


    function escaparHTML(valor) {
        if (valor === null || valor === undefined) {
            return "";
        }

        return String(valor)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }


    function mostrarAlerta(id, mensaje, tipo = "info") {
        const alerta = document.getElementById(id);

        alerta.textContent = mensaje;
        alerta.className = "alert visible alert-" + tipo;
    }


    function ocultarAlerta(id) {
        const alerta = document.getElementById(id);

        alerta.textContent = "";
        alerta.className = "alert";
    }


    function mostrarAplicacion(usuario) {
        usuarioActual = usuario;

        document.getElementById("loginScreen").classList.add("hidden");
        document.getElementById("appShell").classList.add("visible");

        document.getElementById("sidebarUsername").textContent =
            usuario.username;

        document.getElementById("sidebarRole").textContent =
            usuario.rol;

        const elementosAdmin = document.querySelectorAll(".admin-only");

        elementosAdmin.forEach(elemento => {
            elemento.classList.toggle(
                "hidden",
                usuario.rol !== "admin"
            );
        });

        cambiarVistaPorNombre("resumen");
        cargarResumen();
    }


    function mostrarLogin() {
        document.getElementById("appShell").classList.remove("visible");
        document.getElementById("loginScreen").classList.remove("hidden");
    }


    async function solicitarConToken(url, opciones = {}) {
        const token = obtenerToken();

        if (!token) {
            cerrarSesion();
            throw new Error("Debes iniciar sesión.");
        }

        const configuracion = {
            ...opciones,
            headers: {
                ...(opciones.headers || {}),
                "Authorization": "Bearer " + token
            }
        };

        const response = await fetch(url, configuracion);

        let data = {};

        try {
            data = await response.json();
        } catch (error) {
            data = {};
        }

        if (response.status === 401) {
            cerrarSesion();
            throw new Error(
                data.detail || "La sesión ha expirado."
            );
        }

        if (!response.ok) {
            throw new Error(
                data.detail || "No fue posible completar la operación."
            );
        }

        return data;
    }


    async function iniciarSesion(evento) {
        evento.preventDefault();

        ocultarAlerta("loginAlert");

        const username = document
            .getElementById("username")
            .value
            .trim();

        const password = document
            .getElementById("password")
            .value;

        if (!username || !password) {
            mostrarAlerta(
                "loginAlert",
                "Ingresa tu usuario y contraseña.",
                "error"
            );
            return;
        }

        const boton = document.getElementById("loginButton");
        boton.disabled = true;
        boton.textContent = "Verificando...";

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Credenciales inválidas."
                );
            }

            localStorage.setItem(
                "netadmin_token",
                data.access_token
            );

            mostrarAplicacion({
                username: data.username,
                rol: data.rol
            });

            document.getElementById("password").value = "";

        } catch (error) {
            mostrarAlerta(
                "loginAlert",
                error.message || "Error de conexión con la API.",
                "error"
            );

        } finally {
            boton.disabled = false;
            boton.textContent = "Iniciar sesión";
        }
    }


    async function restaurarSesion() {
        const token = obtenerToken();

        if (!token) {
            mostrarLogin();
            return;
        }

        try {
            const usuario = await solicitarConToken("/auth/me");

            mostrarAplicacion(usuario);

        } catch (error) {
            localStorage.removeItem("netadmin_token");
            mostrarLogin();
        }
    }


    function cerrarSesion() {
        localStorage.removeItem("netadmin_token");

        usuarioActual = null;
        dispositivos = [];
        historial = [];

        mostrarLogin();

        document.getElementById("username").focus();
    }


    function cambiarVista(nombre, boton) {
        document.querySelectorAll(".view").forEach(vista => {
            vista.classList.remove("active");
        });

        document.querySelectorAll(".nav-button").forEach(elemento => {
            elemento.classList.remove("active");
        });

        const vista = document.getElementById("view-" + nombre);

        if (vista) {
            vista.classList.add("active");
        }

        if (boton) {
            boton.classList.add("active");
        }

        actualizarTitulo(nombre);

        if (nombre === "inventario" && dispositivos.length === 0) {
            cargarInventario();
        }

        if (
            nombre === "historial" &&
            historial.length === 0 &&
            usuarioActual?.rol === "admin"
        ) {
            cargarHistorial();
        }
    }


    function cambiarVistaPorNombre(nombre) {
        const boton = document.querySelector(
            '.nav-button[data-view="' + nombre + '"]'
        );

        cambiarVista(nombre, boton);
    }


    function actualizarTitulo(nombre) {
        const titulos = {
            resumen: {
                titulo: "Resumen general",
                subtitulo:
                    "Estado actual de la infraestructura registrada"
            },
            inventario: {
                titulo: "Inventario",
                subtitulo:
                    "Consulta de dispositivos almacenados"
            },
            historial: {
                titulo: "Historial de cambios",
                subtitulo:
                    "Trazabilidad de operaciones realizadas"
            },
            exportacion: {
                titulo: "Exportación",
                subtitulo:
                    "Generación de archivos de respaldo"
            }
        };

        const datos = titulos[nombre] || titulos.resumen;

        document.getElementById("topbarTitle").textContent =
            datos.titulo;

        document.getElementById("topbarSubtitle").textContent =
            datos.subtitulo;
    }


    async function cargarResumen() {
        ocultarAlerta("globalAlert");

        try {
            dispositivos = await solicitarConToken("/dispositivos");

            actualizarMetricas();
            renderizarResumen();
            renderizarInventario(dispositivos);

        } catch (error) {
            mostrarAlerta(
                "globalAlert",
                error.message,
                "error"
            );
        }
    }


    async function cargarInventario() {
        ocultarAlerta("globalAlert");

        try {
            dispositivos = await solicitarConToken("/dispositivos");

            actualizarMetricas();
            renderizarInventario(dispositivos);
            renderizarResumen();

            mostrarAlerta(
                "globalAlert",
                "Inventario actualizado correctamente.",
                "success"
            );

        } catch (error) {
            mostrarAlerta(
                "globalAlert",
                error.message,
                "error"
            );
        }
    }


    function actualizarMetricas() {
        let activos = 0;
        let routers = 0;
        let switches = 0;

        dispositivos.forEach(dispositivo => {
            const estado = String(
                dispositivo.estado || ""
            ).toLowerCase();

            const tipo = String(
                dispositivo.tipo || ""
            ).toLowerCase();

            if (estado === "activo") {
                activos++;
            }

            if (tipo === "router") {
                routers++;
            }

            if (tipo === "switch") {
                switches++;
            }
        });

        document.getElementById("totalDispositivos").textContent =
            dispositivos.length;

        document.getElementById("totalActivos").textContent =
            activos;

        document.getElementById("totalRouters").textContent =
            routers;

        document.getElementById("totalSwitches").textContent =
            switches;
    }


    function renderizarResumen() {
        const tabla = document.getElementById("tablaResumen");
        tabla.innerHTML = "";

        if (dispositivos.length === 0) {
            tabla.innerHTML = `
                <tr>
                    <td colspan="4">
                        <div class="empty-state">
                            <strong>No hay dispositivos registrados</strong>
                            El inventario está vacío.
                        </div>
                    </td>
                </tr>
            `;
            return;
        }

        dispositivos.slice(0, 5).forEach(dispositivo => {
            const estado = String(
                dispositivo.estado || "desconocido"
            ).toLowerCase();

            const claseEstado =
                estado === "activo"
                    ? "badge-success"
                    : "badge-muted";

            tabla.innerHTML += `
                <tr>
                    <td>
                        <strong>${escaparHTML(dispositivo.ip)}</strong>
                    </td>

                    <td>${escaparHTML(dispositivo.hostname)}</td>

                    <td>
                        <span class="badge badge-info">
                            ${escaparHTML(dispositivo.tipo)}
                        </span>
                    </td>

                    <td>
                        <span class="badge ${claseEstado}">
                            ${escaparHTML(dispositivo.estado)}
                        </span>
                    </td>
                </tr>
            `;
        });
    }


    function renderizarInventario(lista) {
        const tabla = document.getElementById("tablaInventario");
        const contador = document.getElementById("contadorInventario");

        tabla.innerHTML = "";
        contador.textContent =
            lista.length + (
                lista.length === 1
                    ? " dispositivo"
                    : " dispositivos"
            );

        if (lista.length === 0) {
            tabla.innerHTML = `
                <tr>
                    <td colspan="6">
                        <div class="empty-state">
                            <strong>No se encontraron dispositivos</strong>
                            Modifica el criterio de búsqueda o registra
                            un nuevo equipo.
                        </div>
                    </td>
                </tr>
            `;
            return;
        }

        lista.forEach(dispositivo => {
            const estado = String(
                dispositivo.estado || "desconocido"
            ).toLowerCase();

            const claseEstado =
                estado === "activo"
                    ? "badge-success"
                    : "badge-muted";

            tabla.innerHTML += `
                <tr>
                    <td>
                        <strong>${escaparHTML(dispositivo.ip)}</strong>
                    </td>

                    <td>${escaparHTML(dispositivo.hostname)}</td>
                    <td>${escaparHTML(dispositivo.mac)}</td>

                    <td>
                        <span class="badge badge-info">
                            ${escaparHTML(dispositivo.tipo)}
                        </span>
                    </td>

                    <td>${escaparHTML(dispositivo.sistema)}</td>

                    <td>
                        <span class="badge ${claseEstado}">
                            ${escaparHTML(dispositivo.estado)}
                        </span>
                    </td>
                </tr>
            `;
        });
    }


    function filtrarInventario() {
        const texto = document
            .getElementById("buscarDispositivo")
            .value
            .toLowerCase()
            .trim();

        const filtrados = dispositivos.filter(dispositivo => {
            return [
                dispositivo.ip,
                dispositivo.hostname,
                dispositivo.mac,
                dispositivo.tipo,
                dispositivo.sistema,
                dispositivo.estado
            ].some(valor =>
                String(valor || "")
                    .toLowerCase()
                    .includes(texto)
            );
        });

        renderizarInventario(filtrados);
    }


    async function cargarHistorial() {
        ocultarAlerta("globalAlert");

        try {
            historial = await solicitarConToken("/historial");

            renderizarHistorial(historial);

            mostrarAlerta(
                "globalAlert",
                "Historial actualizado correctamente.",
                "success"
            );

        } catch (error) {
            mostrarAlerta(
                "globalAlert",
                error.message,
                "error"
            );
        }
    }


    function obtenerClaseAccion(accion) {
        const valor = String(accion || "").toUpperCase();

        if (valor === "CREAR") {
            return "badge-success";
        }

        if (valor === "ACTUALIZAR") {
            return "badge-warning";
        }

        if (valor === "ELIMINAR") {
            return "badge-danger";
        }

        return "badge-muted";
    }


    function renderizarHistorial(lista) {
        const tabla = document.getElementById("tablaHistorial");
        const contador = document.getElementById("contadorHistorial");

        tabla.innerHTML = "";

        contador.textContent =
            lista.length + (
                lista.length === 1
                    ? " registro"
                    : " registros"
            );

        if (lista.length === 0) {
            tabla.innerHTML = `
                <tr>
                    <td colspan="4">
                        <div class="empty-state">
                            <strong>No hay movimientos registrados</strong>
                            El historial de cambios está vacío.
                        </div>
                    </td>
                </tr>
            `;
            return;
        }

        lista.forEach(registro => {
            tabla.innerHTML += `
                <tr>
                    <td>${escaparHTML(registro.id)}</td>

                    <td>
                        <span class="badge ${obtenerClaseAccion(registro.accion)}">
                            ${escaparHTML(registro.accion)}
                        </span>
                    </td>

                    <td>
                        <strong>${escaparHTML(registro.ip)}</strong>
                    </td>

                    <td>${escaparHTML(registro.fecha)}</td>
                </tr>
            `;
        });
    }


    function filtrarHistorial() {
        const texto = document
            .getElementById("buscarHistorial")
            .value
            .toLowerCase()
            .trim();

        const filtrados = historial.filter(registro => {
            return [
                registro.id,
                registro.accion,
                registro.ip,
                registro.fecha
            ].some(valor =>
                String(valor || "")
                    .toLowerCase()
                    .includes(texto)
            );
        });

        renderizarHistorial(filtrados);
    }


    async function exportarInventario() {
        ocultarAlerta("globalAlert");

        const boton = document.getElementById("exportButton");
        boton.disabled = true;
        boton.textContent = "Generando archivos...";

        try {
            await solicitarConToken("/exportar");

            const fecha = new Date().toLocaleString("es-MX");

            document.getElementById("ultimaExportacion").textContent =
                fecha;

            mostrarAlerta(
                "globalAlert",
                "Inventario exportado correctamente en JSON, YAML y XML.",
                "success"
            );

        } catch (error) {
            mostrarAlerta(
                "globalAlert",
                error.message,
                "error"
            );

        } finally {
            boton.disabled = false;
            boton.textContent =
                "Generar archivos de exportación";
        }
    }


    document
        .getElementById("loginForm")
        .addEventListener("submit", iniciarSesion);


    document.addEventListener(
        "DOMContentLoaded",
        restaurarSesion
    );
</script>

</body>
</html>
"""
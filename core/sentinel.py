"""Portable, read-only diagnostics and guarded actions for SENTINEL."""

from __future__ import annotations

import platform
import shutil
import socket
import subprocess
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None


IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"


def _run(args, timeout=20):
    try:
        result = subprocess.run(args, capture_output=True, text=True,
                                timeout=timeout, encoding="utf-8", errors="replace")
        return (result.stdout or result.stderr or "Sin salida").strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"No disponible: {exc}"


def system_status(bridge):
    return bridge.diagnostics() + "\n\nESTADO GENERAL\n" + bridge.system_module()


def storage_status(bridge):
    return bridge.files_module() + "\n\nCARPETA PERSONAL\n" + str(Path.home())


def list_user_files():
    try:
        entries = sorted(Path.home().iterdir(), key=lambda item: (not item.is_dir(), item.name.casefold()))
        if not entries:
            return "La carpeta personal está vacía."
        lines = ["CONTENIDO DE " + str(Path.home())]
        lines.extend(("[DIR]  " if item.is_dir() else "[FILE] ") + item.name for item in entries[:200])
        if len(entries) > 200:
            lines.append(f"\nSe muestran 200 de {len(entries)} elementos.")
        return "\n".join(lines)
    except OSError as exc:
        return f"No se pudo listar la carpeta personal: {exc}"


def sandbox_status():
    if IS_WINDOWS:
        if shutil.which("WindowsSandbox.exe"):
            return "Windows Sandbox está disponible."
        result = _run(["powershell", "-NoProfile", "-Command",
                       "(Get-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM -ErrorAction SilentlyContinue).State"])
        return "Windows Sandbox: " + (result if result not in ("", "Sin salida") else "no está habilitado o no es compatible con este equipo.")
    if IS_LINUX:
        found = [tool for tool in ("bwrap", "firejail") if shutil.which(tool)]
        return ("Herramientas disponibles: " + ", ".join(found) if found
                else "No se detectó bubblewrap ni firejail. Instala una herramienta de sandbox desde tu distribución.")
    return "La administración de sandbox no está disponible en este sistema operativo."


def network_status(bridge):
    lines = [bridge.network_module(), "", "RESOLUCIÓN DNS"]
    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo("example.com", None)})
        lines.append("example.com → " + ", ".join(addresses[:8]))
    except OSError as exc:
        lines.append(f"No se pudo resolver example.com: {exc}")
    if IS_WINDOWS:
        lines += ["", "PUERTOS Y CONEXIONES", _run(["netstat", "-ano"], 15)]
    elif IS_LINUX and shutil.which("ss"):
        lines += ["", "PUERTOS Y CONEXIONES", _run(["ss", "-tuln"], 15)]
    elif IS_LINUX and shutil.which("netstat"):
        lines += ["", "PUERTOS Y CONEXIONES", _run(["netstat", "-tuln"], 15)]
    else:
        lines += ["", "La consulta de puertos no está disponible en este sistema."]
    return "\n".join(lines)


def winget_available():
    return IS_WINDOWS and bool(shutil.which("winget"))


def package_action(action, package_id=None):
    if not winget_available():
        return "Winget solo está disponible en Windows cuando está instalado."
    if action in {"install", "uninstall"}:
        if not package_id or not all(c.isalnum() or c in ".-_" for c in package_id):
            return "Indica un identificador de paquete Winget válido."
        args = ["winget", action, "--id", package_id, "--exact"]
    elif action == "upgrade-all":
        args = ["winget", "upgrade", "--all"]
    elif action == "search":
        if not package_id:
            return "Escribe un término o ID para buscar."
        args = ["winget", "search", package_id]
    elif action == "list":
        args = ["winget", "list"]
    else:
        return "Acción desconocida."
    if action != "search":
        args += ["--accept-source-agreements", "--disable-interactivity"]
    if action in {"install", "upgrade-all"}:
        args += ["--accept-package-agreements"]
    return _run(args, 120)


def overdrive_status(bridge):
    lines = ["PROCESOS (mayor uso de CPU)", bridge.processes_module(), "", "PROGRAMAS DE INICIO"]
    if IS_WINDOWS:
        lines.append(_run(["powershell", "-NoProfile", "-Command",
                           "Get-CimInstance Win32_StartupCommand | Select-Object -First 30 Name,Location,User | Format-Table -AutoSize"]))
        lines += ["", "SERVICIOS ACTIVOS", _run(["powershell", "-NoProfile", "-Command",
                 "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object -First 30 Status,Name,DisplayName | Format-Table -AutoSize"], 25)]
    elif IS_LINUX:
        startup = Path.home() / ".config/autostart"
        lines.append("\n".join(sorted(p.name for p in startup.glob("*.desktop"))) if startup.is_dir() else "No se encontró ~/.config/autostart.")
        if shutil.which("systemctl"):
            lines += ["", "SERVICIOS ACTIVOS", _run(["systemctl", "--type=service", "--state=running", "--no-pager"], 25)]
        else:
            lines += ["", "systemctl no está disponible en este sistema."]
    else:
        lines.append("Inicio y servicios no disponibles en este sistema operativo.")
    return "\n".join(lines)


def stop_process(pid):
    if psutil is None:
        return "Esta acción requiere psutil."
    try:
        process = psutil.Process(int(pid))
        name = process.name()
        process.terminate()
        return f"Se solicitó cerrar {name} (PID {pid})."
    except (ValueError, psutil.Error, OSError) as exc:
        return f"No se pudo cerrar el proceso: {exc}"


def service_action(operation, service_name):
    if operation not in {"start", "stop"}:
        return "Acción de servicio desconocida."
    if not service_name or not all(c.isalnum() or c in "_.@-" for c in service_name):
        return "Indica un nombre de servicio válido."
    if IS_WINDOWS:
        command = ["powershell", "-NoProfile", "-Command",
                   f"{operation.title()}-Service -Name '{service_name}' -ErrorAction Stop"]
    elif IS_LINUX and shutil.which("systemctl"):
        command = ["systemctl", operation, service_name]
    else:
        return "La gestión de servicios no está disponible en este sistema."
    return _run(command, 30)


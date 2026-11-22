#!/usr/bin/env python3
"""
ULTRON PANEL 2.1 // PLATFORM ADAPTER
Compatibilidad base para Linux y Windows.
"""

import os
import platform
import shutil
import socket
import subprocess
import webbrowser
from pathlib import Path

try:
    import winreg
except ImportError:
    winreg = None

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    psutil = None
    HAS_PSUTIL = False

SYSTEM = platform.system().lower()
IS_WINDOWS = SYSTEM == "windows"
IS_LINUX = SYSTEM == "linux"


def platform_name():
    if IS_WINDOWS:
        return "Windows"
    if IS_LINUX:
        return "Linux"
    return platform.system() or "Desconocido"


def run_command(command, timeout=20):
    try:
        result = subprocess.run(
            command,
            shell=isinstance(command, str),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return (result.stdout or "").strip() or "Sin salida"
    except subprocess.TimeoutExpired:
        return "Tiempo de espera agotado"
    except Exception as exc:
        return f"No disponible: {exc}"


def hostname():
    try:
        return socket.gethostname()
    except Exception:
        return "ULTRON"


def local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
        finally:
            sock.close()
    except Exception:
        try:
            return socket.gethostbyname(hostname())
        except Exception:
            return "No disponible"


def system_info():
    lines = [
        f"Sistema: {platform.system()} {platform.release()}",
        f"Version: {platform.version()}",
        f"Arquitectura: {platform.machine()}",
        f"Equipo: {hostname()}",
        f"Procesador: {platform.processor() or 'No disponible'}",
    ]
    if HAS_PSUTIL:
        try:
            ram = psutil.virtual_memory()
            root = Path.home().anchor if IS_WINDOWS else "/"
            disk = psutil.disk_usage(root)
            lines += [
                f"CPU: {psutil.cpu_percent(interval=0.2):.0f}%",
                f"RAM: {ram.percent:.0f}% ({ram.used/1024**3:.1f} / {ram.total/1024**3:.1f} GB)",
                f"Disco: {disk.percent:.0f}% ({disk.used/1024**3:.1f} / {disk.total/1024**3:.1f} GB)",
            ]
        except Exception:
            pass
    return "\n".join(lines)


def network_info():
    """Resume la conexión con etiquetas legibles, sin volcar comandos de red."""
    lines = ["CONEXIÓN A INTERNET"]
    try:
        with socket.create_connection(("1.1.1.1", 443), timeout=2):
            lines.append("Estado: Conectado")
    except OSError:
        lines.append("Estado: No se pudo confirmar la conexión")
        lines.append("(La red local puede seguir funcionando.)")

    lines.extend(["", "REDES DE ESTE EQUIPO"])
    found = False
    if HAS_PSUTIL:
        try:
            addresses = psutil.net_if_addrs()
            statuses = psutil.net_if_stats()
            for interface, stats in statuses.items():
                if not stats.isup or interface.lower() in {"lo", "loopback"}:
                    continue
                ipv4 = next((
                    addr.address for addr in addresses.get(interface, [])
                    if addr.family == socket.AF_INET
                    and not addr.address.startswith("127.")
                ), None)
                if not ipv4:
                    continue
                key = interface.lower()
                if any(tag in key for tag in ("wi-fi", "wifi", "wlan", "wireless")):
                    kind = "Wi-Fi"
                elif any(tag in key for tag in ("ethernet", "eth", "enp", "ens")):
                    kind = "Cable"
                else:
                    kind = "Red"
                lines.append(f"{kind}: Conectada · IP local {ipv4}")
                found = True
        except Exception:
            pass
    if not found:
        address = local_ip()
        if address != "No disponible":
            lines.append(f"Conectada · IP local {address}")
            found = True
    if not found:
        lines.append("No se detectó una conexión activa.")
    return "\n".join(lines)


def open_ports():
    if IS_WINDOWS:
        return run_command(["netstat", "-ano"])
    if IS_LINUX and shutil.which("ss"):
        return run_command(["ss", "-tuln"])
    if IS_LINUX and shutil.which("netstat"):
        return run_command(["netstat", "-tuln"])
    return "No disponible"


def running_services():
    if IS_WINDOWS:
        return run_command([
            "powershell", "-NoProfile", "-Command",
            "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object -First 30 Status,Name,DisplayName | Format-Table -AutoSize"
        ], 25)
    if IS_LINUX and shutil.which("systemctl"):
        return run_command(["systemctl", "--type=service", "--state=running", "--no-pager"], 25)
    return "No disponible"


def security_info():
    return (
        f"SISTEMA:\n{platform.system()} {platform.release()}\n\n"
        f"PUERTOS / CONEXIONES:\n{open_ports()}\n\n"
        f"SERVICIOS ACTIVOS:\n{running_services()}"
    )


def disk_info():
    if HAS_PSUTIL:
        lines = []
        try:
            seen = set()
            for part in psutil.disk_partitions(all=False):
                mountpoint = part.mountpoint
                if mountpoint in seen:
                    continue
                seen.add(mountpoint)
                try:
                    usage = psutil.disk_usage(mountpoint)
                    if IS_WINDOWS:
                        drive = mountpoint.rstrip("\\") or part.device
                        name = f"Unidad {drive}"
                    elif mountpoint == "/":
                        name = "Disco del sistema"
                    elif mountpoint == str(Path.home()):
                        name = "Archivos personales"
                    else:
                        name = f"Unidad {mountpoint}"
                    free_gb = usage.free / 1024**3
                    total_gb = usage.total / 1024**3
                    lines.append(
                        f"{name}\n"
                        f"  Espacio libre: {free_gb:.1f} GB de {total_gb:.1f} GB"
                        f"  ·  {usage.percent:.0f}% ocupado"
                    )
                except (PermissionError, OSError):
                    pass
        except Exception:
            pass
        if lines:
            return "ALMACENAMIENTO\n\n" + "\n\n".join(lines)

    if IS_WINDOWS:
        return run_command([
            "powershell", "-NoProfile", "-Command",
            "Get-CimInstance Win32_LogicalDisk | Select-Object DeviceID,VolumeName,FileSystem,Size,FreeSpace | Format-Table -AutoSize"
        ])
    if IS_LINUX:
        return run_command(["df", "-h"])
    return "No disponible"


def installed_programs(limit=80):
    """Lista programas instalados con detalles breves, usando fuentes del SO."""
    programs = []
    if IS_WINDOWS and winreg is not None:
        uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        locations = (
            (winreg.HKEY_LOCAL_MACHINE, getattr(winreg, "KEY_WOW64_64KEY", 0)),
            (winreg.HKEY_LOCAL_MACHINE, getattr(winreg, "KEY_WOW64_32KEY", 0)),
            (winreg.HKEY_CURRENT_USER, 0),
        )
        seen = set()
        for root, view in locations:
            try:
                parent = winreg.OpenKey(root, uninstall_key, 0, winreg.KEY_READ | view)
            except OSError:
                continue
            with parent:
                for index in range(winreg.QueryInfoKey(parent)[0]):
                    try:
                        subkey_name = winreg.EnumKey(parent, index)
                        with winreg.OpenKey(parent, subkey_name) as subkey:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0].strip()
                            if not name or name.casefold() in seen:
                                continue
                            try:
                                if winreg.QueryValueEx(subkey, "SystemComponent")[0] == 1:
                                    continue
                            except OSError:
                                pass
                            try:
                                version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                            except OSError:
                                version = ""
                            try:
                                publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                            except OSError:
                                publisher = ""
                            details = " · ".join(part for part in (
                                f"Versión {version}" if version else "",
                                publisher,
                            ) if part)
                            programs.append((name, details or "Programa instalado"))
                            seen.add(name.casefold())
                    except (OSError, AttributeError):
                        continue
    elif IS_LINUX:
        # El menú de aplicaciones muestra programas reconocibles, sin llenar la
        # lista con bibliotecas internas del sistema.
        seen = set()
        for directory in (Path("/usr/share/applications"), Path.home() / ".local/share/applications"):
            try:
                desktop_files = directory.glob("*.desktop")
                for desktop_file in desktop_files:
                    try:
                        values = {}
                        in_entry = False
                        for line in desktop_file.read_text(encoding="utf-8", errors="replace").splitlines():
                            line = line.strip()
                            if line.startswith("["):
                                in_entry = line == "[Desktop Entry]"
                                continue
                            if in_entry and "=" in line and not line.startswith("#"):
                                key, value = line.split("=", 1)
                                values[key] = value.strip()
                        if (values.get("Type") != "Application"
                                or values.get("NoDisplay", "false").lower() == "true"
                                or values.get("Hidden", "false").lower() == "true"):
                            continue
                        name = values.get("Name[es]") or values.get("Name")
                        if not name or name.casefold() in seen:
                            continue
                        details = values.get("Comment[es]") or values.get("Comment")
                        if not details:
                            details = values.get("GenericName[es]") or values.get("GenericName")
                        programs.append((name, details or "Aplicación instalada"))
                        seen.add(name.casefold())
                    except OSError:
                        continue
            except OSError:
                continue

        if not programs and shutil.which("dpkg-query"):
            raw = run_command([
                "dpkg-query", "-W",
                "-f=${binary:Package}\\t${Version}\\t${binary:Summary}\\n",
            ], timeout=25)
            for row in raw.splitlines():
                fields = row.split("\t", 2)
                if fields and fields[0] and not fields[0].startswith("No disponible"):
                    name = fields[0]
                    version = fields[1] if len(fields) > 1 else ""
                    summary = fields[2] if len(fields) > 2 else "Paquete instalado"
                    programs.append((name, f"Versión {version} · {summary}".strip(" ·")))
        elif shutil.which("rpm"):
            raw = run_command(["rpm", "-qa", "--qf", "%{NAME}\\t%{VERSION}\\t%{SUMMARY}\\n"], timeout=25)
            for row in raw.splitlines():
                fields = row.split("\t", 2)
                if fields and fields[0]:
                    version = fields[1] if len(fields) > 1 else ""
                    summary = fields[2] if len(fields) > 2 else "Paquete instalado"
                    programs.append((fields[0], f"Versión {version} · {summary}".strip(" ·")))

    if not programs:
        return "No se pudo obtener la lista de programas de este sistema."
    programs.sort(key=lambda item: item[0].casefold())
    shown = programs[:limit]
    lines = ["PROGRAMAS INSTALADOS", f"Se encontraron {len(programs)} programas.\n"]
    lines.extend(f"• {name}\n  {details}" for name, details in shown)
    if len(programs) > limit:
        lines.append(f"\nSe muestran los primeros {limit}; hay {len(programs) - limit} más.")
    return "\n\n".join(lines)


def process_info(limit=20):
    if HAS_PSUTIL:
        rows = []
        try:
            procs = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
                try:
                    procs.append(proc.info)
                except Exception:
                    pass
            procs.sort(key=lambda p: p.get("cpu_percent") or 0, reverse=True)
            for p in procs[:limit]:
                rows.append(
                    f"{p.get('pid', 0):>6}  {(p.get('cpu_percent') or 0):>5.1f}%  "
                    f"{(p.get('memory_percent') or 0):>5.1f}%  {p.get('name') or '?'}"
                )
            return "PID     CPU     RAM    PROCESO\n" + "\n".join(rows)
        except Exception:
            pass
    if IS_WINDOWS:
        return run_command(["tasklist"])
    if IS_LINUX:
        return run_command("ps aux --sort=-%cpu | head -21")
    return "No disponible"



def temperature_info():
    """Devuelve las temperaturas disponibles del equipo."""
    if HAS_PSUTIL:
        try:
            temps = psutil.sensors_temperatures()
            lines = []

            for chip, entries in temps.items():
                for entry in entries:
                    label = entry.label or chip
                    current = entry.current

                    if current is not None:
                        lines.append(f"{label}: {current:.1f} °C")

            if lines:
                return "TEMPERATURAS:\n" + "\n".join(lines)
        except Exception:
            pass

    if IS_LINUX and shutil.which("sensors"):
        return run_command(["sensors"])

    return "Temperatura no disponible en este sistema."


def battery_info():
    if not HAS_PSUTIL:
        return "psutil no instalado"
    try:
        batt = psutil.sensors_battery()
        if batt is None:
            return "Bateria no disponible"
        return f"Bateria: {batt.percent:.0f}%\nConectado a corriente: {'Si' if batt.power_plugged else 'No'}"
    except Exception:
        return "Bateria no disponible"


def open_url(url):
    try:
        return bool(webbrowser.open(url))
    except Exception:
        return False


def open_path(path):
    target = str(Path(path).expanduser())
    try:
        if IS_WINDOWS:
            os.startfile(target)
            return True
        if IS_LINUX and shutil.which("xdg-open"):
            subprocess.Popen(["xdg-open", target],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
            return True
    except Exception:
        pass
    return False


def open_terminal():
    try:
        if IS_WINDOWS:
            subprocess.Popen(["cmd.exe"])
            return True
        for terminal in ("x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "kitty", "alacritty"):
            if shutil.which(terminal):
                subprocess.Popen([terminal],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
                return True
    except Exception:
        pass
    return False


def open_app(app):
    name = app.strip().lower()

    urls = {
        "youtube": "https://www.youtube.com",
        "whatsapp": "https://web.whatsapp.com",
        "spotify": "https://open.spotify.com",
    }
    if name in urls:
        return open_url(urls[name])

    try:
        if IS_WINDOWS:
            apps = {
                "terminal": ["cmd.exe"],
                "cmd": ["cmd.exe"],
                "powershell": ["powershell.exe"],
                "explorer": ["explorer.exe"],
                "archivos": ["explorer.exe"],
                "notepad": ["notepad.exe"],
                "bloc de notas": ["notepad.exe"],
                "calculadora": ["calc.exe"],
            }
            cmd = apps.get(name)
            if cmd:
                subprocess.Popen(cmd)
                return True

        if IS_LINUX:
            if name in {"terminal", "consola"}:
                return open_terminal()
            if name == "archivos" and shutil.which("xdg-open"):
                subprocess.Popen(["xdg-open", str(Path.home())],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
                return True
    except Exception:
        pass

    return False


def platform_summary():
    return {
        "system": platform_name(),
        "is_windows": IS_WINDOWS,
        "is_linux": IS_LINUX,
        "hostname": hostname(),
        "local_ip": local_ip(),
        "python": platform.python_version(),
        "architecture": platform.machine(),
    }


if __name__ == "__main__":
    print("ULTRON // PLATFORM ADAPTER")
    print("=" * 40)
    for key, value in platform_summary().items():
        print(f"{key}: {value}")

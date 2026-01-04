import subprocess
import os
import sys
import time
from pathlib import Path

def run_service(name, command, cwd):
    print(f"🚀 Iniciando {name}...")
    return subprocess.Popen(
        command,
        cwd=cwd,
        shell=True,
        stdout=None,
        stderr=None
    )

def main():
    # Detectar el directorio del proyecto
    project_root = Path(__file__).parent.resolve()
    
    # Comandos para cada servicio
    services = [
        {
            "name": "🛡️ Sentinel (Security)",
            "command": "python -m uvicorn security.main:app --host 0.0.0.0 --port 9000 --reload",
            "cwd": project_root
        },
        {
            "name": "🧠 Oracle (Backend API)",
            "command": "python -m uvicorn app.web.server:app --host 0.0.0.0 --port 8080 --reload",
            "cwd": project_root
        },
        {
            "name": "🎨 Antigravity Frontend",
            "command": "python -m uvicorn web.main_web:app --host 0.0.0.0 --port 8000 --reload",
            "cwd": project_root
        }
    ]

    processes = []
    
    try:
        for s in services:
            p = run_service(s["name"], s["command"], s["cwd"])
            processes.append(p)
            time.sleep(1)  # Pequeño delay para no saturar la salida

        print("\n✨ Todos los servicios están corriendo. Presiona Ctrl+C para detenerlos.\n")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servicios...")
        for p in processes:
            p.terminate()
        print("✅ Entorno cerrado correctamente.")

if __name__ == "__main__":
    # Asegurar que el PYTHONPATH incluya la raíz del proyecto
    os.environ["PYTHONPATH"] = str(Path(__file__).parent.resolve())
    main()

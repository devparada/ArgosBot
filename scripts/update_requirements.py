import subprocess
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent

# Detectar el Python del entorno virtual
candidates = [
    project_dir / ".venv" / "Scripts" / "python.exe",
    project_dir / ".venv" / "bin" / "python",
]

venv_python = next((path for path in candidates if path.is_file()), None)

if venv_python is None:
    sys.exit(f"Error: no se encuentra .venv en {project_dir}")

requirements = project_dir / "requirements.txt"

try:
    result = subprocess.run(
        [str(venv_python), "-X", "utf8", "-m", "pip", "freeze"],
        capture_output=True,
        check=True,
    )

    content = result.stdout.decode("utf-8")

    with requirements.open("w", encoding="utf-8", newline="\n") as file:
        file.write(content)

    print("requirements.txt actualizado correctamente")
    print(f"Archivo: {requirements}")
    print(f"Python: {venv_python}")
    print("Codificación: UTF-8 sin BOM")

except subprocess.CalledProcessError as error:
    print(error.stderr.decode("utf-8", errors="replace"), file=sys.stderr)
    sys.exit(error.returncode)
except (OSError, UnicodeDecodeError) as error:
    sys.exit(f"Error: {error}")

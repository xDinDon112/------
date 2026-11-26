import os
import socket
import subprocess
import sys
import time
import venv
import webbrowser
from pathlib import Path
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener


ROOT = Path(__file__).resolve().parent
ENV = ROOT / ".venv"
PYTHON = ENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def find_port():
    for port in range(8001, 8011):
        with socket.socket() as probe:
            try:
                probe.bind(("127.0.0.1", port))
            except OSError:
                continue
        return port
    raise RuntimeError("Все порты от 8001 до 8010 заняты.")


def start():
    if sys.version_info < (3, 10):
        raise RuntimeError("Для запуска Django нужен Python 3.10 или новее.")

    if not PYTHON.is_file():
        venv.EnvBuilder(with_pip=True).create(ENV)

    installed = subprocess.run(
        [PYTHON, "-m", "django", "--version"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    requirement = (ROOT / "requirements.txt").read_text().strip()
    if f"Django=={installed.stdout.strip()}" != requirement:
        subprocess.run(
            [
                PYTHON, "-m", "pip", "install", "--no-index",
                "--find-links", "wheels", "-r", "requirements.txt",
            ],
            cwd=ROOT,
            check=True,
        )

    port = find_port()
    url = f"http://127.0.0.1:{port}/"
    print(f"Сайт запускается. Адрес в браузере: {url}", flush=True)
    environment = os.environ.copy()
    environment.update(DJANGO_DEBUG="1", DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost")
    with subprocess.Popen(
        [PYTHON, "manage.py", "runserver", f"127.0.0.1:{port}", "--noreload"],
        cwd=ROOT,
        env=environment,
    ) as server:
        try:
            local = build_opener(ProxyHandler({}))
            for _ in range(40):
                if server.poll() is not None:
                    break
                try:
                    with local.open(url, timeout=0.5):
                        webbrowser.open(url)
                        break
                except (URLError, TimeoutError):
                    time.sleep(0.25)
            return server.wait()
        except KeyboardInterrupt:
            if server.poll() is None:
                server.terminate()
            return 0


if __name__ == "__main__":
    try:
        sys.exit(start())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Запуск не удался. {error}", file=sys.stderr)
        sys.exit(1)

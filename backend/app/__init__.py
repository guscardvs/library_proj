try:
    from core.settings import BASE_DIR
except ModuleNotFoundError:
    from pathlib import Path
    from sys import path

    path.append(str(Path(__file__).resolve().parent))

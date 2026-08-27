import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from offline2fa.app import run

if __name__ == "__main__":
    sys.exit(run())

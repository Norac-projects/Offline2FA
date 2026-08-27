import json
import os
import sys
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path


def data_dir() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", str(Path.home()))
    elif sys.platform == "darwin":
        base = str(Path.home() / "Library" / "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
    path = Path(base) / "Offline2FA"
    path.mkdir(parents=True, exist_ok=True)
    return path


@dataclass
class Account:
    id: str
    kind: str
    issuer: str
    name: str
    secret: str
    digits: int = 6
    algorithm: str = "SHA1"
    period: int = 30
    counter: int = 0
    color: str = ""

    @classmethod
    def new(cls, kind: str, issuer: str, name: str, secret: str,
            digits: int = 6, algorithm: str = "SHA1",
            period: int = 30, counter: int = 0, color: str = "") -> "Account":
        return cls(uuid.uuid4().hex, kind, issuer, name, secret,
                   digits, algorithm, period, counter, color)

    @property
    def display_name(self) -> str:
        return self.issuer or self.name or "Account"

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        fields = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in data.items() if k in fields})


class Store:
    def __init__(self, path: Path | None = None):
        self.path = path or data_dir() / "accounts.json"
        self.accounts: list[Account] = []
        self.theme = "dark"
        self.load()

    def load(self):
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        self.theme = data.get("theme", "dark")
        self.accounts = [Account.from_dict(a) for a in data.get("accounts", [])]

    def save(self):
        data = {"theme": self.theme, "accounts": [asdict(a) for a in self.accounts]}
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        os.replace(tmp, self.path)

    def add(self, account: Account):
        self.accounts.append(account)
        self.save()

    def remove(self, account_id: str):
        self.accounts = [a for a in self.accounts if a.id != account_id]
        self.save()

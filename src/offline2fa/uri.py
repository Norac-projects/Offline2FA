from urllib.parse import parse_qs, unquote, urlparse

from . import otp
from .storage import Account


def parse(uri: str) -> Account:
    parsed = urlparse(uri.strip())
    if parsed.scheme != "otpauth":
        raise ValueError("Not an otpauth:// link")

    kind = parsed.netloc.lower()
    if kind not in ("totp", "hotp"):
        raise ValueError(f"Unsupported OTP type: {kind or 'none'}")

    label = unquote(parsed.path.lstrip("/"))
    issuer, name = "", label
    if ":" in label:
        issuer, name = (part.strip() for part in label.split(":", 1))

    params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
    secret = params.get("secret", "")
    if not secret:
        raise ValueError("Link has no secret")
    otp.decode_secret(secret)

    issuer = params.get("issuer", issuer).strip()
    algorithm = params.get("algorithm", "SHA1").upper()
    if algorithm not in otp.ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    return Account.new(
        kind=kind,
        issuer=issuer,
        name=name.strip(),
        secret=secret,
        digits=int(params.get("digits", 6)),
        algorithm=algorithm,
        period=int(params.get("period", 30)),
        counter=int(params.get("counter", 0)),
    )


def smart_build(text: str, name: str = "") -> Account:
    text = text.strip()
    if not text:
        raise ValueError("Paste your 2FA secret or setup link")

    if text.lower().startswith("otpauth://"):
        account = parse(text)
        if name.strip() and not account.issuer:
            account.issuer = name.strip()
        return account

    otp.decode_secret(text)
    label = name.strip()
    return Account.new(kind="totp", issuer=label, name="", secret=text)


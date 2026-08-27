import base64
import hashlib
import hmac
import struct
import time

ALGORITHMS = {
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA512": hashlib.sha512,
}


def normalize_secret(secret: str) -> str:
    s = secret.strip().replace(" ", "").replace("-", "").upper()
    return s + "=" * ((-len(s)) % 8)


def decode_secret(secret: str) -> bytes:
    key = base64.b32decode(normalize_secret(secret), casefold=True)
    if not key:
        raise ValueError("empty secret")
    return key


def hotp(secret: str, counter: int, digits: int = 6, algorithm: str = "SHA1") -> str:
    key = decode_secret(secret)
    digest = hmac.new(key, struct.pack(">Q", counter), ALGORITHMS[algorithm]).digest()
    offset = digest[-1] & 0x0F
    value = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(value % 10 ** digits).zfill(digits)


def totp(secret: str, digits: int = 6, algorithm: str = "SHA1",
         period: int = 30, timestamp: float | None = None) -> str:
    now = time.time() if timestamp is None else timestamp
    return hotp(secret, int(now // period), digits, algorithm)


def time_remaining(period: int = 30, timestamp: float | None = None) -> float:
    now = time.time() if timestamp is None else timestamp
    return period - (now % period)

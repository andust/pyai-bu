import hashlib


def byte_hash(content: bytes) -> str:
    hasher = hashlib.sha256()
    hasher.update(content)
    return hasher.hexdigest()


def slugify(s: str) -> str:
    return s.replace(" ", "-").lower()

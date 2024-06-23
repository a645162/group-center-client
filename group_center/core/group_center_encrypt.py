import hashlib


def encrypt_password_to_display(password: str, display_string: str = "*") -> str:
    return display_string * len(password)


def get_md5_hash(input: str) -> str:
    md5_hash = hashlib.md5(input.encode("utf-8"))
    return md5_hash.hexdigest()


def get_password_hash(input: str):
    return get_md5_hash(input)

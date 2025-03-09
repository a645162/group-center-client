import hashlib
from typing import Optional


def encrypt_password_to_display(password: str, display_string: str = "*") -> str:
    """将密码转换为显示字符串

    Args:
        password: 原始密码
        display_string: 用于显示的字符，默认为'*'

    Returns:
        str: 由显示字符组成的字符串，长度与密码相同
    """
    return display_string * len(password)


def get_md5_hash(input: str) -> str:
    """生成字符串的 MD5 哈希值

    Args:
        input: 需要哈希的字符串

    Returns:
        str: 哈希值
    """
    md5_hash = hashlib.md5(input.encode("utf-8"))
    return md5_hash.hexdigest()


def get_password_hash(input: str) -> str:
    """生成group-center后端使用的密码哈希值

    Args:
        input: 需要哈希的字符串

    Returns:
        str: 哈希值
    """
    return get_md5_hash(input)


def get_sha256_hash(input: str) -> str:
    """生成字符串的 SHA-256 哈希值

    Args:
        input: 需要哈希的字符串

    Returns:
        str: 64字符的十六进制哈希值
    """
    sha256_hash = hashlib.sha256(input.encode("utf-8"))
    return sha256_hash.hexdigest()


def get_program_hash(input: str, salt: Optional[str] = None) -> str:
    """生成哈希值(整个项目都调用这个函数，统一计算方式)

    Args:
        input: 原始密码
        salt: 可选的盐值，用于增强安全性

    Returns:
        str: 64字符的十六进制哈希值
    """
    if salt:
        input = salt + input
    return get_sha256_hash(input)

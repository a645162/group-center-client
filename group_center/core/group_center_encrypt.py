import hashlib  # 哈希算法库 / Hash algorithm library
from typing import Optional


def encrypt_password_to_display(password: str, display_string: str = "*") -> str:
    """将密码转换为显示字符串
    Convert password to display string

    Args:
        password (str): 原始密码 / Original password
        display_string (str): 用于显示的字符，默认为'*' / Display character, defaults to '*'

    Returns:
        str: 由显示字符组成的字符串，长度与密码相同
        String consisting of display characters with same length as password
    """
    return display_string * len(password)


def get_md5_hash(input: str) -> str:
    """生成字符串的 MD5 哈希值
    Generate MD5 hash of input string

    Args:
        input (str): 需要哈希的字符串 / String to hash

    Returns:
        str: 32字符的十六进制哈希值
        32-character hexadecimal hash value
    """
    md5_hash: hashlib._Hash = hashlib.md5(input.encode("utf-8"))
    return md5_hash.hexdigest()


def get_password_hash(input: str) -> str:
    """生成group-center后端使用的密码哈希值
    Generate password hash for group-center backend

    Args:
        input (str): 需要哈希的字符串 / String to hash

    Returns:
        str: MD5哈希值
        MD5 hash value
    """
    return get_md5_hash(input)


def get_sha256_hash(input: str) -> str:
    """生成字符串的 SHA-256 哈希值
    Generate SHA-256 hash of input string

    Args:
        input (str): 需要哈希的字符串 / String to hash

    Returns:
        str: 64字符的十六进制哈希值
        64-character hexadecimal hash value
    """
    sha256_hash: hashlib._Hash = hashlib.sha256(input.encode("utf-8"))
    return sha256_hash.hexdigest()


def get_program_hash(input: str, salt: Optional[str] = None) -> str:
    """生成哈希值(整个项目都调用这个函数，统一计算方式)
    Generate program hash (used throughout the project for consistent hashing)

    Args:
        input (str): 原始密码 / Original password
        salt (Optional[str]): 可选的盐值，用于增强安全性 / Optional salt for added security

    Returns:
        str: 64字符的十六进制哈希值
        64-character hexadecimal hash value
    """
    if salt:
        input = salt + input
    return get_sha256_hash(input)

from enum import Enum, auto
from typing import Tuple


class SizeUnit(Enum):
    """数据大小单位枚举类"""

    BYTE = auto()  # 字节
    KB = auto()  # 千字节
    MB = auto()  # 兆字节
    GB = auto()  # 吉字节
    TB = auto()  # 太字节
    PB = auto()  # 拍字节
    EB = auto()  # 艾字节


# 单位间的倍数关系（2^10 = 1024）
UNIT_MULTIPLIER = 1024

# 单位名称与符号映射
UNIT_SYMBOLS = {
    SizeUnit.BYTE: "B",
    SizeUnit.KB: "KB",
    SizeUnit.MB: "MB",
    SizeUnit.GB: "GB",
    SizeUnit.TB: "TB",
    SizeUnit.PB: "PB",
    SizeUnit.EB: "EB",
}


def convert_size(size: float, from_unit: SizeUnit, to_unit: SizeUnit) -> float:
    """
    在不同数据大小单位之间转换

    Args:
        size: 要转换的大小值
        from_unit: 输入的单位
        to_unit: 输出的单位

    Returns:
        转换后的大小值
    """
    if from_unit == to_unit:
        return size

    # 确定单位大小关系
    unit_difference = from_unit.value - to_unit.value

    # 进行转换
    if unit_difference > 0:
        # 从大单位转换到小单位（乘以1024的n次方）
        return size * (UNIT_MULTIPLIER ** abs(unit_difference))
    else:
        # 从小单位转换到大单位（除以1024的n次方）
        return size / (UNIT_MULTIPLIER ** abs(unit_difference))


def auto_convert_size(size_bytes: float) -> Tuple[float, SizeUnit]:
    """
    自动将字节大小转换为最适合的单位

    Args:
        size_bytes: 字节大小

    Returns:
        元组 (转换后的值, 单位枚举)
    """
    units = list(SizeUnit)
    unit_index = 0

    while size_bytes >= UNIT_MULTIPLIER and unit_index < len(units) - 1:
        size_bytes /= UNIT_MULTIPLIER
        unit_index += 1

    return size_bytes, units[unit_index]


def format_size(size_bytes: float, precision: int = 2) -> str:
    """
    格式化字节大小为易读的字符串

    Args:
        size_bytes: 字节大小
        precision: 小数位数

    Returns:
        格式化后的字符串，例如 "1.50 MB"
    """
    value, unit = auto_convert_size(size_bytes)
    return f"{value:.{precision}f} {UNIT_SYMBOLS[unit]}"


def parse_size(size_str: str) -> float:
    """
    解析包含单位的大小字符串为字节数

    Args:
        size_str: 包含单位的大小字符串，例如 "1.5 GB"

    Returns:
        对应的字节大小
    """
    size_str = size_str.strip()

    # 查找数字和单位部分
    num_part = ""
    unit_part = ""

    for char in size_str:
        if char.isdigit() or char == "." or char == "-":
            num_part += char
        elif not char.isspace():
            unit_part += char

    unit_part = unit_part.strip().upper()

    # 获取对应的单位枚举
    target_unit = None
    for unit, symbol in UNIT_SYMBOLS.items():
        if unit_part == symbol:
            target_unit = unit
            break

    if target_unit is None:
        raise ValueError(f"未知的大小单位: {unit_part}")

    # 转换为字节
    value = float(num_part)
    return convert_size(value, target_unit, SizeUnit.BYTE)


def main():
    """测试数据单位转换功能"""
    print("===== 数据大小单位转换测试 =====")

    # 测试基本转换
    print("\n1. 基本单位转换测试:")
    test_cases = [
        (1024, SizeUnit.BYTE, SizeUnit.KB),
        (1, SizeUnit.KB, SizeUnit.BYTE),
        (1, SizeUnit.MB, SizeUnit.KB),
        (2.5, SizeUnit.GB, SizeUnit.MB),
        (0.1, SizeUnit.TB, SizeUnit.GB),
    ]

    for size, from_unit, to_unit in test_cases:
        result = convert_size(size, from_unit, to_unit)
        print(f"{size} {UNIT_SYMBOLS[from_unit]} = {result} {UNIT_SYMBOLS[to_unit]}")

    # 测试自动单位转换
    print("\n2. 自动单位转换测试:")
    byte_sizes = [
        10,
        1500,
        1024 * 1024 * 3.5,
        1024 * 1024 * 1024 * 2.7,
        1024 * 1024 * 1024 * 1024 * 0.8,
    ]

    for bytes_value in byte_sizes:
        value, unit = auto_convert_size(bytes_value)
        print(f"{bytes_value} B 自动转换为: {value:.2f} {UNIT_SYMBOLS[unit]}")

    # 测试格式化
    print("\n3. 格式化测试:")
    for bytes_value in byte_sizes:
        formatted = format_size(bytes_value)
        print(f"{bytes_value} B 格式化为: {formatted}")

    # 测试解析
    print("\n4. 解析测试:")
    size_strings = ["1024 B", "1.5 KB", "2.75 MB", "0.5 GB", "0.01 TB"]

    for size_str in size_strings:
        bytes_value = parse_size(size_str)
        print(f"'{size_str}' 解析为: {bytes_value} B")
        # 循环转换回易读格式
        print(f"'{size_str}' 重新格式化: {format_size(bytes_value)}")


if __name__ == "__main__":
    main()

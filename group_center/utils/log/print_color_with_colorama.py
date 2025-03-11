import colorama


def convert_str_to_colorama_color(color: str) -> str:
    """Convert string to colorama color / 将字符串转换为colorama颜色

    Args:
        color (str): Color name / 颜色名称

    Returns:
        str: Colorama color code / Colorama颜色代码
    """
    color = color.upper().strip()

    if color == "BLACK":
        return colorama.Fore.BLACK
    if color == "RED":
        return colorama.Fore.RED
    if color == "GREEN":
        return colorama.Fore.GREEN
    if color == "YELLOW":
        return colorama.Fore.YELLOW
    if color == "BLUE":
        return colorama.Fore.BLUE
    if color == "MAGENTA":
        return colorama.Fore.MAGENTA
    if color == "CYAN":
        return colorama.Fore.CYAN
    if color == "WHITE":
        return colorama.Fore.WHITE

    return colorama.Fore.RESET


def convert_str_to_colorama_background_color(color: str) -> str:
    """Convert string to colorama background color / 将字符串转换为colorama背景颜色

    Args:
        color (str): Background color name / 背景颜色名称

    Returns:
        str: Colorama background color code / Colorama背景颜色代码
    """
    color = color.upper().strip()

    if color == "BLACK":
        return colorama.Back.BLACK
    if color == "RED":
        return colorama.Back.RED
    if color == "GREEN":
        return colorama.Back.GREEN
    if color == "YELLOW":
        return colorama.Back.YELLOW
    if color == "BLUE":
        return colorama.Back.BLUE
    if color == "MAGENTA":
        return colorama.Back.MAGENTA
    if color == "CYAN":
        return colorama.Back.CYAN
    if color == "WHITE":
        return colorama.Back.WHITE

    return colorama.Back.RESET


def print_color(
    message: str, color: str = "", background_color: str = "", end: str = "\n"
) -> None:
    """Print colored message / 打印彩色消息

    Args:
        message (str): Message to print / 要打印的消息
        color (str, optional): Text color / 文本颜色. Defaults to "".
        background_color (str, optional): Background color / 背景颜色. Defaults to "".
        end (str, optional): End character / 结束字符. Defaults to "\n".
    """
    colorama.init(autoreset=True)

    print(
        convert_str_to_colorama_color(color)
        + convert_str_to_colorama_background_color(background_color)
        + message,
        end=end,
    )

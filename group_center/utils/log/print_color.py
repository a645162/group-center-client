import colorama


def convert_str_to_colorama_color(color: str):
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


def convert_str_to_colorama_background_color(color: str):
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


def print_color(message, color: str = "", background_color: str = "", end: str = "\n"):
    colorama.init(autoreset=True)

    print(
        convert_str_to_colorama_color(color) +
        convert_str_to_colorama_background_color(background_color) +
        message,
        end=end
    )

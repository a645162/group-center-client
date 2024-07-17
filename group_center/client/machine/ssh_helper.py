import os
import platform
import curses
import signal
import sys
from typing import List, Any

system_name = platform.system()

is_linux = system_name == "Linux"
is_root_user = is_linux and os.geteuid() == 0

wait_key_input = True


class TuiItem:
    text: str = ""

    x: int = -1
    y: int = -1

    key: str = ""

    def __init__(self, text: str, key: str = "", handler=None):
        self.text = text
        self.key = key
        self.handler = handler

    def try_to_handle(self):
        if self.handler:
            self.handler()


def init_main_interface_content() -> List[TuiItem]:
    str_list: List[TuiItem] = []

    str_list.append(TuiItem("SSH Helper - Group Center Client"))
    str_list.append(TuiItem(""))

    str_list.append(TuiItem(f"System:{system_name}"))
    if is_root_user:
        str_list.append(TuiItem("With 'root' user to run this program"))

    str_list.append(TuiItem(""))
    str_list.append(TuiItem("Exit", key="q", handler=lambda: exit(0)))

    return str_list


def main_interface(stdscr):
    # Clear screen
    curses.curs_set(0)  # 隐藏光标
    stdscr.clear()

    # Create a new window
    height, width = stdscr.getmaxyx()
    win = curses.newwin(height, width, 0, 0)

    # Draw a box around the window
    win.box()

    # Init content
    tui_list = init_main_interface_content()
    for i, tui_item in enumerate(tui_list):
        key_tip = ""
        if tui_item.key:
            key_tip = f"({tui_item.key})"
        win.addstr(i + 1, 2, key_tip + tui_item.text)

    # Refresh the window
    win.refresh()

    # Handle key input
    global wait_key_input
    while wait_key_input:
        key = win.getkey()

        for tui_item in tui_list:
            if not tui_item.key:
                continue

            if key == tui_item.key:
                tui_item.try_to_handle()


def signal_handler(signal: int, frame: Any) -> None:
    global wait_key_input
    wait_key_input = False

    sys.exit(0)


def init_tui():
    # Register the signal handler
    # Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Init curses
    curses.wrapper(main_interface)


def main():
    init_tui()


if __name__ == "__main__":
    main()

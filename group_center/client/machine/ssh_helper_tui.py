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
    """TUI项表示 / TUI item representation

    Attributes:
        text (str): 显示文本 / Display text
        x (int): x坐标 / x-coordinate
        y (int): y坐标 / y-coordinate
        key (str): 激活键 / Activation key
        color (int): 颜色代码 / Color code
    """

    text: str = ""  # 显示文本 / Display text
    x: int = -1  # x坐标 / x-coordinate
    y: int = -1  # y坐标 / y-coordinate
    key: str = ""  # 激活键 / Activation key
    color: int = 0  # 颜色代码 / Color code

    def __init__(self, text: str, key: str = "", handler=None, color: int = -1) -> None:
        """
        初始化TUI项 / Initialize TUI item

        Args:
            text (str): 显示文本 / Display text
            key (str, optional): 激活键 / Activation key. Defaults to "".
            handler (callable, optional): 处理函数 / Handler function. Defaults to None.
            color (int, optional): 颜色代码 / Color code. Defaults to -1.
        """
        self.text = text
        self.key = key
        self.handler = handler
        self.color = color

    def try_to_handle(self) -> None:
        """
        尝试执行处理函数 / Try to execute handler function
        """
        if self.handler:
            self.handler()


def generate_new_ssh_key() -> None:
    """
    生成新的SSH密钥对 / Generate new SSH key pair

    使用系统ssh-keygen命令生成新的SSH密钥对 /
    Generate new SSH key pair using system's ssh-keygen command
    """
    os.system("ssh-keygen")


def backup_current_user() -> None:
    """
    备份当前用户的SSH配置 / Backup current user's SSH configuration

    当前未实现，占位函数 / Currently not implemented. Place holder function only.
    """


def restore_current_user() -> None:
    """
    恢复当前用户的SSH配置 / Restore current user's SSH configuration

    当前未实现，占位函数 / Currently not implemented. Place holder function only.
    """


def get_all_user_list() -> List[str]:
    """
    获取所有系统用户列表 / Retrieve list of all system users

    Returns:
        List[str]: 包含所有系统用户名的列表 / List containing usernames of all system users
    """
    result: List[str] = ["root"]

    # Walk "/home"
    for root, dirs, files in os.walk("/home"):
        for dir_name in dirs:
            result.append(dir_name)

    return result


def backup_all_user() -> None:
    """
    备份所有用户的SSH配置 / Backup SSH configuration for all users

    当前未实现，占位函数 / Currently not implemented. Place holder function only.
    """


def restore_all_user() -> None:
    """
    恢复所有用户的SSH配置 / Restore SSH configuration for all users

    当前未实现，占位函数 / Currently not implemented. Place holder function only.
    """


def init_main_interface_content() -> List[TuiItem]:
    """
    初始化并返回主界面内容 / Initialize and return main interface content

    Returns:
        List[TuiItem]: 包含所有TUI项实例的列表 / List containing all TuiItem instances for display
    """
    str_list: List[TuiItem] = []

    str_list.append(TuiItem("SSH Helper - Group Center Client", color=1))
    str_list.append(TuiItem(""))

    str_list.append(TuiItem(f"System:{system_name}"))
    if is_root_user:
        str_list.append(TuiItem("With 'root' user to run this program"))

    str_list.append(TuiItem(""))

    # str_list.append(TuiItem("Generate New 'SSH key'", key="c", handler=generate_new_ssh_key))

    str_list.append(
        TuiItem("Backup Current User", key="1", handler=backup_current_user)
    )
    str_list.append(
        TuiItem("Restore Current User", key="2", handler=restore_current_user)
    )

    if is_root_user:
        str_list.append(
            TuiItem("Backup All User(Root Only)", key="3", handler=backup_current_user)
        )
        str_list.append(
            TuiItem(
                "Restore All User(Root Only)", key="4", handler=restore_current_user
            )
        )

    str_list.append(TuiItem(""))
    str_list.append(TuiItem("Exit", key="q", handler=lambda: exit(0)))

    return str_list


def main_interface(stdscr) -> None:
    """
    主界面渲染函数 / Main interface rendering function

    使用curses库渲染界面 / Render interface using curses library

    Args:
        stdscr: curses提供的主窗口对象 / Main window object provided by curses
    """
    # Clear screen
    stdscr.clear()

    # Set up the screen
    # Hide the cursor
    curses.curs_set(0)
    # Disable the input buffer
    stdscr.nodelay(1)

    # Create a new window
    height, width = stdscr.getmaxyx()
    win = curses.newwin(height, width, 0, 0)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
    item_with_key_color_index = 3

    # Draw a box around the window
    win.box()

    # Init content
    tui_list = init_main_interface_content()
    for i, tui_item in enumerate(tui_list):
        key_tip = ""
        if tui_item.key:
            key_tip = f"({tui_item.key})"

        if tui_item.color > 0:
            win.addstr(
                i + 1, 2, key_tip + tui_item.text, curses.color_pair(tui_item.color)
            )
        else:
            if tui_item.key:
                win.addstr(
                    i + 1,
                    2,
                    key_tip + tui_item.text,
                    curses.color_pair(item_with_key_color_index),
                )
            else:
                win.addstr(i + 1, 2, key_tip + tui_item.text)

    # Refresh the window
    win.refresh()

    try:
        # Handle key input
        global wait_key_input
        while wait_key_input:
            key = win.getkey()

            for tui_item in tui_list:
                if not tui_item.key:
                    continue

                if key == tui_item.key:
                    tui_item.try_to_handle()
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


def signal_handler(signal: int, frame: Any) -> None:
    """
    处理系统信号以在退出前清理资源 / Handle system signals to clean up resources before exit
    """
    global wait_key_input
    wait_key_input = False

    sys.exit(0)


def init_tui() -> None:
    """
    初始化TUI环境并设置信号处理程序 / Initialize TUI environment and setup signal handlers
    """
    # Register the signal handler
    # Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Init curses
    curses.wrapper(main_interface)


def main() -> None:
    """
    TUI应用程序的主入口 / Main entry point for the TUI application
    """
    init_tui()


if __name__ == "__main__":
    main()

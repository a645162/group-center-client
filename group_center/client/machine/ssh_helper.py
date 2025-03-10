import argparse
import os
import platform
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

from group_center.client.machine.feature.ssh.ssh_helper_linux import LinuxUserSsh

console = Console()
from group_center.core.group_center_machine import setup_group_center_by_opt
from group_center.utils.linux.linux_system import is_run_with_sudo

system_name = platform.system()

is_linux = system_name == "Linux"
is_root_user = is_linux and os.geteuid() == 0


class OptionItem:
    """选项项类 / Option item class"""

    text: str = ""  # 显示文本 / Display text
    key: str = ""  # 快捷键 / Shortcut key
    color: str = ""  # 颜色 / Color

    def __init__(self, text: str, key: str = "", handler=None, color: str = ""):
        """
        初始化选项项 / Initialize option item

        Args:
            text (str): 显示文本 / Display text
            key (str, optional): 快捷键 / Shortcut key. Defaults to "".
            handler (callable, optional): 处理函数 / Handler function. Defaults to None.
            color (str, optional): 颜色 / Color. Defaults to "".
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


def print_color_bool(text: str, is_success: bool) -> None:
    """
    打印带有颜色的布尔结果 / Print colored boolean result

    Args:
        text (str): 文本内容 / Text content
        is_success (bool): 成功状态 / Success status
    """
    style = "bold green" if is_success else "bold red"
    console.print(text, style=style)


def generate_new_ssh_key() -> None:
    """
    生成新的 SSH 密钥对 / Generate new SSH key pair

    使用系统ssh-keygen命令生成新的SSH密钥对 / Generate new SSH key pair using system ssh-keygen command
    """
    os.system("ssh-keygen")


def backup_current_user(user_name: str = "") -> None:
    """
    备份当前用户的 SSH 配置 / Backup current user's SSH configuration

    Args:
        user_name (str, optional): 用户名，默认为当前用户 / Username, defaults to current user
    """
    linux_user_ssh = LinuxUserSsh(user_name=user_name)

    result_backup_authorized_keys = linux_user_ssh.backup_authorized_keys()
    print_color_bool(
        "Backup authorized_keys:" + str(result_backup_authorized_keys),
        result_backup_authorized_keys,
    )

    result_backup_ssh_key_pair = linux_user_ssh.backup_ssh_key_pair()
    print_color_bool(
        "Backup Key pair:" + str(result_backup_ssh_key_pair), result_backup_ssh_key_pair
    )


def restore_current_user(user_name: str = "") -> None:
    """
    恢复当前用户的 SSH 配置 / Restore current user's SSH configuration

    Args:
        user_name (str, optional): 用户名，默认为当前用户 / Username, defaults to current user
    """
    restore_current_user_authorized_keys(user_name=user_name)
    restore_current_user_key_pair(user_name=user_name)


def restore_current_user_authorized_keys(user_name: str = "") -> None:
    """
    恢复当前用户的authorized_keys文件 / Restore current user's authorized_keys file

    Args:
        user_name (str, optional): 用户名，默认为当前用户 / Username, defaults to current user
    """
    linux_user_ssh = LinuxUserSsh(user_name=user_name)

    result = linux_user_ssh.restore_authorized_keys()
    print_color_bool("Restore authorized_keys:" + str(result), result)


def restore_current_user_key_pair(user_name: str = "") -> None:
    """
    恢复当前用户的SSH密钥对 / Restore current user's SSH key pairs

    Args:
        user_name (str, optional): 用户名，默认为当前用户 / Username, defaults to current user
    """
    linux_user_ssh = LinuxUserSsh(user_name=user_name)

    result = linux_user_ssh.restore_ssh_key_pair()
    print_color_bool("Restore Key pair:" + str(result), result)


def get_all_user_list() -> List[str]:
    """
    获取所有用户列表 / Get list of all users

    Returns:
        List[str]: 所有用户名的列表 / List of all usernames
    """
    result: List[str] = []

    # Walk "/home"
    for root, dirs, files in os.walk("/home"):
        for dir_name in dirs:
            result.append(dir_name)

        break

    return result


def backup_all_user() -> None:
    """
    备份所有用户的 SSH 配置 / Backup SSH configuration for all users

    遍历/home目录下的所有用户并备份其SSH配置 /
    Iterate through all users in /home directory and backup their SSH configuration
    """
    user_list = get_all_user_list()
    for user_name in user_list:
        print("Working for " + user_name)
        backup_current_user(user_name)
        print()


def restore_all_user() -> None:
    """
    恢复所有用户的 SSH 配置 / Restore SSH configuration for all users

    遍历/home目录下的所有用户并恢复其SSH配置 /
    Iterate through all users in /home directory and restore their SSH configuration
    """
    user_list = get_all_user_list()
    for user_name in user_list:
        print("Working for " + user_name)
        restore_current_user(user_name)
        print()


def init_main_interface_content() -> List[OptionItem]:
    """
    初始化主界面内容 / Initialize main interface content

    Returns:
        List[OptionItem]: 界面选项列表 / List of interface options
    """
    str_list: List[OptionItem] = []

    str_list.append(OptionItem("SSH Helper - Group Center Client", color="green"))
    str_list.append(OptionItem(""))

    str_list.append(OptionItem(f"System:{system_name}"))
    if is_root_user:
        str_list.append(OptionItem("With 'root' user to run this program"))

    str_list.append(OptionItem(""))

    str_list.append(
        OptionItem("Generate New 'SSH key'", key="c", handler=generate_new_ssh_key)
    )

    str_list.append(
        OptionItem("Backup Current User", key="1", handler=backup_current_user)
    )
    str_list.append(
        OptionItem("Restore Current User", key="2", handler=restore_current_user)
    )
    str_list.append(
        OptionItem(
            " - Restore Current User(authorized_key)",
            key="3",
            handler=restore_current_user_authorized_keys,
        )
    )
    str_list.append(
        OptionItem(
            " - Restore Current User(Key pair)",
            key="4",
            handler=restore_current_user_key_pair,
        )
    )

    if is_root_user:
        str_list.append(
            OptionItem("Backup All User(Root Only)", key="5", handler=backup_all_user)
        )
        str_list.append(
            OptionItem("Restore All User(Root Only)", key="6", handler=restore_all_user)
        )

    str_list.append(OptionItem(""))
    str_list.append(OptionItem("Exit", key="q", handler=lambda: exit(0)))

    return str_list


def hello() -> None:
    """
    显示欢迎信息 / Display welcome message

    使用rich库显示带样式的欢迎信息 / Display styled welcome message using rich library
    """
    console.print(
        Panel.fit(
            "[bold green]Hello, Group Center Client![/]",
            border_style="green",
            padding=(1, 4),
        )
    )


def press_enter_to_continue() -> None:
    """
    等待用户按下回车继续 / Wait for user to press Enter to continue

    如果用户输入'q'则退出程序 / Exit program if user inputs 'q'
    """
    input_text = Prompt.ask("[blue]Press 'Enter' to continue...[/]", default="")
    if input_text.lower() == "q":
        exit(0)


def cli_main_cycle() -> None:
    """
    主界面循环 / Main interface loop

    显示主界面并处理用户输入 / Display main interface and handle user input
    """
    interface_content: List[OptionItem] = init_main_interface_content()

    def print_main_interface_content():
        table = Table(show_header=False, box=None, padding=(0, 2))

        for item in interface_content:
            key_tip = f"({item.key}) " if item.key else ""
            text = key_tip + item.text

            if item.color:
                style = item.color
            else:
                style = "blue" if key_tip else ""

            table.add_row(Text(text, style=style))

        panel = Panel(
            table,
            title="[bold green]SSH Helper - Group Center Client[/]",
            border_style="blue",
            padding=(1, 4),
        )
        console.print(panel)

    print_main_interface_content()

    # Waiting for user input
    key = Prompt.ask("[blue]Please input the key[/]")
    # key = input("Please input the key:").strip()

    found = False
    for item in interface_content:
        if item.key == key:
            found = True
            console.print(f"[bold green]Go to => {item.text}[/]")
            item.try_to_handle()
            break

    if not found:
        console.print("[bold red]Invalid key![/]")

    press_enter_to_continue()


def init_cli() -> None:
    """
    初始化命令行界面 / Initialize command line interface

    显示欢迎信息并进入主循环 / Display welcome message and enter main loop
    """
    hello()

    while True:
        cli_main_cycle()


def get_options() -> argparse.Namespace:
    """
    获取命令行选项 / Get command line options

    Returns:
        argparse.Namespace: 解析后的选项对象 / Parsed options object
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--center-name", type=str, default="")
    parser.add_argument("--center-password", type=str, default="")

    parser.add_argument(
        "-b",
        "--backup",
        help="Backup Mode",
        action="store_true",
    )

    parser.add_argument(
        "-r",
        "--restore",
        help="Restore Mode",
        action="store_true",
    )

    parser.add_argument(
        "-a",
        "--all",
        help="All User Mode",
        action="store_true",
    )

    opt = parser.parse_args()

    return opt


def main() -> None:
    """
    主程序入口 / Main program entry point

    初始化日志级别并处理命令行参数 / Initialize log level and handle command line arguments
    """
    from group_center.utils.log.log_level import get_log_level

    log_level = get_log_level()
    log_level.current_level = log_level.INFO

    opt = get_options()

    setup_group_center_by_opt(opt)

    backup_mode = opt.backup
    restore_mode = opt.restore

    if not (backup_mode or restore_mode):
        init_cli()
        return

    all_user_mode = opt.all and is_run_with_sudo()

    if not (backup_mode ^ restore_mode):
        print_color_bool("Cannot backup and restore at the same time!", False)
        return

    if backup_mode:
        if all_user_mode:
            backup_all_user()
        else:
            backup_current_user()
    else:
        if all_user_mode:
            restore_all_user()
        else:
            restore_current_user()


if __name__ == "__main__":
    main()

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
    text: str = ""

    key: str = ""

    color: str

    def __init__(self, text: str, key: str = "", handler=None, color: str = ""):
        self.text = text
        self.key = key
        self.handler = handler
        self.color = color

    def try_to_handle(self):
        if self.handler:
            self.handler()


def print_color_bool(text: str, is_success: bool):
    style = "bold green" if is_success else "bold red"
    console.print(text, style=style)


def generate_new_ssh_key():
    os.system("ssh-keygen")


def backup_current_user(user_name=""):
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


def restore_current_user(user_name=""):
    restore_current_user_authorized_keys(user_name=user_name)
    restore_current_user_key_pair(user_name=user_name)


def restore_current_user_authorized_keys(user_name=""):
    linux_user_ssh = LinuxUserSsh(user_name=user_name)

    result = linux_user_ssh.restore_authorized_keys()
    print_color_bool("Restore authorized_keys:" + str(result), result)


def restore_current_user_key_pair(user_name=""):
    linux_user_ssh = LinuxUserSsh(user_name=user_name)

    result = linux_user_ssh.restore_ssh_key_pair()
    print_color_bool("Restore Key pair:" + str(result), result)


def get_all_user_list() -> List[str]:
    result: List[str] = []

    # Walk "/home"
    for root, dirs, files in os.walk("/home"):
        for dir_name in dirs:
            result.append(dir_name)

        break

    return result


def backup_all_user():
    user_list = get_all_user_list()
    for user_name in user_list:
        print("Working for " + user_name)
        backup_current_user(user_name)
        print()


def restore_all_user():
    user_list = get_all_user_list()
    for user_name in user_list:
        print("Working for " + user_name)
        restore_current_user(user_name)
        print()


def init_main_interface_content() -> List[OptionItem]:
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


def hello():
    console.print(
        Panel.fit(
            "[bold green]Hello, Group Center Client![/]",
            border_style="green",
            padding=(1, 4),
        )
    )


def press_enter_to_continue():
    input_text = Prompt.ask("[blue]Press 'Enter' to continue...[/]", default="")
    if input_text.lower() == "q":
        exit(0)


def cli_main_cycle():
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


def init_cli():
    hello()

    while True:
        cli_main_cycle()


def get_options():
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


def main():
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

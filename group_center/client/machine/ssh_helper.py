import argparse
import os
import platform

from typing import List

from termcolor import colored

from group_center.client.machine.feature.ssh.ssh_helper_linux import LinuxUserSsh
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
    if is_success:
        print(colored(text, "green"))
    else:
        print(colored(text, "red"))


def generate_new_ssh_key():
    os.system("ssh-keygen")


def backup_current_user(user_name=""):
    linux_user_ssh = LinuxUserSsh(user_name=user_name)

    result_backup_authorized_keys = linux_user_ssh.backup_authorized_keys()
    print_color_bool(
        "Backup authorized_keys:" + str(result_backup_authorized_keys),
        result_backup_authorized_keys
    )

    result_backup_ssh_key_pair = linux_user_ssh.backup_ssh_key_pair()
    print_color_bool(
        "Backup Key pair:" + str(result_backup_ssh_key_pair),
        result_backup_ssh_key_pair
    )


def restore_current_user(user_name=""):
    restore_current_user_authorized_keys(user_name=user_name)
    restore_current_user_key_pair(user_name=user_name)


def restore_current_user_authorized_keys(user_name=""):
    linux_user_ssh = LinuxUserSsh(user_name=user_name)

    result = linux_user_ssh.restore_authorized_keys()
    print_color_bool(
        "Restore authorized_keys:" + str(result),
        result
    )


def restore_current_user_key_pair(user_name=""):
    linux_user_ssh = LinuxUserSsh(user_name=user_name)

    result = linux_user_ssh.restore_ssh_key_pair()
    print_color_bool(
        "Restore Key pair:" + str(result),
        result
    )


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

    str_list.append(OptionItem("Generate New 'SSH key'", key="c", handler=generate_new_ssh_key))

    str_list.append(OptionItem(
        "Backup Current User", key="1",
        handler=backup_current_user))
    str_list.append(OptionItem(
        "Restore Current User", key="2",
        handler=restore_current_user))
    str_list.append(OptionItem(
        "Restore Current User(authorized_key)", key="3",
        handler=restore_current_user_authorized_keys))
    str_list.append(OptionItem(
        "Restore Current User(Key pair)", key="4",
        handler=restore_current_user_key_pair))

    if is_root_user:
        str_list.append(OptionItem("Backup All User(Root Only)", key="5", handler=backup_all_user))
        str_list.append(OptionItem("Restore All User(Root Only)", key="6", handler=restore_all_user))

    str_list.append(OptionItem(""))
    str_list.append(OptionItem("Exit", key="q", handler=lambda: exit(0)))

    return str_list


def hello():
    print(colored("Hello, Group Center Client!", "green"))
    print()


def press_enter_to_continue():
    input_text = input("Press 'Enter' to continue...").strip()
    if input_text == "q":
        exit(0)


def cli_main_cycle():
    interface_content = init_main_interface_content()

    def print_main_interface_content():
        for item in interface_content:
            key_tip = f"({item.key})" if item.key else ""
            text = key_tip + item.text

            if item.color == "":
                if key_tip:
                    print(colored(text, color="blue"))
                else:
                    print(text)
            else:
                print(colored(text, color=item.color))

        print()

    print_main_interface_content()

    # Waiting for user input
    key = input("Please input the key:").strip()

    found = False
    for item in interface_content:
        if item.key == key:
            found = True
            print(colored("Go to => " + item.text, "green"))
            item.try_to_handle()
            break

    if not found:
        print(colored("Invalid key!", "red"))

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

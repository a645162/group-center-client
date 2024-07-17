import os
import platform

from typing import List, Any

from termcolor import colored

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


def generate_new_ssh_key():
    os.system("ssh-keygen")


def backup_current_user():
    pass


def restore_current_user():
    pass


def get_all_user_list() -> List[str]:
    result: List[str] = ["root"]

    # Walk "/home"
    for root, dirs, files in os.walk("/home"):
        for dir_name in dirs:
            result.append(dir_name)

    return result


def backup_all_user():
    pass


def restore_all_user():
    pass


def init_main_interface_content() -> List[OptionItem]:
    str_list: List[OptionItem] = []

    str_list.append(OptionItem("SSH Helper - Group Center Client", color="green"))
    str_list.append(OptionItem(""))

    str_list.append(OptionItem(f"System:{system_name}"))
    if is_root_user:
        str_list.append(OptionItem("With 'root' user to run this program"))

    str_list.append(OptionItem(""))

    str_list.append(OptionItem("Generate New 'SSH key'", key="c", handler=generate_new_ssh_key))

    str_list.append(OptionItem("Backup Current User", key="1", handler=backup_current_user))
    str_list.append(OptionItem("Restore Current User", key="2", handler=restore_current_user))

    if is_root_user:
        str_list.append(OptionItem("Backup All User(Root Only)", key="3", handler=backup_current_user))
        str_list.append(OptionItem("Restore All User(Root Only)", key="4", handler=restore_current_user))

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


def main():
    init_cli()


if __name__ == "__main__":
    main()

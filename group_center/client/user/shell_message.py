import argparse

from group_center.user_tools import *


def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n", "--user-name",
        help="User name",
        type=str, default=""
    )
    parser.add_argument(
        "-m", "--message",
        help="Message Content",
        type=str, default=""
    )
    parser.add_argument(
        "-s",
        "--screen",
        help="Include screen session name",
        action="store_true",
    )

    opt = parser.parse_args()

    return opt


def main():
    opt = get_options()

    user_name = str(opt.user_name).strip()
    message = str(opt.message).strip()
    screen_name = ""

    if not message:
        print("No message")
        return

    if opt.screen:
        screen_name = ENV_SCREEN_SESSION_NAME()

    if screen_name:
        screen_name = f"[{screen_name}]"

    message = f"{screen_name}{message}"

    # Enable Group Center
    group_center_set_is_valid()
    group_center_set_user_name(user_name)

    push_message(message)


if __name__ == '__main__':
    main()

import argparse

from group_center.user_env import ENV_SCREEN_SESSION_NAME
from group_center.user_tools import (
    group_center_set_user_name,
    group_center_set_is_valid,
    push_message,
)


def get_options() -> argparse.Namespace:
    """获取命令行参数 / Get command line arguments

    Returns:
        argparse.Namespace: 包含解析后参数的命名空间 / Namespace containing parsed arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n", "--user-name", help="用户名称 / User name", type=str, default=""
    )
    parser.add_argument("message", help="消息内容 / Message content", type=str)
    parser.add_argument(
        "-s",
        "--screen",
        help="包含屏幕会话名称 / Include screen session name",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="是否输出详细信息 / Whether to output verbose information",
        action="store_true",
    )

    opt = parser.parse_args()

    return opt


def main():
    """主函数，处理 shell 消息 / Main function to handle shell messages"""
    opt = get_options()

    user_name = str(opt.user_name).strip()
    message = str(opt.message).strip()
    screen_name = ""

    if not message:
        print("没有消息 / No message")
        return

    if opt.screen:
        screen_name = ENV_SCREEN_SESSION_NAME()
        # print("Screen", screen_name)

    if screen_name:
        screen_name = f"[{screen_name}] "

    message = f"{screen_name}{message}"

    # 启用 Group Center / Enable Group Center
    group_center_set_is_valid(enable=True)
    group_center_set_user_name(user_name)

    if push_message(message):
        print("消息已发送! / Message sent!")
    else:
        print("消息发送失败！ / Message send failed!!!")


if __name__ == "__main__":
    main()

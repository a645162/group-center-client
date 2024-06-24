import os

user_name_black_list = ["ubuntu", "root", "public"]


def get_current_user_name() -> str:
    try:
        # 获取当前用户的用户名
        current_user = os.getlogin()

        # 检查用户名是否在黑名单中
        if current_user in user_name_black_list:
            return ""

        # 如果不在黑名单中，返回用户名
        return current_user.strip()
    except Exception:
        return ""


if __name__ == "__main__":
    current_user_name = get_current_user_name()
    print(current_user_name)
    print()

# 全局用户名 (Global user name)
global_user_name: str = ""

# 消息推送开关 (Message push enable flag)
global_enable: bool = False


def group_center_set_is_valid(enable: bool = True) -> None:
    """启用/禁用消息推送 (Enable/Disable message push)

    Args:
        enable (bool, optional): 是否启用 (Enable flag). Defaults to True.
    """
    global global_enable
    global_enable = enable


def group_center_set_user_name(new_user_name: str) -> None:
    """设置全局用户名 (Set global user name)

    Args:
        new_user_name (str): 新用户名 (New user name)
    """
    global global_user_name
    global_user_name = new_user_name.strip()

    if not global_user_name:
        global_user_name = get_current_login_user_name()


def global_enable_status() -> bool:
    """获取全局消息推送开关状态 (Get global message push enable status)

    Returns:
        bool: 消息推送开关状态 (Message push enable status)
    """
    global global_enable
    return global_enable


def global_user_name_status() -> str:
    """获取全局用户名 (Get global user name)

    Returns:
        str: 全局用户名 (Global user name)
    """
    global global_user_name
    return global_user_name


def get_current_login_user_name() -> str:
    """获取当前登录用户名 (Get current login user name)

    Returns:
        str: 当前登录用户名 (Current login user name)
    """
    import os

    return os.getlogin()

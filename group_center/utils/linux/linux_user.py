import os
import subprocess
from typing import Optional, List

user_name_black_list = [
    "ubuntu",
    "root",
    "public",
    "linuxbrew",
]  # 用户名黑名单 / Username blacklist


def create_linux_user(username: str, password: str) -> bool:
    """创建Linux用户
    Create Linux user

    Args:
        username: 用户名 / Username
        password: 密码 / Password

    Returns:
        bool: 如果用户创建成功返回True，否则返回False / Returns True if user created successfully, False otherwise
    """
    if check_linux_user_is_exist(username):
        return True

    # Create User
    # -m: create home directory
    create_user_cmd = f'useradd -m "{username}" -s /bin/bash'
    create_user_process = subprocess.run(create_user_cmd, shell=True, check=False)

    # Set Password
    set_password_cmd = f"echo {username}:{password} | chpasswd"
    set_password_process = subprocess.run(set_password_cmd, shell=True, check=False)

    return create_user_process.returncode == 0 and set_password_process.returncode == 0


def check_linux_user_is_exist(username: str) -> bool:
    """检查Linux用户是否存在
    Check if Linux user exists

    Args:
        username: 用户名 / Username

    Returns:
        bool: 如果用户存在返回True，否则返回False / Returns True if user exists, False otherwise
    """
    check_user_cmd = f"id -u {username}"
    check_user_process = subprocess.run(
        check_user_cmd, shell=True, capture_output=True, text=True
    )

    return check_user_process.returncode == 0


def reset_password(username: str, password: Optional[str] = None) -> bool:
    """重置Linux用户密码
    Reset Linux user password

    Args:
        username: 用户名 / Username
        password: 新密码，如果未提供则使用用户名作为密码 / New password, if not provided, use username as password

    Returns:
        bool: 如果密码重置成功返回True，否则返回False / Returns True if password reset successfully, False otherwise
    """
    if password is None:
        password = username
    reset_password_cmd = f"echo {username}:{password} | chpasswd"
    reset_password_process = subprocess.run(reset_password_cmd, shell=True, check=False)
    return reset_password_process.returncode == 0


def delete_linux_user(username: str, delete_home: bool = True) -> None:
    """删除Linux用户
    Delete Linux user

    Args:
        username: 用户名 / Username
        delete_home: 是否删除用户主目录 / Whether to delete user home directory
    """
    if delete_home:
        subprocess.run(f"userdel -r {username}", shell=True, check=True)
        # subprocess.run(f'rm -rf /home/{username}', shell=True, check=True)
    else:
        subprocess.run(f"userdel {username}", shell=True, check=True)


def get_user_home_directory(username: str) -> str:
    """获取用户主目录路径
    Get user home directory path

    Args:
        username: 用户名 / Username

    Returns:
        str: 用户主目录路径 / User home directory path
    """
    get_home_cmd = f"getent passwd {username} | cut -d: -f6"
    get_home_process = subprocess.run(
        get_home_cmd, shell=True, capture_output=True, text=True
    )

    return get_home_process.stdout.strip()


def check_group_is_exist(group_name: str) -> bool:
    """检查Linux用户组是否存在
    Check if Linux group exists

    Args:
        group_name: 用户组名 / Group name

    Returns:
        bool: 如果用户组存在返回True，否则返回False / Returns True if group exists, False otherwise
    """
    check_group_cmd = f"getent group {group_name}"
    check_group_process = subprocess.run(
        check_group_cmd, shell=True, capture_output=True, text=True
    )

    return check_group_process.returncode == 0


def add_user_to_group(username: str, group_name: str) -> bool:
    """将用户添加到用户组
    Add user to group

    Args:
        username: 用户名 / Username
        group_name: 用户组名 / Group name

    Returns:
        bool: 如果添加成功返回True，否则返回False / Returns True if added successfully, False otherwise
    """
    if not check_group_is_exist(group_name):
        return False

    add_user_to_group_cmd = f"usermod -a -G {group_name} {username}"
    add_user_to_group_process = subprocess.run(
        add_user_to_group_cmd, shell=True, check=True
    )

    return add_user_to_group_process.returncode == 0


def get_user_groups(username: str) -> str:
    """获取用户所属的用户组
    Get groups that the user belongs to

    Args:
        username: 用户名 / Username

    Returns:
        str: 用户所属的用户组列表，以空格分隔 / List of groups the user belongs to, separated by spaces
    """
    get_user_groups_cmd = f"id -Gn {username}"
    get_user_groups_process = subprocess.run(
        get_user_groups_cmd, shell=True, capture_output=True, text=True
    )

    return get_user_groups_process.stdout.strip()


def get_user_groups_list(username: str) -> List[str]:
    """获取用户所属的用户组列表
    Get list of groups that the user belongs to

    Args:
        username: 用户名 / Username

    Returns:
        List[str]: 用户所属的用户组列表 / List of groups the user belongs to
    """
    result_list: List[str] = get_user_groups(username).split(" ")

    result_list = [item.strip() for item in result_list if len(item.strip()) > 0]

    return result_list


def get_uid(username: str) -> int:
    """获取用户的UID
    Get user's UID

    Args:
        username: 用户名 / Username

    Returns:
        int: 用户的UID，如果获取失败返回0 / User's UID, returns 0 if failed to get
    """
    try:
        result = subprocess.run(
            ["id", "-u", username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            return int(result.stdout.strip())
        else:
            return 0
    except Exception:
        return 0


def get_gid(username: str) -> int:
    """获取用户的GID
    Get user's GID

    Args:
        username: 用户名 / Username

    Returns:
        int: 用户的GID，如果获取失败返回0 / User's GID, returns 0 if failed to get
    """
    try:
        result = subprocess.run(
            ["id", "-g", username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            return int(result.stdout.strip())
        else:
            return 0
    except Exception:
        return 0


def set_uid(username: str, uid: int) -> bool:
    """设置用户的UID
    Set user's UID

    Args:
        username: 用户名 / Username
        uid: 新的UID / New UID

    Returns:
        bool: 如果设置成功返回True，否则返回False / Returns True if set successfully, False otherwise
    """
    try:
        result = subprocess.run(
            ["usermod", "-u", str(uid), username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception:
        return False


def set_gid(username: str, gid: int) -> bool:
    """设置用户的GID
    Set user's GID

    Args:
        username: 用户名 / Username
        gid: 新的GID / New GID

    Returns:
        bool: 如果设置成功返回True，否则返回False / Returns True if set successfully, False otherwise
    """
    try:
        result = subprocess.run(
            ["usermod", "-g", str(gid), username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception:
        return False


def get_current_user_name() -> str:
    """获取当前用户名
    Get current username

    Returns:
        str: 当前用户名，如果用户名在黑名单中或获取失败返回空字符串 / Current username, returns empty string if username is in blacklist or failed to get
    """
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
    # print("Is Exist:", check_linux_user_is_exist("userpy"))
    # print("Is Exist:", check_linux_user_is_exist("userpy0"))

    # create_linux_user("userpy", "password")

    print(get_user_home_directory("root"))

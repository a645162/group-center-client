import os
import subprocess
from typing import Optional, List

user_name_black_list = ["ubuntu", "root", "public"]


def create_linux_user(username: str, password: str) -> bool:
    if check_linux_user_is_exist(username):
        return True

    # Create User
    # -m: create home directory
    create_user_cmd = f'useradd -m "{username}" -s /bin/bash'
    create_user_process = (
        subprocess.run(create_user_cmd, shell=True, check=False))

    # Set Password
    set_password_cmd = f'echo {username}:{password} | chpasswd'
    set_password_process = \
        subprocess.run(set_password_cmd, shell=True, check=False)

    return (
            create_user_process.returncode == 0 and
            set_password_process.returncode == 0
    )


def check_linux_user_is_exist(username: str):
    check_user_cmd = f'id -u {username}'
    check_user_process = subprocess.run(
        check_user_cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    return check_user_process.returncode == 0


def reset_password(username: str, password: Optional[str] = None) -> bool:
    if password is None:
        password = username
    reset_password_cmd = f'echo {username}:{password} | chpasswd'
    reset_password_process = \
        subprocess.run(reset_password_cmd, shell=True, check=False)
    return reset_password_process.returncode == 0


def delete_linux_user(username: str, delete_home: bool = True):
    if delete_home:
        subprocess.run(f'userdel -r {username}', shell=True, check=True)
        # subprocess.run(f'rm -rf /home/{username}', shell=True, check=True)
    else:
        subprocess.run(f'userdel {username}', shell=True, check=True)


def get_user_home_directory(username: str):
    get_home_cmd = f'getent passwd {username} | cut -d: -f6'
    get_home_process = subprocess.run(get_home_cmd, shell=True, capture_output=True, text=True)

    return get_home_process.stdout.strip()


def check_group_is_exist(group_name: str):
    check_group_cmd = f'getent group {group_name}'
    check_group_process = subprocess.run(check_group_cmd, shell=True, capture_output=True, text=True)

    return check_group_process.returncode == 0


def add_user_to_group(username: str, group_name: str) -> bool:
    if not check_group_is_exist(group_name):
        return False

    add_user_to_group_cmd = f'usermod -a -G {group_name} {username}'
    add_user_to_group_process = subprocess.run(add_user_to_group_cmd, shell=True, check=True)

    return add_user_to_group_process.returncode == 0


def get_user_groups(username: str) -> str:
    get_user_groups_cmd = f'id -Gn {username}'
    get_user_groups_process = \
        subprocess.run(
            get_user_groups_cmd,
            shell=True, capture_output=True, text=True
        )

    return get_user_groups_process.stdout.strip()


def get_user_groups_list(username: str) -> List[str]:
    result_list: List[str] = get_user_groups(username).split(" ")

    result_list = [
        item.strip()
        for item in result_list
        if len(item.strip()) > 0
    ]

    return result_list


def get_uid(username):
    try:
        result = subprocess.run(
            ['id', '-u', username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return int(result.stdout.strip())
        else:
            return 0
    except Exception as e:
        return 0


def get_gid(username):
    try:
        result = subprocess.run(
            ['id', '-g', username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return int(result.stdout.strip())
        else:
            return 0
    except Exception as e:
        return 0


def set_uid(username, uid):
    try:
        result = subprocess.run(
            ['usermod', '-u', str(uid), username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False


def set_gid(username, gid):
    try:
        result = subprocess.run(
            ['usermod', '-g', str(gid), username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False


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


if __name__ == '__main__':
    # print("Is Exist:", check_linux_user_is_exist("userpy"))
    # print("Is Exist:", check_linux_user_is_exist("userpy0"))

    # create_linux_user("userpy", "password")

    print(get_user_home_directory("root"))

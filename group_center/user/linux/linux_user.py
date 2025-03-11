from typing import List

from group_center.user.system_user import SystemUser
from group_center.utils.linux.linux_system import (
    is_run_on_linux,
)
from group_center.utils.linux.linux_user import (
    check_linux_user_is_exist,
    get_user_home_directory,
    create_linux_user,
    reset_password,
    delete_linux_user,
    add_user_to_group,
    get_user_groups,
    get_user_groups_list,
    get_uid,
    set_uid,
    get_gid,
    set_gid,
)


class LinuxUser(SystemUser):
    """Linux用户类 (Linux User Class)
    Linux User Class

    继承自SystemUser，提供Linux用户管理功能
    Inherits from SystemUser, provides Linux user management functionalities
    """

    def __init__(self, user_name: str):
        """初始化Linux用户 (Initialize Linux User)
        Initialize Linux User

        Args:
            user_name (str): 用户名 (User name)
        """
        if not is_run_on_linux():
            raise Exception("Current system is not linux")
        super().__init__(user_name=user_name)

    def is_exist(self) -> bool:
        """检查用户是否存在 (Check if user exists)
        Check if user exists

        Returns:
            bool: 用户是否存在 (Whether user exists)
        """
        return check_linux_user_is_exist(self.user_name)

    def get_home_directory(self) -> str:
        """获取用户主目录 (Get user home directory)
        Get user home directory

        Returns:
            str: 用户主目录路径 (User home directory path)
        """
        return get_user_home_directory(self.user_name)

    def create(self, password: str = "") -> bool:
        """创建用户 (Create user)
        Create user

        Args:
            password (str, optional): 用户密码 (User password). Defaults to "".

        Returns:
            bool: 是否创建成功 (Whether creation succeeded)
        """
        return create_linux_user(self.user_name, password)

    def reset_password(self, password: str = "") -> bool:
        """重置用户密码 (Reset user password)
        Reset user password

        Args:
            password (str, optional): 新密码 (New password). Defaults to "".

        Returns:
            bool: 是否重置成功 (Whether reset succeeded)
        """
        return reset_password(self.user_name, password)

    def delete(self, delete_home: bool = True) -> bool:
        """删除用户 (Delete user)
        Delete user

        Args:
            delete_home (bool, optional): 是否删除主目录 (Whether to delete home directory). Defaults to True.

        Returns:
            bool: 是否删除成功 (Whether deletion succeeded)
        """
        return delete_linux_user(self.user_name, delete_home)

    def add_to_group(self, group_name: str) -> bool:
        """将用户添加到组 (Add user to group)
        Add user to group

        Args:
            group_name (str): 组名 (Group name)

        Returns:
            bool: 是否添加成功 (Whether addition succeeded)
        """
        return add_user_to_group(self.user_name, group_name)

    def get_groups(self) -> str:
        """获取用户所属组 (Get user groups)
        Get user groups

        Returns:
            str: 用户所属组 (User groups)
        """
        return get_user_groups(self.user_name)

    def get_groups_list(self) -> List[str]:
        """获取用户所属组列表 (Get user groups list)
        Get user groups list

        Returns:
            List[str]: 用户所属组列表 (User groups list)
        """
        return get_user_groups_list(self.user_name)

    @property
    def uid(self):
        """获取用户ID (Get user ID)
        Get user ID

        Returns:
            int: 用户ID (User ID)
        """
        return get_uid(self.user_name)

    @uid.setter
    def uid(self, value):
        """设置用户ID (Set user ID)
        Set user ID

        Args:
            value (int): 新用户ID (New user ID)

        Raises:
            ValueError: 如果用户ID不是整数 (If user ID is not integer)
        """
        if not isinstance(value, int):
            raise ValueError("uid must be int")
        if value == get_uid(self.user_name):
            return
        set_uid(self.user_name, value)

    @property
    def gid(self):
        """获取组ID (Get group ID)
        Get group ID

        Returns:
            int: 组ID (Group ID)
        """
        return get_gid(self.user_name)

    @gid.setter
    def gid(self, value):
        """设置组ID (Set group ID)
        Set group ID

        Args:
            value (int): 新组ID (New group ID)

        Raises:
            ValueError: 如果组ID不是整数 (If group ID is not integer)
        """
        if not isinstance(value, int):
            raise ValueError("gid must be int")
        if value == get_gid(self.user_name):
            return
        set_gid(self.user_name, value)


if __name__ == "__main__":
    print()

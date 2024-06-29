from group_center.user.system_user import SystemUser
from group_center.utils.linux.linux_system import *
from group_center.utils.linux.linux_user import *


class LinuxUser(SystemUser):

    def __init__(self, user_name: str):
        if not is_run_on_linux():
            raise Exception("Current system is not linux")
        super().__init__(user_name=user_name)

    def is_exist(self) -> bool:
        return check_linux_user_is_exist(self.user_name)

    def get_home_directory(self) -> str:
        return get_user_home_directory(self.user_name)

    def create(self, password: str = "") -> bool:
        return create_linux_user(self.user_name, password)

    def reset_password(self, password: str = "") -> bool:
        return reset_password(self.user_name, password)

    def delete(self, delete_home: bool = True) -> bool:
        return delete_linux_user(self.user_name, delete_home)

    def add_to_group(self, group_name: str) -> bool:
        return add_user_to_group(self.user_name, group_name)

    def get_groups(self) -> str:
        return get_user_groups(self.user_name)

    def get_groups_list(self) -> List[str]:
        return get_user_groups_list(self.user_name)


if __name__ == "__main__":
    print()

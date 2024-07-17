import os
import shutil

# from group_center.utils.log.log_level import get_log_level
#
# log_level = get_log_level()
# log_level.current_level = log_level.DEBUG

from group_center.client.machine.feature. \
    ssh.ssh_key_pair_manager import fix_ssh_dir, SshKeyPairManager, restore_ssh_zip
from group_center.core.feature. \
    backup_user_file import upload_file, download_file
from group_center.utils.envs import get_a_tmp_dir
from group_center.utils.linux. \
    linux_user import get_current_user_name

from group_center.utils.log.logger import get_logger

logger = get_logger()


class LinuxUserSsh:
    __user_name: str = ""
    __tmp_dir_path: str = ""

    def __init__(self, user_name: str = ""):
        self.__user_name = user_name

    @property
    def user_name(self) -> str:
        if not self.__user_name:
            return get_current_user_name()

        return self.__user_name

    @property
    def home_dir(self) -> str:
        if not self.__user_name:
            return os.path.expanduser("~")

        return f"/home/{self.__user_name}"

    @property
    def ssh_dir(self) -> str:
        return os.path.join(self.home_dir, ".ssh")

    def fix_ssh_dir(self) -> None:
        fix_ssh_dir(self.ssh_dir)

    def __get_tmp_dir(self) -> str:
        if not self.__tmp_dir_path:
            self.__tmp_dir_path = get_a_tmp_dir()

        return self.__tmp_dir_path

    def __remove_tmp_dir(self) -> None:
        if os.path.exists(self.__tmp_dir_path):
            shutil.rmtree(self.__tmp_dir_path)

    def backup_authorized_keys(self):
        authorized_keys_file_path = os.path.join(self.ssh_dir, "authorized_keys")
        if not os.path.exists(authorized_keys_file_path):
            logger.info(f"authorized_keys file not found: {authorized_keys_file_path}")
            return

        upload_result = \
            upload_file(
                file_path=authorized_keys_file_path,
                target_api="/api/client/file/ssh_key",
                params={
                    "userNameEng": self.user_name
                }
            )

        return upload_result

    def backup_ssh_key_pair(self) -> bool:
        if not (
                os.path.exists(self.ssh_dir) and
                os.path.isdir(self.ssh_dir)
        ):
            return False

        key_pair_manager = \
            SshKeyPairManager(ssh_dir_path=self.ssh_dir)
        key_pair_manager.walk()

        if not key_pair_manager:
            return False

        tmp_dir = self.__get_tmp_dir()
        save_path = os.path.join(tmp_dir, "ssh_key_pair.zip")

        key_pair_manager.zip(zip_filename=save_path)

        upload_result = \
            upload_file(
                file_path=save_path,
                target_api="/api/client/file/ssh_key",
                params={
                    "userNameEng": self.user_name
                }
            )

        self.__remove_tmp_dir()
        return upload_result

    def restore_authorized_keys(self) -> bool:
        tmp_dir = self.__get_tmp_dir()
        file_name = "authorized_keys"
        tmp_file_path = os.path.join(tmp_dir, file_name)

        download_result = \
            download_file(
                save_path=tmp_file_path,
                target_api="/api/client/file/ssh_key/" + file_name,
                params={
                    "userNameEng": self.user_name
                }
            )

        isValid = False
        if download_result:
            with open(tmp_file_path, "r") as f:
                authorized_keys_content = f.read().strip()

            if authorized_keys_content:
                isValid = True

        if isValid:
            shutil.copy(
                tmp_file_path,
                os.path.join(self.ssh_dir, "authorized_keys")
            )
            os.chmod(os.path.join(self.ssh_dir, "authorized_keys"), 0o600)
            self.fix_ssh_dir()

        self.__remove_tmp_dir()
        return isValid

    def restore_ssh_key_pair(self) -> bool:
        tmp_dir = self.__get_tmp_dir()
        file_name = "ssh_key_pair.zip"
        tmp_file_path = os.path.join(tmp_dir, file_name)

        download_result = \
            download_file(
                save_path=tmp_file_path,
                target_api="/api/client/file/ssh_key/" + file_name,
                params={
                    "userNameEng": self.user_name
                }
            )

        isValid = download_result

        if isValid:
            restore_ssh_zip(zip_path=tmp_file_path)
            self.fix_ssh_dir()

        self.__remove_tmp_dir()
        return isValid


if __name__ == '__main__':
    linux_user_ssh = LinuxUserSsh()

    result_backup_authorized_keys = linux_user_ssh.backup_authorized_keys()
    print(result_backup_authorized_keys)

    result_backup_ssh_key_pair = linux_user_ssh.backup_ssh_key_pair()
    print(result_backup_ssh_key_pair)

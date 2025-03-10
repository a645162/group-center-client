import datetime
import os
import shutil
import zipfile
from typing import List

from group_center.client.machine.feature.ssh.key_pair_file import KeyPairFile
from group_center.utils.envs import get_a_tmp_dir


def get_system_ssh_dir() -> str:
    """
    获取系统SSH目录 / Get system SSH directory

    Returns:
        str: SSH目录路径 / SSH directory path
    """
    return os.path.expanduser("~/.ssh")


def fix_ssh_dir(ssh_dir_path="~/.ssh") -> None:
    """
    修复SSH目录权限 / Fix SSH directory permissions

    Args:
        ssh_dir_path (str, optional): SSH目录路径，默认为~/.ssh /
                                    SSH directory path, defaults to ~/.ssh
    """
    ssh_dir = os.path.expanduser(ssh_dir_path)

    if not os.path.exists(ssh_dir):
        os.mkdir(ssh_dir)

    # chmod -R 700 ~/.ssh
    os.chmod(ssh_dir, 0o700)


class SshKeyPairManager:
    """SSH密钥对管理类 / SSH key pair manager"""

    ssh_dir: str  # SSH目录路径 / SSH directory path
    key_pair_list: List[KeyPairFile]  # 密钥对列表 / Key pair list

    def __init__(self, ssh_dir_path: str = "~/.ssh"):
        """
        初始化SSH密钥对管理器 / Initialize SSH key pair manager

        Args:
            ssh_dir_path (str, optional): SSH目录路径，默认为~/.ssh /
                                        SSH directory path, defaults to ~/.ssh

        Raises:
            ValueError: 如果SSH目录无效 / If SSH directory is invalid
        """
        ssh_dir_path = os.path.expanduser(ssh_dir_path)
        if not os.path.exists(ssh_dir_path) or not os.path.isdir(ssh_dir_path):
            raise ValueError(f"Invalid ssh_dir: {ssh_dir_path}")

        self.ssh_dir = os.path.abspath(ssh_dir_path)

        self.key_pair_list = []

    def walk(self) -> None:
        """
        遍历SSH目录查找密钥对 / Walk SSH directory to find key pairs
        """
        for root, dirs, files in os.walk(self.ssh_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".pub"):
                    key_pair_file = KeyPairFile(file_path)

                    if key_pair_file.is_valid():
                        self.key_pair_list.append(key_pair_file)

    def __contains__(self, item: KeyPairFile) -> bool:
        """
        检查密钥对是否在列表中 / Check if key pair is in list

        Args:
            item (KeyPairFile): 要检查的密钥对 / Key pair to check

        Returns:
            bool: 如果存在返回True，否则返回False / Returns True if exists, False otherwise
        """
        return item in self.key_pair_list

    def __len__(self) -> int:
        """
        获取密钥对数量 / Get number of key pairs

        Returns:
            int: 密钥对数量 / Number of key pairs
        """
        return len(self.key_pair_list)

    def __iter__(self) -> iter:
        """
        获取密钥对迭代器 / Get key pair iterator

        Returns:
            iter: 密钥对迭代器 / Key pair iterator
        """
        return iter(self.key_pair_list)

    def __getitem__(self, item: int) -> KeyPairFile:
        """
        通过索引获取密钥对 / Get key pair by index

        Args:
            item (int): 索引 / Index

        Returns:
            KeyPairFile: 密钥对对象 / Key pair object
        """
        return self.key_pair_list[item]

    def __setitem__(self, key: int, value: KeyPairFile) -> None:
        """
        通过索引设置密钥对 / Set key pair by index

        Args:
            key (int): 索引 / Index
            value (KeyPairFile): 密钥对对象 / Key pair object
        """
        self.key_pair_list[key] = value

    def __delitem__(self, key: int) -> None:
        """
        通过索引删除密钥对 / Delete key pair by index

        Args:
            key (int): 索引 / Index
        """
        del self.key_pair_list[key]

    def __bool__(self) -> bool:
        """
        检查是否有密钥对 / Check if has any key pairs

        Returns:
            bool: 如果有密钥对返回True，否则返回False /
                  Returns True if has key pairs, False otherwise
        """
        return len(self.key_pair_list) > 0

    def remove_from_list(self, key_pair_file: KeyPairFile) -> None:
        """
        从列表中移除密钥对 / Remove key pair from list

        Args:
            key_pair_file (KeyPairFile): 要移除的密钥对 / Key pair to remove
        """
        for i, key_pair in enumerate(self.key_pair_list):
            if key_pair == key_pair_file:
                del self.key_pair_list[i]
                return

    def zip(self, zip_filename: str = "ssh_key_pair.zip") -> None:
        """
        将密钥对打包为zip文件 / Zip key pairs into a zip file

        Args:
            zip_filename (str, optional): zip文件名，默认为ssh_key_pair.zip /
                                        Zip file name, defaults to ssh_key_pair.zip
        """
        file_list = []

        for key_pair in self.key_pair_list:
            if key_pair.is_valid():
                file_list.append(key_pair.public_key_path)
                file_list.append(key_pair.private_key_path)

        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_list:
                arc_name = os.path.basename(file_path)
                zipf.write(file_path, arcname=arc_name)


def restore_ssh_zip(zip_path: str) -> None:
    """
    从zip文件恢复SSH密钥对 / Restore SSH key pairs from zip file

    Args:
        zip_path (str): zip文件路径 / Zip file path
    """
    fix_ssh_dir()

    system_ssh_dir = get_system_ssh_dir()
    tmp_dir = get_a_tmp_dir()

    with zipfile.ZipFile(zip_path, "r") as zipf:
        zipf.extractall(tmp_dir)

    ssh_manager_zip = SshKeyPairManager(tmp_dir)
    ssh_manager_zip.walk()

    ssh_manager_system = SshKeyPairManager()
    ssh_manager_system.walk()

    for key_pair in ssh_manager_system.key_pair_list:
        if key_pair in ssh_manager_zip:
            ssh_manager_zip.remove_from_list(key_pair)

    for key_pair in ssh_manager_zip.key_pair_list:
        if not key_pair.is_valid():
            continue

        private_key_name = os.path.basename(key_pair.private_key_path)

        target_private_key_path = os.path.join(
            system_ssh_dir, key_pair.private_key_name
        )
        target_public_key_path = os.path.join(system_ssh_dir, key_pair.public_key_name)

        if os.path.exists(target_private_key_path) or os.path.exists(
            target_public_key_path
        ):
            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            private_key_name += "_" + current_time

            target_private_key_path = os.path.join(system_ssh_dir, private_key_name)
            target_public_key_path = os.path.join(
                system_ssh_dir, private_key_name + ".pub"
            )

        shutil.move(key_pair.private_key_path, target_private_key_path)
        shutil.move(key_pair.public_key_path, target_public_key_path)

        os.chmod(target_private_key_path, 0o600)
        os.chmod(target_public_key_path, 0o644)

    # Remove Tmp Dir
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    key_pair_manager = SshKeyPairManager()
    key_pair_manager.walk()
    key_pair_manager.zip()

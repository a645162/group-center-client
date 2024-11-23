import datetime
import os
import shutil
import zipfile
from typing import List

from group_center.client.machine.feature. \
    ssh.key_pair_file import KeyPairFile
from group_center.utils.envs import get_a_tmp_dir


def get_system_ssh_dir() -> str:
    return os.path.expanduser("~/.ssh")


def fix_ssh_dir(ssh_dir_path="~/.ssh"):
    ssh_dir = os.path.expanduser(ssh_dir_path)

    if not os.path.exists(ssh_dir):
        os.mkdir(ssh_dir)

    # chmod -R 700 ~/.ssh
    os.chmod(ssh_dir, 0o700)


class SshKeyPairManager:
    ssh_dir: str

    key_pair_list: List[KeyPairFile]

    def __init__(self, ssh_dir_path: str = "~/.ssh"):
        ssh_dir_path = os.path.expanduser(ssh_dir_path)
        if (
                not os.path.exists(ssh_dir_path) or
                not os.path.isdir(ssh_dir_path)
        ):
            raise ValueError(f"Invalid ssh_dir: {ssh_dir_path}")

        self.ssh_dir = os.path.abspath(ssh_dir_path)

        self.key_pair_list = []

    def walk(self):
        for root, dirs, files in os.walk(self.ssh_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".pub"):
                    key_pair_file = KeyPairFile(file_path)

                    if key_pair_file.is_valid():
                        self.key_pair_list.append(key_pair_file)

    def __contains__(self, item: KeyPairFile):
        return item in self.key_pair_list

    def __len__(self):
        return len(self.key_pair_list)

    def __iter__(self):
        return iter(self.key_pair_list)

    def __getitem__(self, item):
        return self.key_pair_list[item]

    def __setitem__(self, key, value):
        self.key_pair_list[key] = value

    def __delitem__(self, key):
        del self.key_pair_list[key]

    def __bool__(self):
        return len(self.key_pair_list) > 0

    def remove_from_list(self, key_pair_file: KeyPairFile):
        for i, key_pair in enumerate(self.key_pair_list):
            if key_pair == key_pair_file:
                del self.key_pair_list[i]
                return

    def zip(self, zip_filename="ssh_key_pair.zip"):
        file_list = []

        for key_pair in self.key_pair_list:
            if key_pair.is_valid():
                file_list.append(key_pair.public_key_path)
                file_list.append(key_pair.private_key_path)

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_list:
                arc_name = os.path.basename(file_path)
                zipf.write(file_path, arcname=arc_name)


def restore_ssh_zip(zip_path: str):
    fix_ssh_dir()

    system_ssh_dir = get_system_ssh_dir()
    tmp_dir = get_a_tmp_dir()

    with zipfile.ZipFile(zip_path, 'r') as zipf:
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

        target_private_key_path = \
            os.path.join(system_ssh_dir, key_pair.private_key_name)
        target_public_key_path = \
            os.path.join(system_ssh_dir, key_pair.public_key_name)

        if os.path.exists(target_private_key_path) or \
                os.path.exists(target_public_key_path):
            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            private_key_name += "_" + current_time

            target_private_key_path = \
                os.path.join(system_ssh_dir, private_key_name)
            target_public_key_path = \
                os.path.join(system_ssh_dir, private_key_name + ".pub")

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

import os.path


class KeyPairFile:
    """SSH密钥对文件处理类 / SSH key pair file handler"""

    private_key_path: str  # 私钥文件路径 / Private key file path
    __public_key_path__: str  # 公钥文件路径 / Public key file path

    __pub_ext__ = ".pub"  # 公钥文件扩展名 / Public key file extension

    def __init__(self, key_pair_file: str):
        """
        初始化密钥对文件处理器 / Initialize key pair file handler

        Args:
            key_pair_file (str): 密钥对文件路径 / Key pair file path

        Raises:
            FileNotFoundError: 如果文件不存在 / If file does not exist
        """
        if not os.path.exists(key_pair_file):
            raise FileNotFoundError(f"Key pair file not found: {key_pair_file}")

        if key_pair_file.endswith(".pub"):
            self.public_key_path = key_pair_file
        else:
            self.private_key_path = key_pair_file

    @property
    def public_key_path(self) -> str:
        """
        获取公钥文件路径 / Get public key file path

        Returns:
            str: 公钥文件路径 / Public key file path
        """
        return self.private_key_path + self.__pub_ext__

    @public_key_path.setter
    def public_key_path(self, value: str) -> None:
        """
        设置公钥文件路径 / Set public key file path

        Args:
            value (str): 公钥文件路径 / Public key file path

        Raises:
            ValueError: 如果路径不以.pub结尾 / If path does not end with .pub
        """
        if not value.endswith(self.__pub_ext__):
            raise ValueError("Public key file must end with .pub")

        self.private_key_path = value[: len(value) - len(self.__pub_ext__)]

    @property
    def private_key_name(self) -> str:
        """
        获取私钥文件名 / Get private key file name

        Returns:
            str: 私钥文件名 / Private key file name
        """
        return os.path.basename(self.private_key_path)

    @property
    def public_key_name(self) -> str:
        """
        获取公钥文件名 / Get public key file name

        Returns:
            str: 公钥文件名 / Public key file name
        """
        return os.path.basename(self.public_key_path)

    def is_valid(self) -> bool:
        """
        检查密钥对文件是否有效 / Check if key pair files are valid

        Returns:
            bool: 如果私钥和公钥文件都存在返回True，否则返回False /
                  Returns True if both private and public key files exist, False otherwise
        """
        return os.path.exists(self.private_key_path) and os.path.exists(
            self.public_key_path
        )

    def __str__(self) -> str:
        """
        获取私钥文件名 / Get private key file name

        Returns:
            str: 私钥文件名 / Private key file name
        """
        return os.path.basename(self.private_key_path)

    def __eq__(self, other: "KeyPairFile") -> bool:
        """
        比较两个密钥对文件是否相等 / Compare if two key pair files are equal

        Args:
            other (KeyPairFile): 要比较的另一个密钥对文件对象 / Another key pair file object to compare

        Returns:
            bool: 如果路径或内容相同返回True，否则返回False /
                  Returns True if paths or contents are same, False otherwise
        """
        if (
            self.private_key_path == other.private_key_path
            or self.public_key_path == other.public_key_path
        ):
            return True

        # Check if the content of the files are the same

        # Private key
        with open(self.private_key_path, "r") as f:
            private_key_content = f.read().strip()
        with open(other.private_key_path, "r") as f:
            other_private_key_content = f.read().strip()
        if private_key_content == other_private_key_content:
            return True

        # Public key
        with open(self.public_key_path, "r") as f:
            public_key_content = f.read().strip()
        with open(other.public_key_path, "r") as f:
            other_public_key_content = f.read().strip()
        if public_key_content == other_public_key_content:
            return True

        # Not Same
        return False

import os.path


class KeyPairFile:
    private_key_path: str
    __public_key_path__: str

    __pub_ext__ = ".pub"

    def __init__(self, key_pair_file: str):
        if not os.path.exists(key_pair_file):
            raise FileNotFoundError(f"Key pair file not found: {key_pair_file}")

        if key_pair_file.endswith(".pub"):
            self.public_key_path = key_pair_file
        else:
            self.private_key_path = key_pair_file

    @property
    def public_key_path(self):
        return self.private_key_path + self.__pub_ext__

    @public_key_path.setter
    def public_key_path(self, value):
        if not value.endswith(self.__pub_ext__):
            raise ValueError("Public key file must end with .pub")

        self.private_key_path = \
            value[:len(value) - len(self.__pub_ext__)]

    @property
    def private_key_name(self):
        return os.path.basename(self.private_key_path)

    @property
    def public_key_name(self):
        return os.path.basename(self.public_key_path)

    def is_valid(self) -> bool:
        return (
                os.path.exists(self.private_key_path) and
                os.path.exists(self.public_key_path)
        )

    def __str__(self):
        return os.path.basename(self.private_key_path)

    def __eq__(self, other):
        if (
                self.private_key_path == other.private_key_path or
                self.public_key_path == other.public_key_path
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

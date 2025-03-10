from typing import List


class AuthorizedKeysFile:
    """SSH授权密钥文件处理类 / SSH authorized keys file handler"""

    class AuthorizedKey:
        """授权密钥类 / Authorized key class"""

        def __init__(self, key: str, comment: str = "", title: str = ""):
            """
            初始化授权密钥对象 / Initialize authorized key object

            Args:
                key (str): SSH公钥 / SSH public key
                comment (str, optional): 注释 / Comment. Defaults to "".
                title (str, optional): 标题 / Title. Defaults to "".
            """
            self.key: str = key
            self.comment: str = comment
            self.title: str = title

    authorized_keys: str  # 原始授权密钥字符串 / Raw authorized keys string
    authorized_keys_list: List[
        AuthorizedKey
    ]  # 解析后的授权密钥列表 / Parsed authorized keys list

    def __init__(self, authorized_keys: str):
        """
        初始化授权密钥文件处理器 / Initialize authorized keys file handler

        Args:
            authorized_keys (str): 授权密钥字符串 / Authorized keys string
        """
        self.authorized_keys = authorized_keys
        self.authorized_keys_list = []
        self.parse()

    def add(self, authorized_key: "AuthorizedKey") -> None:
        """
        添加授权密钥 / Add authorized key

        Args:
            authorized_key (AuthorizedKey): 要添加的授权密钥对象 / Authorized key object to add
        """
        for current_obj in self.authorized_keys_list:
            if current_obj.key == authorized_key.key:
                if authorized_key.comment:
                    current_obj.comment += f"\n{authorized_key.comment}"
                return
        self.authorized_keys_list.append(authorized_key)

    def parse(self) -> None:
        """
        解析授权密钥字符串 / Parse authorized keys string

        将原始字符串解析为AuthorizedKey对象列表 / Parse raw string into list of AuthorizedKey objects
        """
        authorized_keys_string_list = [
            line.strip() for line in self.authorized_keys.split("\n") if line.strip()
        ]

        for i, line in enumerate(authorized_keys_string_list):
            if line.startswith("#"):
                continue

            pub_key_split = line.split(" ", 2)

            title = ""
            if len(pub_key_split) > 2:
                publicKeyString = pub_key_split[0] + " " + pub_key_split[1]
                title = pub_key_split[2]
            else:
                publicKeyString = line

            comment = ""
            comment_start_index = i - 1
            while comment_start_index >= 0:
                if not authorized_keys_string_list[comment_start_index].startswith("#"):
                    break
                comment = (
                    authorized_keys_string_list[comment_start_index] + "\n" + comment
                )
                comment_start_index -= 1
            comment = comment.strip()

            self.authorized_keys_list.append(
                self.AuthorizedKey(publicKeyString, comment, title)
            )

    def build(self) -> str:
        """
        构建授权密钥字符串 / Build authorized keys string

        Returns:
            str: 格式化后的授权密钥字符串 / Formatted authorized keys string
        """
        output = []
        for authorized_key in self.authorized_keys_list:
            if authorized_key.key:
                if not authorized_key.comment:
                    if authorized_key.title:
                        output.append(f"# {authorized_key.title}\n")
                else:
                    output.append(authorized_key.comment + "\n")
                output.append(authorized_key.key)
                if authorized_key.title:
                    output.append(f" {authorized_key.title}")
                output.append("\n\n")
        return "".join(output).rstrip() + "\n"

    def combine(self, other: "AuthorizedKeysFile") -> None:
        """
        合并另一个授权密钥文件 / Combine another authorized keys file

        Args:
            other (AuthorizedKeysFile): 要合并的授权密钥文件对象 / Authorized keys file object to combine
        """
        for authorized_key in other.authorized_keys_list:
            self.add(authorized_key)

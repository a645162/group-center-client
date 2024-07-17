from typing import List


class AuthorizedKeysFile:
    class AuthorizedKey:
        def __init__(self, key: str, comment: str = "", title: str = ""):
            self.key: str = key
            self.comment: str = comment
            self.title: str = title

    authorized_keys: str
    authorized_keys_list: List[AuthorizedKey]

    def __init__(self, authorized_keys: str):
        self.authorized_keys = authorized_keys
        self.authorized_keys_list = []
        self.parse()

    def add(self, authorized_key: 'AuthorizedKey') -> None:
        for current_obj in self.authorized_keys_list:
            if current_obj.key == authorized_key.key:
                if authorized_key.comment:
                    current_obj.comment += f"\n{authorized_key.comment}"
                return
        self.authorized_keys_list.append(authorized_key)

    def parse(self) -> None:
        authorized_keys_string_list = [line.strip() for line in self.authorized_keys.split('\n') if line.strip()]

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
                comment = authorized_keys_string_list[comment_start_index] + "\n" + comment
                comment_start_index -= 1
            comment = comment.strip()

            self.authorized_keys_list.append(self.AuthorizedKey(publicKeyString, comment, title))

    def build(self) -> str:
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

    def combine(self, other: 'AuthorizedKeysFile') -> None:
        for authorized_key in other.authorized_keys_list:
            self.add(authorized_key)

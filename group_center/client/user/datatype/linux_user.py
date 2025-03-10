class LinuxUserJava:
    """Linux 用户信息类 / Linux user information class

    Attributes:
        uid (int): 用户 ID / User ID
        gid (int): 组 ID / Group ID
    """

    uid: int = 0
    gid: int = 0

    def from_dict(self, dict_data: dict):
        """从字典加载数据 / Load data from dictionary

        Args:
            dict_data (dict): 包含用户信息的字典 / Dictionary containing user information
        """
        self.uid = dict_data["uid"]
        self.gid = dict_data["gid"]

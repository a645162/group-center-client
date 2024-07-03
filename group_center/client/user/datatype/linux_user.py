class LinuxUserJava:
    uid: int = 0
    gid: int = 0

    def from_dict(self, dict_data: dict):
        self.uid = dict_data["uid"]
        self.gid = dict_data["gid"]

class SilentModeConfig:
    start_time: str = ""
    end_time: str = ""

    def from_dict(self, dict_data: dict):
        self.start_time = dict_data["startTime"]
        self.end_time = dict_data["endTime"]


class BaseWebHookUser:
    enable: bool = True

    def from_dict(self, dict_data: dict):
        self.enable = dict_data["enable"]


class WeComUser(BaseWebHookUser):
    user_id: str = ""
    user_mobile_phone: str = ""

    def from_dict(self, dict_data: dict):
        super().from_dict(dict_data=dict_data)
        self.user_id = dict_data["userId"]
        self.user_mobile_phone = dict_data["userMobilePhone"]


class LarkUser(BaseWebHookUser):
    user_id: str = ""
    user_mobile_phone: str = ""

    def from_dict(self, dict_data: dict):
        super().from_dict(dict_data=dict_data)
        self.user_id = dict_data["userId"]
        self.user_mobile_phone = dict_data["userMobilePhone"]


class AllWebHookUser:
    silent_mode: SilentModeConfig

    we_com: WeComUser
    lark: LarkUser

    def __init__(self):
        self.silent_mode = SilentModeConfig()

        self.we_com = WeComUser()
        self.lark = LarkUser()

    def from_dict(self, dict_data: dict):
        self.silent_mode.from_dict(dict_data=dict_data["silentMode"])

        self.we_com.from_dict(dict_data=dict_data["weCom"])
        self.lark.from_dict(dict_data=dict_data["lark"])

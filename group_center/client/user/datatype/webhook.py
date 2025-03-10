class SilentModeConfig:
    """静默模式配置 / Silent mode configuration

    Attributes:
        start_time (str): 开始时间 / Start time
        end_time (str): 结束时间 / End time
    """

    start_time: str = ""
    end_time: str = ""

    def from_dict(self, dict_data: dict):
        """从字典加载数据 / Load data from dictionary

        Args:
            dict_data (dict): 包含静默模式配置的字典 / Dictionary containing silent mode configuration
        """
        self.start_time = dict_data["startTime"]
        self.end_time = dict_data["endTime"]


class BaseWebHookUser:
    """Webhook 用户基类 / Base webhook user class

    Attributes:
        enable (bool): 是否启用 / Whether enabled
    """

    enable: bool = True

    def from_dict(self, dict_data: dict):
        """从字典加载数据 / Load data from dictionary

        Args:
            dict_data (dict): 包含 Webhook 用户配置的字典 / Dictionary containing webhook user configuration
        """
        self.enable = dict_data["enable"]


class WeComUser(BaseWebHookUser):
    """企业微信用户类 / WeCom user class

    Attributes:
        user_id (str): 用户 ID / User ID
        user_mobile_phone (str): 用户手机号 / User mobile phone
    """

    user_id: str = ""
    user_mobile_phone: str = ""

    def from_dict(self, dict_data: dict):
        """从字典加载数据 / Load data from dictionary

        Args:
            dict_data (dict): 包含企业微信用户配置的字典 / Dictionary containing WeCom user configuration
        """
        super().from_dict(dict_data=dict_data)
        self.user_id = dict_data["userId"]
        self.user_mobile_phone = dict_data["userMobilePhone"]


class LarkUser(BaseWebHookUser):
    """飞书用户类 / Lark user class

    Attributes:
        user_id (str): 用户 ID / User ID
        user_mobile_phone (str): 用户手机号 / User mobile phone
    """

    user_id: str = ""
    user_mobile_phone: str = ""

    def from_dict(self, dict_data: dict):
        """从字典加载数据 / Load data from dictionary

        Args:
            dict_data (dict): 包含飞书用户配置的字典 / Dictionary containing Lark user configuration
        """
        super().from_dict(dict_data=dict_data)
        self.user_id = dict_data["userId"]
        self.user_mobile_phone = dict_data["userMobilePhone"]


class AllWebHookUser:
    """所有 Webhook 用户类 / All webhook users class

    Attributes:
        silent_mode (SilentModeConfig): 静默模式配置 / Silent mode configuration
        we_com (WeComUser): 企业微信用户 / WeCom user
        lark (LarkUser): 飞书用户 / Lark user
    """

    silent_mode: SilentModeConfig
    we_com: WeComUser
    lark: LarkUser

    def __init__(self):
        """初始化所有 Webhook 用户 / Initialize all webhook users"""
        self.silent_mode = SilentModeConfig()
        self.we_com = WeComUser()
        self.lark = LarkUser()

    def from_dict(self, dict_data: dict):
        """从字典加载数据 / Load data from dictionary

        Args:
            dict_data (dict): 包含所有 Webhook 用户配置的字典 / Dictionary containing all webhook users configuration
        """
        self.silent_mode.from_dict(dict_data=dict_data["silentMode"])
        self.we_com.from_dict(dict_data=dict_data["weCom"])
        self.lark.from_dict(dict_data=dict_data["lark"])

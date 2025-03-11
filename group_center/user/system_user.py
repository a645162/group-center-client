class SystemUser:
    """系统用户基类 (System User Base Class)
    System User Base Class

    提供系统用户的基本功能
    Provides basic functionalities for system users
    """

    user_name: str

    def __init__(self, user_name: str = ""):
        """初始化系统用户 (Initialize system user)
        Initialize system user

        Args:
            user_name (str, optional): 用户名 (User name). Defaults to "".
        """
        self.user_name = user_name

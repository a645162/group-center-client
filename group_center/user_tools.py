from group_center.tools.user_tools import (
    group_center_set_is_valid,
    group_center_set_user_name,
    push_message,
)  # 导入用户工具 / Import user tools

if __name__ == "__main__":
    # 初始化用户工具配置 / Initialize user tools configuration
    group_center_set_is_valid(True)  # 设置工具有效性 / Set tools validity
    group_center_set_user_name("konghaomin")  # 设置用户名 / Set username

    import datetime  # 时间处理模块 / Datetime module

    # 获取当前时间 / Get current time
    now: datetime.datetime = datetime.datetime.now()
    now_str: str = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间 / Format time

    # 测试消息推送 / Test message push
    if push_message(f"测试消息推送 | Test message push: {now_str}"):
        print("消息推送完毕！ | Message push completed!")
    else:
        print("消息推送失败！ | Message push failed!")

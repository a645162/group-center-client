from group_center.tools.user_tools import *

if __name__ == "__main__":
    group_center_set_is_valid(True)
    group_center_set_user_name("konghaomin")

    import datetime

    now: datetime = datetime.datetime.now()
    now_str: str = now.strftime("%Y-%m-%d %H:%M:%S")

    push_message(f"测试消息推送: {now_str}")
    print("消息推送完毕！")

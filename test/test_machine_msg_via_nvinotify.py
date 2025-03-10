from group_center.user_tools import push_message

if __name__ == "__main__":
    # Send test message via nvinotify
    # 通过nvinotify发送测试消息
    push_message(
        content="test1",  # Message content 消息内容
        user_name="konghaomin",  # Target user name 目标用户名
    )

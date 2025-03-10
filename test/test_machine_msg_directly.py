from group_center.core.feature.custom_client_message import (
    machine_user_message_directly,
)

# Send machine message directly
# 直接发送机器消息
machine_user_message_directly(
    "konghaomin",  # Target user name 目标用户名
    "[Machine User Message]Test passed!",  # Message content 消息内容
)
machine_user_message_directly(
    "konghaomin",  # Target user name 目标用户名
    "[Machine User Message]Test passed again!",  # Message content 消息内容
)

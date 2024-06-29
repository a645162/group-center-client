#!/bin/bash

# 获取所有非root用户的列表
user_list=$(ls /home | grep -Ev '^root$')

# 从参数中获取要执行的命令
command="$@"

# 遍历用户列表
for username in $user_list; do
    # 以用户身份执行指定的命令
    sudo -u "$username" bash -c "$command"
done

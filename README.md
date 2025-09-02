# group-center-client

<!-- markdownlint-disable html -->

![Python 3.8+](https://img.shields.io/badge/Python-3.6%2B-brightgreen)
[![PyPI](https://img.shields.io/pypi/v/li-group-center?label=pypi&logo=pypi)](https://pypi.org/project/li-group-center)
[![GitHub Repo Stars](https://img.shields.io/github/stars/a645162/group-center-client?label=stars&logo=github&color=brightgreen)](https://github.com/a645162/group-center-client/stargazers)
[![License](https://img.shields.io/github/license/a645162/group-center-client?label=license&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiBmaWxsPSIjZmZmZmZmIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xMi43NSAyLjc1YS43NS43NSAwIDAwLTEuNSAwVjQuNUg5LjI3NmExLjc1IDEuNzUgMCAwMC0uOTg1LjMwM0w2LjU5NiA1Ljk1N0EuMjUuMjUgMCAwMTYuNDU1IDZIMi4zNTNhLjc1Ljc1IDAgMTAwIDEuNUgzLjkzTC41NjMgMTUuMThhLjc2Mi43NjIgMCAwMC4yMS44OGMuMDguMDY0LjE2MS4xMjUuMzA5LjIyMS4xODYuMTIxLjQ1Mi4yNzguNzkyLjQzMy42OC4zMTEgMS42NjIuNjIgMi44NzYuNjJhNi45MTkgNi45MTkgMCAwMDIuODc2LS42MmMuMzQtLjE1NS42MDYtLjMxMi43OTItLjQzMy4xNS0uMDk3LjIzLS4xNTguMzEtLjIyM2EuNzUuNzUgMCAwMC4yMDktLjg3OEw1LjU2OSA3LjVoLjg4NmMuMzUxIDAgLjY5NC0uMTA2Ljk4NC0uMzAzbDEuNjk2LTEuMTU0QS4yNS4yNSAwIDAxOS4yNzUgNmgxLjk3NXYxNC41SDYuNzYzYS43NS43NSAwIDAwMCAxLjVoMTAuNDc0YS43NS43NSAwIDAwMC0xLjVIMTIuNzVWNmgxLjk3NGMuMDUgMCAuMS4wMTUuMTQuMDQzbDEuNjk3IDEuMTU0Yy4yOS4xOTcuNjMzLjMwMy45ODQuMzAzaC44ODZsLTMuMzY4IDcuNjhhLjc1Ljc1IDAgMDAuMjMuODk2Yy4wMTIuMDA5IDAgMCAuMDAyIDBhMy4xNTQgMy4xNTQgMCAwMC4zMS4yMDZjLjE4NS4xMTIuNDUuMjU2Ljc5LjRhNy4zNDMgNy4zNDMgMCAwMDIuODU1LjU2OCA3LjM0MyA3LjM0MyAwIDAwMi44NTYtLjU2OWMuMzM4LS4xNDMuNjA0LS4yODcuNzktLjM5OWEzLjUgMy41IDAgMDAuMzEtLjIwNi43NS43NSAwIDAwLjIzLS44OTZMMjAuMDcgNy41aDEuNTc4YS43NS43NSAwIDAwMC0xLjVoLTQuMTAyYS4yNS4yNSAwIDAxLS4xNC0uMDQzbC0xLjY5Ny0xLjE1NGExLjc1IDEuNzUgMCAwMC0uOTg0LS4zMDNIMTIuNzVWMi43NXpNMi4xOTMgMTUuMTk4YTUuNDE4IDUuNDE4IDAgMDAyLjU1Ny42MzUgNS40MTggNS40MTggMCAwMDIuNTU3LS42MzVMNC43NSA5LjM2OGwtMi41NTcgNS44M3ptMTQuNTEtLjAyNGMuMDgyLjA0LjE3NC4wODMuMjc1LjEyNi41My4yMjMgMS4zMDUuNDUgMi4yNzIuNDVhNS44NDYgNS44NDYgMCAwMDIuNTQ3LS41NzZMMTkuMjUgOS4zNjdsLTIuNTQ3IDUuODA3eiI+PC9wYXRoPjwvc3ZnPgo=)](#license)

Group Center(<https://github.com/a645162/group-center>) Client for Python

[GitHub](https://github.com/a645162/group-center-client)

[PyPI](https://pypi.org/project/li-group-center/)

## Struct

- [x] Python Package For Group Center Client
  - [x] Group Center Auth(Machine)
  - [x] Remote Config
  - [x] Send Json Array Dict To Group Center
  - [x] Send Message Directly To Group Center
- [x] User Tools(Python Package)
  - [x] (Python)Push Message To `nvi-notify` finally push to `group-center`
  - [x] (Terminal)Push Message To `nvi-notify` finally push to `group-center`
- [x] Machine Tools(Command Line Tools)
  - [x] User Manage Tool
  - [x] SSH Helper
- [x] User Tools(Command Line Tools)
  - [x] pykill - Python进程终止工具
  - [x] dummy_gpu - 虚拟GPU工具

## Command Line Tools

### 用户管理工具 (user_manager)

```bash
user_manager [options]
Options:
  --host GROUP_CENTER_URL          Group Center服务地址
  --center-name MACHINE_NAME       机器短名称
  --center-password MACHINE_PASS   机器密码
  --create-users                  创建用户
  --remove-users                  删除用户
  --user-password PASSWORD        用户密码
  --user-group GROUP_NAME         用户组名
  --year YEAR                     按年份筛选用户
```

### SSH管理工具 (ssh_helper)

```bash
ssh_helper [options]
Options:
  --host GROUP_CENTER_URL          Group Center服务地址
  --center-name MACHINE_NAME       机器短名称
  --center-password MACHINE_PASS   机器密码
  --backup (-b)                   备份模式
  --restore (-r)                  恢复模式
  --all (-a)                      所有用户模式(需root权限)

交互模式:
  1 - 备份当前用户SSH配置
  2 - 恢复当前用户SSH配置
  3 - 仅恢复authorized_keys
  4 - 仅恢复密钥对
  5 - 备份所有用户(root)
  6 - 恢复所有用户(root)
  c - 生成新SSH密钥
```

### 用户消息工具 (user_message)

```bash
user_message "消息内容" [options]
Options:
  -n, --user-name USERNAME  指定用户名
  -s, --screen             包含screen会话名称
```

### Python进程管理工具 (pykill)

## Command Line Tools

### 用户管理工具 (user_manager)

```bash
user_manager [options]
Options:
  --host GROUP_CENTER_URL          Group Center服务地址
  --center-name MACHINE_NAME       机器短名称
  --center-password MACHINE_PASS   机器密码
  --create-users                  创建用户
  --remove-users                  删除用户
  --user-password PASSWORD        用户密码
  --user-group GROUP_NAME         用户组名
  --year YEAR                     按年份筛选用户
```

### SSH管理工具 (ssh_helper)

```bash
ssh_helper [options]
Options:
  --host GROUP_CENTER_URL          Group Center服务地址
  --center-name MACHINE_NAME       机器短名称
  --center-password MACHINE_PASS   机器密码
  --backup (-b)                   备份模式
  --restore (-r)                  恢复模式
  --all (-a)                      所有用户模式(需root权限)

交互模式:
  1 - 备份当前用户SSH配置
  2 - 恢复当前用户SSH配置
  3 - 仅恢复authorized_keys
  4 - 仅恢复密钥对
  5 - 备份所有用户(root)
  6 - 恢复所有用户(root)
  c - 生成新SSH密钥
```

### 用户消息工具 (user_message)

```bash
user_message "消息内容" [options]
Options:
  -n, --user-name USERNAME  指定用户名
  -s, --screen             包含screen会话名称
```

### Python进程管理工具 (pykill)

该工具能够根据进程树，寻找最上层的Python进程，并终止该进程及其所有子进程。

传递用户名则搜索该用户下的所有Python进程。

```bash
pykill --pid PID           终止指定PID的Python进程及其父进程链中的Python进程
pykill --user USERNAME     终止指定用户的所有Python进程
```

### 虚拟GPU任务工具 (dummy_gpu)

使用PyTorch，虚拟出一个GPU任务，占据显存（调试使用）

```bash
dummy_gpu --size SIZE_MB   占用指定大小的GPU显存(单位MB)
```

### 其他工具

- group_center_windows_terminal - Windows终端集成
- torch_ddp_port - Torch DDP端口工具
- debugpy_port - DebugPy端口工具  
- rtsp_viewer - RTSP查看器CLI
- python_cleanup - Python清理工具

```bash
pykill --pid PID           终止指定PID的Python进程及其父进程链中的Python进程
pykill --user USERNAME     终止指定用户的所有Python进程
```

### 虚拟GPU任务工具 (dummy_gpu)

使用PyTorch，虚拟出一个GPU任务，占据显存（调试使用）

```bash
dummy_gpu --size SIZE_MB   占用指定大小的GPU显存(单位MB)
```

### 其他工具

- group_center_windows_terminal - Windows终端集成
- torch_ddp_port - Torch DDP端口工具
- debugpy_port - DebugPy端口工具  
- rtsp_viewer - RTSP查看器CLI
- python_cleanup - Python清理工具

## Install

```bash
pip install li-group-center -i https://pypi.python.org/simple
```

```bash
pip install li-group-center==2.4.3 -i https://pypi.python.org/simple
```

## Upgrade

```bash
pip install --upgrade li-group-center -i https://pypi.python.org/simple
```

## Feature(User)

### Machine User Message

Use Environment variable `NVI_NOTIFY_IGNORE_USER_MSG=1` to ignore all!

#### Terminal Command

- `-n,--user-name` to set username.
- `-s,--screen` to contain screen session name.

```bash
user_message "Test Message~"
```

#### Python Version

User use their own account to push message to Group Center.

```python
from group_center.tools.user_tools import *

# Enable Group Center
group_center_set_is_valid()

# Auto Get Current User Name 
push_message("Test Message~")
```

User uses a public account to push a message to Group Center.

```python
from group_center.tools.user_tools import *

# Enable Group Center
group_center_set_is_valid()

# Set Global Username
group_center_set_user_name("konghaomin")

push_message("Test Message~")

# Or Specify Username on Push Message(Not Recommend)
push_message("Test Message~", "konghaomin")
```

#### Use `argparser` to set `group-center` is enable or not

```python
import argparse

from group_center.tools.user_tools import *

parser = argparse.ArgumentParser(description="Example of Group Center")

parser.add_argument(
    "-g",
    "--group-center",
    help="Enable Group Center",
    action="store_true",
)

opt = parser.parse_args()

if opt.groupcenter:
    group_center_set_is_valid()
```

## Feature(Machine)

### Generate User Account

## Group Center

- GROUP_CENTER_URL
- GROUP_CENTER_MACHINE_NAME
- GROUP_CENTER_MACHINE_NAME_SHORT
- GROUP_CENTER_MACHINE_PASSWORD

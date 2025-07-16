# group-center-client

<!-- markdownlint-disable html -->

![Python 3.8+](https://img.shields.io/badge/Python-3.6%2B-brightgreen)
[![PyPI](https://img.shields.io/pypi/v/li-group-center?label=pypi&logo=pypi)](https://pypi.org/project/li-group-center)
[![GitHub Repo Stars](https://img.shields.io/github/stars/a645162/group-center-client?label=stars&logo=github&color=brightgreen)](https://github.com/a645162/group-center-client/stargazers)
[![License](https://img.shields.io/github/license/a645162/group-center-client?label=license&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiBmaWxsPSIjZmZmZmZmIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xMi43NSAyLjc1YS43NS43NSAwIDAwLTEuNSAwVjQuNUg5LjI3NmExLjc1IDEuNzUgMCAwMC0uOTg1LjMwM0w2LjU5NiA1Ljk1N0EuMjUuMjUgMCAwMTYuNDU1IDZIMi4zNTNhLjc1Ljc1IDAgMTAwIDEuNUgzLjkzTC41NjMgMTUuMThhLjc2Mi43NjIgMCAwMC4yMS44OGMuMDguMDY0LjE2MS4xMjUuMzA5LjIyMS4xODYuMTIxLjQ1Mi4yNzguNzkyLjQzMy42OC4zMTEgMS42NjIuNjIgMi44NzYuNjJhNi45MTkgNi45MTkgMCAwMDIuODc2LS42MmMuMzQtLjE1NS42MDYtLjMxMi43OTItLjQzMy4xNS0uMDk3LjIzLS4xNTguMzEtLjIyM2EuNzUuNzUgMCAwMC4yMDktLjg3OEw1LjU2OSA3LjVoLjg4NmMuMzUxIDAgLjY5NC0uMTA2Ljk4NC0uMzAzbDEuNjk2LTEuMTU0QS4yNS4yNSAwIDAxOS4yNzUgNmgxLjk3NXYxNC41SDYuNzYzYS43NS43NSAwIDAwMCAxLjVoMTAuNDc0YS43NS43NSAwIDAwMC0xLjVIMTIuNzVWNmgxLjk3NGMuMDUgMCAuMS4wMTUuMTQuMDQzbDEuNjk3IDEuMTU0Yy4yOS4xOTcuNjMzLjMwMy45ODQuMzAzaC44ODZsLTMuMzY4IDcuNjhhLjc1Ljc1IDAgMDAuMjMuODk2Yy4wMTIuMDA5IDAgMCAuMDAyIDBhMy4xNTQgMy4xNTQgMCAwMC4zMS4yMDZjLjE4NS4xMTIuNDUuMjU2Ljc5LjRhNy4zNDMgNy4zNDMgMCAwMDIuODU1LjU2OCA3LjM0MyA3LjM0MyAwIDAwMi44NTYtLjU2OWMuMzM4LS4xNDMuNjA0LS4yODcuNzktLjM5OWEzLjUgMy41IDAgMDAuMzEtLjIwNi43NS43NSAwIDAwLjIzLS44OTZMMjAuMDcgNy41aDEuNTc4YS43NS43NSAwIDAwMC0xLjVoLTQuMTAyYS4yNS4yNSAwIDAxLS4xNC0uMDQzbC0xLjY5Ny0xLjE1NGExLjc1IDEuNzUgMCAwMC0uOTg0LS4zMDNIMTIuNzVWMi43NXpNMi4xOTMgMTUuMTk4YTUuNDE4IDUuNDE4IDAgMDAyLjU1Ny42MzUgNS40MTggNS40MTggMCAwMDIuNTU3LS42MzVMNC43NSA5LjM2OGwtMi41NTcgNS44M3ptMTQuNTEtLjAyNGMuMDgyLjA0LjE3NC4wODMuMjc1LjEyNi41My4yMjMgMS4zMDUuNDUgMi4yNzIuNDVhNS44NDYgNS44NDYgMCAwMDIuNTQ3LS41NzZMMTkuMjUgOS4zNjdsLTIuNTQ3IDUuODA3eiI+PC9wYXRoPjwvc3ZnPgo=)](#license)

Group Center(https://github.com/a645162/group-center) Client for Python

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
- [ ] User Tools(Command Line Tools)

## Command Line Tools

- machine_user
- ssh_helper
- user_message
- group_center_windows_terminal
- torch_ddp_port
- rtsp_viewer
- python_cleanup

## Install

```bash
pip install li-group-center -i https://pypi.python.org/simple
```

```bash
pip install li-group-center==2.3.1 -i https://pypi.python.org/simple
```

## Upgrade

```bash
pip install --upgrade li-group-center -i https://pypi.python.org/simple
```

## Feature(User)

### Machine User Message

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

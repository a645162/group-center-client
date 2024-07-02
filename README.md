# group-center-client

Group Center(https://github.com/a645162/group-center) Client

## Struct

- [x] Python Package For Group Center Client
  - [x] Group Center Auth(Machine)
  - [x] Remote Config
  - [x] Send Json Array Dict To Group Center
  - [x] Send Message Directly To Group Center
- [x] User Python Package
  - [x] Push Message To `nvi-notify` finally push to `group-center`
- [ ] Machine Tools

## Install

```bash
pip install li-group-center -i https://pypi.python.org/simple
```

```bash
pip install li-group-center==1.4.0 -i https://pypi.python.org/simple
```

## Upgrade

```bash
pip install --upgrade li-group-center -i https://pypi.python.org/simple
```

## Feature(User)

### Machine User Message

#### Usage

User use their own account to push message to Group Center.

```python
from group_center.user_tools import *

# Enable Group Center
group_center_set_is_valid()

# Auto Get Current User Name 
push_message("Test Message~")
```

User uses a public account to push a message to Group Center.

```python
from group_center.user_tools import *

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

from group_center.user_tools import *

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

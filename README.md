# group-center-client

Group Center(https://github.com/a645162/group-center) Client

## Install

```bash
pip install li-group-center -i https://pypi.python.org/simple
```

```bash
pip install li-group-center==1.2.1 -i https://pypi.python.org/simple
```

## Upgrade

```bash
pip install --upgrade li-group-center -i https://pypi.python.org/simple
```

## Feature

### Machine User Message

```python
from group_center.feature.nvi_notify.machine_user_message \
    import machine_user_message_via_local_nvi_notify as push_message

push_message("konghaomin", "Test Message~")
```

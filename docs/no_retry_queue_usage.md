# 无重发队列机制使用说明

## 概述

为了解决消息发送失败时重发机制阻塞队列的问题，我们实现了双队列机制：
- **重发队列**：用于重要消息，发送失败时会重试
- **无重发队列**：用于不重要消息，发送失败不重试

## 主要修改

### 1. 核心队列机制 ([`machine_message.py`](../group_center/core/feature/machine_message.py))

- 新增 `retry_queue` 和 `no_retry_queue` 两个队列
- 修改 `GroupCenterWorkThread.run()` 方法，优先处理无重发队列
- 无重发队列消息发送失败时直接丢弃，不会阻塞队列

### 2. 增强的消息发送函数

#### [`new_message_enqueue()`](../group_center/core/feature/machine_message.py#L126)
```python
def new_message_enqueue(data: dict, target: str, enable_retry: bool = True):
    """将新消息加入队列
    
    Args:
        data (dict): 消息数据
        target (str): 目标API路径
        enable_retry (bool): 是否启用重发机制，默认为True
    """
```

#### [`send_message_directly()`](../group_center/core/feature/machine_message.py#L149)
```python
def send_message_directly(data: dict, target: str) -> bool:
    """直接发送消息（无队列，无重发）
    
    Args:
        data (dict): 消息数据
        target (str): 目标API路径
        
    Returns:
        bool: 是否发送成功
    """
```

### 3. 增强的客户端消息函数 ([`custom_client_message.py`](../group_center/core/feature/custom_client_message.py))

#### 机器消息
```python
def machine_message_directly(
    server_name: str,
    server_name_eng: str,
    content: str,
    at: str = "",
    enable_retry: bool = True
):
```

#### 用户消息
```python
def machine_user_message_directly(
    user_name: str,
    content: str,
    enable_retry: bool = True
):
```

## 使用示例

### 重要消息（启用重发）
```python
from group_center.core.feature.custom_client_message import machine_message_directly

# 重要消息，需要确保送达
machine_message_directly(
    server_name="MyServer",
    server_name_eng="MyServer",
    content="重要通知：任务已完成",
    enable_retry=True  # 默认值，可省略
)
```

### 不重要消息（禁用重发）
```python
from group_center.core.feature.custom_client_message import machine_message_directly

# 不重要消息，失败也无所谓
machine_message_directly(
    server_name="MyServer",
    server_name_eng="MyServer",
    content="调试信息：内存使用率85%",
    enable_retry=False  # 禁用重发
)
```

### 直接发送（无队列）
```python
from group_center.core.feature.machine_message import send_message_directly

data = {
    "serverName": "MyServer",
    "serverNameEng": "MyServer",
    "content": "直接发送测试"
}

result = send_message_directly(data, "/api/client/machine/message")
print(f"发送结果: {result}")
```

## 测试

提供了完整的测试脚本：[`test_no_retry_queue.py`](../test/test_no_retry_queue.py)

运行测试：
```bash
cd test
python test_no_retry_queue.py
```

## 优势

1. **避免队列阻塞**：不重要消息失败不会阻塞重要消息
2. **优先级处理**：无重发队列优先处理，确保及时发送
3. **向后兼容**：默认启用重发机制，不影响现有代码
4. **灵活配置**：可根据消息重要性选择是否启用重发

## 注意事项

- 默认情况下所有消息都启用重发机制，保持向后兼容
- 周期性不重要消息建议使用无重发模式
- 重要业务消息建议保持重发机制启用
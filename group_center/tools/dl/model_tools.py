from typing import Union, Any
import torch.nn as nn


def calc_model_params(model: Union[nn.Module, Any]) -> float:
    """
    计算深度学习模型的可训练参数数量。

    该函数计算给定模型的总参数量和可训练参数量，并返回可训练参数量（单位：百万）。
    可训练参数是指 requires_grad 为 True 的参数。

    参数:
        model: 深度学习模型实例，通常是 torch.nn.Module 的子类

    返回:
        float: 模型的可训练参数数量，单位为百万(M)
               如果输入模型类型不正确，返回0

    示例:
        >>> from torchvision.models import resnet18
        >>> model = resnet18()
        >>> trainable_params = calc_model_params(model)
        >>> print(f"模型可训练参数量: {trainable_params:.2f}M")
    """
    # 检查输入类型是否正确
    try:
        # 尝试访问parameters方法，判断是否为PyTorch模型
        parameters = model.parameters()
        # 进一步验证是否可迭代且有numel和requires_grad属性
        next(iter(parameters), None)
    except (AttributeError, TypeError, StopIteration):
        return 0.0

    # Calculate model parameters
    # total_params = sum(p.numel() for p in model.parameters()) / 1e6
    trainable_params = (
        sum(p.numel() for p in model.parameters() if p.requires_grad) / 1e6
    )

    return trainable_params

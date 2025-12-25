# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import setup, find_packages

from group_center import __version__

this_directory: Path = Path(__file__).parent
with open(this_directory / "README.md", encoding="utf-8") as f:
    long_description: str = (
        f.read()
    )  # Read long description from README.md / 从README.md读取长描述

setup(
    name="li_group_center",
    version=__version__,
    description="Group Center Tools",  # Short description of the package / 包的简短描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a645162/group-center-client",  # Project URL / 项目URL
    author="Haomin Kong",  # Author name / 作者姓名
    author_email="a645162@gmail.com",  # Author email / 作者邮箱
    license="GPLv3",  # License type / 许可证类型
    packages=find_packages(
        exclude=[
            "test",  # Exclude test directory / 排除测试目录
        ]
    ),
    python_requires=">=3.6",  # Minimum Python version requirement / 最低Python版本要求
    install_requires=[
        "typing-extensions",  # Typing extensions / 类型扩展
        "urllib3",  # HTTP client library / HTTP客户端库
        "requests",  # HTTP requests library / HTTP请求库
        "termcolor >= 1.0.0",  # Terminal color formatting / 终端颜色格式化
        "colorama >= 0.4.0; platform_system == 'Windows'",  # Cross-platform colored terminal text / 跨平台彩色终端文本
        "windows-curses >= 2.2.0; platform_system == 'Windows'",  # Windows curses compatibility / Windows curses兼容
        # "objprint",  # Object printing utility / 对象打印工具
        "psutil",  # Process and system utilities / 进程和系统工具
        "rich>=12.0.0",  # Rich text and beautiful formatting / 富文本和美化格式化
        "tqdm",  # Progress bar / 进度条
    ],
    entry_points={
        "console_scripts": [
            "user_manager = group_center.client.machine.user_manager:main",  # User management CLI / 用户管理CLI
            "ssh_helper = group_center.client.machine.ssh_helper:main",  # SSH helper CLI / SSH助手CLI
            "user_message = group_center.client.user.shell_message:main",  # User message CLI / 用户消息CLI
            "group_center_windows_terminal = group_center.client.user.windows_terminal:main",  # Windows terminal integration / Windows终端集成
            "torch_ddp_port = group_center.tools.dl.ddp_port:main",  # Torch DDP port utility / Torch DDP端口工具
            "debugpy_port = group_center.tools.dl.debugpy_port:main",  # DebugPy port utility / DebugPy端口工具
            "rtsp_viewer = group_center.tools.rtsp.rtsp_viewer:main",  # RTSP viewer CLI / RTSP查看器CLI
            "python_cleanup = group_center.tools.user_tools.python_cleanup:main",  # Python cleanup utility / Python清理工具
            "pykill = group_center.tools.user_tools.pykill:main",  # pykill命令
            "dummy_gpu = group_center.tools.user_tools.dummy_gpu:main",
            "torch_info = group_center.utils.anaconda.torch_info:main",  # torch_info命令
            "list_conda_torch = group_center.utils.anaconda.list_conda_torch:main",  # list_conda_torch命令
            "conda_env_clean = group_center.tools.conda.env_clean:main",  # Conda environment cleanup tool / Conda环境清理工具
        ],
    },
)

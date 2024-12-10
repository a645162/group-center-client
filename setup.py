# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import setup, find_packages

from config.version import __version__

this_directory = Path(__file__).parent
with open(this_directory / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="li_group_center",
    version=__version__,
    description="Group Center Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a645162/group-center-client",
    author="Haomin Kong",
    author_email="a645162@gmail.com",
    license="GPLv3",
    packages=find_packages(
        exclude=[
            "test",
        ]
    ),
    python_requires=">=3.6",
    install_requires=[
        "urllib3", "requests",
        "termcolor >= 1.0.0",
        "colorama >= 0.4.0; platform_system == 'Windows'",
        "windows-curses >= 2.2.0; platform_system == 'Windows'",
    ],
    entry_points={
        "console_scripts": [
            "group_center_machine_user = group_center.client.machine.user_manager:main",
            "group_center_ssh_helper = group_center.client.machine.ssh_helper:main",
            "group_center_user_message = group_center.client.user.shell_message:main",
            "group_center_terminal = group_center.user.windows_terminal:main",

            "torch_ddp_port = group_center.tools.dl.ddp_port:main",

            "rtsp_viewer = group_center.tools.rtsp.rtsp_viewer:main",
        ],
    },
)

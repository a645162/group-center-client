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
    python_requires=">=3.5",
    install_requires=[
        "urllib3<2", "requests",
        "loguru"
    ],
    # entry_points={
    #     "console_scripts": [
    #         "shmtu-auth = shmtu_auth.main_start:main",
    #     ],
    # },
)

"""
Use setup tools to setup the dankbot as a standard python module
"""
from setuptools import find_packages, setup

setup(
    name="dankbot",
    version="0.0.3",
    description="Slack bot for posting dank memes",
    packages=find_packages(),
    test_suite="tests",
    tests_require=['tox'],
    entry_points={
        "console_scripts": [
            "dankbot=dankbot.cli:main",
        ]
    },
    install_requires=[
        'slacker',
        'praw',
        'configparser>=3.5.0b2',
        'mysqlclient',
    ],
)

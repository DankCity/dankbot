"""
Use setup tools to setup the dankbot as a standard python module
"""
from setuptools import setup, find_packages

setup(
    name="dankbot",
    version="0.0.1",
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
    ],
)

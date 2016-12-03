"""
Use setup tools to setup the dankbot as a standard python module
"""
import versioneer
from setuptools import find_packages, setup

setup(
    name="dankbot",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
        'praw==3.6.0',
        'retryz',
        'slacker',
        'mysqlclient',
        'imgurpython',
        'configparser>=3.5.0b2',
    ],
)

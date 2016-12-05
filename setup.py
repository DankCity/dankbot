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
        'appdirs==1.4.0',
        'configparser==3.5.0',
        'imgurpython==1.1.7',
        'mysqlclient==1.3.9',
        'praw==3.6.0',
        'retryz==0.1.8',
        'slacker==0.9.30',
    ],
)

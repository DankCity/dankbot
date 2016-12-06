"""
Use setup tools to setup the dankbot as a standard python module
"""
from os import path
from setuptools import find_packages, setup

import versioneer

here = path.dirname(path.abspath(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

install_requires = [
    'appdirs==1.4.0',
    'configparser==3.5.0',
    'imgurpython==1.1.7',
    'mysqlclient==1.3.9',
    'praw==3.6.0',
    'retryz==0.1.8',
    'slacker==0.9.30',
]

setup(
    name="dankbot",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Levi Noecker',
    author_email='levi.noecker [at] gmail [dot] com',
    url='https://github.com/DankCity/dankbot',
    keywords=['reddit', 'slack', 'imgur', 'dank', 'memes', 'bot', 'slack bot', 'dankbot'],
    description="Slack bot for posting dank memes from Reddit",
    packages=find_packages(),
    license='MIT',
    long_description=long_description,
    test_suite="tests",
    tests_require=['tox'],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "dankbot=dankbot.cli:main",
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)

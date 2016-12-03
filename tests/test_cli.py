from logging import Logger
from configparser import ConfigParser
from unittest.mock import patch

from dankbot import cli


@patch('dankbot.cli.DankBot')
def test_main(dankbot):
    dankbot.return_value = dankbot

    cli.main()

    assert dankbot.called
    assert isinstance(dankbot.call_args[0][0], ConfigParser)
    assert isinstance(dankbot.call_args[0][1], Logger)
    assert dankbot.find_and_post_memes.called


@patch('dankbot.cli.configure_logger')
@patch('dankbot.cli.DankBot')
def test_main_exception(dankbot, logger_mock):
    logger_mock.return_value = logger_mock
    dankbot.return_value = ValueError("Mock exception")

    cli.main()

    assert logger_mock.exception.called

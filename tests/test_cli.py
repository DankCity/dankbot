from configparser import ConfigParser
from unittest.mock import patch

from dankbot import cli


@patch('dankbot.cli.DEFAULT_CONFIG', 'dankbot.sample.ini')
@patch('dankbot.cli.logging.getLogger')
@patch('dankbot.cli.RotatingFileHandler')
@patch('dankbot.cli.DankBot')
def test_main(dankbot, _, gl_mock):
    gl_mock.return_value = gl_mock
    dankbot.return_value = dankbot

    cli.main()

    assert dankbot.called
    assert isinstance(dankbot.call_args[0][0], ConfigParser)
    assert dankbot.call_args[0][1], gl_mock
    assert dankbot.find_and_post_memes.called


@patch('dankbot.cli.DEFAULT_CONFIG', 'dankbot.sample.ini')
@patch('dankbot.cli.configure_logger')
@patch('dankbot.cli.DankBot')
def test_main_exception(dankbot, logger_mock):
    logger_mock.return_value = logger_mock, None
    dankbot.return_value = ValueError("Mock exception")

    cli.main()

    assert logger_mock.exception.called

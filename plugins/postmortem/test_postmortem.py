# content of test_class.py
import postmortem
import pytest

extra_plugin_dir = '.'
pytest_plugins = ["errbot.backends.test"]


# class TestClass:
def test_one():
    x = "this"
    assert "h" in x


def test_database():
    postmortem.Postmortem.create_postmortem_database()


def test_message():
    expected = "muh"
    result = postmortem.Postmortem.test_message()
    assert result == expected

import importlib

import pytest
from rest_framework.parsers import JSONParser

from tests.parser import SimpleCustomParser


@pytest.fixture
def reload_parser(request):
    """
    Exists to provide a finalizer which reloads the parser library to allow for
    changing settings which affect the CamelCaseJSONParser class' parent class.

    This fixture should be listed before the settings fixture.
    """
    from drf_dromedary import parser

    def reload():
        importlib.reload(parser)

    request.addfinalizer(reload)


def test_parser_default_parent_class():
    from drf_dromedary import parser

    assert issubclass(parser.CamelCaseJSONParser, JSONParser)


def test_parser_custom_parent_class(reload_parser, settings):
    settings.JSON_CAMEL_CASE = {
        "PARSER_CLASS": "tests.parser.SimpleCustomParser",
    }
    from drf_dromedary import parser

    importlib.reload(parser)
    assert issubclass(parser.CamelCaseJSONParser, SimpleCustomParser)

import importlib
import io
import json
import pytest
from rest_framework.parsers import JSONParser

from drf_dromedary import parser
from tests.parser import SimpleCustomParser, AddsFooCustomParser


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
    assert issubclass(parser.CamelCaseJSONParser, JSONParser)


def test_parser_custom_parent_class(reload_parser, settings):
    settings.JSON_CAMEL_CASE = {
        "PARSER_CLASS": "tests.parser.SimpleCustomParser",
    }

    importlib.reload(parser)
    assert issubclass(parser.CamelCaseJSONParser, SimpleCustomParser)


def test_parse_with_default_class():
    p = parser.CamelCaseJSONParser()
    input = {
        "aKey": "foo",
        "aBiggerKey": "Bar",
        "keyAndVal4Int": 1,
        "keyAndVal4AFloat": 2.345,
        "dictKey": {"innerKey": "val"},
    }
    input_stream = io.BytesIO(json.dumps(input).encode("utf-8"))
    result = p.parse(input_stream)
    assert {
        "a_key": "foo",
        "a_bigger_key": "Bar",
        "key_and_val_4_int": 1,
        "key_and_val_4a_float": 2.345,
        "dict_key": {"inner_key": "val"},
    } == result

def test_parse_with_custom_class(reload_parser, settings):
    settings.JSON_CAMEL_CASE = {
        "PARSER_CLASS": "tests.parser.AddsFooCustomParser",
    }

    importlib.reload(parser)

    p = parser.CamelCaseJSONParser()

    input = {
        "aKey": "foo",
        "aBiggerKey": "Bar",
        "keyAndVal4Int": 1,
        "keyAndVal4AFloat": 2.345,
        "dictKey": {"innerKey": "val"},
    }
    input_stream = io.BytesIO(json.dumps(input).encode("utf-8"))
    result = p.parse(input_stream)
    assert result == {
        "foo_a_key": "foo",
        "foo_a_bigger_key": "Bar",
        "foo_key_and_val_4_int": 1,
        "foo_key_and_val_4a_float": 2.345,
        "foo_dict_key": {"inner_key": "val"},
    }

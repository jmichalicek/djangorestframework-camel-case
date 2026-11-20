from copy import deepcopy

from django.utils.functional import lazy
from rest_framework.serializers import BaseSerializer
from rest_framework.utils.serializer_helpers import ReturnDict

from drf_dromedary.util import camelize


def test_under_to_camel_keys():
    data = {
        "two_word": 1,
        "long_key_with_many_underscores": 2,
        "only_1_key": 3,
        "only_one_letter_a": 4,
        "b_only_one_letter": 5,
        "only_c_letter": 6,
        "mix_123123a_and_letters": 7,
        "mix_123123aa_and_letters_complex": 8,
        "no_underscore_before123": 9,
    }
    output = {
        "twoWord": 1,
        "longKeyWithManyUnderscores": 2,
        "only1Key": 3,
        "onlyOneLetterA": 4,
        "bOnlyOneLetter": 5,
        "onlyCLetter": 6,
        "mix123123aAndLetters": 7,
        "mix123123aaAndLettersComplex": 8,
        "noUnderscoreBefore123": 9,
    }
    assert camelize(data) == output


def test_tuples():
    data = {"multiple_values": (1, 2), "data": [1, 3, 4]}
    output = {"multipleValues": [1, 2], "data": [1, 3, 4]}
    assert camelize(data) == output


def test_camel_to_under_input_untouched_for_sequence():
    data = [{"firstInput": 1}, {"secondInput": 2}]
    reference_input = deepcopy(data)
    camelize(data)
    assert data == reference_input


def test_recursive_camelize_with_ignored_fields_and_keys():
    ignore_fields = ("ignored_field", "newKeyIgnoredField", "ignored_field_and_key", "ignoredFieldAndKey2")
    ignore_keys = ("ignored_key", "newKeyIgnoredKey", "ignored_field_and_key", "ignoredFieldAndKey2")
    data = {
        "ignored_field": {"no_change_recursive": 1},
        "change_me": {"change_recursive": 2},
        "new_key_ignored_field": {"also_no_change": 3},
        "ignored_key": {"also_change_recursive": 4},
        "new_key_ignored_key": {"change_is_here_to_stay": 5},
        "ignored_field_and_key": {"no_change_here": 6},
        "ignored_field_and_key2": {"no_change_here_either": 7},
    }
    output = {
        "ignoredField": {"no_change_recursive": 1},
        "changeMe": {"changeRecursive": 2},
        "newKeyIgnoredField": {"also_no_change": 3},
        "ignored_key": {"alsoChangeRecursive": 4},
        "new_key_ignored_key": {"changeIsHereToStay": 5},
        "ignored_field_and_key": {"no_change_here": 6},
        "ignored_field_and_key2": {"no_change_here_either": 7},
    }
    assert camelize(data, ignore_fields=ignore_fields, ignore_keys=ignore_keys) == output


def test_camelize_iterates_over_generator():
    def _underscore_generator():
        yield {"simple_is_better": "than complex"}
        yield {"that_is": "correct"}

    data = _underscore_generator()
    output = [{"simpleIsBetter": "than complex"}, {"thatIs": "correct"}]
    assert camelize(data) == output


def test_dict_with_numbers_as_keys():
    data = {1: "test", "a": "abc"}
    assert camelize(data) == data


def test_return_dict():
    # Making mypy happy. If this is inline with ReturnDict() as the first arg
    # with no type specified, due to mixed value types, mypy sees it as
    # dict[str, object] and complains that it does not match the types for ReturnDict
    map: dict[str, int | str] = {"id": 3, "value": "val"}
    data = ReturnDict(map, serializer=BaseSerializer())
    camelized = camelize(data)
    assert data == camelized
    assert data.serializer == camelized.serializer


def test_promise_strings():
    def return_string(text):
        return text

    lazy_func = lazy(return_string, str)
    data = {lazy_func("test_key"): lazy_func("test_value value")}
    camelized = camelize(data)
    assert camelized == {"testKey": "test_value value"}

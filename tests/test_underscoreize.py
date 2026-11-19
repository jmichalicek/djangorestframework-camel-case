from __future__ import annotations

from copy import deepcopy

from django.http import QueryDict

from drf_dromedary.util import underscoreize


def test_camel_to_under_keys():
    data = {
        "twoWord": 1,
        "longKeyWithManyUnderscores": 2,
        "only1Key": 3,
        "onlyOneLetterA": 4,
        "bOnlyOneLetter": 5,
        "onlyCLetter": 6,
        "mix123123aAndLetters": 7,
        "mix123123aaAndLettersComplex": 8,
        "wordWITHCaps": 9,
        "key10": 10,
        "anotherKey1": 11,
        "anotherKey10": 12,
        "optionS1": 13,
        "optionS10": 14,
        "UPPERCASE": 15,
        "PascalCase": 16,
        "Pascal10Case": 17,
    }
    output = {
        "two_word": 1,
        "long_key_with_many_underscores": 2,
        "only_1_key": 3,
        "only_one_letter_a": 4,
        "b_only_one_letter": 5,
        "only_c_letter": 6,
        "mix_123123a_and_letters": 7,
        "mix_123123aa_and_letters_complex": 8,
        "word_with_caps": 9,
        "key_10": 10,
        "another_key_1": 11,
        "another_key_10": 12,
        "option_s_1": 13,
        "option_s_10": 14,
        "uppercase": 15,
        "pascal_case": 16,
        "pascal_10_case": 17,
    }
    assert underscoreize(data) == output


def test_camel_to_under_keys_with_no_underscore_before_number():
    data = {"noUnderscoreBefore123": 1}
    output = {"no_underscore_before123": 1}
    options = {"no_underscore_before_number": True}
    assert underscoreize(data, **options) == output


def test_under_to_camel_input_untouched_for_sequence():
    data = [{"first_input": 1}, {"second_input": 2}]
    reference_input = deepcopy(data)
    underscoreize(data)
    assert data == reference_input


def test_recursive_underscoreize_with_ignored_fields_and_keys():
    ignore_fields = ("ignoredField", "new_key_ignored_field", "ignoredFieldAndKey", "ignored_field_and_key_2")
    ignore_keys = ("ignoredKey", "new_key_ignored_key", "ignoredFieldAndKey", "ignored_field_and_key_2")
    data = {
        "ignoredField": {"noChangeRecursive": 1},
        "changeMeField": {"changeRecursive": 2},
        "newKeyIgnoredField": {"alsoNoChange": 3},
        "ignoredKey": {"changeRecursiveAgain": 4},
        "newKeyIgnoredKey": {"changeIsHereToStay": 5},
        "ignoredFieldAndKey": {"noChangeHere": 6},
        "ignoredFieldAndKey2": {"noChangeHereEither": 7},
    }
    output = {
        "ignored_field": {"noChangeRecursive": 1},
        "change_me_field": {"change_recursive": 2},
        "new_key_ignored_field": {"alsoNoChange": 3},
        "ignoredKey": {"change_recursive_again": 4},
        "newKeyIgnoredKey": {"change_is_here_to_stay": 5},
        "ignoredFieldAndKey": {"noChangeHere": 6},
        "ignoredFieldAndKey2": {"noChangeHereEither": 7},
    }
    assert underscoreize(data, ignore_fields=ignore_fields, ignore_keys=ignore_keys) == output


def test_underscoreize_iterates_over_generator():
    def _camel_generator():
        yield {"simpleIsBetter": "than complex"}
        yield {"thatIs": "correct"}

    data = _camel_generator()
    output = [
        {"simple_is_better": "than complex"},
        {"that_is": "correct"},
    ]
    assert underscoreize(data) == output


def test_underscoreize_with_query_dict():
    query_dict = QueryDict("testList=1&testList=2", mutable=True)
    data = {
        "twoWord": "1",
        "longKeyWithManyUnderscores": "2",
        "only1Key": "3",
        "onlyOneLetterA": "4",
        "bOnlyOneLetter": "5",
        "onlyCLetter": "6",
        "mix123123aAndLetters": "7",
        "mix123123aaAndLettersComplex": "8",
        "wordWITHCaps": "9",
        "key10": "10",
        "anotherKey1": "11",
        "anotherKey10": "12",
        "optionS1": "13",
        "optionS10": "14",
        "UPPERCASE": "15",
        "PascalCase": "16",
        "Pascal10Case": "17",
    }
    query_dict.update(data)

    output_query = QueryDict("test_list=1&test_list=2", mutable=True)

    output = {
        "two_word": "1",
        "long_key_with_many_underscores": "2",
        "only_1_key": "3",
        "only_one_letter_a": "4",
        "b_only_one_letter": "5",
        "only_c_letter": "6",
        "mix_123123a_and_letters": "7",
        "mix_123123aa_and_letters_complex": "8",
        "word_with_caps": "9",
        "key_10": "10",
        "another_key_1": "11",
        "another_key_10": "12",
        "option_s_1": "13",
        "option_s_10": "14",
        "uppercase": "15",
        "pascal_case": "16",
        "pascal_10_case": "17",
    }
    output_query.update(output)
    assert underscoreize(query_dict) == output_query


def test_numeric_key():
    data = {1: "test"}
    assert underscoreize(data) == data

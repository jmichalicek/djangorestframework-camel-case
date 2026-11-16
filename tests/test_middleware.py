from unittest import mock

from django.http import QueryDict

from drf_dromedary.middleware import CamelCaseMiddleWare


def test_camel_case_to_underscore_query_params(rf):
    get_response_mock = mock.MagicMock()
    middleware = CamelCaseMiddleWare(get_response_mock)
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
    request = rf.get("/", query_dict)

    middleware(request)
    (args, _) = get_response_mock.call_args
    assert args[0].GET == output_query

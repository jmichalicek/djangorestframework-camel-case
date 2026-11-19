# DRF Dromedary

Camel case JSON support for Django REST framework.

> [!NOTE]
> DRF Dromedary is a continuation of the work started by [@vbabiy](https://github.com/vbabiy/djangorestframework-camel-case) and other contributors
>
> Django REST Framework JSON CamelCase has seen very little activity
> and is not tested against recent Python, Django, or Django REST
> Framework versions although it continues to function with them.
> With that in mind the project has been forked to allow testing with
> current versions and to take advantage of language and packaging
> ecosystem improvements.


# Installation

At the command line:

```
$ pip install drf-dromedary
```

Add the render and parser to your django settings file.

```python
# ...
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "drf_dromedary.render.CamelCaseJSONRenderer",
        "drf_dromedary.render.CamelCaseBrowsableAPIRenderer",
        # Any other renders
    ),
    "DEFAULT_PARSER_CLASSES": (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        "drf_dromedary.parser.CamelCaseFormParser",
        "drf_dromedary.parser.CamelCaseMultiPartParser",
        "drf_dromedary.parser.CamelCaseJSONParser",
        # Any other parsers
    ),
}
# ...
```

Add query param middleware to django settings file.

```python
# ...
MIDDLEWARE = [
    # Any other middleware
    "drf_dromedary.middleware.CamelCaseMiddleWare",
]
# ...
```

# Swapping Renderers and Parsers

By default the package uses `rest_framework.renderers.JSONRenderer` and `rest_framework.parsers.JSONParser`.
You can configure a different render in the settings.

```python
# ...
JSON_CAMEL_CASE = {
    "RENDERER_CLASS": "django_orjson.rest_framework.JSONRenderer",
    "PARSER_CLASS": "django_orjson.rest_framework.JSONParser",
}
# ...
```

# Underscoreize Options

**No Underscore Before Number**

As raised in `this comment <https://github.com/krasa/StringManipulation/issues/8#issuecomment-121203018>` there are two conventions of snake case.

```text
# Case 1 (Package default)
v2Counter -> v_2_counter
fooBar2 -> foo_bar_2

# Case 2
v2Counter -> v2_counter
fooBar2 -> foo_bar2
```

By default, the package uses the first case. To use the second case, specify it in your django settings file.

```python
JSON_CAMEL_CASE = {
    # ...
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
    # ...
}
```

Alternatively, you can change this behavior on a class level by setting `json_underscoreize`:

```python
from drf_dromedary.parser import CamelCaseJSONParser
from rest_framework.generics import CreateAPIView


class NoUnderscoreBeforeNumberCamelCaseJSONParser(CamelCaseJSONParser):
    json_underscoreize = {"no_underscore_before_number": True}


class MyView(CreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
    parser_classes = (NoUnderscoreBeforeNumberCamelCaseJSONParser,)
```
# Ignore Fields

You can also specify fields which should not have their data changed.
The specified field(s) would still have their name change, but there would be no recursion.
For example:

```python
data = {"my_key": {"do_not_change": 1}}
```

Would become:

```python
{"myKey": {"doNotChange": 1}}
```

However, if you set in your settings:

```python
JSON_CAMEL_CASE = {
    # ...
    "JSON_UNDERSCOREIZE": {
        # ...
        "ignore_fields": ("my_key",),
        # ...
    },
    # ...
}
```

The `my_key` field would not have its data changed:

```python
{"myKey": {"do_not_change": 1}}
```

# Ignore Keys

You can also specify keys which should *not* be renamed.
The specified field(s) would still change (even recursively).
For example:

```python
data = {"unchanging_key": {"change_me": 1}}
```

Would become:

```python
{"unchangingKey": {"changeMe": 1}}
```

However, if you set in your settings:

```python
JSON_CAMEL_CASE = {
    # ...
    "JSON_UNDERSCOREIZE": {
        # ...
        "ignore_keys": ("unchanging_key",),
        # ...
    },
    # ...
}
```

The `unchanging_key` field would not be renamed:

```python
{"unchanging_key": {"changeMe": 1}}
```

ignore_keys and ignore_fields can be applied to the same key if required.

# Running Tests

To run the current test suite, execute the following from the root of he project:

```
$ uv run pytest
```

or to test against all combinations of Python, Djanog, and Django REST Framework:

```
$ tox
```

# License

* Free software: BSD license

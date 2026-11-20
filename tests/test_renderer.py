import importlib

import pytest
from rest_framework.renderers import JSONRenderer

from tests.render import SimpleCustomRenderer


@pytest.fixture
def reload_render(request):
    """
    Exists to provide a finalizer which reloads the render library to allow for
    changing settings which affect the CamelCaseJSONRenderer class' parent class.

    This fixture should be listed before the settings fixture.
    """
    from drf_dromedary import render

    def reload():
        importlib.reload(render)

    request.addfinalizer(reload)


def test_renderer_default_parent_class():
    from drf_dromedary import render

    assert issubclass(render.CamelCaseJSONRenderer, JSONRenderer)


def test_renderer_custom_parent_class(reload_render, settings):
    settings.JSON_CAMEL_CASE = {
        "RENDERER_CLASS": "tests.render.SimpleCustomRenderer",
    }
    from drf_dromedary import render

    importlib.reload(render)
    assert issubclass(render.CamelCaseJSONRenderer, SimpleCustomRenderer)

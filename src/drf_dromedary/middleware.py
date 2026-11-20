from __future__ import annotations

from collections.abc import Callable

from django.http import HttpRequest, HttpResponseBase

from drf_dromedary.settings import api_settings
from drf_dromedary.util import underscoreize


class CamelCaseMiddleWare:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponseBase]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponseBase:
        request.GET = underscoreize(request.GET, **api_settings.JSON_UNDERSCOREIZE)

        response = self.get_response(request)
        return response

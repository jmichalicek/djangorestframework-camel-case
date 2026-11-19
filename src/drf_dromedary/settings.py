from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.conf import settings
from django.core.signals import setting_changed
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.settings import APISettings as BaseAPISettings

USER_SETTINGS = getattr(settings, "JSON_CAMEL_CASE", {})

DEFAULTS = {
    "RENDERER_CLASS": "rest_framework.renderers.JSONRenderer",
    "PARSER_CLASS": "rest_framework.parsers.JSONParser",
    "JSON_UNDERSCOREIZE": {"no_underscore_before_number": False, "ignore_fields": None, "ignore_keys": None},
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = ("RENDERER_CLASS", "PARSER_CLASS")


class APISettings(BaseAPISettings):
    RENDERER_CLASS: type[JSONRenderer]
    PARSER_CLASS: type[JSONParser]
    JSON_UNDERSCOREIZE: Mapping[str, Any]

    @property
    def user_settings(self) -> Any:
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "JSON_CAMEL_CASE", {})
        return self._user_settings


api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)  # type: ignore[arg-type]


def reload_settings(*args: Any, **kwargs: Any) -> None:
    setting = kwargs["setting"]
    if setting == "JSON_CAMEL_CASE":
        api_settings.reload()


setting_changed.connect(reload_settings)

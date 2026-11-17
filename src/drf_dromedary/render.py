from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from rest_framework.renderers import BrowsableAPIRenderer

from drf_dromedary.settings import api_settings
from drf_dromedary.util import camelize


# This works as expected but every type checker really does not like it
# I suspect due to how DRF's APISettings class works and that this is a dynamically created attribute
class CamelCaseJSONRenderer(api_settings.RENDERER_CLASS): # type: ignore[misc, name-defined]
    json_underscoreize: Mapping[str, Any] = api_settings.JSON_UNDERSCOREIZE

    def render(self, data: Any, accepted_media_type: str | None = None, renderer_context: Mapping[str, Any] | None = None) -> str | bytes:
        return super().render(camelize(data, **self.json_underscoreize), accepted_media_type, renderer_context) # type: ignore[no-any-return]


class CamelCaseBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data: Any, accepted_media_type: str | None = None, renderer_context: Mapping[str, Any] | None = None) -> str | bytes:
        return super().render(camelize(data, **api_settings.JSON_UNDERSCOREIZE), accepted_media_type, renderer_context) # type: ignore[no-any-return]

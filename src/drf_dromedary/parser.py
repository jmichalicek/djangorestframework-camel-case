from __future__ import annotations

import json
from collections.abc import Mapping
from typing import IO, TYPE_CHECKING, Any

from django.conf import settings
from django.http.multipartparser import (
    MultiPartParser as DjangoMultiPartParser,
)
from django.http.multipartparser import (
    MultiPartParserError,
)
from django.utils.datastructures import MultiValueDict
from rest_framework.exceptions import ParseError
from rest_framework.parsers import DataAndFiles, FormParser, MultiPartParser

from drf_dromedary.settings import api_settings
from drf_dromedary.util import underscoreize

if TYPE_CHECKING:
    from django.http.request import _ImmutableQueryDict
else:
    _ImmutableQueryDict = Any


class CamelCaseJSONParser(api_settings.PARSER_CLASS):  # type: ignore[misc, name-defined]
    json_underscoreize: Mapping[str, Any] = api_settings.JSON_UNDERSCOREIZE

    # ideally this does not return Any. djangorestframework-stubs has a proper type definition, but
    # it requires type checking only imports and underscoreize() return values do not match the type def.
    def parse(
        self, stream: IO[Any], media_type: str | None = None, parser_context: Mapping[str, Any] | None = None
    ) -> Any:
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)

        try:
            data = stream.read().decode(encoding)
            return underscoreize(json.loads(data), **self.json_underscoreize)
        except ValueError as exc:
            raise ParseError(f"JSON parse error - {exc}")


class CamelCaseFormParser(FormParser):
    """
    Parser for form data.
    """

    def parse(
        self, stream: IO[Any], media_type: str | None = None, parser_context: Mapping[str, Any] | None = None
    ) -> _ImmutableQueryDict:
        return underscoreize(  # type: ignore[no-any-return]
            super().parse(stream, media_type, parser_context),
            **api_settings.JSON_UNDERSCOREIZE,
        )


class CamelCaseMultiPartParser(MultiPartParser):
    """
    Parser for multipart form data, which may include file data.
    """

    media_type = "multipart/form-data"

    def parse(
        self, stream: IO[Any], media_type: str | None = None, parser_context: Mapping[str, Any] | None = None
    ) -> DataAndFiles[_ImmutableQueryDict, MultiValueDict[Any, Any]]:
        """
        Parses the incoming bytestream as a multipart encoded form,
        and returns a DataAndFiles object.

        `.data` will be a `QueryDict` containing all the form parameters.
        `.files` will be a `QueryDict` containing all the form files.
        """
        parser_context = parser_context or {}
        request = parser_context["request"]
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)
        meta = request.META.copy()
        meta["CONTENT_TYPE"] = media_type
        upload_handlers = request.upload_handlers

        try:
            parser = DjangoMultiPartParser(meta, stream, upload_handlers, encoding)
            data, files = parser.parse()
            return DataAndFiles(
                underscoreize(data, **api_settings.JSON_UNDERSCOREIZE),
                underscoreize(files, **api_settings.JSON_UNDERSCOREIZE),
            )
        except MultiPartParserError as exc:
            raise ParseError(f"Multipart form parse error - {exc}")

from __future__ import annotations

from collections.abc import Mapping
from typing import IO, TYPE_CHECKING, Any

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

        try:
            return underscoreize(super().parse(stream, media_type, parser_context), **self.json_underscoreize)
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
        meta = request.META.copy()
        meta["CONTENT_TYPE"] = media_type

        try:
            data_and_files = super().parse(stream, media_type, parser_context)
            data_and_files.data = underscoreize(data_and_files.data, **api_settings.JSON_UNDERSCOREIZE)
            data_and_files.files = underscoreize(data_and_files.files, **api_settings.JSON_UNDERSCOREIZE)
            return data_and_files
        except MultiPartParserError as exc:
            raise ParseError(f"Multipart form parse error - {exc}")

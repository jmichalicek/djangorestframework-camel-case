from rest_framework.parsers import JSONParser


class SimpleCustomParser(JSONParser):
    pass


class AddsFooCustomParser(JSONParser):
    """
    Adds foo_ to the beginning of every key
    """

    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        return {f"foo_{k}": v for k, v in data.items()}


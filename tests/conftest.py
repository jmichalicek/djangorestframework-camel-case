from django.conf import settings


def pytest_configure():
    settings.configure(
        REST_FRAMEWORK={
            "DEFAULT_RENDERER_CLASSES": (
                "drf_dromedary.render.CamelCaseJSONRenderer",
                "drf_dromedary.render.CamelCaseBrowsableAPIRenderer",
            )
        },
    )

from __future__ import annotations

from pathlib import Path

from composed_configuration import (
    ComposedConfiguration,
    ConfigMixin,
    DevelopmentBaseConfiguration,
    HerokuProductionBaseConfiguration,
    ProductionBaseConfiguration,
    TestingBaseConfiguration,
)


class TestAppMixin(ConfigMixin):
    WSGI_APPLICATION = "test_app.wsgi.application"
    ROOT_URLCONF = "test_app.urls"

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    @staticmethod
    def mutate_configuration(configuration: ComposedConfiguration) -> None:
        # Install local apps first, to ensure any overridden resources are found first
        configuration.INSTALLED_APPS = [
            "test_app.core.apps.CoreConfig",
        ] + configuration.INSTALLED_APPS

        # Install additional apps
        configuration.INSTALLED_APPS += [
            "s3_file_field",
        ]


class DevelopmentConfiguration(TestAppMixin, DevelopmentBaseConfiguration):
    pass


class TestingConfiguration(TestAppMixin, TestingBaseConfiguration):
    pass


class ProductionConfiguration(TestAppMixin, ProductionBaseConfiguration):
    pass


class HerokuProductionConfiguration(TestAppMixin, HerokuProductionBaseConfiguration):
    pass

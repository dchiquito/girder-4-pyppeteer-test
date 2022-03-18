# Setup instructions

## Prerequisites
These instructions assume:

* Your project is built on the [cookiecutter](https://github.com/girder/cookiecutter-girder-4)
* You have a Vue-based frontend
* That Vue-based frontend is in the same repository as your Django project
* You have an existing CI pipeline that runs `tox`

If your project does not match these assumptions, keep in mind that the instructions are not tailored for your use case and will likely require some adjustments.

## Instructions

##### Add `girder-pytest-pyppeteer` and `pytest-asyncio` to your project's test dependencies
The tests you will be writing will live next to the rest of your tests, so Pytest needs to have all the fixtures and plugins available when it runs your normal suite of tests.

Installing `girder-pytest-pyppeteer` makes the plugin and fixtures available, but does not actually install [`pyppeteer`](https://github.com/pyppeteer/pyppeteer). To do that, you need to install the extra `girder-pytest-pyppeteer[pyppeteer]`.

Pyppeteer requires an async runner, so we also install `pytest-asyncio` to allow Pytest to deal with `async` test functions. You are free to use whatever async runner is convenient, but these instructions will assume `pytest-asyncio`.

##### Add the `test-pyppeteer` tox environment
To run the pyppeteer tests, you will need a new tox environment that looks something like this:

```
[testenv:test-pyppeteer]
setenv =
    # See https://docs.djangoproject.com/en/4.0/topics/async/#envvar-DJANGO_ALLOW_ASYNC_UNSAFE
    DJANGO_ALLOW_ASYNC_UNSAFE = true
    # This is necessary for the Django dev server to behave correctly
    DJANGO_CONFIGURATION = DevelopmentConfiguration
    PYPPETEER_TEST_CLIENT_COMMAND=npm run serve
    PYPPETEER_TEST_CLIENT_DIR=client
    # nodeversion >=17 deprecated some OpenSSL algorithms which a dependency is still using
    # https://nodejs.org/en/blog/release/v17.0.0/
    NODE_OPTIONS=--openssl-legacy-provider
    # I had to set this to get the browser window to show up in Ubuntu 20.04
    DISPLAY=:1
passenv =
    DJANGO_CELERY_BROKER_URL
    DJANGO_DATABASE_URL
    DJANGO_MINIO_STORAGE_ACCESS_KEY
    DJANGO_MINIO_STORAGE_ENDPOINT
    DJANGO_MINIO_STORAGE_SECRET_KEY
    DJANGO_STORAGE_BUCKET_NAME
deps =
    factory-boy
    girder-pytest-pyppeteer[pyppeteer]
    pytest
    pytest-django
    pytest-factoryboy
    pytest-mock
commands =
    pytest -m pyppeteer {posargs}
```

This should be pretty close to your existing `[testenv:test]`, but with some additions. Let's go over the differences:

* `DJANGO_ALLOW_ASYNC_UNSAFE = true` - This setting overrides [Django's aversion](https://docs.djangoproject.com/en/4.0/topics/async/#envvar-DJANGO_ALLOW_ASYNC_UNSAFE) to running in an asynchronous environment. It is required since we need to use `async` test methods to drive the pyppeteer browser.
* `DJANGO_CONFIGURATION = DevelopmentConfiguration` - This is a shortcut that uses a default [composed configuration](https://github.com/girder/django-composed-configuration) to conveniently set everything required for a more-or-less functioning server environment suitable for testing against. The `TestingConfiguration` omits several settings that are needed when running a realistic server, so the `DevelopmentConfiguration` is used instead. You may have an existing configuration that is more suitable, or you may want to set up your own custom `PyppeteerTestingConfiguration` for explicitly configuring the test environment.
* `PYPETEER_TEST_CLIENT_COMMAND` - The command used to launch the frontend server. This should generally be one of `npm run serve` or `yarn run serve`, depending on which you are using in the frontend.
* `PYPPETEER_TEST_CLIENT_DIR` - The path to the directory containing the frontend project, relative to the root of the Django project. For example, if you had two folders `my_django_app` and `my_vue_app` that contained the Django project and Vue projects respectively, this would be set to `../my_vue_app`. If instead your Vue project is contained within your Django project, like `my_django_app/my_vue_app`, this would be set to `my_vue_app`.
    * If your project is not a monorepo, you will need to make some policy decisions about where developers and the CI environment keep their Vue repository. You could require developers to clone or symlink the Vue repository to the same location (`/my_vue_app`), or perhaps document how to configure a custom tox environment that allows them to customize the location of the Vue repository. In CI, you can explicitly check out a specific tag in the Vue repository at a specific location that matches this configuration setting.
* `NODE_OPTIONS=--openssl-legacy-provider` - Required when using certain older libraries with node >= 17. The CI image uses Node version 17, so you should ensure your local development node version is similarly up to date. Hopefully at some point the legacy dependencies that are necessitating this setting will be updated and this requirement can be removed.
* `DISPLAY=:1` - This was required in my environment (Ubuntu 20.04) for the browser window to render when running locally in non-headless mode. Your mileage may vary.
* `passenv DJANGO_STORAGE_BUCKET_NAME` - This is the only setting required by the `DevelopmentConfiguration` that isn't included in the normal test configuration. You may need to include more settings here depending on your configuration.
* `deps = girder-pytest-pyppeteer[pyppeteer]` - This ensures `pyppeteer` is installed, in addition to the pytest plugin.
* `pytest -m pyppeteer {posargs}` - This invokes only the tests tagged with `@pytest.mark.pyppeteer`. 
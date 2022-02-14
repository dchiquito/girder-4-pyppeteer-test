# girder-4-pyppeteer-test
Pyppeteer testing configuration for Girder 4 applications

`pyppeteer` is not actually a required dependency. This is so that normal Girder 4 applications can include this package as a dependency without including pyppeteer tests in their normal unit test runs. Any pyppeteer tests will simply be skipped.

Pyppeteer test runs should instead use the docker image to run the tests in CI, or install `girder-pytest-pyppeteer[pyppeteer]` as a development dependency for local testing.

# Features
- page fixture
- webpack_server fixture
- conveniently runnable locally with tox
- conveniently runnable in CI with docker image

# Installation
- add `girder-pytest-pyppeteer` dependency
- tox.ini
  - addopts = -m "not pyppeteer"
  - asyncio_mode = auto
  - [testenv:test-pyppeteer]
    - DJANGO_ALLOW_ASYNC_UNSAFE = true
    - use either env vars or pytest flags
    - pytest -m pyppeteer
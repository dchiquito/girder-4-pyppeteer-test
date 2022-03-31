# Setup instructions

## Prerequisites
These instructions assume:

* Your project is built on the [cookiecutter](https://github.com/girder/cookiecutter-girder-4)
* You have a Vue-based frontend
* That Vue-based frontend is in the same repository as your Django project
* You have an existing CI pipeline that runs `tox`

If your project does not match these assumptions, keep in mind that the instructions are not tailored for your use case and will likely require some adjustments.

## Installation

### Add [`girder-pytest-pyppeteer`](https://pypi.org/project/girder-pytest-pyppeteer/) and [`pytest-asyncio`](https://pypi.org/project/pytest-asyncio/) to your project's test dependencies
The tests you will be writing will live next to the rest of your tests, so Pytest needs to have all the fixtures and plugins available when it runs your normal suite of tests.

Since `girder-pytest-pyppeteer` is still in its infancy, it's recommended that you pin to `girder-pytest-pyppeteer=={{ poetry_version() }}` to avoid any accidental breaking changes.

Installing [`girder-pytest-pyppeteer`](https://pypi.org/project/girder-pytest-pyppeteer/) makes the plugin and fixtures available, but does not actually install [`pyppeteer`](https://github.com/pyppeteer/pyppeteer). To do that, you need to install the extra `girder-pytest-pyppeteer[pyppeteer]=={{ poetry_version() }}`.

Pyppeteer requires an async runner, so we also install [`pytest-asyncio`](https://pypi.org/project/pytest-asyncio/) to allow Pytest to deal with `async` test functions. You are free to use whatever async runner is convenient, but these instructions will assume `pytest-asyncio`.

### Add the `test-pyppeteer` tox environment
To run the pyppeteer tests, you will need a new tox environment that looks something like this:

```toml
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
    PYPPETEER_NODE_OPTIONS=--openssl-legacy-provider
    # I had to set this to get the browser window to show up in Ubuntu 20.04
    DISPLAY=:1
passenv =
    DJANGO_CELERY_BROKER_URL
    DJANGO_DATABASE_URL
    DJANGO_MINIO_STORAGE_ACCESS_KEY
    DJANGO_MINIO_STORAGE_ENDPOINT
    DJANGO_MINIO_STORAGE_SECRET_KEY
    DJANGO_STORAGE_BUCKET_NAME
    PYPPETEER_BROWSER_HEADLESS
deps =
    factory-boy
    girder-pytest-pyppeteer[pyppeteer]=={{ poetry_version() }}
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
* `PYPPETEER_NODE_OPTIONS=--openssl-legacy-provider` - Required when using certain older libraries with node >= 17. The CI image uses Node version 17, so you should ensure your local development node version is similarly up to date. Hopefully at some point the legacy dependencies that are necessitating this setting will be updated and this requirement can be removed.
* `DISPLAY=:1` - This was required in my environment (Ubuntu 20.04) for the browser window to render when running locally in non-headless mode. Your mileage may vary.
* `passenv DJANGO_STORAGE_BUCKET_NAME` - This is the only setting required by the `DevelopmentConfiguration` that isn't included in the normal test configuration. You may need to include more settings here depending on your configuration.
* `passenv PYPPETEER_BROWSER_HEADLESS` - This is a debugging feature to make it easier to open the Chromium browser in non-headless mode for debugging purposes. The intended usage is to invoke tox with `PYPPETEER_BROWSER_HEADLESS=0 tox -e test-pyppeteer`.
* `deps = girder-pytest-pyppeteer[pyppeteer]=={{ poetry_version() }}` - This ensures `pyppeteer` is installed, in addition to the pytest plugin.
* `pytest -m pyppeteer {posargs}` - This invokes only the tests tagged with `@pytest.mark.pyppeteer`.

This list should be treated as a guide, not a cookiecutter. You will likely need to make some additions, omissions, and modifications to tune your project correctly. If you have any ideas that might apply more generally, issues and PRs are welcome.

## Writing your first test
Pyppeteer tests are exactly the same as normal pytest tests, just with some extra bells and whistles.

Here's a simple example of a test for the Kitware homepage:

```python
import pytest

@pytest.mark.pyppeteer
async def test_kitware_homepage(page):
    # Go to the kitware home page
    await page.goto('https://www.kitware.com/')
    # Click the "About" link
    about_link = await page.waitForXPath('//a[.="About"]')
    await about_link.click()
    # Wait one second for the page to finish loading
    await page.waitFor(1_000)
    # Implicitly assert that the page contains the text "Open Source" somewhere
    assert await page.waitForXPath('//div[contains(.,"Open Source")]') 
```

* The `@pytest.mark.pyppeteer` is required to distinguish your pyppeteer tests from your other unit/integration tests. 
* The `async` in the function definition is required because pyppeteer uses `async`/`await` to drive page actions.
* The [`page`](pytest_plugin.md#page) fixture is a [Pyppeteer Page](https://miyakogi.github.io/pyppeteer/reference.html#page-class) instance. This is what you will use to interact with the browser.

Because of its special environmental requirements, by default pyppeteer tests will not run when simply invoking `tox`. To run this test, you will need to call out pyppeteer explicitly:

```bash
tox -e test-pyppeteer
```

If you want to see the browser to confirm that it's doing what it says it's doing, run with the `PYPPETEER_BROWSER_HEADLESS` environment variable set to `False`:

```bash
PYPPETEER_BROWSER_HEADLESS=0 tox -e test-pyppeteer
```

## The [webpack_server](pytest_plugin.md#webpack_server) fixture
Now that we have confirmed pyppeteer is working, lets get the frontend plugged in. It should be as simple as:

```python
import pytest

@pytest.mark.pyppeteer
async def test_homepage(page, webpack_server):
    # Navigate to the webpack server
    await page.goto(webpack_server)
    # Wait for any JS to run
    await page.waitFor(5_000)
    # Take a screenshot
    await page.screenshot({'path': 'test_screenshot.png'})
```

Behind the scenes, the [`webpack_server`](pytest_plugin.md#webpack_server) fixture invokes the `PYPPETEER_TEST_CLIENT_COMMAND` you specified in your `tox.ini` in a background process to serve your web app. You may notice that pyppeteer tests hang for a few seconds before tests begin to execute. This is because the dev server takes a few moments to spin up.

To your test method, `webpack_server` is simply a string URL pointing to the dev server. To use it, simply navigate your `page` there.

When you run this test, you should see a `test_screenshot.png` appear in your project root. (Note that running with `PYPPETEER_BROWSER_HEADLESS=0` is generally a much better debugging tool, though.)

## Handling log ins
We now have a web site to test and a browser to test it with, but there is one more snag you will probably encounter: log ins. Girder 4 apps generally use `oauth2_provider` to handle logins, where the web server delegates to the API server to arbitrate the login process. For `oauth2_provider`, this means you need an OAuth Application model saved in the database which is configured for your specific frontend. Also, different applications have different login UX: OAuth2 providers are different, buttons are different, and signup policies are different. Furthermore, you may want to test different users being logged in to different browsers at different times and in different ways.

There is no general solution to this problem, but girder-pytest-pyppeteer does provide some tools to help you solve it yourself.

* [**The `oauth_application` fixture**](pytest_plugin.md#oauth_application) - Saves an OAuth2 Application into the DB that is configured to work with the `webpack_server`. 
* [**The `page_login` fixture**](pytest_plugin.md#page_login) - A function which saves a cookie into the `page` fixture that tricks the test API server (a fixture called [`live_server`](https://pytest-django.readthedocs.io/en/latest/helpers.html#live-server)) into thinking the given user is already logged in via the `oauth_application` fixture. 

With `page_login`, you can easily skip the API half of the OAuth2 workflow. Without it, you would need to set up users with passwords, and then write some pyppeteer code that manually types the user's login information into the browser. However, note that the frontend still doesn't know that the user has already authenticated with the API server. This sample code illustrates one way around the problem:

```python
import pytest

@pytest.fixture
def log_in(webpack_server, page, page_login):
    """Log the given user into the page."""
    # Return a helper that can be used to log in any given User
    async def _log_in(user):
        # Invoke the page_login fixture
        await page_login(page, user)
        # The API server now thinks that the user has already logged in using the browser.
        # Navigate to the dev server
        await page.goto(webpack_server)
        # Find the login button
        login_button = await page.waitForXPath('//button[contains(., "Login")]')
        # Click it
        await login_button.click()
        # Clicking login should redirect the browser to the API server,
        # which sees the cookie set by `page_login` and redirects the browser back to the dev server,
        # with some URL parameters containing the OAuth2 session token.
        # After all this navigation resolves (asynchronously), the browser should be logged in.
        return page

    return _log_in


@pytest.mark.pyppeteer
async def test_pyppeteer(page, log_in, user, webpack_server):
    await log_in(user)
    # Assert that the page contains the welcome message for logged in users
    # This has the side effect of waiting for the redirects to finish resolving
    assert await page.watForXPath(f'//div[.="Welcome, {user.email}!"]')
```

## CI
At this point, you have everything you need to write a test and to run it locally. The last step is to run your tests in CI next to your regular workflow. This can be easily accomplished using the [GitHub Action](github_action.md).

Since pyppeteer tests serve an adjacent purpose to the rest of your pytests, I recommend setting up a separate job to run them rather than simply running them before/after the rest of the `tox` suite. This unfortunately means that much of the backing service configuration needs to be copy/pasted.

Here is an example GitHub workflow:
```yaml
name: ci
on:
  ... default values ...
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        ...
      rabbitmq:
        ...
      minio:
        ...
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.9"
      - name: Install tox
        run: |
          pip install --upgrade pip
          pip install tox
      - name: Run tests
        run: |
          tox
        working-directory: test-app
        env:
          DJANGO_DATABASE_URL: postgres://postgres:postgres@localhost:5432/django
          DJANGO_MINIO_STORAGE_ENDPOINT: localhost:9000
          DJANGO_MINIO_STORAGE_ACCESS_KEY: minioAccessKey
          DJANGO_MINIO_STORAGE_SECRET_KEY: minioSecretKey
  test-pyppeteer:
    runs-on: ubuntu-latest
    services:
      postgres:
        ... same as above ...
      rabbitmq:
        ... same as above ...
      minio:
        ... same as above ...
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        uses: docker://ghcr.io/girder/pytest-pyppeteer:{{ gh_action_version() }}
        with:
          install_directory: test-client
          install_command: yarn install
          test_directory: test-app
          test_command: tox -e test-pyppeteer
        env:
          DJANGO_DATABASE_URL: postgres://postgres:postgres@postgres:5432/django
          DJANGO_MINIO_STORAGE_ENDPOINT: minio:9000
          DJANGO_MINIO_STORAGE_ACCESS_KEY: minioAccessKey
          DJANGO_MINIO_STORAGE_SECRET_KEY: minioSecretKey
          DJANGO_STORAGE_BUCKET_NAME: integration-test-bucket
```

You will need to set the values of `install_directory`, `install_command`, `test_directory`, and `test_command` appropriately for your repository.
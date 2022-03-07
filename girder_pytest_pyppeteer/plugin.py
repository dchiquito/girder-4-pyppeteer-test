import os

import pytest
import re
import shlex
import signal
from subprocess import PIPE, Popen, TimeoutExpired

# def pytest_configure(config) -> None:
#     config.addinivalue_line("markers", "options(kwargs): update browser initial options.")

def pytest_addoption(parser, pluginmanager):
    parser.addoption(
        "--client-command",
        dest='PYPPETEER_TEST_CLIENT_COMMAND',
        help="The command to start the test client",
        default=os.getenv('PYPPETEER_TEST_CLIENT_COMMAND'),
    )
    parser.addoption(
        "--client-dir",
        dest='PYPPETEER_TEST_CLIENT_DIR',
        help="The directory to start the test client in",
        default=os.getenv('PYPPETEER_TEST_CLIENT_DIR'),
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "pyppeteer: This is a pyppeteer test.")


@pytest.fixture(scope='session')
def _pyppeteer_config(request):
    config = {
        'PYPPETEER_TEST_CLIENT_COMMAND': request.config.getoption('PYPPETEER_TEST_CLIENT_COMMAND'),
        'PYPPETEER_TEST_CLIENT_DIR': request.config.getoption('PYPPETEER_TEST_CLIENT_DIR'),
    }
    for key, value in config.items():
        if value is None:
            pytest.fail(f'{key} not defined')
    return config

@pytest.fixture(scope='session')
def webpack_server(_pyppeteer_config, live_server):
    try:
        import pyppeteer
        import pytest_asyncio
    except ModuleNotFoundError as e:
        pytest.skip(f'{e.name} not found')
    env = {
        **os.environ,
        'VUE_APP_API_URL': f'{live_server.url}/api/v1',
        'VUE_APP_OAUTH_API_ROOT': f'{live_server.url}/oauth/',
    }

    command = ['/usr/bin/env'] + shlex.split(_pyppeteer_config['PYPPETEER_TEST_CLIENT_COMMAND'])
    print(f'Launching node server with {command}')
    process = Popen(
        command,
        cwd=_pyppeteer_config['PYPPETEER_TEST_CLIENT_DIR'],
        env=env,
        stdout=PIPE,
        stderr=PIPE,
        preexec_fn=os.setsid,
    )
    try:
        # Wait until the server starts by polling stdout
        max_timeout = 60
        retry_interval = 3
        err = b''
        for _ in range(0, max_timeout // retry_interval):
            try:
                _out, err = process.communicate(timeout=retry_interval)
            except TimeoutExpired as e:
                if match := re.search(
                    b'App running at:\n  - Local:   (http[s]?://[a-z]+:[0-9]+/?) \n', e.stdout
                ):
                    url = match.group(1).decode('utf-8')
                    break
        else:
            raise Exception(f'webpack server failed to start: {err}')
        yield url
    finally:
        # Kill every process in the webpack server's process group
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            # TODO set up some signal handlers to ensure it always gets cleaned up
        except ProcessLookupError:
            # The process has already terminated, no need to intervene
            pass


# @pytest.fixture
# def npm_serve(webpack_server, admin_user):
#     makeclient.callback(username=admin_user.username, uri=webpack_server + '/')
#     return webpack_server


@pytest.fixture
async def page(live_server, client, user):
    try:
        import pyppeteer
        from pyppeteer.errors import BrowserError
        import pytest_asyncio
    except ModuleNotFoundError as e:
        pytest.skip(f'{e.name} not found')
    client.force_login(user)
    sessionid = client.cookies['sessionid'].value
    try:
        browser = await pyppeteer.launch(
            ignoreHTTPSErrors=True,
            headless=True,
            defaultViewport={'width': 1024, 'height': 800},
            args=['--no-sandbox'],
        )
    except BrowserError as e:
        # TODO log the invocation that failed using Launcher(**kwargs).cmd
        raise e
    page = await browser.newPage()
    await page.setCookie(
        {
            'name': 'sessionid',
            'value': sessionid,
            'url': live_server.url,
            'path': '/',
        }
    )

    @page.on('console')
    def console_log_handler(message):
        print('AAAH', message.type, message.args, message.text)

    yield page
    await browser.close()

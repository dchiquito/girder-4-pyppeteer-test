# Debugging common problems

## Running in non-headless mode
Because tests must run in a CI environment which obviously don't have a display environment, girder-pytest-pyppeteer defaults to launching Chromium in headless mode. However, when debugging a pyppeteer test, it is frequently invaluable to see and interact with the browser as the test is running.

This can be achieved by setting the environment variable `PYPPETEER_BROWSER_HEADLESS=0`. In the [recommended `tox.ini` configuration](setup.md#installation), `PYPPETEER_BROWSER_HEADLESS` is set to be passed through from the shell environment, so you can simply invoke tox like this:

```bash
PYPPETEER_BROWSER_HEADLESS=0 tox -e test-pyppeteer
```

Since the test will generally use the page much faster than a human would, using `breakpoint()` or other debugging tools is also recommended so you have time to inspect the browser state.

## Running in a container
The [cookiecutter recommends running tox like this](https://github.com/girder/cookiecutter-girder-4/blob/d1912b887133ae2407277f772f6329c082fafb73/%7B%7B%20cookiecutter.project_slug%20%7D%7D/README.md#initial-setup-2):

```bash
docker-compose run --rm django tox
```

This is sadly not supported at this time; you will need to run `tox` natively for pyppeteer to work correctly.

## Why aren't my Celery tasks running?
There is sadly no way to have Celery tasks run normally (i.e. asynchronously) while running pyppeteer tests. This is a drawback of using the [`live_server`](https://pytest-django.readthedocs.io/en/latest/helpers.html#live-server) fixture. To keep test data atomic, `live_server` wraps the entire test in a transaction so that it can easily reset the database after the test is over. Within the test thread, this is not a huge concern. However, external services like Celery obviously cannot interact with the transaction, so there is no way for Celery tasks to read or write test data.

The workaround is to use [`CELERY_TASK_ALWAYS_EAGER`](https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-always-eager) to force your Celery tasks to execute immediately instead of being queued. Because they execute within the test context, they will be within the bounds of the `live_server` transaction and will be able to read and write test data.

The default configuration specifies `DJANGO_CONFIGURATION = DevelopmentConfiguration` in `tox.ini`. To enable `CELERY_TASK_ALWAYS_EAGER`, you will probably need a new configuration:

```python
class PyppeteerTestingConfiguration(TestAppMixin, DevelopmentBaseConfiguration):
    ... copy required config from DevelopmentConfiguration ...
    CELERY_TASK_ALWAYS_EAGER = True
```

You can then specify `DJANGO_CONFIGURATION = PyppeteerTestingConfiguration` in your `tox.ini` to use that new configuration in your pyppeteer tests.

Note that any code that `delay`s a task will now block until the task is complete, which may break assumptions.

## Browser closed unexpectedly: cannot open display
When running in non-headless mode in Ubuntu, you may encounter this error:
```
LaunchProcess: failed to execvp:
/home/daniel/.local/share/pyppeteer/local-chromium/588429/chrome-linux/nacl_helper
[1722838:1722838:0322/221316.140551:ERROR:nacl_fork_delegate_linux.cc(314)] Bad NaCl helper startup ack (0 bytes)

(chrome:1722836): Gtk-WARNING **: 22:13:16.142: cannot open display: :2
```
I was able to resolve this by setting the `DISPLAY=:1` environment variable in `tox.ini`, then running `DISPLAY=:1 xhost +` to open up your X server. 

See https://stackoverflow.com/questions/28392949/running-chromium-inside-docker-gtk-cannot-open-display-0#28395350

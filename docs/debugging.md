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

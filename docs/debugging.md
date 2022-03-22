# Debugging common problems

## Running in non-headless mode
TODO you can't do this yet

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

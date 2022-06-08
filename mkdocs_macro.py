import pkg_resources


def define_env(env):
    @env.macro
    def poetry_version():
        return pkg_resources.get_distribution('girder-pytest-pyppeteer').version

    @env.macro
    def gh_action_version():
        return f'v{pkg_resources.get_distribution("girder-pytest-pyppeteer").version}'

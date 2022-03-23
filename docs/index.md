# girder-pytest-pyppeteer

[girder-pytest-pyppeteer](https://github.com/girder/girder-pytest-pyppeteer) is a toolkit that makes it easy to use [pyppeteer](https://github.com/pyppeteer/pyppeteer) to implement browser-based end-to-end testing for [Girder 4 applications](https://github.com/girder/cookiecutter-girder-4).

## Components
Girder 4 applications all share a common stack, but implementation and deployment details tend to differ between applications. Since end-to-end testing necessarily involves deploying the whole application into a test environment, there is no one size fits all plugin that can be used for end-to-end testing.

Instead, girder-pytest-pyppeteer offers you a number of tools for setting up your end-to-end tests:

* [**A pytest plugin**](pytest_plugin.md) - Defines helpful fixtures that set up and manipulate the browser context.
* [**A GitHub Action**](github_action.md) - Easily run your tests in CI
* [**Installation instructions**](setup.md) - Get started ASAP
* ** *Coming Soon!* Vuetify locators** - Identify Vuetify page elements without sweating about locators

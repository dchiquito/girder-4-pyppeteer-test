# girder-pytest-pyppeteer
A collection of tools for using [pyppeteer](https://github.com/pyppeteer/pyppeteer) to implement browser-based end-to-end testing for [Girder 4 applications](https://github.com/girder/cookiecutter-girder-4). This toolkit will enable you to easily write tests for your entire application stack that behave like real users interacting with a real web browser.

Specifically, **girder-pytest-pyppeteer** is
- A pytest plugin
- A [GitHub Action](https://github.com/girder/girder-pytest-pyppeteer/pkgs/container/pytest-pyppeteer)
- Instructions and examples for installation

## The problem
Generally, writing useful browser-based end-to-end tests is difficult for a number of reasons.

- **Writing them is hard.** To write a browser test, you need to use a browser interface tool like [Selenium](https://www.selenium.dev/) or [Puppeteer](https://developers.google.com/web/tools/puppeteer/), and then integrate it into your testing framework and pipeline. This specialized tooling requires specialized knowledge.
- **Orchestrating them is hard.** Unlike a unit test, a browser test requires the entire application with all its sub-services to be running before the browser can even open the page. Managing all those moving parts while creating and destroying test data is an often overlooked cost to writing a useful browser test.
- **Running them is hard.** Browser testing tools require a browser, which means that the browser executable must be packaged and installed before any tests can be run. In addition to all the required services, that means a separate environment to be accomodated for CI and for every developer who wants to write/run tests.

## Features
Luckily, Girder 4 applications have a bit of homogeneity, at least enough to build a browser testing toolkit.

- **Tests are written with [pytest](https://docs.pytest.org/), [pyppeteer](https://github.com/pyppeteer/pyppeteer), and [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html).** This means you can write and store your browser tests right next to your Django unit tests, and run them with [tox](https://tox.wiki/). Various pyppeteer fixtures are provided, so you don't need to worry about invoking pyppeteer yourself.
- **Django and node servers are managed by fixtures.** [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html) provides a handy fixture `live_server`, which runs a real web server backed by the test database. This makes it trivial to create models for testing; simply save a model in the test method, and it will be available immediately to the web frontend. The node server is provided by the `webpack_server` fixture, and is automatically plugged in to the Django `live_server`. Other service dependencies (Minio, RabbitMQ, etc.) are expected to be provided through docker containers, just like in normal Django unit tests.
- **Pyppeteer is easy to run locally.** If you already have Chrome installed, installing `pyppeteer` package will handle the rest. It automatically bundles the required Chromium version, so you don't need to worry about browser installation or versioning.
- **A GitHub Action is provided for running in CI.** The action has everything installed and wired up. All you need to do is add a new step to your existing CI that invokes the action.

## Is girder-pytest-pyppeteer right for me?
This project provides solutions by making assumptions. If those assumptions are violated, this toolkit might not be the best fit, although individual parts can always be used in isolation.

This is the toolkit for you if:
- **You want to write browser tests for your entire application.** If you only want to test your frontend in isolation, you probably want to look into [component testing](https://v2.vuejs.org/v2/cookbook/unit-testing-vue-components.html?redirect=true) with [Jest](https://jestjs.io/).
- **Your project was ejected from [the Girder 4 cookiecutter](https://github.com/girder/cookiecutter-girder-4).** If you're using a similar stack you should still be able to adopt this project, but it will be a little bumpier.
- **You have an SPA.** The web server needs to launchable with a single command like `npm run serve` or `yarn run serve`.
- **You are using GitHub Actions.** A custom GitHub action is provided, which obviously only works in GitHub actions.
- **You have your backend and frontend in the same repository.** It's possible to pull from a different repository in a GitHub workflow, but managing versions and releases is much harder.


# Installation
TODO

# Writing tests
TODO

# Running tests
TODO
# GitHub Action
The GitHub Action is provided as a [GitHub package](https://github.com/girder/girder-pytest-pyppeteer/pkgs/container/pytest-pyppeteer) that can be embedded into your GitHub Actions workflow right next to the rest of your CI.

## Normal usage

Pyppeteer tests require a test environment that looks basically the same as the development environment. Fortunately, the [default CI configuration](https://github.com/girder/cookiecutter-girder-4/blob/d1912b887133ae2407277f772f6329c082fafb73/%7B%7B%20cookiecutter.project_slug%20%7D%7D/.github/workflows/ci.yml) already includes the default services (postgres, minio, and rabbitmq), and if your application requires more services you have almost definitely already set them up in CI. You should be able to simply copy/paste your existing CI service definitions into a new job/workflow.

Invoking the GitHub action should look something like this:
```yaml
name: Example integration tests
on:
  ...
jobs:
  test-pyppeteer:
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

You can also look at the [test app's workflow](https://github.com/girder/girder-pytest-pyppeteer/blob/main/.github/workflows/example-integration-tests.yml) to see an example that is actually running in the wild.

## Configuration
The following (hopefully self-explanatory) inputs are available to the Action:

<!-- Disgusting, but required to keep the column width from shrinking into illegibility -->
Input&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|Example Value&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|Description
---|---|---
`install_directory`|`web`|The directory containing the web app. If your web app is in a separate repository, you can use `actions/checkout@v2` to check it out into a separate directory, then use the absolute path to that directory here.
`install_command`|`npm install` or `yarn install`|The command used to install the web app.
`test_directory`|`django-app` or `.`|The directory containing the Django app.
`test_command`|`tox -e test-pyppeteer`|The command used to run the pyppeteer tests. This should be `tox -e test-pyppeteer` unless you explicitly modified your `tox.ini`.

FROM python:3.8-slim
# Install system libraries for Python packages:
# * psycopg2
RUN apt-get update && \
    apt-get install --no-install-recommends --yes \
        libpq-dev gcc libc6-dev \
        # Required to run the dev server
        npm yarn \
        # Required by pyppeteer
        chromium libxcursor1 libxss1 libpangocairo-1.0-0 libgtk-3-0 && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# # Only copy the setup.py, it will still force all install_requires to be installed,
# # but find_packages() will find nothing (which is fine). When Docker Compose mounts the real source
# # over top of this directory, the .egg-link in site-packages resolves to the mounted directory
# # and all package modules are importable.
# COPY ./setup.py /opt/django-project/setup.py
# RUN pip install --editable /opt/django-project[dev]
#
# # Use a directory name which will never be an import name, as isort considers this as first-party.
# WORKDIR /opt/django-project

RUN pip install \
    # Standard django dependencies
    celery \
    django \
    django-allauth \
    django-composed-configuration \
    django-configurations[database,email] \
    django-extensions \
    django-filter \
    django-oauth-toolkit \
    djangorestframework \
    django-click \
    django-guardian \
    drf-yasg \
    uri \
    # Standard test dependencies
    factory-boy \
    pytest \
    pytest-django \
    pytest-factoryboy \
    pytest-mock \
    # pyppeteer dependencies
    pytest-asyncio \
    pyppeteer \
    # Some extras?
    django-cors-headers \
    django-debug-toolbar \
    django-girder-style \
    django-girder-utils \
    django-s3-file-field[minio,s3] \
    psycopg2 \
    rich \
    whitenoise \
    # Definitely only miqa
    pandas \
    schema \
    # tox
    tox

ENV DJANGO_ALLOW_ASYNC_UNSAFE=true

RUN pyppeteer-install

COPY execute-test-command.sh execute-test-command.sh

ENTRYPOINT ./execute-test-command.sh
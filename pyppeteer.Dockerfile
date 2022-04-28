FROM python:3.9-slim
# Install system libraries for Python packages:
# * psycopg2
RUN apt-get update && \
    apt-get install --no-install-recommends --yes \
        libpq-dev gcc libc6-dev \
        # Required to install node
        curl gnupg \
        # Include git for packages using setuptools_scm
        git \
        # Required by pyppeteer
        chromium libxcursor1 libxss1 libpangocairo-1.0-0 libgtk-3-0 && \
    # Install node 17
    curl -sL https://deb.nodesource.com/setup_17.x  | bash - && \
    apt-get install --no-install-recommends --yes \
        nodejs && \
    rm -rf /var/lib/apt/lists/*
# Install yarn in case projects are using that to launch dev server
# Install Vue CLI for the webpack server
RUN npm install --global yarn @vue/cli

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Required to allow async tests in Django
ENV DJANGO_ALLOW_ASYNC_UNSAFE=true

# # Only copy the setup.py, it will still force all install_requires to be installed,
# # but find_packages() will find nothing (which is fine). When Docker Compose mounts the real source
# # over top of this directory, the .egg-link in site-packages resolves to the mounted directory
# # and all package modules are importable.
# COPY ./setup.py /opt/django-project/setup.py
# RUN pip install --editable /opt/django-project[dev]
#
# # Use a directory name which will never be an import name, as isort considers this as first-party.
# WORKDIR /opt/django-project

# Tests should always be run with tox, so that is the only dependency installed now
# We also install pyppeteer so we can pre-install chromium easily
RUN pip install tox pyppeteer

RUN pyppeteer-install

COPY execute-test-command.sh execute-test-command.sh

ENTRYPOINT ["/bin/sh", "/execute-test-command.sh"]

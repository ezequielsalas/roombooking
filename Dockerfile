FROM python:3.9-buster AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y \
    make \
    apt-utils \
    vim \
    postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt ./

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt && \
    find /usr/local \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' +

RUN rm /etc/localtime
RUN ln -s /usr/share/zoneinfo/America/New_York  /etc/localtime


# Development
FROM base AS development
EXPOSE 8000
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
COPY ./tools/scripts/wait_for_database.sh /entrypoint
RUN chmod +x /entrypoint
ENTRYPOINT ["/entrypoint"]
ARG BUILD_NO="development"
ENV BUILD=$BUILD_NO
ENV DJANGO_SETTINGS_MODULE="booking_core.dev_settings"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


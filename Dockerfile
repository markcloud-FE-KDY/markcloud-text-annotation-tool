FROM python:3.10-alpine
RUN apk update && apk upgrade
RUN apk add --no-cache pkgconfig \
                       gcc \
                       openldap \
                       libcurl \
                       gpgme-dev \
                       libc-dev \
                       && rm -rf /var/cache/apk/*


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN . /opt/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Run the application:
COPY . /service

WORKDIR /service
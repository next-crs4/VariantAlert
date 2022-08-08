FROM python:3.8

ARG USER_ID
ARG GROUP_ID
ARG BATCH_SIZE

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN mkdir /config
ADD /config/requirements.pip /config/

RUN apt -qq update && \
    apt install --no-install-recommends -y apt-utils rsync

RUN apt autoremove -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r /config/requirements.pip && \
    rm -rf ~/.cache/

RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -m -u ${USER_ID} -g appuser appuser

USER appuser

ENV  BATCH_SIZE="${BATCH_SIZE}"

FROM python:3

ARG USER_ID
ARG GROUP_ID

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN mkdir /config
ADD /config/requirements.pip /config/


RUN apt-get -qq update && \
    apt-get install --no-install-recommends -y apt-utils rsync && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip install -r /config/requirements.pip && \
    rm -rf ~/.cache/ && \
    groupadd -g ${GROUP_ID} appuser && \
    useradd -m -u ${USER_ID} -g appuser appuser

USER appuser



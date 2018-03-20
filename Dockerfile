FROM armv7/armhf-ubuntu
RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-virtualenv \
    python-setuptools \
    gcc-multilib \
    git \
    ssh \
    --no-install-recommends \
    && pip install --upgrade pip \
    && pip install wheel
WORKDIR /usr/app
COPY requirements.txt /usr/app
RUN pip install -r requirements.txt
COPY . /usr/app
CMD python Read.py

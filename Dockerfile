FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /qrcode && apt-get update && apt-get install -y postgresql \
                           postgresql-client \
                           libpq-dev

WORKDIR /processos
COPY requirements.txt /processos/
RUN pip install -r requirements.txt
COPY . /processos
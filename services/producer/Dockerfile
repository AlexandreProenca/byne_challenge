FROM python:3.8

COPY . /app
RUN pip install  aiohttp aioredis ujson
WORKDIR app
CMD python3 number_producer.py

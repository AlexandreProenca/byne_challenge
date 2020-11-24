FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY . /app
WORKDIR app

RUN pip install fastapi uvicorn python-jose aioredis

CMD uvicorn main:app --host 0.0.0.0 --port 8000 --forwarded-allow-ips='*' --proxy-headers

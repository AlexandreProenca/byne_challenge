FROM python:3.8

COPY . /app
RUN pip install flask python-jose
WORKDIR app
CMD python3 flask_api.py

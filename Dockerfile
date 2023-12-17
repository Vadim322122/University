FROM python:3.11.4-slim

RUN apt-get update && apt-get install -y supervisor

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]

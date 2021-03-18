FROM python:3.8

RUN apt update && apt install ffmpeg -y


RUN mkdir -p /usr/app/
WORKDIR /usr/app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install psycopg2
RUN pip install -r requirements.txt
COPY . .

RUN chmod +x deploy.sh

ENTRYPOINT ["/usr/app/deploy.sh"]


CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 -k gevent --workers 4

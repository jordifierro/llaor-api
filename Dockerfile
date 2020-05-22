FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD python manage.py collectstatic && gunicorn --bind 0.0.0.0:$PORT llaor.wsgi

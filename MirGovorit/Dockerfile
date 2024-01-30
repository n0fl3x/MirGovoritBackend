FROM python:3.10.12-slim

WORKDIR usr/src/app

ENV PYTHONUNBUFFERED=1

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=''

COPY . .

COPY .env .

RUN pip install -r requirements.txt

RUN python manage.py migrate
RUN python manage.py createsuperuser --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

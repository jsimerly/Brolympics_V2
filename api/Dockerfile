FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1 \
    DJANGO_ENV=production
    
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

WORKDIR /api

COPY . /api

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "api.wsgi:application", "--bind", "0.0.0.0:8000"]

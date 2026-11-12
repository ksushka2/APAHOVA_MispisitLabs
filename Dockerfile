FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["sh", "-c", "python manage.py migrate --noinput --fake-initial && python manage.py init_notifications && exec gunicorn it_school.wsgi:application --bind 0.0.0.0:8080 --threads 2"]


FROM python:3.14-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings.dev

EXPOSE 8000 8001

CMD python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000 & \
    uvicorn api.main:app --host 0.0.0.0 --port 8001

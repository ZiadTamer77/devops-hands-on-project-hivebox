FROM python:3.11.15-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY . .

CMD ["python", "/app/main.py","--version"]




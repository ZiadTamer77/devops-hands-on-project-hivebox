FROM python:3.11.15-slim-trixie

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

RUN useradd -m appuser && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

ENTRYPOINT ["python", "main.py"]
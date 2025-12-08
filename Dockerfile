FROM python:3.12-slim

WORKDIR /app

ENV IN_DOCKER=true

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app
COPY web /app/web

EXPOSE 8080
CMD ["uvicorn", "app.web.server:app", "--host", "0.0.0.0", "--port", "8080"]

FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn python-dotenv google-generativeai python-multipart jinja2 sqlalchemy

EXPOSE 8080
CMD ["uvicorn", "web.main_web:app", "--host", "0.0.0.0", "--port", "8080"]

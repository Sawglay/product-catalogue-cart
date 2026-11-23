FROM python:3.14.7-slim

WORKDIR /backend-api
COPY pyproject.toml README.md ./
COPY app ./app
RUN python -m pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

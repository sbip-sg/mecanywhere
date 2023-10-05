FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

# use --no-cache-dir in production
RUN echo "STARTING PO SERVICE..." && \
    pip install -r requirements.txt

COPY . .

ENTRYPOINT ["uvicorn", "main:app", "--port", "8000", \
    "--host", "0.0.0.0", \
    "--reload", \
    "--forwarded-allow-ips", "*"]

EXPOSE 8000

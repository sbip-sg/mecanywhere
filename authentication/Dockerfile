FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

# use --no-cache-dir in production
RUN echo "STARTING PO SERVICE..." && \
    pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--port", "8000", \
    "--host", "0.0.0.0", \
    "--reload", \
    # if using reverse proxy, use this
    # "--root-path", "/authentication", \
    "--forwarded-allow-ips", "*"]

EXPOSE 8000

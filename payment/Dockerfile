FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

# use --no-cache-dir in production
RUN echo "STARTING PAYMENT SERVICE..." && \
    pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--port", "7002", \
    "--host", "0.0.0.0", \
    "--reload", \
    # if using reverse proxy, use this
    # "--root-path", "/payment", \
    "--forwarded-allow-ips", "*"]

EXPOSE 7002

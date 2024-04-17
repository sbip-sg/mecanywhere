FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

# use --no-cache-dir in production
RUN echo "STARTING TEMPLATE SERVICE..." && \
    pip install -r requirements.txt

COPY src src
COPY config config

WORKDIR /app/src

ENTRYPOINT ["python"]

FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

# use --no-cache-dir in production
RUN echo "STARTING TOWER SERVICE..." && \
    pip install -r requirements.txt

COPY src src
COPY config.json config.json

WORKDIR /app/src

ENTRYPOINT ["python", "main.py"]

EXPOSE 7000

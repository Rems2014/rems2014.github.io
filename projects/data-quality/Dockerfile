FROM python:3.11-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless ca-certificates && rm -rf /var/lib/apt/lists/*
ENV SPARK_VERSION=3.5.0 PYSPARK_PYTHON=/usr/local/bin/python PYSPARK_DRIVER_PYTHON=/usr/local/bin/python SPARK_LOCAL_IP=127.0.0.1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY Data_quality.py .
CMD ["python", "-u", "Data_quality.py"]

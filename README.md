# The Ultimate Proof of Concept (POC)

This is a POC app to learn about how http requests are handled by backend servers and what are the general bottlenecks. To replicate the bottlenecks the resources of the app are limited to 1 cpu and 256m memory. The app is containerized using Docker and uses tools like Vegeta, StatsD Exporter, and Prometheus for testing and monitoring.

## Progress

1. Created a simple Django app and ran it in debug mode inside a docker container. It was able to handle upto 500 QPS upto 30 seconds.
2. Ran the app using gunicorn and adjusted the number of workers and threads so that the app can handle upto 1500 QPS upto 30 seconds.
3. Using prom/statsd-exporter and prometheus to capture the metrics provided by gunicorn.

## Prerequisites

Ensure that you have the following installed on your system:

- Docker
- Python3

## Getting Started

### 1. Clone the Repository

```bash
# Replace <repository-url> with the actual URL of your repository
git clone <repository-url>
cd the_ultimate_poc
```

### 2. Pull Required Docker Images

Pull the necessary Docker images:

```bash
docker pull python:3.11-slim
docker pull prom/statsd-exporter
docker pull prom/prometheus
docker pull peterevans/vegeta
```

### 3. Build the Application Image

Build the Docker image for the application:

```bash
docker build -t tup .
```

### 4. Run the Application Container

Run the application container with restricted resources:

```bash
docker run --network tup_network --rm -d --name tup --cpus=1.0 --memory=256m tup
```

### 5. Run Load Testing with Vegeta

Use Vegeta to perform load testing on the application:

```bash
docker run --network tup_network --rm -i peterevans/vegeta sh -c \
"echo 'GET http://tup:8000/hello' | vegeta attack -rate=1500 -duration=30s | tee results.bin | vegeta report"
```

### 6. Start StatsD Exporter

Run the StatsD Exporter container:

```bash
docker run --rm --cpus=1.0 --memory=256m -dP --network tup_network -v ${PWD}/statsd.conf:/statsd/statsd.conf --name statsd_exporter prom/statsd-exporter "--statsd.mapping-config=/statsd/statsd.conf"
```

### 7. Start Prometheus

Run the Prometheus container for monitoring:

```bash
docker run --rm --cpus=1.0 --memory=256m -d --network tup_network -v ${PWD}/prom.yml:/home/prom.yml --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus "--config.file=/home/prom.yml"
```

## Configuration Files

### statsd.conf

Place your StatsD Exporter configuration in `statsd.conf` at the root of the project directory. Example:

```yaml
mappings:
  - match: "example.metric.*"
    name: "example_metric"
    labels:
      label1: "$1"
      label2: "$2"
```

### prom.yml

Place your Prometheus configuration in `prom.yml` at the root of the project directory. Example:

```yaml
scrape_configs:
  - job_name: 'statsd'
    static_configs:
      - targets: ['statsd_exporter:9102']
```

## Notes

- Replace `tup_network` with your actual Docker network name, or create it if it doesn’t exist:

```bash
docker network create tup_network
```

- Ensure that `statsd.conf` and `prom.yml` are correctly configured based on your monitoring requirements.

## Cleanup

To stop and remove all containers:

```bash
docker stop tup statsd_exporter prometheus
```

To remove the Docker network (if created manually):

```bash
docker network rm tup_network
```


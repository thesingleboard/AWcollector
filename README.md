# AWcollector

A Prometheus collector for the Ambient Weather [API](https://ambientweather.docs.apiary.io/#introduction/authentication).

## Setup

**Tools used**

Python Prometheus v0.17.1
Docker

**Build**

Build the container with the *build_container.sh* shell script.

**Environment Variables**

You will need to set several environment variables in order for the container to operate properly.

```bash
AMBIENT_ENDPOINT='https://api.ambientweather.net/v1'
AMBIENT_API_KEY='xxxxxxx'
AMBIENT_APPLICATION_KEY='xxxxxxx'
```

**Run the container**

In this example the collectors internal scrape port 9028 is passed through to the outside world on the same port on the Docker network called container_net.

```bash
docker run -d -p 9028:9028 --network container_net --name AWcollector -e AMBIENT_APPLICATION_KEY="xxxxx" -e AMBIENT_API_KEY="xxxxx" -e AMBIENT_ENDPOINT="https://api.ambientweather.net/v1" AWcollector:latest
```

## Prometheus Config

**Config**
```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s
rule_files:
  - /etc/prometheus/prometheus.rules
alerting:
  alertmanagers:
  - scheme: http
    static_configs:
    - targets:
      - "alertmanager.monitoring.svc:9093"

scrape_configs:
  - job_name: 'AWcollector'
    metrics_path: /metrics
    static_configs:
      - targets: ['192.168.10.88:9028']
```

## Grafana Dash

Build the dashboards
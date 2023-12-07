# AWcollector

A Prometheus collector for the Ambient Weather [API](https://ambientweather.docs.apiary.io/#introduction/authentication).

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

The container 

```bash
docker run -d -p 9028:9028 --network container_net --name connectorbot -e AMBIENT_APPLICATION_KEY="xxxxx" -e AMBIENT_API_KEY="xxxxx" -e AMBIENT_ENDPOINT="https://api.ambientweather.net/v1" connectorbot:latest
```
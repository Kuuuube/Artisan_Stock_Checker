# Discord Webhook Script Docker Deployment

Note: Docker images are not maintained by Kuuuube.

## Requirements

Docker: [Installation Guide](https://docs.docker.com/engine/install/)

Ensure proper permissions are set on the volume mount should you run the container as non-root.

## Deployment

### Docker Run

```shell
docker run -d \
  --restart unless-stopped \
  --name artisan-stock-checker \
  --user $(id -u):$(id -g) \
  -e ARTISAN_STOCK_CHECKER_CONFIG_DIR=/config \
  -v $(pwd)/artisan-data:/config \
  matthewdesouza/artisan-stock-checker:latest
```

### Docker Compose

See [compose.yaml](../compose.yaml).

Ensure that you properly set the .env file, otherwise default values will be used regardless of the .env file being present.

#### Compose Variables

| Variable | Default Value | Required? |                                Purpose                                 |
| :------: | :-----------: | :-------: |:----------------------------------------------------------------------:|
| PUID | 1000 | ❌ |            Set which user the container will deploy under.             |
| PGID | 1001 | ❌ |            Set which group the container will deploy under.            |
| ARTISAN_STOCK_CHECKER_CONFIG_DIR | /config | ❌ | Set which folder will contain the generated data within the container. |
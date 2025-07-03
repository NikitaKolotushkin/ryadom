# ryadom
Event-management app


### Установка

```bash
```


### Прочие указания

**Запуск контейнера:**

```bash
DOCKER_BUILDKIT=1 docker build --secret id=github_token,src=.github_token -t <container_name> .
docker run -d -p 80:80 --name <container_name> <image_name>
```
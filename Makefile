
docker_tag=konfu
container=konfu
PORT=3000
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

build: Dockerfile
	docker build -t $(docker_tag) .

run: stop build
	docker run -d --rm  --name $(container) -v $(ROOT_DIR)/app/src/data:/app/src/data -p $(PORT):3000 -p 8080:8080 $(docker_tag)

make exec:
	docker exec -it $(container) bash

stop:
	-docker stop $(container)
	-docker rm $(container)

health:
	curl -k http://localhost:$(PORT)/health && echo

version:
	curl -k http://localhost:$(PORT)/version && echo

json:
	python -m json.tool app/src/*/*.json

push:
	git push -u origin $(shell git symbolic-ref --short HEAD)


SHELL = /bin/bash

.PHONY: build clean install build-linux

install:
	poetry install

clean:
	rm -rf dist build

build:
	poetry run build

build-linux:
	docker build -t zodbox_linux -f ./infra/docker/Dockerfile.Linux .
	docker create --name zodbox_linux zodbox_linux
	docker cp zodbox_linux:/app/dist/zodbot ./dist/zodbox_linux
	docker rm -f zodbox_linux

test:
	poetry run python -m unittest discover --verbose
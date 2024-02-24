# ZoD Bot

This is a discord bot for my personal use. I run the bot on a VPS, so some of the infra
configuration is around getting it running as a service on a linux machine.

## Requirements
- Python 3.12
- Poetry
- Docker

## Getting started

Run `make install`

## Build

To build for your local machine, run `make build`

To build for a linux (amd 64) machine, run `make build-linux` (uses docker)
# Makefile for discount-alert-bot project

# Variables
PROJECT_NAME := discount-alert-bot
COMPOSE_FILE := docker-compose.yml
DOCKER_COMPOSE := docker compose -f $(COMPOSE_FILE)

.PHONY: help build up down restart logs ps clean shell test lint format

help:
	@echo "Makefile for $(PROJECT_NAME) project"
	@echo ""
	@echo "Usage:"
	@echo "  make build       Build all Docker images"
	@echo "  make up          Start all services in the background"
	@echo "  make down        Stop and remove containers, networks, volumes, and images"
	@echo "  make restart     Restart all services"
	@echo "  make shell       Open a shell in the bot_interface container"
	@echo "  make migrate     Apply latest db migrations"
	@echo ""

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up --build -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

shell:
	$(DOCKER_COMPOSE) exec interface /bin/bash

migrate:
	$(DOCKER_COMPOSE) run --build --rm migrator

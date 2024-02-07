.DEFAULT: help

.PHONY: help
help:
	@echo 'help          - show help information'
	@echo 'prepare_docker -  pull docker network and create a network'
	@echo 'run_hazelcast_cluster - generate a lock file or update it'

prepare_docker:
	@docker pull hazelcast/hazelcast:5.1.7
	@docker network create hazelcast-network

run_hazelcast_cluster:
	docker compose -f docker/docker-compose.yaml up --remove-orphans > logs/claster.logs
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1


all: down build up test 


build: 
	docker-compose build 


down: 
	docker-compose down 


up: 
	docker-compose up -d app

logs:
	docker-compose logs app | tail -100 

black:
	black -l 86 $$(find * -name "*.py")


test:
	pytest --tb=short
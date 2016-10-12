requirements := requirements.txt
dev-requires := requirements-dev.txt

all: dev logs

deps:
	@pip install -r ${requirements}

deps-dev:
	@pip install -r ${dev-requires}

dev:
	@docker-compose up -d

nodev:
	@docker-compose kill
	@docker-compose rm -f

log: logs
logs:
	@docker-compose logs -f

bot:
	@python run.py

ps: status

status:
	@docker-compose ps

dist: package

package:
	@rm -rf dist build
	@python setup.py egg_info
	@python setup.py sdist bdist_wheel
	@twine upload dist/*

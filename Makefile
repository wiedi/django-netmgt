build:
	docker compose build
up:
	docker compose up
reset-volumes:
	docker compose down --volumes
run: build up
reset: reset-volumes run

app-shell:
	docker exec -it netmgt-app-1 bash
django-shell:
	docker exec -it netmgt-app-1 ./manage.py shell

schema:
	docker exec -it netmgt-app-1 bash -c './manage.py spectacular --file docs/openapi-schema.yml --validate'

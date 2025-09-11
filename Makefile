container_name = netmgt-app-1
build:
	docker compose build
up:
	docker compose up
reset-volumes:
	docker compose down --volumes
run: build up
reset: reset-volumes run

app-shell:
	docker exec -it $(container_name) bash
django-shell:
	docker exec -it $(container_name) ./manage.py shell

schema:
	docker exec -it $(container_name) bash -c './manage.py spectacular --file docs/openapi-schema.yml --validate'
test:
	docker exec -it $(container_name) bash -c "pytest"
format:
	docker exec -it $(container_name) sh -c "isort . && ruff format"
publish-plugin:
	( \
		cd certbot_plugin; \
		rm -f dist/*; \
		python3 -m build --sdist; \
		python3 -m twine upload --verbose dist/*; \
	)
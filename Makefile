USER_SERVICE_NAME=user_srv

PLAYWRIGHT_NAME=lem_playwright

migration_dir = migrate/migrations/

playwright-test:
	docker compose run --rm ${PLAYWRIGHT_NAME}

# USER SERVICE
user-build-api:
	docker compose exec ${USER_SERVICE_NAME} env GOOS=linux CGO_ENABLED=0 go build -o api cmd/api/main.go 

user-build-scripts:
	docker compose exec ${USER_SERVICE_NAME} env GOOS=linux CGO_ENABLED=0 go build -o scripts cmd/scripts/main.go 

user-build: user-build-api user-build-scripts
	@echo "build all user services"

user-scripts-migrate-dev-data:
	docker compose exec ${USER_SERVICE_NAME} env GOOS=linux CGO_ENABLED=0 go run cmd/scripts/main.go migrate-dev-data

# ALL
build-api: user-build-api
	@echo "build all services api"

# ALL
build-script: user-build-scripts
	@echo "build all services scripts"

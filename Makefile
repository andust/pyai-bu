USER_SERVICE_NAME=user_srv

# PLAYWRIGHT_NAME=lem_playwright

GENAI_SRV_NAME=genai_srv

migration_dir = migrate/migrations/

genai_srv-test:
	docker exec genai_srv pytest -v

# playwright-test:
# 	docker compose run --rm ${PLAYWRIGHT_NAME}

# USER SERVICE
user-build-api:
	docker exec ${USER_SERVICE_NAME} env GOOS=linux CGO_ENABLED=0 go build -o api cmd/api/main.go 

user-build-scripts:
	docker exec ${USER_SERVICE_NAME} env GOOS=linux CGO_ENABLED=0 go build -o scripts cmd/scripts/main.go 

user-build: user-build-api user-build-scripts
	@echo "build all user services"

user-scripts-migrate-dev-data:
	docker exec ${USER_SERVICE_NAME} env GOOS=linux CGO_ENABLED=0 go run cmd/scripts/main.go migrate-dev-data

# ALL
build-api: user-build-api
	@echo "build all services api"

# ALL
build-script: user-build-scripts
	@echo "build all services scripts"

.DEFAULT_GOAL := help

APP_NAME := api
SHELL = /bin/bash -o pipefail

# Generate an informational tag so we can see where every image comes from.
DATE := $(shell date -u '+%Y%m%d.%H%M%S')
INFO_TAG := $(DATE).$(USER)

GIT_REPO_AVAILABLE := $(shell git rev-parse --is-inside-work-tree 2>/dev/null)

# Generate a unique tag based solely on the git hash.
# This will be the identifier used for deployment via terraform.
ifdef GIT_REPO_AVAILABLE
IMAGE_TAG := $(shell git rev-parse HEAD)
else
IMAGE_TAG := "uknown-dev.$(DATE)"
endif

# Path to Open API file for spectral linting
OPEN_API_PATH := openapi.yaml

# Get open command for Linux/Mac
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	OPEN_CMD := xdg-open
endif
ifeq ($(UNAME_S),Darwin)
	OPEN_CMD := open
endif

PY_RUN_CMD := $(RUN_CMD) poetry run

POETRY_CMD := $(RUN_CMD) poetry

define run_tests
	$(PY_RUN_CMD) pytest $(1)
endef

start-api-dev: ## Run the OPR API with reloading enabled
	$(PY_RUN_CMD) uvicorn opr_api.__main__:app --reload

test: ## Run tests, set $args to pass flags to `pytest`
	$(call run_tests, $(args))

test-coverage: ## Run tests run
	$(PY_RUN_CMD) coverage run --branch --source=opr_api -m pytest $(XDIST) $(args)
	$(PY_RUN_CMD) coverage report

test-coverage-report: ## Open HTML test coverage report
	$(PY_RUN_CMD) coverage html --directory .coverage_report
	$(OPEN_CMD) .coverage_report/index.html

lint-changed: max := 0
lint-changed: FILES := $(shell [ "$(GIT_REPO_AVAILABLE)" = "true" ] && { \
	git diff --diff-filter=d --name-only --relative HEAD~$(max); \
	git diff --diff-filter=d --name-only --staged --relative HEAD~$(max); \
	git ls-files --other --exclude-standard HEAD~$(max);} | \
	grep -E '^(opr_api|tests|bin)/.*\.py' | sort -u)
lint-changed: FILES_MYPY := $(shell echo $(FILES) | tr " " "\n" | grep -E '^(opr_api|bin)/')
lint-changed: ## Lint changed files, $max var determines number of commits to compare
	$(PY_RUN_CMD) flake8 --format=$(FLAKE8_FORMAT) $(FILES)
	$(PY_RUN_CMD) mypy $(MYPY_FLAGS) $(FILES_MYPY) $(MYPY_POSTPROC)

lint-py: ## Run python linting
lint-py: lint-flake lint-mypy

lint-flake: ## Run flake8
	$(PY_RUN_CMD) flake8 --format=$(FLAKE8_FORMAT) opr_api

lint-mypy: ## Run mypy
	$(PY_RUN_CMD) mypy --show-error-codes $(MYPY_FLAGS) opr_api $(MYPY_POSTPROC)

lint-spectral: ## Run OpenAPI Spec linting
	docker run --rm --tty --cap-drop=ALL --network=none --read-only --volume=$(PWD):/tmp:ro \
           stoplight/spectral:6 lint /tmp/$(OPEN_API_PATH) --ruleset /tmp/.spectral.yaml $(SPECTRAL_POSTPROC)

lint: ## Run linting
lint: lint-spectral lint-py

format: ## Format code
	$(PY_RUN_CMD) isort --atomic --gitignore --profile black .
	$(PY_RUN_CMD) black .
	npx prettier --write openapi.yaml

format-check: ## Check format of code
	$(PY_RUN_CMD) isort --atomic --check-only --profile black --gitignore .
	$(PY_RUN_CMD) black . --check
	npx prettier --check openapi.yaml

pre-commit:
	$(PY_RUN_CMD) isort --atomic --apply --profile black $(args)
	$(PY_RUN_CMD) black $(args)
ifdef flake_args
	$(PY_RUN_CMD) flake8 $(flake_args)
endif
ifdef mypy_args
	$(PY_RUN_CMD) mypy $(mypy_args)
endif

start: ## Start all containers
start:
	docker-compose up --detach

start-db: ## Start DB container
	docker-compose up --detach db

start-external-apis: ## Start External APIs container
	docker-compose up --detach mock-external-apis

stop: ## Stop all running containers
	docker-compose down

api-image-build: ## Build release image
	docker build \
		--tag $(APP_NAME):latest \
		--tag $(APP_NAME):$(IMAGE_TAG) \
		--target app

dev-build: ## Build development container
	docker-compose build
.PHONY: help install setup run test migrate clean docker-start docker-stop

help: ## Show this help message
	@echo "Stunting Checking App - Development Commands"
	@echo "============================================="
	@echo ""
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

setup: ## Setup database and run initial migration
	@echo "Setting up database..."
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "⚠️  Please edit .env file with your database configuration!"; \
		echo "   Then run 'make setup' again."; \
		exit 1; \
	fi
	@. venv/bin/activate && alembic upgrade head

run: ## Run the application
	@. venv/bin/activate && python run.py

test: ## Run tests
	@. venv/bin/activate && python test_api.py

migrate: ## Create and apply database migrations
	@. venv/bin/activate && alembic revision --autogenerate -m "Auto migration"
	@. venv/bin/activate && alembic upgrade head

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage

docker-start: ## Start application with Docker
	docker-compose up --build -d

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

dev: ## Start development environment
	@echo "Starting development environment..."
	@make install
	@make setup
	@make run

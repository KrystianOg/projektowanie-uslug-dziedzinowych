.PHONY: setup up down dev logs build clean restart ps health

# Initial setup
setup:
	@echo "Setting up project..."
	@test -f .env || (cp .env.example .env && echo "✓ Created .env file - PLEASE UPDATE WITH YOUR SECRETS!")
# 	@mkdir -p init-scripts/postgres models logs
# 	@echo "✓ Created directories"
	@echo ""
	@echo "⚠️  IMPORTANT: Edit .env file with your actual secrets before running 'make up'"

# Build all containers
build:
	docker compose build

# Start all services
up:
	@test -f .env || (echo "❌ .env file not found! Run 'make setup' first" && exit 1)
	docker compose up -d
	@echo ""
	@echo "✓ Services started!"
	@echo ""
	@echo "Access points:"
	@echo "  - Infisical UI:  http://localhost:8080"
	@echo "  - RabbitMQ UI:   http://localhost:15672"
	@echo "  - API Gateway:   http://localhost:8000"
	@echo ""
	@echo "Run 'make logs' to see logs"
	@echo "Run 'make health' to check service health"

# Start in development mode (with logs)
dev:
	docker compose up

# Stop all services
down:
	docker compose down

# Restart all services
restart:
	docker compose restart

# View logs
logs:
	docker compose logs -f

# Health check
health:
	@echo "Checking service health..."
	@echo ""
	@docker compose ps --format json | jq -r '.[] | "\(.Service): \(.State) - \(.Status)"' || docker compose ps
	@echo ""
	@echo "Detailed health:"
	@docker inspect --format='{{.Name}}: {{.State.Health.Status}}' $$(docker compose ps -q) 2>/dev/null || echo "Run 'docker compose ps' for status"

# Testing
test:
	@echo "Running tests..."
	docker compose exec api_gateway pytest tests/
	docker compose exec ml_processor pytest tests/
	docker compose exec trade_executor pytest tests/

# Clean up everything
clean:
	@echo "⚠️  This will remove all containers and volumes!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose down -v; \
		echo "✓ Cleaned up all containers and volumes"; \
	else \
		echo "Cancelled"; \
	fi

# Backup database
backup:
	@echo "Creating database backup..."
	@mkdir -p backups
	docker-compose exec -T postgres pg_dump -U trading_user trading > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✓ Backup created in backups/"

# Restore database
restore:
	@echo "Available backups:"
	@ls -1 backups/*.sql 2>/dev/null || echo "No backups found"
	@read -p "Enter backup filename: " backup; \
	if [ -f "backups/$$backup" ]; then \
		docker-compose exec -T postgres psql -U trading_user trading < backups/$$backup; \
		echo "✓ Database restored"; \
	else \
		echo "❌ Backup file not found"; \
	fi

# Scale workers
scale-ml:
	@read -p "Number of ML processor instances: " num; \
	docker-compose up -d --scale ml_processor=$$num

scale-finance:
	@read -p "Number of finance worker instances: " num; \
	docker-compose up -d --scale finance_worker=$$num

scale-social:
	@read -p "Number of social worker instances: " num; \
	docker-compose up -d --scale social_worker=$$num
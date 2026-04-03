.PHONY: up down build logs migrate shell-backend shell-db mobile-android mobile-ios test lint reset

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build --no-cache

logs:
	docker compose logs -f

migrate:
	docker compose exec backend alembic upgrade head

shell-backend:
	docker compose exec backend bash

shell-db:
	docker compose exec postgres psql -U postgres -d qard

mobile-android:
	cd mobile && npm install && npx react-native run-android

mobile-ios:
	cd mobile && npm install && npx react-native run-ios

test:
	docker compose exec backend pytest tests/ -v

lint:
	docker compose exec backend ruff check app/ tests/

reset:
	docker compose down -v --remove-orphans
	docker compose up -d --build

.PHONY: help install run dev test clean docker-build docker-run

help:
	@echo "🍋 LEMONBOT - Makefile Commands"
	@echo ""
	@echo "Commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run the bot"
	@echo "  make dev          - Run in development mode with auto-reload"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Remove cache and temp files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run bot in Docker"

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

run:
	@echo "🚀 Starting LEMONBOT..."
	python main.py

dev:
	@echo "👨‍💻 Starting in development mode..."
	watchmedo auto-restart -d . -p '*.py' -- python main.py

test:
	@echo "🧪 Running tests..."
	python -m pytest

clean:
	@echo "🧹 Cleaning..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	@echo "✅ Clean done!"

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t lemonbot:latest .
	@echo "✅ Docker image built!"

docker-run:
	@echo "🚀 Running bot in Docker..."
	docker-compose up -d
	@echo "✅ Bot is running!"

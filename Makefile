.PHONY: setup test run run-termux docker-build docker-push tree

# Variables
IMAGE_NAME = darnellwashingtonjr94-art/apex
TAG = latest

setup:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pytest pytest-asyncio

test:
	PYTHONPATH=. pytest tests/ -v --disable-warnings

run:
	python -m src.cli.main stream --target workspace

run-termux:
	@echo "Executing in Android Termux context..."
	bash scripts/termux_setup.sh
	python -m src.cli.main stream --target termux_local

docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) -f docker/Dockerfile.apex .

docker-push:
	docker push $(IMAGE_NAME):$(TAG)

tree:
	@python -c 'from src.utils.visualizer import TreeVisualizer; print(TreeVisualizer.generate_ascii_tree("."))'

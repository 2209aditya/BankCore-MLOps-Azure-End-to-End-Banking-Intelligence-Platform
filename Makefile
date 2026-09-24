install:
	pip install -r requirements.txt

dev:
	pip install -r requirements-dev.txt

test:
	pytest -v

coverage:
	pytest --cov=src --cov=api

lint:
	flake8 .

format:
	black .
	isort .

train-fraud:
	python -m src.pipelines.fraud_training_pipeline \
		--input data/fraud.csv \
		--output-dir models/fraud

train-credit:
	python -m src.pipelines.credit_training_pipeline \
		--input data/credit.csv \
		--output-dir models/credit

train-churn:
	python -m src.pipelines.churn_training_pipeline \
		--input data/churn.csv \
		--output-dir models/churn

docker-build:
	docker build \
		-f api/Dockerfile \
		-t bankcore-api:latest .

infra-validate:
	az bicep build \
		--file infra/main.bicep
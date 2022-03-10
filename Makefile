format:
	poetry run black .
	poetry run isort .

quicktest:
	poetry run black --check .
	poetry run isort --check .
	poetry run flake8 .
	poetry run mypy --strict .

pytest:
	poetry run pytest --cov=art_conf --cov-fail-under=70 --cache-clear tests --cov-report term-missing

test: quicktest pytest

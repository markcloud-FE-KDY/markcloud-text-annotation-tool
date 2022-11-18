install:
	pip install -e .
	pip install -r requirements.txt
	pip list

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	find . -name '__pycache__' -exec rm -rf  {} +

test:
	find . -name '*.pyc'

formatter:
	black --line-length 119 app text-review
	
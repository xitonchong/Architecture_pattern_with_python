test:
	pytest --tb=short 

watch-tests:
	ls *.py | entr pytest --tb=short 

black:
	black -l 86 $$(find* -name '*.py')

setup: requirements.txt 
	pip install -r requirements.txt

clean:
	rm -rf __pycache__
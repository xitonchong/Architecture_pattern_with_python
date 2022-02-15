# Example application code for the python architecture book 


# SETUP
sudo apt-get install python3.8-venv

python3.8 -m venv .venv && source .venv/bin/activate 



https://github.com/python-leap/code/branches/all


---
## How to test if a link is up?
try: 
    request.get(config.get_api_url)
except ConnectionError:
    time.sleep(0.5)
pytest.fail('API never came up')


## postgre
is a object-relational database 


## pytest 
- Makefile 


## pypi black 
`black` is able to read project-specific default values for its command line options from a `pyproject.toml` file. 


## Multiple exceptions
From Python Documentation:

An except clause may name multiple exceptions as a parenthesized tuple, for example

except (IDontLikeYouException, YouAreBeingMeanException) as e:
    pass
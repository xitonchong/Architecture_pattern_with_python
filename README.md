# Example application code for the python architecture book 


# SETUP
sudo apt-get install python3.8-venv

python3.8 -m venv .venv && source .venv/bin/activate 



https://github.com/python-leap/code/branches/all


---

## pytest 
- Makefile 


## dataclass
 
### frozen vs unsafe_hash 
- frozen:  by passing frozen=True, you can emulate immutability.
- unsafe_hash: if `False` (default), a __hash__()  method is generated according to how `eq` and `frozen` are set.  if unsafe_hash=True, this would means that your class is immutable but can nontheless be mutated. 
Setting this is required to work with sqlalchemy ORM.  

---

## sqlalchemy

- Metadata is a container object that keeps together many different features of a database (or multiple databases) being described. 

- Foregin key:
    this construct defines a reference to a remote table, and is fully described in defining foreign keys.   https://docs.sqlalchemy.org/en/14/core/metadata.html



## mypy configuration file
Mypy supprots reading configuration settings from a file. by default it uses the file `mypy.ini` with a fallback
to `.mypy.ini`. in the current dir. 


## git command
change a branch name
    git checkout <old_name>
    git branch -m <new_name>
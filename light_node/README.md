# Light Node

## Requirement
- python3

## Installation
Steps to install python and its relevant packages
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```
cd src
uvicorn main:app --port 8080 --workers 1 --reload
```

## Compile a distributed task for python
generate a python pickled function to be sent over for computation
```
cd tools
python task_generator.py <path to file>
```

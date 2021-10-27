setup

1. mv env.example env
2. generate secret key 
- import os
- os.random(16).hex()
3. create database and user ad to .env
4. create virtual env: 
- python -m venv venv
5. install package: 
- pip install -r requirements.txt
6. flask db upgrade
7. flask run
8. tests:
- python -m pytest
- python -m pytest tests\test_authors.py
- python -m pytest -k "test_create_author"


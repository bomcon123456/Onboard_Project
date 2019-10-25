# Onboard Project Server side
## Description:
This is a Python Flask Application. It serves multiple endpoints allowing user to manipulate categorized items.

## Prerequisites:
- Python 3.7
- MySQL 5.7

## How to install:
You should create a virtual environment so that it will not affect other projects.
``` 
1. Create virtual env: 
virtualenv venv --python=python3
2. Install pip modules:
pip install -r requirements.txt
3. Fulfill ENVIRONMENT variables, we support loading from .env file placed in the server/ folder:
DATABASE_URL='SOME_URL'
TESTING_DATABASE_URL='SOME_URL'
APP_SECRET_KEY='SOME_KEY'
4. Install any MySQL connector like:
- PyMySQL
- MySQLdb
- mysql-connector-python
Don't know what to choose? Read this awesome answer from Collin: https://stackoverflow.com/a/25724855
- Then remember to update the DATABASE_URL to tell which connector you are using:
'mysql+connector://...'
5. Since Flask-SQLAlchemy can't automatically create a new database, you should create it by yourself.
```
## How to run:
``` 
python run.py
```
## How to run test:
```
$ pwd
.../server
$ pytest --cov-report term-missing --cov='./main'
```
## Project Overview:
### Endpoints:
You can see endpoints and its request/response example here:
[API documentation](https://documenter.getpostman.com/view/6660523/SVtVVoQ3)

### Entity relationship:
![Entity-R](../Markdown/Onboard_EntityRelation.png)

### Project folder structure:
![Folder-Structure](../Markdown/ServerStructure2.png)



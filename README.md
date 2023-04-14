# Test Task

## Implemented
- CRUD operations for three models: Account, Mall, Unit
- Bulk_insert operation for three models
- 97% test coverage is provided

## Setup variants
Choosing any variant, you firstly have to fill .env and .env.docker files according to the templates
### Without docker
1. Run database:
```shell
docker-compose -f docker-compose.database-only.yml up --build
```
2. Run migrations
```shell
flask db upgrade
```
3. Run application
```
export FLASK_APP=src/main.py
python src/main.py
```
### With docker, everything at once:
```
docker-compose up --build
```

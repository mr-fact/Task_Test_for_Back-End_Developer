# taski
## project setup
0- create docker containers
```
docker run -d \
  --name postgres-taski \
  -p 5432:5432 \
  -e POSTGRES_DB=taski \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  postgres:14.1
```
```
docker run -d \
  --name pgadmin4_taski \
  -p 5050:80 \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=pg_pass \
  dpage/pgadmin4
```
```
docker run -d \
  --name rabbitmq-taski \
  rabbitmq:alpine
```
```
docker build -t django_image -f docker/production.Dockerfile .
```
```
docker run -d \
  --name django \
  --link postgres:db \
  --link rabbitmq:rabbitmq \
  -e DATABASE_URL=psql://root:r1o2o3t4@db:5432/bubook \
  -e CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672// \
  -v $(pwd):/app \
  -p 8000:8000 \
  --restart on-failure \
  django_image ./docker/web_entrypoint.sh
```

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd bubook
```

2- SetUp venv
```
virtualenv -p python3.10 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements_dev.txt
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py migrate
```

6- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

7- run the project
```
python manage.py runserver
```
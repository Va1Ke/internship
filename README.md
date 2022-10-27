# internship
Vladyslav Kachur Internship

to build docker-compose image 'docker-compose build'<br />
to run fastapi, postgres, redis docker containers 'docker-compose up -d'

when try alembic 'alembic revision --autogenerate -m "create User model"' get error (log.txt)<br />
but when I try to do that under container using ' docker exec web alembic revision --autogenerate -m "create User model' all is working fine!<br />
I also printed settings.DATABASE_URL and get 'postgresql://admin:admin@db:5432/postgresdb' as expected...<br />
help me pls

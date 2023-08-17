export DJANGO_ALLOWED_HOSTS=$(grep 'DJANGO_ALLOWED_HOSTS' envs.env | sed 's/^.*=//')
export DJANGO_SU_USERNAME=$(grep 'DJANGO_SU_USERNAME' envs.env | sed 's/^.*=//')
export DJANGO_SU_EMAIL=$(grep 'DJANGO_SU_EMAIL' envs.env | sed 's/^.*=//')
export DJANGO_SU_PASSWORD=$(grep 'DJANGO_SU_PASSWORD' envs.env | sed 's/^.*=//')
export POSTGRES_PASSWORD=$(grep 'POSTGRES_PASSWORD' envs.env | sed 's/^.*=//')
export DATA_DIR=$(grep 'DATA_DIR' envs.env | sed 's/^.*=//')


docker build --build-arg DJANGO_ALLOWED_HOSTS_ARG="$DJANGO_ALLOWED_HOSTS" --tag auction-python-image .

docker compose pull redis postgres

docker compose up -d

sleep 10
docker exec -id auction-postgres psql -U postgres -c "CREATE USER auction_app WITH ENCRYPTED PASSWORD '123qwe';"
sleep 1
docker exec -id auction-postgres psql -U postgres -c "CREATE DATABASE auc;"
sleep 1
docker exec -id auction-postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE auc TO auction_app;"
sleep 1
docker exec -id auction-postgres psql -U postgres -c "\c auc;"
sleep 1
docker exec -id auction-postgres psql -U postgres -c "GRANT ALL ON SCHEMA public TO auction_app;"

sleep 10
docker exec -d auction-django python manage.py migrate

sleep 10
docker exec -d auction-django python manage.py shell -c "from django.contrib.auth.models import User; \
                        User.objects.create_superuser('$DJANGO_SU_USERNAME', '$DJANGO_SU_EMAIL', '$DJANGO_SU_PASSWORD')"

echo "SUCCESS"
export DJANGO_ALLOWED_HOSTS=$(grep 'DJANGO_ALLOWED_HOSTS' envs.env | sed 's/^.*=//')
export DJANGO_SU_USERNAME=$(grep 'DJANGO_SU_USERNAME' envs.env | sed 's/^.*=//')
export DJANGO_SU_EMAIL=$(grep 'DJANGO_SU_EMAIL' envs.env | sed 's/^.*=//')
export DJANGO_SU_PASSWORD=$(grep 'DJANGO_SU_PASSWORD' envs.env | sed 's/^.*=//')
export DJANGO_CONTAINER_PORT=$(grep 'DJANGO_CONTAINER_PORT' envs.env | sed 's/^.*=//')

export AUCTION_MONGODB_VOLUME=$(grep 'AUCTION_MONGODB_VOLUME' envs.env | sed 's/^.*=//')
export AUCTION_REDIS_VOLUME=$(grep 'AUCTION_REDIS_VOLUME' envs.env | sed 's/^.*=//')
export AUCTION_DJANGO_VOLUME=$(grep 'AUCTION_DJANGO_VOLUME' envs.env | sed 's/^.*=//')


docker compose build --build-arg DJANGO_ALLOWED_HOSTS_ARG=$DJANGO_ALLOWED_HOSTS
docker compose pull
docker compose up -d

sleep 60

docker exec -d auction-django python manage.py shell -c "from django.contrib.auth.models import User; \
                        User.objects.create_superuser('$DJANGO_SU_USERNAME', '$DJANGO_SU_EMAIL', '$DJANGO_SU_PASSWORD')"
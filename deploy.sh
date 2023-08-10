export DJANGO_ALLOWED_HOSTS=$(grep 'DJANGO_ALLOWED_HOSTS' envs.env | sed 's/^.*=//')
export DJANGO_SU_USERNAME=$(grep 'DJANGO_SU_USERNAME' envs.env | sed 's/^.*=//')
export DJANGO_SU_EMAIL=$(grep 'DJANGO_SU_EMAIL' envs.env | sed 's/^.*=//')
export DJANGO_SU_PASSWORD=$(grep 'DJANGO_SU_PASSWORD' envs.env | sed 's/^.*=//')

docker compose build --build-arg DJANGO_ALLOWED_HOSTS_ARG=
docker compose up -d

docker exec -d auction-django python manage.py shell -c "from django.contrib.auth.models import User; \
                        User.objects.create_superuser('$DJANGO_SU_USERNAME', '$DJANGO_SU_EMAIL', '$DJANGO_SU_PASSWORD')"
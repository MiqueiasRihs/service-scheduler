#!/bin/sh

attempts=1
max_attempts=10

while [ $attempts -lt $max_attempts ]; do
    if pg_isready -h service_scheduler_postgres -p 5432 -U postgres -d service_scheduler; then
        echo "\n================ Banco de dados está pronto, executando migrações... ================ \n"
        python3 manage.py makemigrations
        python3 manage.py migrate
        python3 manage.py createcachetable

        echo "\n================ Criando superusuário... ================\n"
        python3 manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

        echo "\n================ Iniciando os testes unitários... ================\n"
        python3 manage.py test

        echo "\n================ Iniciando o servidor Django... ================\n"
        python3 manage.py runserver 0.0.0.0:8000
        break
    else
        echo "\nTentativa $attempts: Banco de dados não está pronto. Aguarde um momento, reconectando...\n"
        attempts=$((attempts+1))
        sleep 5
    fi
done

if [ $attempts -eq $max_attempts ]; then
    echo "O banco de dados não subiu após $max_attempts tentativas."
fi
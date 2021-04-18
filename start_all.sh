#!/bin/bash

WINDOWS=false
PYTHON=python
ACTIVATE=.venv/bin/activate

if hash wmic 2>/dev/null; then
  if [[ ! $(wmic os get caption) = "Microsoft Windows"* ]];then
    echo "On windows"
    WINDOWS=true
    PYTHON='winpty python'
    ACTIVATE=.venv/Scripts/activate
  fi
fi

NAME=djangodbX
DB_PORT=5439
DB_PASSWORD=mysecretpassword
WAIT=5

SUPERUSER=admin

FROM_SCRATCH=false

function startEmptyContainer {
  local name=$1
  docker stop $name
  docker rm $name
  
  docker run \
    --name $name \
    -d \
    -p$DB_PORT:5432 \
    -e POSTGRES_PASSWORD=$DB_PASSWORD \
    postgres
 
  # TODO: create volume and DB script so that db container gets updated with appropriate logging configuration

  echo "wait $WAIT seconds for db container..."
  sleep $WAIT

  docker cp postgresql.conf $name:/var/lib/postgresql/data/
}

function restartContainer {
  local name=$1
  docker stop $name
  docker start $name
}

function prepareDjango {
  $PYTHON manage.py migrate
  
  echo "create superuser $username; choose password when asked"
  $PYTHON manage.py createsuperuser --email admin@example.com --username $SUPERUSER
  
  # cf https://pythonin1minute.com/where-to-put-django-startup-code/
  $PYTHON manage.py my_custom_startup_command

  echo "prepareDjango finished"
}


while getopts 'a' OPTION; do
    case "$OPTION" in
        a)
            echo "Option a set - start from scratch"
            FROM_SCRATCH=true
            ;;
        *)
            echo "Usage: $0 [-a] [-w]" >&2
            exit 1
        ;;
    esac
done

shift "$(($OPTIND -1))"

source $ACTIVATE

if [ "$FROM_SCRATCH" = true ] ; then
  echo "Initialize container from scratch"
  startEmptyContainer $NAME
  prepareDjango
else
  echo "stop and start existing container"
  restartContainer $NAME
fi

echo "now start Django"
$PYTHON manage.py runserver

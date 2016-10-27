#!/bin/bash

NAME="jamie_app"                                  # Name of the application
PROJDIR=/var/www/jamiefraser.me             # Django project directory
SOCKFILE=/var/www/jamiefraser.me/jamie.sock  # we will communicte using this unix socket
USER=govhack                                        # the user to run as
GROUP=www-data                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $PROJDIR
source /var/venvs/jamiefraser.me/bin/activate

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn app:app \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \

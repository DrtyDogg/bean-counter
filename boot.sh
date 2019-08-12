#!/bin/sh

#set the pythone envirounment
echo entering the venv
source venv/bin/activate

#update the DB
echo Upgrading the database
flask db upgrade

# Run the app
echo running the application
exec gunicorn -e SCRIPT_NAME=$CONTEXT_ROUTE -b :5000 --access-logfile - --error-logfile - budget:app

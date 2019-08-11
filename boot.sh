#!/bin/sh

#set the pythone envirounment
source venv/bin/activate

#update the DB and compile the application
flask db upgrade
if [[ "$?" != 0]]; then
    echo Upgrade command failed
fi

# Run the app without a context route

exec gunicorn -e SCRIPT_NAME=$CONTEXT_ROUTE -b :5000 --access-logfile - --error-logfile - budget:app

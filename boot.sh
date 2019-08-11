#!/bin/sh

#set the pythone envirounment
source venv/bin/activate

#update the DB and compile the application
while true; do
    flask db upgrade
    if [[ "$?" == 0]]; then
       break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done

# Run the app without a context route

exec gunicorn -e SCRIPT_NAME=$CONTEXT_ROUTE -b :5000 --access-logfile - --error-logfile - budget:app

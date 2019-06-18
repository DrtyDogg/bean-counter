#!/bin/sh

#set the pythone envirounment
source venv/bin/activate

#update the DB and compile the application
flask db upgrade
flask translate compile

#Run the app
exec gunicorn -b :5000 --access-logfile - --error-logfile - budget:app
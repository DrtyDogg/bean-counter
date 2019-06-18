FROM python:3.7.3-alpine

RUN adduser -D budget

WORKDIR /home/budget

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN mkdir db

COPY app app
COPY migrations migrations
COPY budget.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP budget.py

RUN chown -R budget:budget ./
USER budget

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
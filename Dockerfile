FROM python:3.12-slim-bullseye
 RUN apt-get update && apt install -y git

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY requirements.txt ./

# export GITHUB_TOKEN=${GITHUB_TOKEN}
RUN pip install -r requirements.txt
#RUN pip install 
# git+https://github.com/benoitc/gunicorn.git@fix-gthread

EXPOSE $PORT
COPY app ./app

# We are expecting run this on a single CPU cloud run instance
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 "app:create_app()"

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--worker-class", "eventlet", "app:create_app"]

#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 "app:create_app()"

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 "app:create_app()"
#!/bin/bash

echo "Building backend image ..."

docker build -t backend .

echo "Deleting former backend-dev ..."

docker rm -f $(docker ps -a | grep backend-dev | awk '{print $1}')

echo "Starting backend-dev ..."

echo "Running on http://127.0.0.1:5000/"

docker run -it --name backend-dev -p 5000:80 -v $(pwd)/app:/app \
    -e FLASK_APP=app.app.py -e FLASK_DEBUG=1 backend bash -c "flask run --host=0.0.0.0 --port=80"
# set base image (host OS)
FROM python:3.9.2-slim-buster
EXPOSE 8000
EXPOSE 9000

# set the working directory in the container
WORKDIR /code

# copy the content of the local src directory to the working directory
COPY src/ .

ENV PYTHONUNBUFFERED=1
# command to run on container start
CMD [ "python", "ServerMonopolio.py" ]

FROM python:3.10
#FROM python:3.10-slim
#install nano text editor in docker container
RUN apt-get update -y && apt-get install nano -y && apt-get install nginx -y &&  apt-get install -y gunicorn systemd && apt-get install net-tools

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Create directory and sub-directory for project

RUN mkdir -p /app/project-video/ 

# set work directory
WORKDIR /app/project-video/


# install dependencies
RUN pip install --upgrade pip && pip install virtualenv
# Create a virtual environment
RUN virtualenv /app/project-video/venv

# Set the Python interpreter to the venv's interpreter
ENV PATH="/app/project-video/venv/bin:$PATH"


ADD . /app/project-video/

# set work directory
WORKDIR /app/project-video/



RUN pip install -r requirements.txt 



RUN chmod +x /app/project-video/docker/backend/entry-point/server-entrypoint.sh


EXPOSE 8000

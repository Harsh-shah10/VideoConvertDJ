FROM python:3.10

#install nano text editor in docker container
RUN apt-get update -y && apt-get install nano -y && apt-get install nginx -y &&  apt-get install -y gunicorn systemd && apt-get install net-tools

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Create directory and sub-directory for project

RUN mkdir -p /app/project-bicycle/ 

# set work directory
WORKDIR /app/project-bicycle/


# install dependencies
RUN pip install --upgrade pip && pip install virtualenv
# Create a virtual environment
RUN virtualenv /app/project-bicycle/venv

# Set the Python interpreter to the venv's interpreter
ENV PATH="/app/project-bicycle/venv/bin:$PATH"

# Add bicyle-project to container.

#ADD ../../ /app/project-bicycle/
ADD . /app/project-bicycle/
#ADD /home/krishna/Development/Django-project/project-bicycle/  /app/project-bicycle/

# set work directory
WORKDIR /app/project-bicycle/bicycle/



RUN pip install -r requirements.txt 


# Create service for gunicorn server. it is possible to start server without create service but we will start, restart and stop gunicorn server using system service. 
RUN cp /app/project-bicycle/bicycle/docker/gunicorn/gunicorn.service /etc/systemd/ && cp /app/project-bicycle/bicycle/docker/gunicorn/gunicorn.socket /etc/systemd/   
#ADD /app/blog-project/blog/docker/gunicorn/gunicorn.socket /etc/systemd/system/
#RUN systemctl start gunicorn.socket && systemctl enable gunicorn.socket

RUN chmod +x /app/project-bicycle/bicycle/docker/backend/entry-point/server-entrypoint.sh
#RUN chmod +x /app/blog-project/blog/docker/backend/entry-point/worker-entrypoint.sh


EXPOSE 8000

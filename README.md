Follow these steps to set up and run the project on your local machine.

1. Clone the Repository
First, clone the repository to your local machine using Git.

git clone https://github.com/Harsh-shah10/VideoConvertDJ.git

2. Build and Run the Docker Containers
Next, use Docker Compose to build and run the Docker containers.

docker-compose up -d
This command builds the Docker images and starts the containers in detached mode.

3. Check Running Containers
Verify that the containers are running using the docker ps command.

docker ps
You should see output similar to this:


CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                    NAMES

123456789abc   my_django_app  "docker-entrypoint.s…"   10 minutes ago   Up 10 minutes   0.0.0.0:8000->8000/tcp   my_django_app_container

4. Run APIs using Postman
Use Postman to run all the APIs.

Import the Postman collection provided in the repository.
Replace the URL in the Postman requests with 0.0.0.0 and the appropriate port (e.g., 8000).
For example, if the original URL in the Postman collection is http://localhost:8000/api/endpoint, change it to http://0.0.0.0:8000/api/endpoint.


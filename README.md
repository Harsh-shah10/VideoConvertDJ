# VideoConvertDJ Project Setup Guide

- **Clone the Repository:**
  - First, clone the repository to your local machine using Git:
    ```bash
    git clone https://github.com/Harsh-shah10/VideoConvertDJ.git
    ```

- **Build and Run the Docker Containers:**
  - Next, use Docker Compose to build and run the Docker containers:
    ```bash
    docker-compose up -d
    ```
  - This command builds the Docker images and starts the containers in detached mode (`-d`).

- **Verify Running Containers:**
  - To verify that the containers are running, use the following command:
    ```bash
    docker ps
    ```
  - You should see output similar to this:
    ```
    CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                    NAMES
    123456789abc   my_django_app  "docker-entrypoint.s…"   10 minutes ago   Up 10 minutes   0.0.0.0:8000->8000/tcp   my_django_app_container
    ```

- **Run APIs using Postman:**
  - To interact with the APIs, follow these steps:
    - Import the provided Postman collection from the repository.
    - Open Postman and update the request URLs in the collection:
      - Replace `localhost` with `0.0.0.0` and ensure the correct port is used (e.g., `8000`).
      - Example: Change `http://localhost:8000/api/endpoint` to `http://0.0.0.0:8000/api/endpoint`.

- **Additional Notes:**
  - Ensure Docker and Docker Compose are installed on your machine before proceeding.
  - Modify any configuration files (`docker-compose.yml`, etc.) according to your environment if needed.

That's it! You should now have the VideoConvertDJ project up and running locally.

Demo Video : 
  - (https://drive.google.com/file/d/1DAqYAOkoUejI_oxDAI03klMJONUFRB5D/view?usp=sharing)

# Devops Home Assignment

## Project Structure

```text
Devops-Home-Assignment/
│
├── nginx/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── html/
│       └── index.html
│
└── README.md
```

The nginx directory contains all files required to build the custom Nginx Docker image, including configuration and static HTML content.

### Custom HTML Response

The first Nginx server block returns a custom static HTML page 
to fulfill the requirement of serving a custom HTML response.

### Nginx Configuration

Two server blocks are defined inside nginx.conf:

- Server 1 (port 8080): serves a custom static HTML page to fulfill the requirement of returning a custom HTML response.
- Server 2 (port 8081): always returns HTTP 404 error to fulfill the requirement of returning an HTTP error response.

Ports 8080 and 8081 were chosen to avoid requiring root privileges (as ports below 1024 require elevated permissions) and to clearly differentiate between the two server behaviors.

HTTP 404 was selected as the error response because it is simple, widely recognized, and clearly indicates a non-successful request.

### Dockerfile (Nginx Image)

- Base image is Ubuntu 22.04 as required.
- Nginx is installed via apt using `--no-install-recommends`.
- apt cache is removed to reduce image size.
- Nginx runs in the foreground using `daemon off;` to keep the container running.

## Local Run (Nginx Image)

### Build the Image

```bash
docker build -t devops-nginx:1 -f nginx/Dockerfile nginx
```

This command builds the custom Nginx Docker image based on Ubuntu 22.04.

### Run the Container
```bash
docker run --name devops-nginx -d -p 8080:8080 -p 8081:8081 devops-nginx:1
```
The container is started in detached mode (-d).
Ports 8080 and 8081 are mapped from the container to the host machine.

### Verify Functionality
```bash
curl http://localhost:8080
curl -i http://localhost:8081
```
Expected behavior:
- `http://localhost:8080` returns the custom HTML page.
- `http://localhost:8081` returns HTTP 404 error.



### Cleanup
```bash
docker stop devops-nginx
docker rm devops-nginx
```
This step stops and removes the container after verification.


## Updated Project Structure
```text
Devops-Home-Assignment/
│
├── nginx/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── html/
│       └── index.html
│
├── test/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── test.py
│
└── README.md
```
The test directory contains a separate Docker image used to validate
the Nginx server behavior.

### Test Script Validation Logic

The test script validates:

- Port 8080 returns HTTP 200 and contains the expected HTML content.
- Port 8081 returns HTTP 404 error.

If any validation fails, the script exits with a non-zero exit code.

## Test Image

A separate Docker image is used to run an automated Python test script.
The script sends HTTP requests to both Nginx ports and validates status codes and response content.
If any validation fails, it exits with a non-zero exit code.

## Docker Compose

A single `docker-compose.yml` file is used to orchestrate both services:

- **nginx**: builds the Ubuntu-based Nginx image and exposes ports `8080` and `8081`.
- **test**: builds a separate Python test image that sends HTTP requests to the nginx service.

The test container connects to the nginx container using the service hostname `nginx` on the internal Docker Compose network.

## Docker Compose Test Run

The `test` service runs an automated Python script that validates the Nginx service behavior:

- Port 8080 returns HTTP 200 and contains the expected HTML content.
- Port 8081 returns HTTP 404 error.

Run:
```bash
docker compose up --build --abort-on-container-exit
```
- build ensures both images are built.
- abort-on-container-exit stops the stack when the test container finishes.

## Cleanup
```bash
docker compose down
```

## GitHub repository that includes all required files and configuration.

GitHub Repository

A GitHub repository was created that includes all required files and configuration for this project.

The repository contains:

nginx/ – Nginx Docker image (Ubuntu-based)

test/ – Test Docker image (Python-based)

docker-compose.yml

.github/workflows/ci-workflow.yml

README.md

## CI (GitHub Actions)

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request.

It performs:
- Builds and runs the project using Docker Compose.
- If tests pass, it uploads an artifact containing a file named `succeeded`.
- If tests fail, it uploads an artifact containing a file named `fail`.

## Committing and Pushing the Workflow
The workflow file was committed and pushed using:
```bash
git add .github/workflows/ci-workflow.yml
git commit -m "Add GitHub Actions CI workflow"
git push
```

## CI Execution Result
After pushing the workflow file, GitHub Actions automatically triggered a CI run.

Because all tests passed:

The test container exited with code 0.

The workflow detected success.

An artifact named test-result was uploaded.

The artifact contains a file named succeeded.

This satisfies the requirement:

If tests pass, publish an artifact containing a file named succeeded.
If tests fail, publish an artifact containing a file named fail.
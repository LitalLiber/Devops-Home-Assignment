# Devops Home Assignment

## Overview

This project implements a Docker-based Nginx service with automated testing and CI integration.

It includes:
- A custom Ubuntu-based Nginx image
- A separate Python test image
- Docker Compose orchestration
- GitHub Actions CI pipeline
- Image size optimizations

## Table of Contents
- Overview
- Nginx Image
- Test Image
- Docker Compose
- CI
- Image Optimization


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
![Project Structure](<images/first steps/Project Structure.png>)

The nginx directory contains all files required to build the custom Nginx Docker image, including configuration and static HTML content.

![Create github ripo](<images/first steps/create github ripo.png>)

### Custom HTML Response

The first Nginx server block returns a custom static HTML page 
to fulfill the requirement of serving a custom HTML response.

![Custom HTML Response](<images/1. Docker Images/a. Nginx Image/Custom HTML Response.png>)

### Nginx Configuration

Two server blocks are defined inside nginx.conf:

- Server 1 (port 8080): serves a custom static HTML page to fulfill the requirement of returning a custom HTML response.
- Server 2 (port 8081): always returns HTTP 404 error to fulfill the requirement of returning an HTTP error response.

Ports 8080 and 8081 were chosen to avoid requiring root privileges (as ports below 1024 require elevated permissions) and to clearly differentiate between the two server behaviors.

HTTP 404 was selected as the error response because it is simple, widely recognized, and clearly indicates a non-successful request.

![Nginx Configuration](<images/1. Docker Images/a. Nginx Image/Nginx Configuration.png>)

### Dockerfile (Nginx Image)

- Base image is Ubuntu 22.04 as required.
- Nginx is installed via apt using `--no-install-recommends`.
- apt cache is removed to reduce image size.
- Nginx runs in the foreground using `daemon off;` to keep the container running.

![Dockerfile (Nginx Image)](<images/1. Docker Images/a. Nginx Image/Dockerfile (Nginx Image).png>)

### Build the Image

```bash
docker build -t devops-nginx:1 -f nginx/Dockerfile nginx
```
![Build the Image](<images/1. Docker Images/a. Nginx Image/Build the Image.png>)

This command builds the custom Nginx Docker image based on Ubuntu 22.04.


### Run the Container
```bash
docker run --name devops-nginx -d -p 8080:8080 -p 8081:8081 devops-nginx:1
```
The container is started in detached mode (-d).
Ports 8080 and 8081 are mapped from the container to the host machine.

![the container is running](<images/1. Docker Images/a. Nginx Image/the container is running.png>)


### Verify Functionality
```bash
curl http://localhost:8080
curl -i http://localhost:8081
```
Expected behavior:
- `http://localhost:8080` returns the custom HTML page.
- `http://localhost:8081` returns HTTP 404 error.

![run the containers with 2 ports](<images/1. Docker Images/a. Nginx Image/run the containers with 2 ports.png>)
![server 1 HTML](<images/1. Docker Images/a. Nginx Image/server 1 HTML.png>)
![server2 HTTP ](<images/1. Docker Images/a. Nginx Image/server2 HTTP .png>)



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

![Updated Project Structure](<images/1. Docker Images/b. Test Image/Updated Project Structure.png>)

### Test Script Validation Logic

The test script validates:

- Port 8080 returns HTTP 200 and contains the expected HTML content.
- Port 8081 returns HTTP 404 error.

If any validation fails, the script exits with a non-zero exit code.

![Test Script Validation Logic](<images/1. Docker Images/b. Test Image/Test Script Validation Logic.png>)

### Design Decisions

- Python was chosen for simplicity and readability.

- python:3.12-slim was selected to keep the image size small.

- The requests library is used for clean and reliable HTTP validation.

- Both status code and content validation are performed to ensure correct behavior, not just connectivity.

## Test Image

A separate Docker image is used to run an automated Python test script.
The script sends HTTP requests to both Nginx ports and validates status codes and response content.
If any validation fails, it exits with a non-zero exit code.

![Test Image](<images/1. Docker Images/b. Test Image/Test Image.png>)

## Docker Compose

A single `docker-compose.yml` file is used to orchestrate both services:

- **nginx**: builds the Ubuntu-based Nginx image and exposes ports `8080` and `8081`.
- **test**: builds a separate Python test image that sends HTTP requests to the nginx service.

The test container connects to the nginx container using the service hostname `nginx` on the internal Docker Compose network.

![Docker Compose](<images/1. Docker Images/b. Test Image/Docker Compose.png>)

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

![Docker Compose Test Run](<images/1. Docker Images/b. Test Image/Docker Compose Test Run.png>)

## Cleanup
```bash
docker compose down
```
![Container devops-home-assignment-nginx-1   Created ](<images/2. Docker Compose/Container devops-home-assignment-nginx-1  Created .png>)
![Container devops-home-assignment-test-1   Created ](<images/2. Docker Compose/Container devops-home-assignment-test-1   Created .png>)
![Allows test container to access nginx container](<images/2. Docker Compose/Allows test container to access nginx container.png>)


## GitHub repository that includes all required files and configuration.

GitHub Repository

A GitHub repository was created that includes all required files and configuration for this project.

The repository contains:

- nginx/ – Nginx Docker image (Ubuntu-based)

- test/ – Test Docker image (Python-based)

- docker-compose.yml

- .github/workflows/ci-workflow.yml

- README.md

![GitHub repository that includes all required files and configuration](<images/3. GitHub Repository & CI/GitHub repository that includes all required files and configuration.png>)


## CI (GitHub Actions)

A GitHub Actions workflow (`.github/workflows/ci-workflow.yml`) runs on every push and pull request.

It performs:
- Builds and runs the project using Docker Compose.
- If tests pass, it uploads an artifact containing a file named `succeeded`.
- If tests fail, it uploads an artifact containing a file named `fail`.

![workflow (ci.yml)](<images/3. GitHub Repository & CI/workflow (ci.yml).png>)

## Committing and Pushing the Workflow
The workflow file was committed and pushed using:
```bash
git add .github/workflows/ci-workflow.yml
git commit -m "Add GitHub Actions CI workflow"
git push
```
![Add GitHub Actions CI workflow](<images/3. GitHub Repository & CI/Add GitHub Actions CI workflow.png>)

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

![Add GitHub Actions CI workflow #1](<images/3. GitHub Repository & CI/Add GitHub Actions CI workflow1.png>)
![Add GitHub Actions CI workflow](<images/3. GitHub Repository & CI/If tests pass, publish an artifact containing a file named succeeded..png>)

## Docker image sizes as small as possible.
![Add GitHub Actions CI workflow #1](<images/Small Docker Images/small images.png>)

The relatively small image sizes were achieved by:

- Using `--no-install-recommends` in the Ubuntu-based Nginx image.(in nginx/Dockerfile).
- Removing apt cache after installation.(in nginx/Dockerfile).
- Using `python:3.12-slim` for the test image.(in test/Dockerfile).
- Installing Python dependencies with `--no-cache-dir`.(in test/Dockerfile).

These optimizations reduce unnecessary layers and prevent storing temporary installation files inside the final images.



## Advanced Functional Requirements 

## HTTPS with Self-Signed Certificate

### Generate Certificate and Private Key

The certificate and key were generated using OpenSSL inside a temporary Alpine container (to avoid installing OpenSSL locally):
```bash
docker run --rm -v ${PWD}\nginx\certs:/certs alpine sh -c \
"apk add --no-cache openssl && \
openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
-keyout /certs/server.key -out /certs/server.crt \
-subj '/CN=localhost'"
```
This creates the following files:

- nginx/certs/server.crt — self-signed certificate

- nginx/certs/server.key — private key

![self-signed certificate with HTTPS](<images/Advanced Functional Requirements/self-signed certificate with HTTPS/create Self-signed certificate.png>)

I added an additional server block that listens on port 443 with SSL enabled and serves the same HTML content as the HTTP server on port 8080.

I configured the paths to the self-signed certificate and private key used by Nginx for HTTPS.

![add 443 port](<images/Advanced Functional Requirements/self-signed certificate with HTTPS/add 443 port.png>)

I copied the self-signed certificate and private key into the Docker image so that Nginx can load them at runtime.

I exposed port 443 in the Nginx Docker image to support HTTPS traffic.

I mapped host port 443 to container port 443 in docker-compose so HTTPS can be accessed from the local machine.

![3](<images/Advanced Functional Requirements/self-signed certificate with HTTPS/3.png>)

### Verify HTTPS

```bash
docker compose up --build -d nginx
curl.exe -k https://localhost/
```
![4](<images/Advanced Functional Requirements/self-signed certificate with HTTPS/4.png>)

The -k flag allows connection using a self-signed certificate.

Expected result: HTTP 200 response with the same HTML page as port 8080.

## Rate Limiting

Rate limiting was configured per client IP at 5 requests per second and verified by sending 20 rapid requests and observing blocked responses (503).

I configured a rate limiting zone per client IP with a limit of 5 requests per second.

![1](<images/Advanced Functional Requirements/Rate Limiting/1.png>)

Rate limiting is enforced on the main endpoints using limit_req inside the location block.
The limit is configured per client IP using limit_req_zone with a rate of 5 requests per second.

![2](images/Advanced Functional Requirements/Rate Limiting/2.png)

The rate limit was tested by sending 20 rapid HTTP requests:

```bash
1..20 | % { curl.exe -s -o NUL -w "%{http_code}`n" http://localhost:8080/ }
```
![3](<images/Advanced Functional Requirements/Rate Limiting/3.png>)

Observed behavior:

Initial requests returned 200 OK

Subsequent requests returned 503 Service Unavailable

This confirms that the rate limit of 5 requests per second is enforced correctly.

## Validate the rate limiting behavior

To validate that the Nginx rate limiting configuration works correctly,
the test script (test/test.py) was extended to simulate a burst of rapid requests.

After validating that port 8080 returns HTTP 200 and the expected HTML content,
the test script now:

Sends 20 rapid HTTP requests to http://nginx:8080/

Counts how many responses return 503 or 429

Fails the test if no rate limiting is triggered

Passes if at least one request is limited

This ensures the rate limit of 5 requests per second is actively enforced.

![1](<images/Advanced Functional Requirements/limiting behavior/1.png>)

When running:
```bash
docker compose up --build --abort-on-container-exit
```

The test output should include:
```bash
Testing rate limiting on http://nginx:8080/ with 20 rapid requests...
[PASS] Rate limiting triggered successfully (X/20 requests were limited)
```
![2](<images/Advanced Functional Requirements/limiting behavior/2.png>)

This confirms:

- Rate limiting is active

- The test script correctly detects it

- The CI pipeline will fail if rate limiting stops working

## CI validates rate limiting as part of the automated tests.

After extending the test script to validate the rate limiting behavior,
a new commit was pushed to the repository. GitHub Actions automatically triggered the CI workflow.

# CI Result

- The workflow completed successfully.

- The Docker images were rebuilt.

- Docker Compose was executed.

The extended test script validated:

- HTTP 200 behavior

- HTTP 404 behavior

- Rate limiting enforcement

- The test container exited with code 0.

- An artifact named test-result was uploaded.

This confirms that:

Rate limiting is correctly enforced.

The extended test logic works properly.

The CI pipeline validates the new functionality automatically.

![3](<images/Advanced Functional Requirements/limiting behavior/3.png>)

## Rate Limiting Configuration

To enhance server stability and prevent abuse, rate limiting was configured in the Nginx server.

---

### How it works

Rate limiting is implemented using the `limit_req_zone` and `limit_req` directives in `nginx.conf`.

At the `http` level, the following configuration is defined:

```bash
limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=5r/s;
```
Explanation:

- $binary_remote_addr
Limits requests per client IP address.

- zone=req_limit_per_ip:10m
Allocates 10MB of shared memory to track request counters per IP.

- rate=5r/s
Allows a maximum of 5 requests per second per IP address.

Inside each relevant server block (8080 and 443), rate limiting is enforced within the location block:
```bash
location / {
    limit_req zone=req_limit_per_ip nodelay;
    try_files $uri $uri/ =404;
```
![1](<images/Advanced Functional Requirements/Rate Limiting/2.png>)

Explanation:

- limit_req zone=req_limit_per_ip
Applies the previously defined rate limiting zone.

- nodelay
Excess requests are rejected immediately instead of being delayed.

When the request rate exceeds the defined threshold, Nginx responds with HTTP 503 (Service Temporarily Unavailable).

## Rate Limiting Test Validation

The automated test script was extended to validate the rate limiting behavior.

It sends 20 rapid requests to the main endpoint and verifies that at least one request is rejected with HTTP 503 or 429.

This ensures that rate limiting is actively enforced and functioning correctly.

![2](<images/Advanced Functional Requirements/limiting behavior/2.png>)

## How to change the rate limit threshold

To modify the allowed request rate, update the following line in nginx.conf:

```bash
limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=5r/s;
```
![1](<images/Advanced Functional Requirements/Rate Limiting/1.png>)

After modifying the configuration, rebuild and restart the containers:

```bash
docker compose down
docker compose up --build
```
The new rate limit will take effect immediately after the rebuild.











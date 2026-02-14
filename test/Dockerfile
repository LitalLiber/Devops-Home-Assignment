# Use a lightweight official Python image to keep the image size small
# We intentionally use the "slim" variant to reduce unnecessary packages
FROM python:3.12-slim

# Set working directory inside the container
# All subsequent commands will run from /app
WORKDIR /app

# Install Python dependencies (keep image small)
# We copy requirements first to leverage Docker layer caching:
# if requirements.txt does not change, dependencies won't reinstall
COPY requirements.txt .

# Install dependencies without caching to reduce final image size
# --no-cache-dir prevents pip from storing unnecessary cache files
RUN pip install --no-cache-dir -r requirements.txt

# Copy the test script into the container
# This is done after installing dependencies to optimize build caching
COPY test.py .

# Run the test script when the container starts
# The script will exit with:
#   0  -> success (tests passed)
#   1  -> failure (tests failed)
# This exit code is critical for CI to determine pass/fail status
CMD ["python", "test.py"]

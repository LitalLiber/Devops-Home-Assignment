FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies (keep image small)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the test script
COPY test.py .

CMD ["python", "test.py"]

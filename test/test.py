import os
import sys
import requests


def fail(message):
    print(f"[FAIL] {message}")
    sys.exit(1)


def main():
    # Read environment variables (with defaults)
    host = os.getenv("NGINX_HOST", "nginx")
    port_ok = int(os.getenv("PORT_OK", 8080))
    port_err = int(os.getenv("PORT_ERR", 8081))

    url_ok = f"http://{host}:{port_ok}/"
    url_err = f"http://{host}:{port_err}/"

    print(f"Testing OK endpoint: {url_ok}")
    try:
        response_ok = requests.get(url_ok)
    except Exception as e:
        fail(f"Could not connect to {url_ok}: {e}")

    # Validate status code
    if response_ok.status_code != 200:
        fail(f"Expected status 200 from {url_ok}, got {response_ok.status_code}")

    # Validate content
    if "Hello from server 1" not in response_ok.text:
        fail("Expected custom HTML content not found in response from port 8080")

    print("[PASS] Port 8080 returned expected HTML and status 200")

    print(f"Testing error endpoint: {url_err}")
    try:
        response_err = requests.get(url_err)
    except Exception as e:
        fail(f"Could not connect to {url_err}: {e}")

    # Validate error status (expecting 404 specifically)
    if response_err.status_code != 404:
        fail(f"Expected status 404 from {url_err}, got {response_err.status_code}")

    print("[PASS] Port 8081 returned expected HTTP 404 error")

    print("All tests passed")
    sys.exit(0)


if __name__ == "__main__":
    main()

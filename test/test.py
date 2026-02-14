# Standard library imports
import os      # Used to read environment variables
import sys     # Used to exit with specific exit codes

# Third-party library used to send HTTP requests
import requests


# Helper function to handle test failures consistently
# Prints a clear failure message and exits with non-zero status
# Non-zero exit code is critical for CI to detect failure
def fail(message):
    print(f"[FAIL] {message}")
    sys.exit(1)


def main():
    # Read environment variables (with defaults)
    # Design decision:
    # We allow overriding host and ports using environment variables
    # This makes the test reusable in different environments (e.g., CI, local)
    host = os.getenv("NGINX_HOST", "nginx")
    port_ok = int(os.getenv("PORT_OK", 8080))
    port_err = int(os.getenv("PORT_ERR", 8081))

    # Construct URLs dynamically based on environment configuration
    url_ok = f"http://{host}:{port_ok}/"
    url_err = f"http://{host}:{port_err}/"

    print(f"Testing OK endpoint: {url_ok}")
    try:
        # Send HTTP request to the success endpoint
        response_ok = requests.get(url_ok)
    except Exception as e:
        # If connection fails (container not reachable, DNS issue, etc.)
        # Immediately fail the test
        fail(f"Could not connect to {url_ok}: {e}")

    # Validate status code
    # Requirement: Server 1 must return HTTP 200
    if response_ok.status_code != 200:
        fail(f"Expected status 200 from {url_ok}, got {response_ok.status_code}")

    # Validate content
    # Assumption:
    # The HTML contains the unique string "Hello from server 1"
    # We validate content to ensure correct server behavior,
    # not just that something responded on the port.
    if "Hello from server 1" not in response_ok.text:
        fail("Expected custom HTML content not found in response from port 8080")

    print("[PASS] Port 8080 returned expected HTML and status 200")

    # Rate limiting validation (5 requests/sec)
    # Send a burst of requests quickly and expect at least one request to be limited (503/429).
    limited_statuses = {429, 503}
    limited_count = 0
    total_requests = 20

    print(f"Testing rate limiting on {url_ok} with {total_requests} rapid requests...")
    for i in range(total_requests):
        try:
            r = requests.get(url_ok)
        except Exception as e:
            fail(f"Rate limit test request failed: {e}")

        if r.status_code in limited_statuses:
            limited_count += 1

    if limited_count == 0:
        fail("Rate limiting did not trigger (expected at least one 503/429 response).")

    print(f"[PASS] Rate limiting triggered successfully ({limited_count}/{total_requests} requests were limited)")


    print(f"Testing error endpoint: {url_err}")
    try:
        # Send HTTP request to the error endpoint
        response_err = requests.get(url_err)
    except Exception as e:
        fail(f"Could not connect to {url_err}: {e}")

    # Validate error status (expecting 404 specifically)
    # Design decision:
    # We check explicitly for 404 because that is how the Nginx server
    # was configured in nginx.conf
    if response_err.status_code != 404:
        fail(f"Expected status 404 from {url_err}, got {response_err.status_code}")

    print("[PASS] Port 8081 returned expected HTTP 404 error")

    # If we reached here, all validations passed
    print("All tests passed")

    # Exit with 0 to signal success (important for CI pipeline)
    sys.exit(0)


# Standard Python entry point guard
# Ensures main() runs only when executed as a script
if __name__ == "__main__":
    main()

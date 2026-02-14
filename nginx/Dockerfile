# Use Ubuntu 22.04 as required by the assignment
# Design decision: Explicit LTS version ensures stability and reproducibility
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
# Assumption: Container builds must be fully non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install nginx
# --no-install-recommends keeps the image smaller (Non-functional requirement: small image size)
# Trade-off: Some optional packages are not installed to reduce image size
# Removing apt lists reduces final image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy custom Nginx configuration file
# Design decision: Override default nginx.conf to define two custom server blocks
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static HTML files to the web root directory
# Assumption: The nginx.conf root directive points to /var/www/html
COPY html/ /var/www/html/

COPY certs/ /etc/nginx/certs/

# Expose both ports used by the two server blocks
# Port 8080 -> custom HTML response
# Port 8081 -> HTTP error response
EXPOSE 8080 8081 443

# Run Nginx in foreground mode
# Required so the container does not exit immediately
# Design decision: Use "daemon off;" to keep container alive
CMD ["nginx", "-g", "daemon off;"]

# Start from a lightweight Python base image
FROM python:3.13-slim

# Set a working directory
WORKDIR /app

# Copy only the relevant files first (for layer caching)
COPY pyproject.toml /app

# Copy the source code
COPY src /app/src

COPY config.yaml /etc/zigbee2mqtt_maas_power/config.yaml

# Install build tools (to build from pyproject.toml)
RUN pip install --no-cache-dir build

# Build a wheel / sdist from your package
RUN python -m build

# Install the built wheel from the dist folder
RUN pip install --no-cache-dir dist/*.whl

ENTRYPOINT ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "zigbee2mqtt_maas_power.wsgi:app"]

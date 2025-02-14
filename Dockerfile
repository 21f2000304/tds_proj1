FROM python:3.12-slim-bookworm

# Install curl and certificates for downloading the UV installer
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest UV installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Set the working directory
WORKDIR /app

# Create the data directory with correct permissions
RUN mkdir -p /data && chmod 777 /data

# Copy the application code
COPY app.py /app

# Install Python dependencies system-wide
RUN uv pip install --system fastapi uvicorn requests

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
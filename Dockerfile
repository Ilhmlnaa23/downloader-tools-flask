FROM python:3.11-slim-buster as build

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3-dev ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --upgrade spotdl

# Stage 2: Production Stage
FROM python:3.11-slim-buster as production

WORKDIR /app

# Copy only necessary files from the build stage
COPY --from=build /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=build /usr/local/bin/spotdl /usr/local/bin/spotdl
COPY . /app/
# Install uWSGI
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3-dev ffmpeg && \
    pip install uwsgi && \
    apt-get purge -y build-essential python3-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*	

EXPOSE 3000

CMD ["uwsgi", "--ini", "/app/wsgi.ini"]

FROM python:3.10-slim-buster

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3-dev ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install --upgrade spotdl

# Copy application files
COPY . /app/

# Install uWSGI
RUN pip install uwsgi

EXPOSE 3000

CMD ["uwsgi", "--ini", "/app/wsgi.ini"]

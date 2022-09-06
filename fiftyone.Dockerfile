# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8.10

# Install system dependencies
RUN set -e; \
    apt-get update -y
RUN apt-get install -y \
    tini \
    libcurl4 \
    libssl-dev \
    curl \
    lsb-release; \
    gcsFuseRepo=gcsfuse-`lsb_release -c -s`; \
    echo "deb http://packages.cloud.google.com/apt $gcsFuseRepo main" | \
    tee /etc/apt/sources.list.d/gcsfuse.list; \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    apt-key add -; \
    apt-get update
    
RUN apt-get install -y gcsfuse
RUN apt-get clean

# Set fallback mount directory
ENV APP_HOME /app
ENV MNT_DIR ${APP_HOME}/data
ENV PYTHONBUFFERED True

WORKDIR $APP_HOME

# Install python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install fiftyone

COPY . ${APP_HOME}
RUN mkdir -p ${MNT_DIR}

# Environment Variables
ENV LOG_LEVEL INFO
ENV BUCKET_NAME ""
ENV BUCKET_PATH_PREFIX ""
ENV GOOGLE_APPLICATION_CREDENTIALS "/key.json"
ENV PORT 5151


# Use tini to manage zombie processes and signal forwarding
# https://github.com/krallin/tini
ENTRYPOINT ["/usr/bin/tini", "--"] 

# Pass the startup script as arguments to Tini
CMD echo echo "Mounting GCS Fuse." && \
    gcsfuse -o allow_other --implicit-dirs $BUCKET $MNT_DIR && \
    echo "Mounting completed." && \
    python src/DataLoader.py
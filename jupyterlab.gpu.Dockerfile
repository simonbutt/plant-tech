FROM tensorflow/tensorflow:2.7.0-gpu

# Base python
RUN python3 -m pip install --upgrade pip
RUN pip install poetry

ENV APP_NAME plant-tech
WORKDIR /${APP_NAME}

# Install Python package dependencies
COPY pyproject.toml /${APP_NAME}
RUN poetry config virtualenvs.create false && poetry install

# Set secret variable as a container volume.
ENV GOOGLE_APPLICATION_CREDENTIALS "/${APP_NAME}/key.json"


# Use tini to manage zombie processes and signal forwarding
# https://github.com/krallin/tini
ENTRYPOINT ["/usr/bin/tini", "--"] 

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter lab --notebook-dir=/${APP_NAME} --ip 0.0.0.0 --no-browser --allow-root"]
<h1><strong> Plant Tech CV Toolkit</strong></h1>

<strong>Objective</strong>: Build an opensource computer vision (CV) toolkit for plant tech use case.


# Pre-requisites

### Python
```
# Install python version
pyenv install

# Install python package dependencies
poetry install

```
### [Direnv](https://direnv.net/)
Direnv is a local environment variable tool. [Installment documentation](https://direnv.net/docs/installation.html)

```
direnv allow
```

There is an example [.envrc.sample](./.envrc.sample)

### [GCSFuse](https://cloud.google.com/storage/docs/gcs-fuse)

Following [this](https://cloud.google.com/run/docs/tutorials/network-filesystems-fuse) approach for GCSFuse in docker, to be used for either local GPU workbench or Cloud Run deployment.

Local GCSFuse

```
gcsfuse --implicit-dirs ${BUCKET_NAME} $(pwd)/data
```
\* This requires setting your `.envrc`

### [Commitizen](https://commitizen-tools.github.io/commitizen/)

To commit to this repo, please use:
```
poetry run cz c -s
```
and follow the instructions.

# UX

## JupyterLab

Local notebook workplace
```
poetry run jupyter lab
```

### Containerisation

```
docker build \
    -t "plant-tech/jupyter:local" 
    -f fiftyone.Dockerfile
    . 


# Run
docker run \
    -v $(path-to-key):key.json \
    --net=host
    plant-tech/jupyter:local
```
\* Replace `docker` for `podman` where required.

## [FiftyOne](https://voxel51.com/docs/fiftyone/)

Fiftyone CV image visualisation opensource package.
```
poetry run src/DataLoader.py
```

### Containerisation
```
# Build 
docker build \
    -t "plant-tech/fiftyone:local" 
    -f fiftyone.Dockerfile
    . 


# Run
docker run \
    -v $(path-to-key):key.json \
    -e BUCKET_NAME:$BUCKET_NAME
    -e BUCKET_PATH_PREFIX:$BUCKET_PATH_PREFIX \
    -e LOG_LEVEL:$LOG_LEVEL \
    --net=host \
    plant-tech/fifyone:local
```
\* Replace `docker` for `podman` where required.


### Mongodb

Mongo is a hard dependency for fiftyone. 

```
# local
docker run --net=host mongo:latest
```
\* Remember to refresh mongo between fiftyone sessions

### ngrok
[ngrok](https://ngrok.com/) can be used for demos (though be careful).

With either the local or containerised application running + mongo
```
ngrok http 5151
```

## [CVAT](https://github.com/opencv/cvat)

TODO


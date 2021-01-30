#!/bin/bash 
# Buildah script to build kni python application and illustrate why buildah 
# is a simpler (and perhaps better?) tool for building container images than
# a Dockerfile. Note that this isn't necessarily best practice, but simply
# examples of what can be done to build an image

# Source Image
SOURCE_IMAGE="python:3.8-slim"

# Destination Image
DEST_IMAGE="quay.io/kni:latest"

# Source Root directory
PROC_CWD=$(readlink -f $0)
SRC_DIR=${PROC_CWD%%/bin/*}

# App dir
APP_DIR=/app

# Build new container image
NEW_IMAGE=$(buildah from $SOURCE_IMAGE)

echo "Building new image $DEST_IMAGE ($NEW_IMAGE)"
echo "        from image $SOURCE_IMAGE"
echo "           src dir $SRC_DIR"

MOUNTPOINT=$(buildah mount $NEW_IMAGE)

buildah config --env PYTHONUNBUFFERED=1 $NEW_IMAGE
buildah config --env LANG=en_US.UTF-8 $NEW_IMAGE
buildah config --env PIP_NO_CACHE_DIR=off $NEW_IMAGE

# VirtualEnv Method
#. $MOUNTPOINT/app/bin/activate
#$PYTHON -m venv $MOUNTPOINT/$APP_DIR

# Use Python interpreter inside the source image
PYTHON=$MOUNTPOINT/usr/local/bin/python
export PYTHONPATH=$MOUNTPOINT/usr/local/lib/python3.8/site-packages


cd $SRC_DIR && $PYTHON -m pip install --upgrade -r requirements.txt --target=$MOUNTPOINT/usr/local/lib/python3.8/site-packages --force-reinstall && $PYTHON setup.py install --root=$MOUNTPOINT

buildah config --port 8080 $NEW_IMAGE

buildah config --env APP_SCRIPT=bin/app.sh $NEW_IMAGE
buildah config --entrypoint "/usr/local/bin/python -m kni" $NEW_IMAGE

buildah commit --squash $NEW_IMAGE
buildah rm $NEW_IMAGE

echo "export MOUNTPOINT=$MOUNTPOINT"

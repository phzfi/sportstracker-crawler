#!/bin/bash

BUILD_ENV=$1
VERSION=$2
USER=$3
PASSWORD=$4
if !( [ "$BUILD_ENV" == "stg" ] || [ "$BUILD_ENV" == "prod" ] ) || [ -z "$VERSION" ]; then
  echo "Usage: ./build.sh [stg|prod] <version>, e.g. ./build.sh stg 1-dev"
  exit 1
fi

TAG=phz/sportstracker:$VERSION

echo "Building $TAG"

docker login  -u $USER -p $PASSWORD
docker build --build-arg BUILD_ENV=$BUILD_ENV -t $TAG .. 
docker tag $TAG /$TAG
docker push /$TAG

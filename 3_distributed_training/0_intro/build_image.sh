#!/bin/bash -e

name=distributed-training-intro
image_name=us-central1-docker.pkg.dev/inductive-world-365914/adv-mlops-repository/${name}
image_tag=latest
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")" 
docker build -f ./Dockerfile -t "${full_image_name}" .
docker push "$full_image_name"

# Output the strict image name, which contains the sha256 image digest
docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name}"
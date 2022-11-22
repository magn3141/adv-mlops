#!/bin/bash
  
CLUSTERNAME=adv-mlops
ZONE=us-central1-a
gcloud config set compute/zone $ZONE
gcloud beta container clusters create $CLUSTERNAME \
  --enable-autoupgrade \
  --zone $ZONE \
  --scopes cloud-platform \
  --logging SYSTEM \
  --monitoring SYSTEM \
  --machine-type n1-standard-2 \
  --num-nodes 4
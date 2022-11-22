CLUSTER_NAME=adv-mlops
ZONE=us-central1-a

gcloud container node-pools create gpu-pool \
    --cluster=${CLUSTER_NAME} \
    --zone ${ZONE} \
    --num-nodes=1 \
    --machine-type n1-highmem-8 \
    --scopes cloud-platform --verbosity error \
    --accelerator=type=nvidia-tesla-k80,count=1
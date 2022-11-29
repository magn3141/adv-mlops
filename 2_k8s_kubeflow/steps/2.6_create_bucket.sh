BUCKET_NAME=adv-mlops-bucket
PROJECT_ID=$(gcloud config get-value project)

gcloud storage buckets create gs://${BUCKET_NAME} \
    --location=us-central1 \
    --storage-class=STANDARD \
    --project=${PROJECT_ID}
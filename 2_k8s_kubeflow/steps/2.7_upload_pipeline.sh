PROJECT_ID=$(gcloud config get-value project)
REPO_ID=adv-mlops-kubeflow
PIPELINE_NAME=TrainBoundaries
ZONE=us-central1

curl -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -F tags=v1,latest \
    -F content=@Pipelines/${PIPELINE_NAME}.yaml \
    https://${ZONE}-kfp.pkg.dev/${PROJECT_ID}/${REPO_ID}
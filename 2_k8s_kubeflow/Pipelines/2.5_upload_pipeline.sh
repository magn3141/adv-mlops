PROJECT_ID=inductive-world-365914
REPO_ID=adv-mlops-kubeflow
PIPELINE_NAME=TrainBoundaries
ZONE=us-central1

curl -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -F tags=v1,latest \
    -F content=@${PIPELINE_NAME}.json \
    https://${ZONE}-kfp.pkg.dev/${PROJECT_ID}/${REPO_ID}
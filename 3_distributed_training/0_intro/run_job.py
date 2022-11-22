from google.cloud import aiplatform

DOCKER_IMAGE_URI = "us-central1-docker.pkg.dev/inductive-world-365914/adv-mlops-repository/distributed-training-intro"
MACHINE = "n1-standard-4"
MACHINE_REDUCTION_SERVER = "n1-standard-16"
BUCKET = "gs://adv-mlops-bucket-2"
ACCELERATOR_TYPE = "NVIDIA_TESLA_K80"
REGION = "us-central1"

# The spec of the worker pools including machine type and Docker image
# Be sure to replace {YOUR-PROJECT-ID} with your project ID.
worker_pool_specs=[
     {
        "replica_count": 1,
        "machine_spec": {
          "machine_type": MACHINE, "accelerator_type": ACCELERATOR_TYPE, "accelerator_count": 1
        },
        "container_spec": {"image_uri": DOCKER_IMAGE_URI}
      },
      {
        "replica_count": 1,
        "machine_spec": {
          "machine_type": MACHINE, "accelerator_type": ACCELERATOR_TYPE, "accelerator_count": 1
        },
        "container_spec": {"image_uri": DOCKER_IMAGE_URI}
      },
      {
        "replica_count": 1,
        "machine_spec": {
          "machine_type": MACHINE_REDUCTION_SERVER
        },
        "container_spec": {"image_uri": "us-docker.pkg.dev/vertex-ai-restricted/training/reductionserver:latest"}
      }
]

# Replace YOUR_BUCKET
my_multiworker_job = aiplatform.CustomJob(display_name='distributed-training-intro',
                              location=REGION,
                              worker_pool_specs=worker_pool_specs,
                              staging_bucket=BUCKET)

my_multiworker_job.run()

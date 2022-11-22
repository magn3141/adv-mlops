import google.cloud.aiplatform as aip


# job = aip.PipelineJob(
#     display_name="TrainBoundariesNoGPU",
#     template_path="TrainBoundariesNoGPU.json",
#     pipeline_root="gs://adv-mlops-bucket",
#     parameter_values={ "classifier_type": "all_deepface", "chosen_num_ratio": 0.1},
# )
# job = aip.PipelineJob(
#     display_name="TrainBoundariesParallel",
#     template_path="TrainBoundariesParallel.json",
#     pipeline_root="gs://adv-mlops-bucket",
#     parameter_values={ "classifier_type": "all_deepface", "chosen_num_ratio": 0.06, "number_of_images": 100},
# )
job = aip.PipelineJob(
    display_name="TrainBoundaries",
    template_path="TrainBoundaries.json",
    pipeline_root="gs://adv-mlops-bucket",
    parameter_values={ "classifier_type": "all_deepface", "chosen_num_ratio": 0.06, "number_of_images": 100},
)
# job = aip.PipelineJob(
#     display_name="TrainBoundaries",
#     template_path="TrainBoundaries.json",
#     pipeline_root="gs://adv-mlops-bucket",
#     parameter_values={"number_of_images": 20, "image_size": 256, "classifier_type": "smile"},
# )

job.submit()
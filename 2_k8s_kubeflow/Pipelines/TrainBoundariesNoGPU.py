import kfp
import kfp.components as comp
from kfp.v2 import compiler
from kfp.v2.dsl import component, InputPath, Output, OutputPath, Dataset, Model, pipeline, Artifact, importer
from google_cloud_pipeline_components.v1.custom_job import load_component_from_file, create_custom_training_job_from_component
import google.cloud.aiplatform as aip

# Define a Python function



@pipeline(
    name='train-boundaries-no-gpu',
    description='Train boundaries for a StyleGAN model.'
)
def train_boundaries(
    project_id: str = 'inductive-world-365914',
    classifier_type: str = 'black',
    chosen_num_ratio: float = 0.1,
    split_ratio: float = 0.7,
    transformer: str = 'SVM'
):
    images_dir_task = importer(
        artifact_uri='gs://adv-mlops-bucket/dataset-24112/images/',
        artifact_class=Dataset,
        reimport=True,
    )
    seed_file_task = importer(
        artifact_uri='gs://adv-mlops-bucket/dataset-24112/seeds.npy',
        artifact_class=Dataset,
        reimport=True,
    )

    latens_file_task = importer(
        artifact_uri='gs://adv-mlops-bucket/dataset-24112/latents.npy',
        artifact_class=Dataset,
        reimport=True,
    )

    # sampler = comp.load_component_from_file('../components/StyleGANSampler/component.yaml')
    # classifier =    comp.load_component_from_file('../components/LatentClassification/component.yaml')
    trainer =       comp.load_component_from_file('../components/TransformerModelTrainer/component.yaml')

    classifier = create_custom_training_job_from_component(
        component_spec = load_component_from_file('../components/LatentClassification/component.yaml'),
        machine_type="n1-standard-16",
        accelerator_type=  aip.gapic.AcceleratorType.NVIDIA_TESLA_K80,
        accelerator_count=8,
        )


    # Define the pipeline
    # sample_task = sampler(number_of_images, image_size).add_node_selector_constraint('cloud.google.com/gke-accelerator', 'NVIDIA_TESLA_K80').set_gpu_limit(1)
    classifier_task = classifier(project=project_id, images_dir=images_dir_task.output,  seeds_file=seed_file_task.output, classifier_type=classifier_type)
    trainer_task =  trainer(scores=classifier_task.outputs['scores'], classifiers='sad,surprise,fear,happy,angry', latents_file=latens_file_task.output, transformer=transformer, chosen_num=chosen_num_ratio, split_ratio=split_ratio)

    


if __name__ == '__main__':
    compiler.Compiler().compile(train_boundaries,  package_path='TrainBoundariesNoGPU.json')

import google.cloud.aiplatform as aip
import kfp
import kfp.components as comp
from google_cloud_pipeline_components.v1.custom_job import (
    create_custom_training_job_from_component, load_component_from_file)
from kfp.v2 import compiler
from kfp.v2.dsl import InputPath, OutputPath

# Define a Python function



@kfp.dsl.component
def combine_data(
    latents_file_1: InputPath('npy'),
    latents_file_2: InputPath('npy'),
    scores_1: InputPath('npy'),
    scores_2: InputPath('npy'),
    latents_file: OutputPath('npy'),
    classifiers: str,
    scores: OutputPath()
):
    import pathlib

    import numpy as np 
 
    pathlib.Path(scores).mkdir(parents=True, exist_ok=True)
    pathlib.Path(latents_file).parent.mkdir(parents=True, exist_ok=True)

    for classifier in classifiers.split(','):
        try:
            scores_1 = np.load(scores_1 + '/' + classifier + '.npy')
            scores_2 = np.load(scores_2 + '/' + classifier + '.npy')
            np.save(scores + '/' + classifier + '.npy', np.concatenate((scores_1, scores_2)))
        except:
            pass
    np.save(latents_file, latents)


@kfp.dsl.pipeline(
    name='train-boundaries-parallel',
    description='Train boundaries for a StyleGAN model.'
)
def train_boundaries(
    project_id: str = 'inductive-world-365914',
    number_of_images: int = 50000,
    image_size: int = 256,
    chosen_num_ratio: float = 0.1,
    split_ratio: float = 0.7,
    classifier_type: str = 'all_deepface',
    transformer: str = 'SVM'
):
    
    sampler = create_custom_training_job_from_component(
        component_spec = load_component_from_file('../components/StyleGANSampler/component.yaml'),
        machine_type="n1-standard-16",
        accelerator_type=  aip.gapic.AcceleratorType.NVIDIA_TESLA_K80,
        accelerator_count=2,
        )

    classifier = create_custom_training_job_from_component(
        component_spec = load_component_from_file('../components/LatentClassification/component.yaml'),
        
        machine_type="n1-standard-16",
        accelerator_type=  aip.gapic.AcceleratorType.NVIDIA_TESLA_K80,
        accelerator_count=2,
    )
    trainer = comp.load_component_from_file('../components/TransformerModelTrainer/component.yaml')

    # Define the pipeline
    sample_task_1= sampler(project=project_id, amount_of_images=number_of_images, image_size = image_size).add_node_selector_constraint('cloud.google.com/gke-accelerator', 'NVIDIA_TESLA_K80').set_gpu_limit(1)
    sample_task_2= sampler(project=project_id, amount_of_images=number_of_images, image_size = image_size).add_node_selector_constraint('cloud.google.com/gke-accelerator', 'NVIDIA_TESLA_K80').set_gpu_limit(1)
    classifier_task_1 = classifier(project=project_id, images_dir=sample_task_1.outputs['images_dir'],  seeds_file=sample_task_1.outputs['seeds_file'], classifier_type=classifier_type).add_node_selector_constraint('cloud.google.com/gke-accelerator', 'NVIDIA_TESLA_K80').set_gpu_limit(1)
    classifier_task_2 = classifier(project=project_id, images_dir=sample_task_2.outputs['images_dir'],  seeds_file=sample_task_2.outputs['seeds_file'], classifier_type=classifier_type).add_node_selector_constraint('cloud.google.com/gke-accelerator', 'NVIDIA_TESLA_K80').set_gpu_limit(1)
    
    combine_data_job = comp.create_component_from_func_v2(combine_data, base_image='python:3.9')

    combine_data_task = combine_data_job(
            latents_file_1=sample_task_1.outputs['latents_file'], 
            latents_file_2=sample_task_2.outputs['latents_file'], 
            scores_1=classifier_task_1.outputs['scores'], 
            scores_2=classifier_task_2.outputs['scores'], 
            classifiers="sad,surprise,fear,happy,angry,indian,asian,latino hispanic,black,middle eastern,age,Man,Woman,"
        )
    trainer_task_sad = trainer(scores=combine_data_task.outputs['scores'], classifiers='sad,surprise,fear,happy,angry', latents_file=combine_data_task.outputs['latents_file'], transformer=transformer, chosen_num=chosen_num_ratio, split_ratio=split_ratio)

if __name__ == '__main__':
    compiler.Compiler().compile(train_boundaries,  package_path='TrainBoundariesParallel.json')

import kfp
import kfp.components as comp
from kfp.v2 import compiler
from google_cloud_pipeline_components.v1.custom_job import load_component_from_file, create_custom_training_job_from_component
import google.cloud.aiplatform as aip
# Define a Python function



@kfp.dsl.pipeline(
    name='train-boundaries',
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
        accelerator_count=4,
        )

    classifier = create_custom_training_job_from_component(
        component_spec = load_component_from_file('../components/LatentClassification/component.yaml'),
        
        machine_type="n1-standard-16",
        accelerator_type=  aip.gapic.AcceleratorType.NVIDIA_TESLA_K80,
        accelerator_count=4,
    )
    trainer = comp.load_component_from_file('../components/TransformerModelTrainer/component.yaml')

    # Define the pipeline
    sample_task= sampler(project=project_id, amount_of_images=number_of_images, image_size = image_size).add_node_selector_constraint('cloud.google.com/gke-accelerator', 'NVIDIA_TESLA_K80').set_gpu_limit(1)
    classifier_task = classifier(project=project_id, images_dir=sample_task.outputs['images_dir'],  seeds_file=sample_task.outputs['seeds_file'], classifier_type=classifier_type).add_node_selector_constraint('cloud.google.com/gke-accelerator', 'NVIDIA_TESLA_K80').set_gpu_limit(1)
    trainer_task_sad = trainer(scores=classifier_task.outputs['scores'], classifiers='sad,surprise,fear,happy,angry', latents_file=sample_task.outputs['latents_file'], transformer=transformer, chosen_num=chosen_num_ratio, split_ratio=split_ratio)
    trainer_task_surprise = trainer(scores=classifier_task.outputs['scores'], classifiers='indian,asian,latino hispanic,black,middle eastern', latents_file=sample_task.outputs['latents_file'], transformer=transformer, chosen_num=chosen_num_ratio, split_ratio=split_ratio)

if __name__ == '__main__':
    compiler.Compiler().compile(train_boundaries,  package_path='TrainBoundaries.json')

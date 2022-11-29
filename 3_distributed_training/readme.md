
# Distributed training

This is about how to train models and GAN in a distributed way. First I did a simple example for multi node distributed training using Tensorflow on Vertex AI. Then I trained StyleGAN2-ADA (Pytorch implementation) for a small amount. Here I first trained it using a multicore GPU. Afterward I modifyied the code to allow for multi node training.

## Basic example with Vertex AI and Tensorflow

In the folder `0_intro`, we have a basic example of how to train a model in a distributed way. The example is from this  [Google tutorial](https://codelabs.developers.google.com/vertex_multiworker_training#0).
It uses Tensorflow and it `MultiWorkerMirroredStrategy` to train a model in a distributed way. The example is very simple and it is not very useful for our purposes. However, it is a good starting point to understand how to train a model in a distributed way and get it running in the cloud. The `run_job.py`creates the job for Vertex AI and submits it

## Distributed training with PyTorch and StyleGAN2-ADA

In the folder `1_stylegan2-ada-example`, we have a more complex example of how to train a model in a distributed way. The code is from the [StyleGAN2-ADA repository](https://github.com/NVlabs/stylegan2-ada-pytorch). To run the job with a single worker with multiple GPUs, we can use the `run_single_worker.py` script. To run the job with multiple workers, we can use the `run_multi_worker.py` script.

## References

Look at this: <https://www.youtube.com/watch?v=qctwfYZKK8M>

Look at this: <https://codelabs.developers.google.com/vertex_multiworker_training#0>

Look at this: <https://keras.io/examples/generative/gan_ada/>

Loot at his: <https://pytorch.org/tutorials/intermediate/ddp_series_multinode.html>

Look at this: <https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/official/reduction_server/pytorch_distributed_training_reduction_server.ipynb>

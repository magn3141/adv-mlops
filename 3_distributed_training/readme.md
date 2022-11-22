
# Distributed training
This is about how to train models in a distributed way.

## Basic example with Vertex AI and Tensorflow

In the folder `0_intro`, we have a basic example of how to train a model in a distributed way. The example is from this  [Google tutorial](https://pytorch.org/tutorials/intermediate/ddp_series_multinode.html).
It uses Tensorflow and it MultiWorkerMirroredStrategy to train a model in a distributed way. The example is very simple and it is not very useful for our purposes. However, it is a good starting point to understand how to train a model in a distributed way and get it running in the cloud.

## Distributed training with PyTorch and StyleGAN2-ADA

In the folder `1_stylegan2-ada-example`, we have a more complex example of how to train a model in a distributed way. The code is from the [StyleGAN2-ADA repository](https://github.com/NVlabs/stylegan2-ada-pytorch).

## References

Look at this: <https://www.youtube.com/watch?v=qctwfYZKK8M>
Look at this: <https://codelabs.developers.google.com/vertex_multiworker_training#0>
Look at this: <https://keras.io/examples/generative/gan_ada/>
Loot at his: <https://pytorch.org/tutorials/intermediate/ddp_series_multinode.html>
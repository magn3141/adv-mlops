FROM us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-9:latest

RUN pip install click requests tqdm pyspng ninja imageio-ffmpeg==0.4.3

# Copies the trainer code to the docker image.
COPY stylegan2-ada-pytorch /stylegan2-ada-pytorch

RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz -o /cifar-10-python.tar.gz
RUN python dataset_tool.py --source=/cifar-10-python.tar.gz --dest=~/datasets/cifar10.zip

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python", "-m", "trainer.task"]
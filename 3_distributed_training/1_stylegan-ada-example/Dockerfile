FROM us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-7:latest

RUN pip install click requests tqdm pyspng ninja imageio-ffmpeg==0.4.3
# RUN pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

# Copies the trainer code to the docker image.
# RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
COPY dog /dog
COPY stylegan2-ada-pytorch/dataset_tool.py /dataset_tool.py
RUN python dataset_tool.py --source=/dog --dest=/afhqdog.zip  --width=32 --height=32

COPY stylegan2-ada-pytorch /stylegan2-ada-pytorch
WORKDIR /stylegan2-ada-pytorch

ENV DNNLIB_CACHE_DIR=/gcs/adv-mlops-bucket-2/
# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python",  "train.py", "--outdir=/gcs/adv-mlops-bucket-2/stylegan2-ada/", "--gpus=2", "--data=/afhqdog.zip", "--kimg=400"]

FROM gcr.io/deeplearning-platform-release/pytorch-gpu.1-12
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \ 
        python3-opencv
RUN python3 -m pip install opencv-python
COPY ./InterfaceTraining/requirements.latent_classification.txt .
RUN python3 -m pip install -U pip wheel cmake
RUN python3 -m pip install -r requirements.latent_classification.txt
COPY ./InterfaceTraining/ /pipelines/component/src/InterfaceTraining/
COPY ./utilities/ /pipelines/component/src/utilities/


FROM gcr.io/deeplearning-platform-release/pytorch-gpu.1-9 
COPY ./InterfaceTraining/requirements.latent_classification.txt .
RUN python3 -m pip install -U pip wheel cmake
RUN python3 -m pip install -r requirements.latent_classification.txt
COPY ./InterfaceTraining/ /pipelines/component/src/InterfaceTraining/
COPY ./utilities/ /pipelines/component/src/utilities/

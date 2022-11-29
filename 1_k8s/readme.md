# Basic k8s

I started using looking at kubeernetes. I started by installing kubeernetes on my local machine using minikube. This is a good way to get started with kubernetes. Here I tested some basic commands and I got a basic understanding of how kubernetes works. I used the code from this [tutorial](https://kubernetes.io/docs/tutorials/hello-minikube/).

Then I installed kubernetes on GCP. I followed the instructions from this [tutorial](https://cloud.google.com/kubernetes-engine/docs/quickstart). I created a cluster and I connected to it using kubectl. I added the different commands I used to create the cluster and connect to it in step folder.

## Installations Steps Local

1. Install kubectl
<https://kubernetes.io/docs/tasks/tools/install-kubectl/>

```bash
brew install kubectl
```

2. Install minikube

```bash
    brew install minikube
```

3. Start minikube

```bash
    minikube start
```

## Installations Steps GCP

1. Create a GCP account
First, you need to create a GCP account. You can do this by going to <https://cloud.google.com/> and clicking on the "Try for free" button. You will need to enter your credit card details, but you will not be charged anything unless you exceed the free tier limits.

2. Create a GCP project
Once you have created a GCP account, you need to create a project. You can do this by going to <https://console.cloud.google.com/project> create and entering a project name. You can also select a billing account if you have one. If you do not have a billing account, you can select "No billing account" and you will not be charged anything unless you exceed the free tier limits.

3. Install gcloud
You need to install gcloud and kubectl on your local machine. You can do this by following the instructions here: <https://cloud.google.com/sdk/docs/install>.

4. Run `./steps/1.1_enable_glcloud_apis.sh`
This script will enable the relevant gcloud apis for you.

5. Run `./steps/1.2_create_cluster.sh`
Run this script to create a cluster. You can change the cluster name and zone in the script.

6. Run `./steps/1.3_enable_glcloud_plugins.sh`
This script will enable gcloud plugins for you. This includes kubectl.

7. Run `./steps/1.4_auth_cluster.sh`
This script will authenticate your cluster

# How to set up a JupyterHub Cluster in Azure
This is a cliff notes version of https://zero-to-jupyterhub.readthedocs.io/en/latest/index.html
so please follow along there as well.

## Select proper subscription

```
az account list --refresh --output table
```

## Ensure multiple node pools is enabled
 See https://docs.microsoft.com/en-us/azure/aks/use-multiple-node-pools#before-you-begin
```
az feature register --name MultiAgentpoolPreview --namespace Microsoft.ContainerService
```

## Create Resource Group
you only need to do this once

```sh
az group create \
              --name=JupyterHub \
              --location=northcentralus \
              --output table
```

## Create Local Config for Cluster
you only need to do this once, but need to return to this directory to perform these operations below

```sh
mkdir JupyterHub
cd JupyterHub
```

## Generate SSL Key for Auth

```
ssh-keygen -f ssh-key-JupyterHub
```

## Create Static Ip
see https://docs.microsoft.com/en-us/azure/aks/static-ip

```sh

az network public-ip create \
    --resource-group MC_JupyterHub_JupyterHub_northcentralus \
    --name myAKSPublicIP \
    --allocation-method static
```
note id and ip, set up dns with this ip


## Create Cluster

```sh
az aks create --name JupyterHub \
              --resource-group JupyterHub \
              --ssh-key-value ssh-key-JupyterHub.pub \
              --node-count 3 \
              --node-vm-size Standard_D2s_v3 \
              --enable-vmss \
              --enable-cluster-autoscaler \
              --min-count 3 \
              --max-count 6 \
              --kubernetes-version 1.14.8 \
              --load-balancer-outbound-ips <ip id from above>\
              --output table
              
```
wait...

## Get Credentials
```sh
az aks get-credentials \
             --name JupyterHub \
             --resource-group JupyterHub \
             --output table
```

## Check Cluster Node status

```sh
kubectl get node
```
wait for hub and proxy nodes to be ready

## Create tiller service account
note that helm comes pre-installed in azure cloud shell
from https://docs.microsoft.com/en-us/azure/aks/kubernetes-helm
```sh
kubectl apply -f helm-rbac.yaml

helm init --service-account tiller --wait
```
if all went well, this will remport back like so:
```sh
$ helm version
Client: &version.Version{SemVer:"v2.15.2", GitCommit:"8dce272473e5f2a7bf58ce79bb5c3691db54c96b", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.15.2", GitCommit:"8dce272473e5f2a7bf58ce79bb5c3691db54c96b", GitTreeState:"clean"}
```
## Add Helm Charts
```sh
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update
```


### TODO apply ssl security to tiller

this one didn't work

```sh
helm install jupyterhub/jupyterhub \
  --namespace jhub \
  --set controller.nodeSelector."beta\.kubernetes\.io/os"=linux \
  --set defaultBackend.nodeSelector."beta\.kubernetes\.io/os"=linux \
  --values config.yaml \
  --timeout=1800
```
wait... this might timeout

check status
```sh
kubectl get pod --namespace jhub
```

## get public ip

```sh
kubectl get service
```

# Troubleshooting

## if a pod fails
debug the pod
```sh
kubectl describe pod --namespace jhub <podname>
```

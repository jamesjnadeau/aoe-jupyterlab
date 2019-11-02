## Ensure multiple node pools is enabled
 See https://docs.microsoft.com/en-us/azure/aks/use-multiple-node-pools#before-you-begin
```
az feature register --name MultiAgentpoolPreview --namespace Microsoft.ContainerService
```

## Create Resource Group

```sh
az group create \
              --name=JupyterHub \
              --location=northcentralus \
              --output table
```

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
              --output table
```

## Get Credentials
```sh
az aks get-credentials \
             --name JupyterHub \
             --resource-group JupyterHub> \
             --output table
```

# Create tiller service account
from https://docs.microsoft.com/en-us/azure/aks/kubernetes-helm
```sh
kubectl apply -f helm-rbac.yaml
```

this one didn't work
```sh
helm upgrade --install jhub jupyterhub/jupyterhub \
  --namespace jhub  \
  --version=1.0.0 \
  --values config.yaml
```

```sh
helm install jupyterhub/jupyterhub \
    --set controller.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set defaultBackend.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --values config.yaml
```

## get public ip

```sh
kubectl get service
```


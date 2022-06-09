# create-cronjob
#### Python client for the kubernetes API

we can use the client module to interact with the resources. 

`CreateResources:` kubectl get commands are used to create all kinds of resources using yaml files in a cluster for eg:

To create the cronjobs in the cluster, we fire following kubectl command:

```kubectl apply -f cronjob.yaml``` 

In Python, we instantiate BatchV1beta1Api class from client module:

`client_api = client.BatchV1beta1Api()`

Here I've created the client with it's respective class BatchV1beta1Api
and storing in a var named as client_api. so furture we can use it.

`KubeConfig:` to pass the on local cluster e.g minikube we use bellowcommand: 

`config. load_kube_config()`

#### Authenticating to the Kubernetes API server

But what if you want to list all the automated cronjobs of a GKE Cluster, you must need to authenticate the configuration

`configuration.api_key = {"authorization": "Bearer" + bearer_token}` 

I've used Bearer Token which enable requests to authenticate using an access key.

#### Create the cronjobs in default namespaces:

call the funcation create_cron_job(batch_v1,cluster_details,"default") 

And run following command:

`python3 create-cronjob.py`

#### create the cronjobs in specific namespace:

call the funcation create_cron_job(batch_v1,cluster_details,"namespace-name") 

`python3 create-cronjob.py`


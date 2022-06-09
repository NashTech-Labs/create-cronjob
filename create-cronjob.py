from time import sleep

import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config


JOB_NAME = "pi"

def __get_kubernetes_client(bearer_token,api_server_endpoint):
    try:
        configuration = kubernetes.client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
            api_instance1 = kubernetes.client.BatchV1beta1Api(api_client)
        return api_instance1
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def create_cron_job(api_instance,cluster_details,namespace):
    container = client.V1Container(
    name="pi",
    image="perl",
    command=["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"])
    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "pi"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)  #specify the number of retries before considering a Job as failed
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=JOB_NAME),
        spec=spec)


    client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )

    api_response = client_api.create_namespaced_cron_job(
        body=client.V1beta1CronJob(
            api_version='batch/v1beta1',
            kind='CronJob',
            metadata=client.V1ObjectMeta(name='cronjob8'),
            spec = client.V1CronJobSpec(

                schedule="25 17 8 6 2", #     25(minute)   5(pm)   8(date)   june(month) tuesday(day of the week)
                job_template=job
            )
            
        ),
        namespace=namespace)
    print("cronJob created. status='%s'" % str(api_response.status))
    
   


if __name__ == '__main__':
    batch_v1 = client.BatchV1Api()
    cluster_details={
        "bearer_token":"GKE-Bearer-Token",
        "api_server_endpoint":"ip-k8s-control-plane"
    }

    create_cron_job(batch_v1,cluster_details,"default") #pass any namespace instead of default
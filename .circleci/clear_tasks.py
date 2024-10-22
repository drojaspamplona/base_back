import os
import sys
import boto3


def clear(args):
    cluster_name = os.getenv('CLUSTER_NAME')
    service_name = f"base-back-{args[0]}"
    ecs_client = boto3.client('ecs', region_name='us-east-1')

    response = ecs_client.list_tasks(
        cluster=cluster_name,
        serviceName=service_name,
        desiredStatus='RUNNING'
    )

    task_arns = response['taskArns']
    for task_arn in task_arns:
        ecs_client.stop_task(
            cluster=cluster_name,
            task=task_arn
        )


if __name__ == '__main__':
    clear(sys.argv[1:])

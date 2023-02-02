import logging

import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)


# ValidationCheck
def validation_check(event):

    logger.info('######### Start Validation Check #########')

    check_list = [
        'Cluster',
        'Service',
        'DesiredCount',
        'MinCapacity',
        'MaxCapacity'
        ]

    for targets in event:

        # キー名確認
        for target_key in targets.keys():

            if target_key not in check_list:
                logger.error(f'キー名:{target_key}は不正な値です。')
                return 1

        # 数値確認
        desire_count = targets['DesiredCount']
        min_capacity = targets['MinCapacity']
        max_capacity = targets['MaxCapacity']

        if not isinstance(desire_count, int) and isinstance(min_capacity, int) and isinstance(max_capacity, int):
            logger.error(f'各ECSタスク値に整数以外が入力されています。タスク最大数:{max_capacity}, タスク希望数:{desire_count}, タスク最少数:{min_capacity}')
            return 1

        if not min_capacity <= desire_count <= max_capacity:
            logger.error(f'各ECSタスク値の大小関係が不正です。タスク最大数:{max_capacity}, タスク希望数:{desire_count}, タスク最少数:{min_capacity}')
            return 1

    logger.info('######### End Validation Check #########')
    return 0


# UpdateEcsService
def update_ecs_service(event):

    logger.info('######### Start Update ECS Service #########')

    for targets in event:

        cluster_name = targets['Cluster'][0]
        desired_count = targets['DesiredCount']
        min_capacity = targets['MinCapacity']
        max_capacity = targets['MaxCapacity']
        service_list = targets['Service']

        application_autoscaling_client = boto3.client('application-autoscaling')
        ecs_client = boto3.client('ecs')

        for service_name in service_list:

            logger.info(f'######### Start Update Cluster: {cluster_name}, Service: {service_name} #########')

            try:
                application_autoscaling_client.register_scalable_target(
                    ServiceNamespace = 'ecs',
                    ResourceId = 'service/' + str(cluster_name) + '/' + str(service_name),
                    ScalableDimension = 'ecs:service:DesiredCount',
                    MinCapacity = int(min_capacity),
                    MaxCapacity = int(max_capacity)
                )

                ecs_client.update_service(
                    cluster = str(cluster_name),
                    service = str(service_name),
                    desiredCount = int(desired_count)
                )

                logger.info(f'Success Update Cluster: {cluster_name}, Service: {service_name} #########')

            except Exception as error:
                logger.error(f'Faild Update Cluster: {cluster_name}, Service: {service_name} #########')
                logger.error(f'Error Message: {error}')


def lambda_handler(event, context):

    logger.info('######### Start Lambda Function #########')

    # ValidationCheck
    result_validation = validation_check(event)

    if not result_validation == 0:
        return 1

    # UpdateEcsService
    update_ecs_service(event)

    logger.info('######### End Lambda Function #########')

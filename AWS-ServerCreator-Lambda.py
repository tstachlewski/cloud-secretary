import json
import boto3
import io
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

types = {
    'nano':'t3.nano',
    'small':'t3.small',
    'medium':'t3.medium',
    'big':'t3.large'
}

def lambda_handler(event, context):

    serverSize = event["queryStringParameters"]["server_size"]
    serverName = event["queryStringParameters"]["server_name"]
    serverType = types[serverSize]
    
    logger.info('Serwer size: %s', serverSize);
    logger.info('Serwer name: %s', serverName);
    logger.info('Serwer type: %s', serverType);

    #Creating server
    ec2 = boto3.client('ec2')
    res = ec2.run_instances(
        ImageId = "ami-08e70de73790e0976",
        InstanceType = serverType,
        MinCount = 1,
        MaxCount = 1,
        TagSpecifications=[ { 'ResourceType': 'instance', 'Tags': [ { 'Key': 'Name', 'Value': serverName }, ] }, ],
    )
            
    return {
        'statusCode': 200,
        'body': json.dumps('SERVER CREATED')
    }

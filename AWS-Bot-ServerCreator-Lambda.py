import json
import boto3
import io
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

types = {
    'nano':'t3.nano',
    'mały':'t3.small',
    'średni':'t3.medium',
    'duży':'t3.large'
}


def lambda_handler(event, context):


    print(event);

    intentName= slots = event["sessionState"]["intent"]["name"]

    if "TworzycielSerwerow" == intentName:
        #Retrieving input parameters
        slots = event["sessionState"]["intent"]["slots"]


        serverSize = slots["wielkosc_serwera"]["value"]["interpretedValue"].lower()
        serverName = slots["nazwa_serwera"]["value"]["interpretedValue"].lower()
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

        if "dzwonionyNumer" in event["sessionState"]["sessionAttributes"]:
            phoneNumber = event["sessionState"]["sessionAttributes"]["dzwonionyNumer"]
            logger.info('Phone Number: %s', phoneNumber);
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table("serwery")
            table.put_item(
                Item={
                    'instanceId' : res["Instances"][0]["InstanceId"],
                    'size' : serverSize,
                    'name' : serverName,
                    'type' : serverType,
                    'phoneNumber' : phoneNumber
                }
            )
        
        #Preparing response
        response = {}
        response["sessionState"] = event["sessionState"]
        response["sessionState"]["intent"]["state"] = "Fulfilled";
        response["sessionState"]["dialogAction"] = {}
        response["sessionState"]["dialogAction"]["type"] = "Close"

        return response

    return null
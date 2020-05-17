import boto3
import logging
import time
from util import *

def extract_entities_from_message(message):
    client = boto3.client(service_name='comprehendmedical',
                          aws_access_key_id="AKIA3FFYAI3OQYG54NGJ",
                          aws_secret_access_key="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",
                          region_name="us-east-1")

    return client.detect_phi(Text=message)

def main(event):
    startTime = 1000*time.time()
    externalServicesTime = 0
    try:
        # Extract the message from the event
        message = event['body']['message']
        # Extract all entities from the message
        tickTime = 1000*time.time()
        entities_response = extract_entities_from_message(message)
        externalServicesTime += 1000*time.time() - tickTime
        entity_list = entities_response['Entities']
        event['body']['entities'] = entity_list
        endTime = 1000*time.time()
        return timestamp(event, event, startTime, endTime, externalServicesTime)
    except Exception as e:
        logging.error('Exception: %s. Unable to extract PII entities from message' % e)
        raise e

import boto3
import logging
import time

def extract_entities_from_message(message):
    client = boto3.client(service_name='comprehendmedical',
                          aws_access_key_id="AKIA3FFYAI3ORS6ANNHL",
                          aws_secret_access_key="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",
                          region_name="us-east-1")

    return client.detect_phi(Text=message)

def main(event):
    print("Start Time: ", str(1000*time.time()))
    print ('Received message payload. Will extract PII')
    try:
        # Extract the message from the event
        message = event['body']['message']
        # Extract all entities from the message
        entities_response = extract_entities_from_message(message)
        entity_list = entities_response['Entities']
        event['body']['entities'] = entity_list
        print ('PII entity extraction completed')
        # return entity_list
        print("End Time: ", str(1000*time.time()))
        return event
    except Exception as e:
        logging.error('Exception: %s. Unable to extract PII entities from message' % e)
        raise e

import json
import hashlib
import base64
import logging
import uuid
import time

def hash_message(message, entity_map):
    hashed_message = hashlib.sha256(message.encode()).hexdigest()
    return hashed_message

def deidentify_entities_in_message(message, entity_list):
    entity_map = dict()
    for entity in entity_list:
      salted_entity = entity['Text'] + str(uuid.uuid4())
      hashkey = hashlib.sha256(salted_entity.encode()).hexdigest()
      entity_map[hashkey] = entity['Text']
      message = message.replace(entity['Text'], hashkey)
    return message, entity_map

def main(event):
    print("Start Time: ", str(1000*time.time()))
    print('Received message payload')
    try:
        # Extract the entities and message from the event
        message = event['body']['message']
        entity_list = event['body']['entities']
        # Mask entities
        deidentified_message, entity_map = deidentify_entities_in_message(message, entity_list)
        hashed_message = hash_message(deidentified_message, entity_map)
        body = {"deid_message": deidentified_message,"hashed_message": hashed_message}
        response = {'statusCode':200, 'body':body}
        print("End Time: ", str(1000*time.time()))
        return response
    except Exception as e:
      logging.error('Exception: %s. Unable to extract entities from message' % e)
      raise e

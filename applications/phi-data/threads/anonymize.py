import time
import logging
import json
from util import *

def mask_entities_in_message(message, entity_list):
  for entity in entity_list:
      message = message.replace(entity['Text'], '#' * len(entity['Text']))
  return message

def main(event):
  startTime = 1000*time.time()
  externalServicesTime = 0
  try:
      # Extract the entities and message from the event
      message = event['body']['message']
      entity_list = event['body']['entities']
      # Mask entities
      masked_message = mask_entities_in_message(message, entity_list)
      response = {'statusCode':200, 'body':{'message': masked_message}}
      endTime = 1000*time.time()
      return timestamp(response, event, startTime, endTime, externalServicesTime)
  except Exception as e:
      logging.error('Exception: %s. Unable to extract entities from message' % e)
      raise e

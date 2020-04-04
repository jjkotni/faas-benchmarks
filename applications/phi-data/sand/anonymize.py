import logging
import json
import time

def mask_entities_in_message(message, entity_list):
  for entity in entity_list:
      message = message.replace(entity['Text'], '#' * len(entity['Text']))
  return message

def handle(event, context):
  startTime = 1000*time.time()
  print('Received message payload ', str(event))
  try:
      # Extract the entities and message from the event
      message = event['body']['message']
      entity_list = event['body']['entities']
      # Mask entities
      masked_message = mask_entities_in_message(message, entity_list)
      response = {'statusCode':200, 'body':{'message': masked_message}}
      priorWorkflowDuration = event['duration'] if 'duration' in event else 0
      #Obscure code, doing this to time.time() as late in the function as possible for end time
      workflowStartTime = float(context.get('workflowStartTime', True))
      endTime = 1000*time.time()
      response['duration']     = priorWorkflowDuration + endTime - startTime
      response['totalRunTime'] = endTime - workflowStartTime
      return response
  except Exception as e:
      logging.error('Exception: %s. Unable to extract entities from message' % e)
      raise e

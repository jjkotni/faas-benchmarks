import logging

def mask_entities_in_message(message, entity_list):
  for entity in entity_list:
      message = message.replace(entity['Text'], '#' * len(entity['Text']))
  return message

def main(event):
  print('Received message payload')
  try:
      # Extract the entities and message from the event
      message = event['body']['message']
      entity_list = event['body']['entities']
      # Mask entities
      masked_message = mask_entities_in_message(message, entity_list)
      return masked_message
  except Exception as e:
      logging.error('Exception: %s. Unable to extract entities from message' % e)
      raise e
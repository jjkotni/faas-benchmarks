import logging
import json

def mask_entities_in_message(message, entity_list):
  for entity in entity_list:
      message = message.replace(entity['Text'], '#' * len(entity['Text']))
  return message

def main(event):
  print('Received message payload ', str(event))
  try:
      # Extract the entities and message from the event
      message = event['body']['message']
      entity_list = event['body']['entities']
      # Mask entities
      masked_message = mask_entities_in_message(message, entity_list)
      response = {'statusCode':200, 'body':{'message': masked_message}}
      return response
  except Exception as e:
      logging.error('Exception: %s. Unable to extract entities from message' % e)
      raise e
# if __name__=="__main__":
#     print(main({'body': {'entities': [{'Id': 0, 'Traits': [], 'Score': 0.9997479319572449, 'BeginOffset': 6, 'Category': 'PROTECTED_HEALTH_INFORMATION', 'Type': 'AGE', 'Text': '87', 'EndOffset': 8}, {'Id': 1, 'Traits': [], 'Score': 0.19382844865322113, 'BeginOffset': 19, 'Category': 'PROTECTED_HEALTH_INFORMATION', 'Type': 'PROFESSION', 'Text': 'highschool teacher', 'EndOffset': 37}, {'Id': 2, 'Traits': [], 'Score': 0.9997519850730896, 'BeginOffset': 121, 'Category': 'PROTECTED_HEALTH_INFORMATION', 'Type': 'DATE', 'Text': 'April 2019', 'EndOffset': 131}], 'usage': 'anonymize', 'message': 'Pt is 87 yo woman, highschool teacher with past medical history that includes - status post cardiac catheterization in April 2019.She presents today with palpitations and chest pressure.HPI : Sleeping trouble on present dosage of Clonidine. Severe Rash  on face and leg, slightly itchy  Meds : Vyvanse 50 mgs po at breakfast daily, Clonidine 0.2 mgs -- 1 and 1 / 2 tabs po qhs HEENT : Boggy inferior turbinates, No oropharyngeal lesion Lungs : clear Heart : Regular rhythm Skin :  Mild erythematous eruption to hairline Follow-up as scheduled'}}))

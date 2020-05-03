from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
from time import time
from multiprocessing import Process


def get_producer ():
    return KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:dumps(x).encode('utf-8'))


def get_consumer (topic):
    return KafkaConsumer(topic,
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='latest',
                         enable_auto_commit=True,
                         value_deserializer=lambda x: loads(x.decode('utf-8')))


def timestamp (output, input, start, end):
    begin = 1000 * time ()
    prior = input.get ('duration', 0.0)
    output['duration'] = prior + end - start
    output['workflowEndTime'] = end
    output['workflowStartTime'] = input.get ('workflowStartTime', start)
    prior_cost = input.get ('timeStampCost', 0.0)
    output['timeStampCost'] = prior_cost - (begin - 1000 * time())
    return output


def send (out_topic, message):
    producer = get_producer ()
    producer.send (out_topic, message)
    producer.flush ()


def receive (function, consumer):
    for message in consumer:
        proc = Process(target=function, args=(message.value,[]))
        proc.start()
        proc.join()
        # These are 1 off messages, wait till 1 message and return?
        return


def forward (function, consumer, out_topics):
    for message in consumer:
        proc = Process(target=function, args=(message.value, out_topics))
        proc.start()
        proc.join()
        # These are 1 off messages, wait till 1 message and return?
        return

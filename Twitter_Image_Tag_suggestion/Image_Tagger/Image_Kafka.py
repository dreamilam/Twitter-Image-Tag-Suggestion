# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from pykafka import KafkaClient
import json
import urllib


client = KafkaClient()
topic = client.topics[b'test']
consumer = topic.get_simple_consumer()


image_client = KafkaClient("localhost:9092")
image_topic = image_client.topics[b'test_image'] #b for byte stream
image_producer = image_topic.get_producer()

for msg in consumer:
    
    data = json.loads(msg.value)
    if 'entities' in data:
        if 'media' in data['entities']:
            if data['entities']['media'][0]['type'] == "photo" and len(data['entities']['hashtags'])>0:
                message = json.dumps({'hash':data['entities']['hashtags'],'img_url':data['entities']['media'][0]['media_url'].encode('utf-8')})
                #image_producer.produce(msg.value.encode('utf-8'))
                print message
                image_producer.produce(message)
                

# -*- coding: utf-8 -*-

from pykafka import KafkaClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
import sys

# read from the file
def read_from_file_key(filepath):
    keys = list()
    f = open(filepath,"r")
    for line in f:
        line = line.strip()
        keys.append(line.strip())
    return keys

class StdOutListener(StreamListener):
    def __init__(self):
        self.counter = 0
        self.time_start = time.time()

    def on_data(self, data):
        sys.stdout.write("\r Time_elapsed: {:.2f} Tweets Read : {} Rate of encounter: {:.2f} images/sec".format(time.time()- self.time_start,self.counter,(self.counter)/((time.time()-self.time_start)*60)))
        sys.stdout.flush()
        self.counter +=1
        producer.produce(data.encode('utf-8'))
        return True
    
    def on_error(self, status):
        print (status)
        return True

if __name__ == '__main__':
    keys = read_from_file_key("keys.txt")
    consumer_key = keys[0]
    consumer_secret = keys[1]
    access_token = keys[2]
    access_token_secret = keys[3]

    client = KafkaClient("localhost:9092")
    topic = client.topics[b'test'] #b for byte stream
    producer = topic.get_producer()
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track="trump")
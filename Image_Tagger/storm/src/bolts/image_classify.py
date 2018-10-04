import os
from collections import Counter

from streamparse import Bolt
from classify import Classifier
import json
import urllib
import datetime

class TagCountBolt(Bolt):
    outputs = ['cls','tag']

    def initialize(self, conf, ctx):
        self.counter = 0
        self.pid = os.getpid()
        self.total = 0
        self.classifier = Classifier()
        self.directory = str(os.getcwd())+"/Tweet_Images"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
    def _increment(self, word, inc_by):
        self.counter[word] += inc_by
        self.total += inc_by

    def process(self, tup):
        data = json.loads(tup.values[0].encode('utf-8'))
    
        if 'img_url' in data:        
                path = "{}/{}.jpg".format(self.directory,self.counter)
                try:
                    urllib.urlretrieve(data['img_url'],path)
                    self.counter = self.counter+1
                    self.classifier.load_image(path)
                    predicted_class = self.classifier.classify()
                    #self.logger.info("\n [INFO_BOLT_PREDICTION] : "+ " ".join(predicted_class))
                    if len(data['hash'])>0:
                        tags = [str(li['text']) for li in data['hash'] if li['text'][0:1]!="\\"]
                        #self.logger.info("\n [INFO_BOLT_TAGS] : "+ " ".join(tags))
                        
                        #now = datetime.datetime.now()
                        for cls in predicted_class:
                            if len(tags)>0:
                                for tag in tags:
                                    self.emit([cls,tag])        
                                    #self.logger.info("{0}/{1}".format(cls,tag))
                        
                    os.remove(path)
                    
                except (KeyboardInterrupt,Exception):
                    print(Exception)
        
        else:
            self.logger.info("NO IMG URL!!!")
            #self.logger.info(json.dumps(data))

        if self.counter % 10 == 0:
            self.logger.info("Processed [{:,}] tweets".format(self.counter))

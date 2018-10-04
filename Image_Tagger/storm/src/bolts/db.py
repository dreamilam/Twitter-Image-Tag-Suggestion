from collections import Counter
from cassandra.cluster import Cluster

from streamparse import Bolt
import datetime

class WriteToDbBolt(Bolt):
    # outputs = ['class','tag','count','minute']

    def initialize(self, conf, ctx):
        self.counter = 0
        self.cluster = Cluster(["54.186.242.133","54.186.17.97"])
        self.session = self.cluster.connect()
        self.session.execute("CREATE KEYSPACE IF NOT EXISTS ImageTagger WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 };")
        self.session.execute("USE ImageTagger;")
        self.session.execute("CREATE TABLE IF NOT EXISTS TagCounts(id int PRIMARY KEY, class text, tag text);")

    # def _increment(self, word, inc_by):
    #     #self.counter[word] += inc_by
    #     self.total += inc_by

    def process(self, tup):
        data = tup.values

        query = "select id, count from Popular_Tags where class = '"+str(data[0])+"' and tag = '"+str(data[1])+"' ALLOW FILTERING"
        item = self.session.execute(query)
        if item.one()!=None:
            id_from_db = item[0][0]
            count_from_db = item[0][1]
            updated_count = count_from_db + 1
            query = "update Popular_Tags SET count = {} where id = {} ;".format(updated_count, id_from_db)
            self.session.execute(query)
        else:
            query = "insert into Popular_Tags (id, class, tag, count) values (uuid(), \'{}\', \'{}\', {})".format(data[0], data[1], 1)
            self.session.execute(query)
            updated_count = 1

        #self.logger.info("----UPDATED VALUE-----{}-{}={}".format(data[0],data[1],updated_count))
        self.counter+=1
        if self.counter % 10 == 0:
            self.logger.info("Processed [{:,}] tweets".format(self.counter))

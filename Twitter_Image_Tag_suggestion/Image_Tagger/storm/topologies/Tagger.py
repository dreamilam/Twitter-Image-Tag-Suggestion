"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.image_classify import TagCountBolt
from spouts.image_stream import TweetSpout
from bolts.db import WriteToDbBolt

class Tagger(Topology):
    tweet_spout = TweetSpout.spec()
    count_bolt = TagCountBolt.spec(inputs=[tweet_spout],par=2)
    cassandra_bolt = WriteToDbBolt.spec(inputs={count_bolt: Grouping.fields(['cls','tag'])},par=2) #SaveCountBolt.spec(inputs=[count_bolt],par=2)

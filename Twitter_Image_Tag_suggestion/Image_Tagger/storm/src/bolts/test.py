# -*- coding: utf-8 -*-

from classify import Classifier
import urllib

clf = Classifier()
clf.load_image("/home/hari/Documents/Big_data/bits-please/car.jpg")
predicted_class = clf.classify()
print (" ".join(predicted_class))

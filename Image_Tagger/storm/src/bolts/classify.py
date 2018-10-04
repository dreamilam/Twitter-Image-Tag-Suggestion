# -*- coding: utf-8 -*-
from keras.preprocessing import image as image_utils
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.vgg16 import VGG16
import numpy as np

class Classifier():
	def __init__(self):
		self.model = VGG16(weights="imagenet")

	def load_image(self,path):
		img = image_utils.load_img(path, target_size=(224, 224))
		img_arr = image_utils.img_to_array(img)
		img_arr = np.expand_dims(img_arr, axis=0)
		self.image = preprocess_input(img_arr)

	def classify(self):
		preds = self.model.predict(self.image)
		preds = decode_predictions(preds)
		return [x[1] for x in preds[0]]



#clf = Classifier()
#clf.load_image("car.jpg")
#print(clf.classify())

# P = decode_predictions(preds)
# (imagenetID, label, prob) = P[0][0]


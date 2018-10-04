from app import app

from flask import render_template
from flask import request,Response,redirect, url_for,jsonify , stream_with_context
import os
import time
import numpy as np
from cassandra.cluster import Cluster
import datetime
from keras.preprocessing import image as image_utils
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.vgg16 import VGG16

cluster = Cluster(["54.186.242.133","54.186.17.97"])
session = cluster.connect("tweet")
#session.set_keyspace("kong")

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_filer():
    if request.method == 'POST':
           file = request.files['image']
           UPLOAD_FOLDER = os.path.basename('uploads')
           # if UPLOAD_FOLDER not exist
           f = os.path.join(UPLOAD_FOLDER, file.filename)

           file.save(f)
           model = VGG16(weights="imagenet")
           img = image_utils.load_img(f, target_size=(224, 224))
           img_arr = image_utils.img_to_array(img)
           img_arr = np.expand_dims(img_arr, axis=0)
           image = preprocess_input(img_arr)
           preds = model.predict(image)
           preds = decode_predictions(preds)
           preds= [x[1] for x in preds[0]]
           # classifier = Classifier()
           # classifier.load_image(f)
           # preds = classifier.classify()
           print(preds)
           tagz=[]
           for x in preds:
               query = "select tag, count from Popular_Tags where class = '"+str(x)+"' ALLOW FILTERING;"
               items = session.execute(query)
               maxy=0
               for item in items:
                   if item[1]>=maxy:
                       tagg = item[0]
                       maxy = item[1]
               print(maxy)
               tagz.append(tagg)
           # flash("saved")
           print(tagz)
           tagz=list(set(tagz))
           tagzz = [{'name':"#"+tag} for tag in tagz]

           trend_tags = list()
           curr_hour = datetime.datetime.now().hour
           prev_hour= curr_hour -1
           for x in preds:
               query = "select tag,count from Trend where class='"+str(x)+"' and hour="+str(prev_hour)+" ALLOW FILTERING;"
               items = session.execute(query)
               maxy=0
               for item in items:
                   if item[1]>=maxy:
                       tagg = item[0]
                       maxy = item[1]
               print(maxy)
               trend_tags.append(tagg)
           print("trend_tags : ", trend_tags)
           trend_tags=list(set(trend_tags))
           trend = [{'name':"#"+tag} for tag in trend_tags]
           os.remove(f)
           return render_template("tags.html",tags = tagzz,trend_one=trend)

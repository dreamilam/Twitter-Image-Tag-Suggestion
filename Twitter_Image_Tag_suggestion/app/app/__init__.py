from flask import Flask

app = Flask(__name__)
app.config.from_object("config")  # Reads config.py contents and stores them into app.config

from app import views

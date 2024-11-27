from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"
from flask import Flask, render_template
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

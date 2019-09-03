from flask import Flask, request
from data_manager import DataManager
from learner import Leaner

app = Flask(__name__)

NUM_Category = 16
datamanaget = DataManager(NUM_Category)
learner = Leaner(NUM_Category)

@app.route('/get_log')
def get_log():
    data = [request.form['1st'],
            request.form['2nd'],
            request.form['3rd'],
            request.form['4th'],
            request.form['5th'],
            request.form['6th'],
            request.form['sex'],
            request.form['grade']]
    pred_data = datamanaget.build_preddata(data)
    train_data = datamanaget.build_learndata(data)
    return

def recommandation(data):
    return learner.predict(data)[0]


def fit(data):
    learner.fit(data)
    return

def save_data():
    return

def load_data():
    return
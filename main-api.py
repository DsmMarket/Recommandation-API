from flask import Flask, request
from data_manager import DataManager
from learner import Leaner
import pandas as pd

app = Flask(__name__)

NUM_Category = 16

@app.route('/get_log', methods=['GET', 'POST'])
def get_log():
    datamanager = DataManager(NUM_Category)
    learner = Leaner(NUM_Category)

    data = [[request.args.get('1st', type=int),
            request.args.get('2nd', type=int),
            request.args.get('3rd', type=int),
            request.args.get('4th', type=int),
            request.args.get('5th', type=int),
            request.args.get('6th', type=int),
            request.args.get('sex', type=int),
            request.args.get('grade', type=int)]]

    train_data, pred_data = datamanager.merge_data(data)
    save_data(data)
    recommand_list = learner.predict(pred_data)
    return str(recommand_list)

def save_data(data):
    try:
        data_pd = pd.DataFrame(data)
        data_pd.to_csv("data.csv", mode='a', header=False)
        return True
    except:
        return False

app.run()
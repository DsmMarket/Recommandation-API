from flask import Flask, request
from data_manager import DataManager
from learner import Leaner
import json
from collections import OrderedDict

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
    save_data(train_data)
    # learner.fit(data=train_data, num_epoches=1000, num_batches=10)
    recommand_list = learner.predict(pred_data)
    return str(recommand_list)

def save_data(data):
    return

app.run()
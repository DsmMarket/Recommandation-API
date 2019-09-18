from flask import Flask, request, make_response
from data_manager import DataManager
from learner import Leaner
import pandas as pd
import json
from collections import OrderedDict

app = Flask(__name__)

NUM_Category = 16

@app.route('/get_log', methods=['GET'])
def get_log():
    datamanager = DataManager(NUM_Category)
    learner = Leaner(NUM_Category)
	category = request.args.get('category', type=list)
	sex = request.args.get('sex', type = int)
	grade = request.args.get('grade', type = int)

    data = [category + sex + grade]

    train_data, pred_data = datamanager.merge_data(data)
    save_data(data)
    recommand_list = learner.predict(pred_data)
    data = OrderedDict()
    data["reclist"] = list(map(str, [recommand_list[0][0], recommand_list[1][0], recommand_list[2][0]]))
    return make_response(json.dumps(data, ensure_ascii=False, indent='\t'))

def save_data(data):
    try:
        data_pd = pd.DataFrame(data)
        data_pd.to_csv("data.csv", mode='a', header=False)
    except: pass

app.run()

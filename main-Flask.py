from flask import Flask, request, make_response
from data_manager import DataManager
from learner import Leaner
from json import dumps
import pandas as pd

app = Flask(__name__)

NUM_Category = 16

@app.route('/get_log', methods=['GET'])
def get_log():
    datamanager = DataManager(NUM_Category)
    learner = Leaner(NUM_Category)

    categories = request.args.get('categories', type=str)[1:-1].split(', ')
    sex = request.args.get('sex', type=int)
    grade = request.args.get('grade', type=int)
    data = [categories + [sex, grade]]

    train_data, pred_data = datamanager.merge_data(data)
    save_data(data)
    recommend_list = list(map(str, sum(learner.predict(pred_data), [])))
    print(recommend_list)
    return make_response(dumps(recommend_list))

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Exception: %s', (e))
    return 'Exception: ' + str(e)

def save_data(data):
    try:
        data_pd = pd.DataFrame(data)
        data_pd.to_csv("data.csv", mode='a', header=False)
    except: pass

app.run()
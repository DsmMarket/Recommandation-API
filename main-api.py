from flask import Flask, redirect, url_for
from data_manager import DataManager
from learner import Leaner

app = Flask(__name__)
datamanager = DataManager()
learner = Leaner()

# category number
NUM_ACTIONS = 2

# data form
# 카테고리 코드가 1, 7, 3, 4 라고 할때
# data = '1, 7, 3, 5'
@app.route('/learning/<data>')
def learning(data):
    data = datamanager.learndata(data)
    check = learner.learn(data)
    return data
# return form
# 1 mean success, 0 mean failed

# data form
# 카테고리 코드가 7이라 할 때
# data = '1'
@app.route('/recommand/<data>')
def recommand(data):
    return data
# return form
# 카테고리 코드가 1, 3, 4라고 할 때
# data = '1, 3, 4'

# data form
# 1 mean click, 0 mean non-click
@app.route('/prob/<check>')
def involve(check):
    return check
# return form
# 1 mean success, 0 mean failed
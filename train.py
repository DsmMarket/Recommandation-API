import csv
from data_manager import DataManager
from learner import Leaner

NUM_category = 16

learner = Leaner(NUM_category)
datamanager = DataManager(NUM_category)

with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

train_data = []
for i in data:
    train_data.append(i[1:])

learner.fit(datamanager.build_learndata(train_data), epochs= 1000, batch_size = 10)

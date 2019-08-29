import numpy as np

class DataManager:
    def __init__(self):
        return

    def learndata(self, data):
        x = []
        y = []
        for i in data:
            x.append(i[:3])
            y.append(i[3])
        data = [x, y]
        return data
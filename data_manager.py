import numpy as np
import pandas as pd

class DataManager:
    def __init__(self, NUM_Category = 0):
        self. NUM_Category = NUM_Category

    def build_learndata(self, data):
        if data is not None:
            data = pd.DataFrame(np.array(data))
            X = pd.concat([pd.DataFrame([]),
                           pd.concat([data[0],
                                      data[1],
                                      data[2],
                                      data[6],
                                      data[7]], axis=1)], axis=0)
            a = pd.concat([pd.DataFrame([]), data[3]], axis=0)
            b = pd.concat([pd.DataFrame([]), data[4]], axis=0)
            c = pd.concat([pd.DataFrame([]), data[5]], axis=0)

            X = X.values.tolist()
            a_target = self.build_ytrain(a.values.tolist())
            b_target = self.build_ytrain(b.values.tolist())
            c_target = self.build_ytrain(c.values.tolist())

            return [X, a_target, b_target, c_target]
        return False

    def toint(self, array):
        intarray = []
        for obj in array:
            intarray.append(list(map(int, obj)))
        return intarray

    def build_ytrain(self, ytrain):
        train_data = []
        for d in ytrain:
            temp = [0] * self.NUM_Category
            temp[int(d[0])] = 1
            train_data.append(temp)
        return train_data

    def build_preddata(self, data):
        data = pd.DataFrame(np.array(data))
        data = pd.concat([pd.DataFrame([]),
                          pd.concat([data[3],
                                     data[4],
                                     data[5],
                                     data[6],
                                     data[7]], axis=1)], axis=0)
        return data

    def merge_data(self, data):
        train_data = self.build_learndata(data)
        pred_data = self.build_preddata(data)
        return train_data, pred_data

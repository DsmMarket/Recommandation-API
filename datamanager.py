import numpy as np
import pandas as pd

class DataManager:
    def __init__(self, NUM_Category = 0):
        self. NUM_Category = NUM_Category

    def build_learndata(self, data):

        if data is not None:
            X, a_target, b_target, c_target = self.build(data = data)

            return X, a_target, b_target, c_target

    def build(self, data, X = [], a = [], b = [], c = []):
        data = pd.DataFrame(np.array(data))

        X = pd.concat([pd.DataFrame(X),
                       pd.concat([data[0], data[1], data[2]], axis=1),
                       pd.concat([data[0], data[1], data[3]], axis=1),
                       pd.concat([data[0], data[2], data[3]], axis=1)],
                      axis=0)
        a = pd.concat([pd.DataFrame(a), data[1], data[1], data[2]], axis=0)
        b = pd.concat([pd.DataFrame(b), data[2], data[3], data[3]], axis=0)
        c = pd.concat([pd.DataFrame(c), data[3], data[2], data[1]], axis=0)

        x = []
        for i in X.fillna(0.1).values.tolist():
            i.remove(0.1)
            x.append(i)
        a = a.values.tolist()
        b = b.values.tolist()
        c = c.values.tolist()
        return list(map(np.array, [x, a, b, c]))
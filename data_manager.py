import numpy as np
import pandas as pd

class DataManager:
    def __init__(self, NUM_Category = 0):
        self. NUM_Category = NUM_Category

    # example data = [[1, 14, 12, 7, 6, 5, 1, 2]]
    # 1, 14, 12번 카테고리 상품을 보고 난 뒤, 7, 6번 상품을 보고, 5번 상품을 보고 있는 경우.
    # 1은 남성을 의미, 2는 2학년을 의미.
    def build_learndata(self, data, X = [], a = [], b = [], c = []):
        if data is not None:
            data = pd.DataFrame(np.array(data))
            X = pd.concat([pd.DataFrame(X),
                           pd.concat([data[0], data[1], data[2], data[6], data[7]], axis=1)], axis=0)
            a = pd.concat([pd.DataFrame(a), data[3]], axis=0)
            b = pd.concat([pd.DataFrame(b), data[4]], axis=0)
            c = pd.concat([pd.DataFrame(c), data[5]], axis=0)

            X = X.values.tolist()
            a_target = self.build_ytrain(a.values.tolist())
            b_target = self.build_ytrain(b.values.tolist())
            c_target = self.build_ytrain(c.values.tolist())

            return X, a_target, b_target, c_target
        else:
            return False

    def toint(self, array):
        res = []
        for obj in array:
            res.append(list(map(int, obj)))
        return res

    def build_ytrain(self, ytrain):
        res = []
        for d in ytrain:
            temp = [0] * self.NUM_Category
            temp[int(d[0])] = 1
            res.append(temp)
        return res

    def build_preddata(self, data):
        if data is not None:
            data = pd.DataFrame(np.array(data))
            data = pd.concat([pd.DataFrame([]),
                           pd.concat([data[3], data[4], data[5], data[6], data[7]], axis=1)], axis=0)
            return data
        else:
            return


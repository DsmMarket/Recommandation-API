from network import Network
from data_manager import DataManager
import numpy as np

class Leaner:
    def __init__(self, NUM_Category, data):
        self.network = Network(NUM_Category = NUM_Category)
        self.DataManager = DataManager(NUM_Category = NUM_Category)
        self.data_train, self.data_a, self.data_b, self.data_c = self.DataManager.build_learndata(data)

    def fit(self, num_epoches = 1000, num_batches = 10):
        return self.network.fit(train = np.array(self.data_train), a_targets = np.array(self.data_a),
                                b_targets = np.array(self.data_b), c_targets = np.array(self.data_c),
                                num_epoches=num_epoches, num_batches = num_batches)

    def predict(self, pred_data):
        return self.network.predict(pred_data)



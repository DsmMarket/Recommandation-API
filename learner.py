from network import Network
from data_manager import DataManager
import numpy as np

class Leaner:
    def __init__(self, NUM_Category,
                 model_path='model.json', weight_path='weight.h5'):
        self.model_path = model_path
        self.weight_path = weight_path
        self.network = Network(NUM_Category = NUM_Category,
                               model_path = model_path,
                               weight_path = weight_path)
        self.DataManager = DataManager(NUM_Category = NUM_Category)

    def fit(self, data, num_epoches = 1000, num_batches = 10):
        self.data_train = data[0]
        self.data_a = data[1]
        self.data_b = data[2]
        self.data_c = data[3]
        self.network.fit(train = np.array(self.data_train),
                         a_targets = np.array(self.data_a),
                         b_targets = np.array(self.data_b),
                         c_targets = np.array(self.data_c),
                         num_epoches=num_epoches, num_batches = num_batches)
        self.savemodel()

    def predict(self, pred_data):
        return self.network.predict(pred_data)

    def savemodel(self):
        self.network.save_model(self.model_path, self.weight_path)



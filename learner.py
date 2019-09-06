from network import Network
from data_manager import DataManager
import numpy as np

class Leaner:
    def __init__(self, NUM_Category, model_path = 'model.h5'):
        self.network = Network(NUM_Category = NUM_Category, model_path=model_path)
        self.DataManager = DataManager(NUM_Category = NUM_Category)

    def fit(self, data, num_epoches = 1000, num_batches = 10, model_path = 'model.h5'):
        if data is not False:
            self.data_train, self.data_a, self.data_b, self.data_c = data[0], data[1], data[2], data[3]
            self.network.fit(train = np.array(self.data_train), a_targets = np.array(self.data_a),
                                    b_targets = np.array(self.data_b), c_targets = np.array(self.data_c),
                                    num_epoches=num_epoches, num_batches = num_batches)
            self.savemodel(model_path)
            return
        return False

    def predict(self, pred_data):
        if pred_data is not False:
            return self.network.predict(pred_data)
        return False

    def savemodel(self, model_path):
        model_path = model_path
        self.network.save_model(model_path)



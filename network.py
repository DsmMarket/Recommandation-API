from keras import layers
from keras.models import Model, model_from_json
from keras.losses import mean_squared_error
import numpy as np
import os
import json

class Network:

    def __init__(self, NUM_Category, model_path, weight_path):

        self.model = ''

        if os.path.exists(model_path) and os.path.exists(weight_path):
            self.load_model(model_path, weight_path)
        else:
            self.inputs = layers.Input(shape=(5,), name='input')
            x = layers.Dense(16, activation='relu', input_dim=5)(self.inputs)
            x = layers.Dropout(0.50)(x)
            x = layers.Dense(20, activation='relu')(x)
            x = layers.Dropout(0.50)(x)
            x = layers.Dense(20, activation='sigmoid')(x)
            x = layers.Dropout(0.50)(x)
            x = layers.Dense(20, activation='sigmoid')(x)
            x = layers.Dropout(0.50)(x)
            a_prediction = layers.Dense(NUM_Category, activation='softmax', name='a')(x)
            b_prediction = layers.Dense(NUM_Category, activation='softmax', name='b')(x)
            c_prediction = layers.Dense(NUM_Category, activation='softmax', name='c')(x)
            self.model = Model(self.inputs, [a_prediction, b_prediction, c_prediction])

        self.model.compile(optimizer='rmsprop',
                           loss={'a': mean_squared_error, 'b': mean_squared_error, 'c': mean_squared_error},
                           loss_weights={'a': 1., 'b': 1., 'c': 1.})

    def fit(self, train, a_targets, b_targets, c_targets, epochs, batch_size):
        self.model.fit(train, {'a': a_targets, 'b': b_targets, 'c': c_targets},
                        epochs=epochs, batch_size = batch_size)

    def predict(self, pred_data):
        self.pred = self.model.predict(np.array(pred_data))
        self.pred_a = list(map(np.argmax, self.pred[0]))
        self.pred_b = list(map(np.argmax, self.pred[1]))
        self.pred_c = list(map(np.argmax, self.pred[2]))
        return [self.pred_a, self.pred_b, self.pred_c]

    def save_model(self, model_path, weight_path):
        model_json = self.model.to_json()
        if model_path is not None and self.model is not None:
            with open(model_path, 'w' ) as json_file:
                json.dump(model_json, json_file, indent='\t')
            self.model.save_weights(weight_path)

    def load_model(self, model_path, weight_path):
        if model_path is not None and os.path.exists(model_path):
            with open(model_path, 'r') as f:
                model_json = json.load(f)
            self.model = model_from_json(model_json)
            try: self.model.load_weights(weight_path)
            except: pass
            print('model load complete')

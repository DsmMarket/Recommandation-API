from keras import layers
from keras.models import Model
from keras.losses import mean_squared_error
import numpy as np

class Network:

    def __init__(self, NUM_Category):
        self.inputs = layers.Input(shape=(5,), name='input')

        x = layers.Dense(16, activation='relu')(self.inputs)
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
                      loss_weights={'a': 0.25, 'b': 1., 'c': 10.})

    def fit(self, train, a_targets, b_targets, c_targets, num_epoches, num_batches):
        self.model.fit(train, {'a': a_targets, 'b': b_targets, 'c': c_targets},
                        epochs=num_epoches, batch_size = num_batches)

    def predict(self, pred_data):
        self.pred = self.model.predict(np.array(pred_data))
        self.pred_a = list(map(np.argmax, self.pred[0]))
        self.pred_b = list(map(np.argmax, self.pred[1]))
        self.pred_c = list(map(np.argmax, self.pred[2]))
        return [self.pred_a, self.pred_b, self.pred_c]

    def save_model(self, model_path):
        if model_path is not None and self.model is not None:
            self.model.save_weights(model_path, overwrite=True)
        else:
            self.model.save_weights(model_path )

    def load_model(self, model_path):
        if model_path is not None:
            self.model.load_weights(model_path)
from network import Network

class Leaner:
    def __init__(self, stock_code, data, NUM_Category,
                 delayed_reward_threshold = 0.05, lr = 0.01):
        self.stock_code = stock_code
        self.data = data
        self.sample = None

        self.num_features = self.data.shape[1]
        self.policy_network = Network(NUM_Category = NUM_Category)

    def fit(self, a_targets, b_targets, c_targets):
        return Network.fit(a_targets, b_targets, c_targets)

    def predict(self, sample = None):
        return Network.predict(sample)



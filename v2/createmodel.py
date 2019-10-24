import tensorrec
from scipy import sparse

class Model:
    def __init__(self, Data):

        self.Data = Data

        # model
        self.rent_model = tensorrec.TensorRec(n_components=5, loss_graph=tensorrec.loss_graphs.WMRBLossGraph())
        self.rent_model.fit(interactions=self.Data.sparse_rent,
                            user_features=self.Data.user_indicator_features_rent,
                            item_features=self.Data.full_rentitem_features,
                            n_sampled_items=self.Data.n_items_rent)

        self.deal_model = tensorrec.TensorRec(n_components=5, loss_graph=tensorrec.loss_graphs.WMRBLossGraph())
        self.deal_model.fit(interactions=self.Data.sparse_deal,
                            user_features=self.Data.user_indicator_features_deal,
                            item_features=self.Data.full_dealitem_features,
                            n_sampled_items=self.Data.n_items_deal)


    def recommend(self, userId, rentordeal):

        if rentordeal == 'rent':
            user_features = sparse.csr_matrix(self.Data.user_indicator_features_rent)[userId]
            user_rankings = self.rent_model.predict_rank(user_features=user_features,
                                                         item_features=self.Data.full_rentitem_features)[0]

        elif rentordeal == 'deal':
            user_features = sparse.csr_matrix(self.Data.user_indicator_features_deal)[userId]
            user_rankings = self.deal_model.predict_rank(user_features=user_features,
                                                             item_features=self.Data.full_dealitem_features)[0]

        else:
            raise ValueError

        user_rankings = list(map(lambda x: x-1, user_rankings))
        user_rankings.remove(0)
        if len(user_rankings) > 3:
            user_rankings = user_rankings[:3]
        else:
            user_rankings = user_rankings + [0] *(3 - len(user_rankings))

        return user_rankings

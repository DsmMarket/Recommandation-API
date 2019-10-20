from collections import defaultdict
import numpy
import random
from scipy import sparse
from sklearn.preprocessing import MultiLabelBinarizer
import tensorrec
from database import data

class CreateData:

    def __init__(self, cursor):

        Data = data(cursor)
        rentLog, dealLog = Data.Logs()
        rentitems, dealitems = Data.items()

        # itemLogs
        rentLog, n_users_rent, n_items_rent = self.raw_ratings(rentLog, 0)
        dealLog, n_users_deal, n_items_deal = self.raw_ratings(dealLog, 1)

        sparse_rent = self.interactions_list_to_sparse_matrix(rentLog, n_users_rent, n_items_rent)
        sparse_deal = self.interactions_list_to_sparse_matrix(dealLog, n_users_deal, n_items_deal)

        self.user_indicator_features_rent = sparse.identity(n_users_rent)
        self.item_indicator_features_rent = sparse.identity(n_items_rent)
        self.user_indicator_features_deal = sparse.identity(n_users_deal)
        self.item_indicator_features_deal = sparse.identity(n_items_deal)

        # itemCategories
        rentitems_categories, rentitems_titles = self.items_categories(rentitems)
        dealitems_categories, dealitems_titles = self.items_categories(dealitems)

        rent_categories = [rentitems_categories[internal_id] for internal_id in range(n_items_rent)]
        deal_categories = [dealitems_categories[internal_id] for internal_id in range(n_items_deal)]

        rent_categories_features = MultiLabelBinarizer().fit_transform(rent_categories)
        n_genres_rent = rent_categories_features.shape[1]
        deal_categories_features = MultiLabelBinarizer().fit_transform(deal_categories)
        n_genres_deal = deal_categories_features.shape[1]

        rent_categories_features = sparse.coo_matrix(rent_categories_features)
        deal_categories_features = sparse.coo_matrix(deal_categories_features)

        # result
        self.full_rentitem_features = sparse.hstack([self.item_indicator_features_rent, rent_categories_features])
        self.full_dealitem_features = sparse.hstack([self.item_indicator_features_deal, deal_categories_features])

        # model
        self.rent_model = tensorrec.TensorRec(n_components=5, loss_graph=tensorrec.loss_graphs.WMRBLossGraph())
        self.rent_model.fit(interactions=sparse_rent,
                            user_features=self.user_indicator_features_rent,
                            item_features=self.full_rentitem_features,
                            n_sampled_items=n_items_rent)

        self.deal_model = tensorrec.TensorRec(n_components=5, loss_graph=tensorrec.loss_graphs.WMRBLossGraph())
        self.deal_model.fit(interactions=sparse_deal,
                            user_features=self.user_indicator_features_deal,
                            item_features=self.full_dealitem_features,
                            n_sampled_items=n_items_deal)

    def raw_ratings(self, log, check):
        Log = log
        lens_to_internal_user_ids = defaultdict(lambda: len(lens_to_internal_user_ids))
        lens_to_internal_item_ids = defaultdict(lambda: len(lens_to_internal_item_ids))
        if check == 0:
            for row in range(1, len(Log)+1):
                Log['userId'][row] = lens_to_internal_user_ids[int(Log['userId'][row])]
                Log['rentId'][row] = lens_to_internal_item_ids[int(Log['rentId'][row])]
                Log['ratings'][row] = float(Log['ratings'][row])
        else:
            for row in range(1, len(Log)+1):
                Log['userId'][row] = lens_to_internal_user_ids[int(Log['userId'][row])]
                Log['dealId'][row] = lens_to_internal_item_ids[int(Log['dealId'][row])]
                Log['ratings'][row] = float(Log['ratings'][row])
        n_users = len(lens_to_internal_user_ids)
        n_items = len(lens_to_internal_item_ids)
        return Log, n_users, n_items

    def Shuffle(self, Log):
        random.shuffle(Log)
        cutoff = int(.8 * len(Log))
        train_ratings = Log[:cutoff]
        test_ratings = Log[cutoff:]
        return train_ratings, test_ratings

    def interactions_list_to_sparse_matrix(self, interactions, n_users, n_items):
        users_column, items_column, ratings_column = zip(*interactions.values.tolist())
        return sparse.coo_matrix((ratings_column, (users_column, items_column)),
                                 shape=(n_users, n_items))

    def items_categories(self, items):
        items = items.values.tolist()
        lens_to_internal_item_ids = defaultdict(lambda: len(lens_to_internal_item_ids))
        item_categories_by_internal_id = {}
        item_titles_by_internal_id = {}
        for row in items:
            row[0] = lens_to_internal_item_ids[int(row[0])]
            row[2] = row[2].split(',')
            item_categories_by_internal_id[row[0]] = row[2]
            item_titles_by_internal_id[row[0]] = row[1]
        return item_categories_by_internal_id, item_titles_by_internal_id

    def recommandation(self, userid, rentordeal):
        if rentordeal == 0:
            user_features = sparse.csr_matrix(self.user_indicator_features_rent)[userid]
            user_rankings = self.rent_model.predict_rank(user_features=user_features,
                                                         item_features=self.full_rentitem_features)[0]
        else:
            user_features = sparse.csr_matrix(self.user_indicator_features_deal)[userid]
            user_rankings = self.deal_model.predict_rank(user_features=user_features,
                                                         item_features=self.full_dealitem_features)[0]

        return numpy.where(user_rankings <= 20)[0]

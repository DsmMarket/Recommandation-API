from collections import defaultdict
import random
from scipy import sparse
from sklearn.preprocessing import MultiLabelBinarizer
import tensorrec
from getdatabase import getdatabase

class CreateModel:

    def __init__(self, cursor):

        DB = getdatabase(cursor)
        rentLog, dealLog = DB.Logs()
        rentitems, dealitems = DB.items()

        self.lens_to_internal_rentuser_ids = defaultdict(lambda: len(self.lens_to_internal_rentuser_ids))
        self.lens_to_internal_rentitem_ids = defaultdict(lambda: len(self.lens_to_internal_rentitem_ids))
        self.lens_to_internal_dealuser_ids = defaultdict(lambda: len(self.lens_to_internal_dealuser_ids))
        self.lens_to_internal_dealitem_ids = defaultdict(lambda: len(self.lens_to_internal_dealitem_ids))

        # itemLogs
        rentLog, n_users_rent, n_items_rent = self.raw_ratings(rentLog, 'rent')
        dealLog, n_users_deal, n_items_deal = self.raw_ratings(dealLog, 'deal')
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
        deal_categories_features = MultiLabelBinarizer().fit_transform(deal_categories)

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

    def raw_ratings(self, log, rentordeal):
        Log = log
        if rentordeal == 'rent':
            for row in range(1, len(Log)+1):
                Log['userId'][row] = self.lens_to_internal_rentuser_ids[int(Log['userId'][row])]
                Log['rentId'][row] = self.lens_to_internal_rentitem_ids[int(Log['rentId'][row])]
                Log['ratings'][row] = float(Log['ratings'][row])
            n_users = len(self.lens_to_internal_rentuser_ids)
            n_items = len(self.lens_to_internal_rentitem_ids)

        else:
            for row in range(1, len(Log)+1):
                Log['userId'][row] = self.lens_to_internal_dealuser_ids[int(Log['userId'][row])]
                Log['dealId'][row] = self.lens_to_internal_dealitem_ids[int(Log['dealId'][row])]
                Log['ratings'][row] = float(Log['ratings'][row])
            n_users = len(self.lens_to_internal_dealuser_ids)
            n_items = len(self.lens_to_internal_dealitem_ids)
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
        item_categories_by_internal_id = {}
        item_titles_by_internal_id = {}
        for i, row in enumerate(items):
            row[0] = i
            row[2] = row[2].split(',')
            item_categories_by_internal_id[row[0]] = row[2]
            item_titles_by_internal_id[row[0]] = row[1]
        return item_categories_by_internal_id, item_titles_by_internal_id

    def recommendation(self, userid, rentordeal):
        if rentordeal == 'rent':
            user_features = sparse.csr_matrix(self.user_indicator_features_rent)[userid]
            user_rankings = self.rent_model.predict_rank(user_features=user_features,
                                                         item_features=self.full_rentitem_features)[0]

        else:
            user_features = sparse.csr_matrix(self.user_indicator_features_deal)[userid]
            user_rankings = self.deal_model.predict_rank(user_features=user_features,
                                                         item_features=self.full_dealitem_features)[0]

        return user_rankings

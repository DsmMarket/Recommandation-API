from collections import defaultdict
import random
from scipy import sparse
from sklearn.preprocessing import MultiLabelBinarizer
from getdatabase import getdatabase

class Data:

    def __init__(self, cursor):

        DB = getdatabase(cursor)
        rentLog = DB.rentLog
        dealLog = DB.dealLog
        rentitems = DB.rent
        dealitems = DB.deal

        self.lens_to_internal_rentuser_ids = defaultdict(lambda: len(self.lens_to_internal_rentuser_ids))
        self.lens_to_internal_rentitem_ids = defaultdict(lambda: len(self.lens_to_internal_rentitem_ids))
        self.lens_to_internal_dealuser_ids = defaultdict(lambda: len(self.lens_to_internal_dealuser_ids))
        self.lens_to_internal_dealitem_ids = defaultdict(lambda: len(self.lens_to_internal_dealitem_ids))

        # itemLogs
        rentLog, self.n_users_rent, self.n_items_rent = self.raw_ratings(rentLog, 'rent')
        dealLog, self.n_users_deal, self.n_items_deal = self.raw_ratings(dealLog, 'deal')

        self.sparse_rent = self.interactions_list_to_sparse_matrix(rentLog, self.n_users_rent, self.n_items_rent)
        self.sparse_deal = self.interactions_list_to_sparse_matrix(dealLog, self.n_users_deal, self.n_items_deal)

        self.user_indicator_features_rent = sparse.identity(self.n_users_rent)
        self.item_indicator_features_rent = sparse.identity(self.n_items_rent)
        self.user_indicator_features_deal = sparse.identity(self.n_users_deal)
        self.item_indicator_features_deal = sparse.identity(self.n_items_deal)

        # itemCategories
        rentitems_categories, rentitems_titles = self.items_categories(rentitems)
        dealitems_categories, dealitems_titles = self.items_categories(dealitems)

        rent_categories = [rentitems_categories[internal_id] for internal_id in range(self.n_items_rent)]
        deal_categories = [dealitems_categories[internal_id] for internal_id in range(self.n_items_deal)]

        rent_categories_features = MultiLabelBinarizer().fit_transform(rent_categories)
        deal_categories_features = MultiLabelBinarizer().fit_transform(deal_categories)

        rent_categories_features = sparse.coo_matrix(rent_categories_features)
        deal_categories_features = sparse.coo_matrix(deal_categories_features)

        # result
        self.full_rentitem_features = sparse.hstack([self.item_indicator_features_rent, rent_categories_features])
        self.full_dealitem_features = sparse.hstack([self.item_indicator_features_deal, deal_categories_features])

    def raw_ratings(self, log, rentordeal):
        Log = log
        if rentordeal == 'rent':
            for row in range(len(Log)):
                Log['userId'][row] = self.lens_to_internal_rentuser_ids[int(Log['userId'][row])]
                Log['rentId'][row] = self.lens_to_internal_rentitem_ids[int(Log['rentId'][row])]
                Log['ratings'][row] = float(Log['ratings'][row])
            n_users = len(self.lens_to_internal_rentuser_ids)
            n_items = len(self.lens_to_internal_rentitem_ids)

        elif rentordeal == 'deal':
            for row in range(len(Log)):
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


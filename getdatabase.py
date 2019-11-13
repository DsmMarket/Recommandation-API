import pandas as pd
import json

class Config:

    def __init__(self):
        self.usrexe = "SELECT * FROM dsm_market.users;"
        self.rentexe = "SELECT * FROM dsm_market.rentPosts;"
        self.dealexe = "SELECT * FROM dsm_market.dealPosts;"
        self.usrdrop = [1, 2, 4, 5, 9, 10]
        self.dealdrop = [1, 2, 4, 5, 7, 8, 9]
        self.rentdrop = [1, 2, 4, 5, 7, 8, 9, 10]
        self.usrcol = ['id', 'grade', 'gender', 'dealLog', 'rentLog']
        self.rentcol = ['id', 'name', 'category']
        self.dealcol = ['id', 'name', 'category']

class getdatabase:

    def __init__(self, cursor):
        config = Config()
        cursor.execute(config.usrexe)
        usr = pd.DataFrame(cursor.fetchall())
        cursor.execute(config.rentexe)
        rent = pd.DataFrame(cursor.fetchall())
        cursor.execute(config.dealexe)
        deal = pd.DataFrame(cursor.fetchall())

        self.usr = usr.drop(config.usrdrop, axis='columns')
        self.rent = rent.drop(config.rentdrop, axis='columns')
        self.deal = deal.drop(config.dealdrop, axis='columns')

        self.usr.columns = config.usrcol
        self.rent.columns = config.dealcol
        self.deal.columns = config.rentcol

        # dummy item
        dummy = pd.DataFrame({'id':[0], 'name':['dummy merchant'], 'category':['dummy']})
        self.rent = pd.concat([dummy, self.rent])
        self.deal = pd.concat([dummy, self.deal])

        self.rentLog = self.Log('rent')
        self.dealLog = self.Log('deal')

    def Log(self, rentordeal):
        if rentordeal == 'rent':
            log = pd.DataFrame(columns=['userId', 'rentId', 'ratings'])
            itemlen = self.rent['id'].tolist()
        else:
            log = pd.DataFrame(columns=['userId', 'dealId', 'ratings'])
            itemlen = self.deal['id'].tolist()
        i = 1

        # dummy user
        for j in itemlen:
            log.loc[i] = [0, j, 1]
            i += 1

        overlap = ''
        for u in range(len(self.usr)):
            j = json.loads(self.usr[rentordeal + 'Log'][u])
            for Id in j['logs']:
                if overlap != [self.usr['id'][u], Id, 1]:
                    log.loc[i] = [self.usr['id'][u], Id, 1]
                    i += 1
                overlap = [self.usr['id'][u], Id, 1]
        return log

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

    def Log(self, rentordeal):
        if rentordeal == 'rent':
            log = pd.DataFrame(columns=['userId', 'rentId', 'ratings'])
        else:
            log = pd.DataFrame(columns=['userId', 'dealId', 'ratings'])
        i = 1
        for u in range(len(self.usr)):
            j = json.loads(self.usr[rentordeal + 'Log'][u])
            for key in j:
                log.loc[i] = [self.usr['id'][u], j[key], 1]
                i += 1
        return log

    def Logs(self):
        rentLog = self.Log('rent')
        dealLog = self.Log('deal')
        return rentLog, dealLog

    def items(self):
        return self.rent, self.deal

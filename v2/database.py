import pandas as pd
import json

class data:
    def __init__(self, cursor):

        exes = self.excute()
        cursor.execute(exes[0])
        usr = pd.DataFrame(cursor.fetchall())
        cursor.execute(exes[1])
        rent = pd.DataFrame(cursor.fetchall())
        cursor.execute(exes[2])
        deal = pd.DataFrame(cursor.fetchall())

        dropcol = self.dropcol()
        self.usr = usr.drop(dropcol[0], axis='columns')
        self.deal = deal.drop(dropcol[1], axis='columns')
        self.rent = rent.drop(dropcol[2], axis='columns')

        colname = self.colname()
        self.usr.columns = colname[0]
        self.deal.columns = colname[1]
        self.rent.columns = colname[2]

    def excute(self):
        usrexe = "SELECT * FROM dsm_market.users;"
        rentexe = "SELECT * FROM dsm_market.rentPosts;"
        dealexe = "SELECT * FROM dsm_market.dealPosts;"
        return [usrexe, rentexe, dealexe]

    def dropcol(self):
        usrdrop = [1, 2, 4, 5, 9, 10]
        rentdrop = [1, 2, 4, 5, 7, 8, 9]
        dealdrop = [1, 2, 4, 5, 7, 8, 9, 10]
        return [usrdrop, rentdrop, dealdrop]

    def colname(self):
        usrcol = ['id', 'grade', 'gender', 'dealLog', 'RentLog']
        rentcol = ['id', 'name', 'category']
        dealcol = ['id', 'name', 'category']
        return [usrcol, dealcol, rentcol]

    def dealLog(self):
        deallog = pd.DataFrame(columns=['userId', 'dealId', 'ratings'])
        i = 1
        for u in range(len(self.usr)):
            j = json.loads(self.usr['dealLog'][u])
            for key in j:
                deallog.loc[i] = [self.usr['id'][u], j[key], 1]
                i += 1
        return deallog

    def rentLog(self):
        rentlog = pd.DataFrame(columns=['userId', 'rentId', 'ratings'])
        i = 1
        for u in range(len(self.usr)):
            j = json.loads(self.usr['RentLog'][u])
            for key in j:
                rentlog.loc[i] = [self.usr['id'][u], j[key], 1]
                i += 1
        return rentlog

    def Logs(self):
        dealLog = self.dealLog()
        rentLog = self.rentLog()
        return rentLog, dealLog

    def items(self):
        return self.rent, self.deal

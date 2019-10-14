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
        self.usr = usr.drop(dropcol[0], axis='columns', inplace=True)
        self.deal = deal.drop(dropcol[1], axis='columns', inplace=True)
        self.rent = rent.drop(dropcol[2], axis='columns', inplace=True)

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
        usrdrop = [1, 2, 3, 4, 9, 10]
        rentdrop = [1, 2, 3, 4, 7, 8, 9]
        dealdrop = [1, 2, 3, 4, 7, 8, 9, 10]
        return [usrdrop, rentdrop, dealdrop]

    def colname(self):
        usrcol = ['id', 'grade', 'gender', 'dealLog', 'RentLog']
        rentcol = ['id', 'price', 'category']
        dealcol = ['id', 'price', 'category']
        return [usrcol, dealcol, rentcol]

    def dealLog(self):
        deallog = pd.DataFrame()
        deallog.columns = ['userId', 'dealId', 'rating']
        for u in self.usr:
            j = json.loads(u['dealLog'])
            for key in j:
                deallog.append([u['id'], j[key], 1])
        return deallog

    def rentLog(self):
        rentlog = pd.DataFrame()
        rentlog.columns = ['userId', 'rentId', 'rating']
        for u in self.usr:
            j = json.loads(u['rentLog'])
            for key in j:
                rentlog.append([u['id'], j[key], 1])
        return rentlog

    def Logs(self):
        dealLog = self.dealLog()
        rentLog = self.rentLog()
        return dealLog, rentLog

    def items(self):
        return self.deal, self.rent

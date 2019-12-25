import datetime, os
from app.Certificates import Certificates, Certificates
from app.Stocks import Stocks

MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]

class Portfolio(object):
    
    def __init__(self):
        self.reportsDirectory = "reports/"
        self.investments = [Certificates(),Stocks()]

    def generateMonthlyEarningsReportAll(self, year, reportName="AnnualEarningsReport"):
        csv = self._getCSVHeader(year)
        for investment in self.investments:
            earnings = investment.getMonthlyEarningsAll(year)
            csv = csv + self._generateMonthlyCSVData(earnings)
        csv = self._appendTotals(csv)
        self._createReport(csv, reportName+str(year))

    def loadInvestments(self, investments):
        for investment in investments:
            if("cds" in investment):
                self.investments[0].bulkLoad(investments.get("cds"))
            if("stocks" in investment):
                self.investments[1].bulkLoad(investments.get("stocks"))

    def _generateMonthlyCSVData(self, earningData):
        text = ""
        row = ""
        
        for eDatum in earningData:
            row = eDatum.get("name") + ","
            earnings = eDatum.get("earnings")
            columns = eDatum.get("columns")
            total = 0

            for i in range(len(earnings)):

                total = round(total,2) + earnings[i]

                if(i != len(earnings)-1):
                    row = row + str(round(earnings[i],2)) + ","
                elif(i == len(earnings)-1):
                    row = row + str(round(earnings[i],2)) + "," + str(round(total,2)) + "\n"

            text = text + row

        return text

    def _createReport(self, text, fileName):
        if not os.path.exists(self.reportsDirectory):
            os.makedirs(self.reportsDirectory)
        fn = (self.reportsDirectory + fileName).replace(" ", "") + ".csv"
        f = open(fn, "w+", newline='')
        f.write(text)
        f.close

    def _appendTotals(self, csv):

        totals = ["Totals"]
        for index, line in enumerate(csv.splitlines()):
            if(index > 0):
                vals = line.split(",")
                for i, val in enumerate(vals):
                    
                    if(index == 1 and i > 0):
                        totals.append(float(vals[i]))
                    elif(index > 1 and i > 0) :
                        totals[i] = round(totals[i] + float(val),2)

        csvTotals = ",".join(map(str, totals))
        csv = csv + csvTotals
        return csv

    def _getCSVHeader(self, year) :
        header = "Investment Name,"
        for index, month in enumerate(MONTHS):
            header = header + month + " " + str(year) 
            if(index != len(MONTHS)-1): 
                header = header + ","
            else :
                header = header + ",Total\n"
        return header
import datetime, math
from dateutil.relativedelta import *
from app.Asset import Asset
from app.Investment import Investment
import app.DateHelper as DateHelper

"""
A = P(1+r/n)^ (nt)
"""

class Certificates(Investment):
    """Certificates(). Manages a collection of Certificate objects"""
    
    def __init__(self):
        self.certificates = []

    def addCertificate(self, name, principal, rate, time, start):
        """Adds a certificate of deposit to collection."""
        if(not self._getCd(name)):
            cert = Certificate(name, principal, rate, time, start)
            self.certificates.append(cert)
        else:
            raise TypeError("A certificate of deposit already exists with that name.")

    def bulkLoad(self, investment):
        for cd in investment:
            self.addCertificate(cd.get("name"), cd.get("principal"), cd.get("rate"), cd.get("time"), cd.get("start"))

    def getMonthlyEarningsAll(self, year=None, dataOnly=False):
        """Returns a list of all monthly growths for each saved CD."""
        earningsList = []

        for certificate in self.certificates:
            # Retrieve all records for the certificate
            data = certificate.getMonthlyGrowth(year)
            # Parses data into dictionary
            if(len(data) != 0):
                earnings = self._getMonthlyEarnings(certificate.name, data, dataOnly)
                earningsList.append(earnings)

        return earningsList

    def getMonthlyEarningsById(self, name, year=None, dataOnly=False):
        """Returns a single monthly growth for saved CD by name.
        
        Parameters:

        - name: (string) Name of the certificate
        - year: (int) The year you would like to retrieve earnings for
        - dataOnly: (bool) Whether or not you would like to append zeros to the beginning and and of earningsList to fit a monthly calendar year.
        
        """
        cd = self._getCd(name)

        if(cd):
            earningsList = []
            data = cd.getMonthlyGrowth(year)
            if(len(data) != 0):
                earnings = self._getMonthlyEarnings(cd.name, data, dataOnly)
                earningsList.append(earnings)

            return earningsList
        else:
            raise TypeError("There is not CD saved with that name.")

    def getAnnualEarningsAll(self, startYear, endYear):
        """Returns a list annual growths for each saved CD."""
        earningsList = []
        for certificate in self.certificates:
            data = certificate.getAnnualGrowth(startYear, endYear)
            if(len(data) != 0):
                earnings = self._getAnnualEarnings(certificate.name, data, startYear, endYear)
                earningsList.append(earnings)
        return earningsList

    def getAnnualEarningsById(self, name, startYear, endYear):
        """Returns a single annual growth for saved CD by name."""
        cd = self._getCd(name)
        if(cd):
            earningsList = []
            data = cd.getAnnualGrowth(startYear, endYear)
            if(len(data) != 0):
                earnings = self._getAnnualEarnings(cd.name, data, startYear, endYear)
                earningsList.append(earnings)
            return earningsList
        else:
            raise TypeError("There is not CD saved with that name.")

    def getMonthlyAssetValueAll(self, year, dataOnly=False):
        
        assetTotal = None
        assetValueList = []

        for certificate in self.certificates:

            data = certificate.getMonthlyGrowth(year)

            if(len(data) > 0):
                assetData = self._getMonthlyAssetValue(certificate.name, data, dataOnly)
                assetTotal = self._updateAssetValueList(assetTotal, assetData)
        
        assetValueList.append(assetTotal)
        return assetValueList

    def _getCd(self, name):
        """Returns a cd if it is found otherwise returns None"""
        result = None

        for certificate in self.certificates:
            if(certificate.name == name):
                result = certificate
                break
        return result

    def _getMonthlyEarnings(self, certName, certData, dataOnly=False):
        i = 1
        earnings = []
        columns = []
        date = certData[0].get("endDate")
        if(not dataOnly):
            while(i != date.month):
                columnDate = DateHelper.getLastDay(datetime.date(date.year, i, 1))
                columns.append(columnDate)
                earnings.append(0)
                i = i + 1

        for cd in certData:
            columns.append(cd.get("endDate"))
            earnings.append(cd.get("interest"))
            #if(cd.get("endDate").month == 12): break

        if(not dataOnly):
            eDate = columns[len(columns)-1]
            endDate = datetime.date(eDate.year, 12, 31)
            #endDate = datetime.date.today()
            # FIXME: find a beter way to get the next month
            eDate = DateHelper.getLastDay(eDate, plusMonths=1)
            #eDate = eDate + relativedelta(weeks=+4)
            while(eDate.year <= endDate.year):
                earnings.append(0)
                columns.append(eDate)
                eDate = DateHelper.getLastDay(eDate, plusMonths=1)
                #eDate = eDate + relativedelta(weeks=+4)

        return {
            "name" : certName,
            "earnings" : earnings,
            "columns" : columns
        }

    def _getMonthlyAssetValue(self, certName, certData, dataOnly):
        i = 1
        assetValue = []
        columns = []
        date = certData[0].get("endDate")

        # Prefix 0s for months without assetValue
        if(not dataOnly):
            while(i != date.month):
                columnDate = DateHelper.getLastDay(datetime.date(date.year, i, 1))
                columns.append(columnDate)
                assetValue.append(0)
                i = i + 1
        # Insert assetValue
        for cd in certData:
            columns.append(cd.get("endDate"))
            assetValue.append(cd.get("value"))

        if(not dataOnly):
            eDate = columns[len(columns)-1]
            endDate = datetime.date(eDate.year, 12, 31)
            #endDate = datetime.date.today()
            # FIXME: find a beter way to get the next month
            eDate = DateHelper.getLastDay(eDate, plusMonths=1)
            #eDate = eDate + relativedelta(weeks=+4)
            while(eDate.year <= endDate.year):
                assetValue.append(0)
                columns.append(eDate)
                eDate = DateHelper.getLastDay(eDate, plusMonths=1)

        return {
            "name" : certName,
            "assetValue" : assetValue,
            "columns" : columns
        }

    def _updateAssetValueList(self, assetTotal, assetData):
        if assetTotal == None :
            assetData["name"] = "Overall Certificate Value"
            return assetData
        else :
            for index, assetValue in enumerate(assetData["assetValue"]):
                assetTotal["assetValue"][index] =  assetTotal["assetValue"][index] + assetValue
            return assetTotal

    def _getAnnualEarnings(self, certName, data, start, end):
        earnings = []
        columns = []
        date = data[0].get("endDate")

        if(date.year > start):
            for i in range(date.year-start):
                earnings.append(0)
                columns.append(datetime.date(start+i, 12, 31))
            
        for datum in data:
            interest = datum.get("interest")
            earnings.append(interest)
            columns.append(datum.get("endDate"))
            if(datum.get("endDate").year == end): break

        remaining = end - data[len(data)-1].get("endDate").year
        date = columns[len(columns)-1]
        for i in range(remaining):
            earnings.append(0)
            columns.append(datetime.date(date.year+i+1, 12, 31))

        return {
            "name" : certName,
            "earnings" : earnings,
            "columns" : columns
        }


class Certificate(Asset):
    """Certificate(principal, rate, time, start). Compounds daily

    Parameters:
    - name: a unqiue string value for identifying the CD
    - principal: integer dollar value greater that 0
    - rate: float percentage value greater that 0.0
    - time: integer number of months greater that 0
    - start: datetime.date
    """
    assetType = "cd"

    def __init__(self, name, principal, rate, time, start):
        self.name = name
        self.principal = principal
        self.rate = rate/100
        self.periods = 365
        self.time = time # months
        self.start = start

    def updateCd(self, principal, rate, time, start) :
        """Updates the existing Certificate of Deposit values"""
        self.principal = principal
        self.rate = rate/100
        self.time = time
        self.start = start

    def getDailyGrowth(self, month):
        pass

    def getMonthlyGrowth(self, year=None):
        """Calculates the monthly growth of the Certificate of Deposit. If no year is given, the entire assest is calucated.
           
        Formula: A = P(1+r/n)^ (nt)
        P = principal
        r = rate
        n = time (months)
        """

        if( not isinstance(year, int) and year is not None):
            raise TypeError("If arguments is present then it must be of type int")

        monthlyGrowth = []

        days = 0
        periodStart = self.start
        currValue = self.principal 
        materityDate = periodStart + relativedelta(months=+self.time)

        for i in range(self.time+1):

            eom = getLastDayOfMonth(periodStart)
            periodEnd = eom if eom < materityDate else materityDate
            
            days = days + (periodEnd - periodStart).days
            if(periodEnd != materityDate): 
                days = days + 1

            monthValue = self.principal * math.pow((1 + self.rate/self.periods), (self.periods * days/self.periods))

            period = self._createPeriod(monthValue, periodStart, periodEnd, monthValue-currValue)
            if( (year == periodStart.year and year == periodEnd.year) or year == None) :
                monthlyGrowth.append(period)

            periodStart = eom + datetime.timedelta(+1)
            currValue = monthValue

        return monthlyGrowth        

    def getAnnualGrowth(self, startYear, endYear):
        """Calculates the annual growth of the Certificate of Deposit. Returns values with range.
           
        Formula: A = P(1+r/n)^ (nt)
        P = principal
        r = rate
        n = time (months)
        """ 
        if( not isinstance(startYear, int) and not isinstance(endYear, int)):
            raise TypeError("Arguments must be of type datetime")

        annualGrowth = []

        days = 0
        periodStart = periodEnd = self.start
        currValue = self.principal 
        materityDate = periodStart + relativedelta(months=+self.time)

        while(periodEnd != materityDate):

            eoy = getLastDayOfYear(periodStart)
            periodEnd = eoy if eoy < materityDate else materityDate
            
            days = days + (periodEnd - periodStart).days
            if(periodEnd != materityDate): 
                days = days + 1

            monthValue = self.principal * math.pow((1 + self.rate/self.periods), (self.periods * days/self.periods))

            period = self._createPeriod(monthValue, periodStart, periodEnd, monthValue-currValue)
            if( (startYear <= periodStart.year and endYear >= periodEnd.year)) :
                annualGrowth.append(period)

            periodStart = eoy + datetime.timedelta(+1)
            currValue = monthValue

        return annualGrowth

    def _createPeriod(self, value, startDate, endDate, interest):
        return {
            "value" : value, 
            "startDate" : startDate, 
            "endDate" : endDate, 
            "interest" : interest
        }

def getLastDayOfMonth(dt):
    a, m = divmod(dt.month, 12)
    return datetime.date(dt.year+a, m+1, 1) + datetime.timedelta(-1)

def getLastDayOfYear(dt):
    return datetime.date(dt.year, 12, 31)

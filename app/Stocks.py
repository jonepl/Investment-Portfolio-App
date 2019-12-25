import datetime
from dateutil.relativedelta import *
import pandas_datareader.data as web
from app.Asset import Asset
from app.Investment import Investment

"""
LINKS:
    https://investopedia.com/articles/investing/060313/what-determines-your-cost-basis.asp
    https://www.investopedia.com/ask/answers/05/costbasis.asp


Total cost = (share1 * price1) + (share2 * price2) + ...
Total shares = (share1 + share2 + ...)

                Total cost
Cost basis =  --------------
               Total shares

                    Current Cost - Cost Basis 
Growth formala = ------------------------------
                            Cost Basis

Cost basis =  after selling using FIFO as per IRS. Which means. Subtract all shares from the first investment before subtracting from later investments. Divide Total cost by total shares to get the new cost basis.

"""

class Stocks(Investment):

    def __init__(self):
        self.stocks = []

    def addBuy(self, ticker, shares, price, date):
        """Adds a buy trade to the given stock. If the ticker name does not exist then a new Stock object is created.
        
        Parameters:
            - ticker: (string) valid Stock name
            - shares: (int) number of shares purchase
            - price: (float) value paid for the stock
            - date: (datetime.date): date stock was purchased
        """
        stock = self._getStock(ticker)

        if(stock == None) :
            stock = Stock(ticker)
            self.stocks.append(stock)

        stock.addBuy(shares, price, date)

    def addBuys(self, ticker, buys):
        for buy in buys:
            self.addBuy(ticker, buy.get("shares"), buy.get("price"), buy.get("date"))

    def addSell(self, ticker, shares, price, date):
        """Adds a sell trade to the given stock.
        
        Parameters:
            - ticker: (string) valid Stock name
            - shares: (int) number of shares purchase
            - price: (float) value paid for the stock
            - date: (datetime.date): date stock was purchased
        """
        stock = self._getStock(ticker)

        if(stock == None) :
            stock = Stock(ticker)
            self.stocks.append(stock)

        stock.addBuy(shares, price, date)
        
    def addSells(self, ticker, sells):
        for sell in sells:
            self.addBuy(ticker, sell.get("shares"), sell.get("price"), sell.get("date"))

    def bulkLoad(self, investment):
        """Loads a collections of assests.
        
        Parameters:
            - investment: (dict)

            exampleInvestment = {
                "cds" : [
                    {
                        "name" : cdName",
                        "principal" : 3000,
                        "rate" : 3.40,
                        "time" : 12,
                        "start" : datetime.date(2018,3,12)    
                    }
                ],
                "stocks" :[{
                    "ticker" : "tickerName",
                    "buys" : [{
                        "shares" : 20.0,
                        "price" : 69.9705,
                        "date" : datetime.date(2018,3,5)
                    }],
                    "sells" : [{
                        "shares" : 20.0,
                        "price" : 75.0,
                        "date" : datetime.date(2018,4,5)
                    }]
                }]
            }
        """
        for stock in investment:
            self.addBuys(stock.get("ticker"), stock.get("buys"))
            self.addSells(stock.get("ticker"), stock.get("sells"))

    def getMonthlyEarningsAll(self, year=None, dataOnly=False):
        """Returns a list of all monthly growths for each saved Stock."""
        earningsList = []
        for stock in self.stocks:
            data = stock.getMonthlyGrowth(year)
            if(len(data) > 0):
                earnings = self._getMonthlyEarnings(stock.ticker, data, dataOnly)
                earningsList.append(earnings)
        return earningsList

    def getMonthlyEarningsById(self, ticker, year=None, dataOnly=False):
        """Returns a single monthly growth for saved symbol by name."""
        stock = self._getStock(ticker)
        if(stock) :
            earningsList = []
            data = stock.getMonthlyGrowth(year)
            earnings = self._getMonthlyEarnings(stock.ticker, data, dataOnly)
            earningsList.append(earnings)
            return earningsList
        else:
            raise TypeError("There is not stock saved with that symbol.")

        return growth

    def getAnnualEarningsAll(self, startYear, endYear):
        """Returns all annual growths for a given range.
        
        Parameters:
            - startYear (int)
            - endYear (int)
        """
        earningsList = []
        for stock in self.stocks:
            data = stock.getAnnualGrowth(startYear, endYear)
            if(len(data) != 0):
                earnings = self._getAnnualEarnings(stock.ticker, data, startYear, endYear)
                earningsList.append(earnings)
        return earningsList

    def getAnnualEarningsById(self, id, startYear, endYear):
        """Returns a single annual growth for saved symbol by name.
        
        Parameters:
            - startYear (int)
            - endYear (int)
        """
        stock = self._getStock(id)
        if(stock):
            earningsList = []
            data = stock.getAnnualGrowth(startYear, endYear)
            if(len(data) != 0):
                earnings = self._getAnnualEarnings(stock.ticker, data, startYear, endYear)
                earningsList.append(earnings)
            return earningsList
        else:
            raise TypeError("There is not stock saved with that name.")

    def _getStock(self, ticker):
        for stock in self.stocks:
            if(stock.ticker == ticker):
                return stock

    def _getMonthlyEarnings(self, stockName, stockData, dataOnly=False):
        i = 1
        earnings = []
        columns = []
        date = stockData[0].get("endDate")

        # adds padding before data
        if(not dataOnly):
            while(i != date.month):
                columns.append(datetime.date(date.year, i, 1))
                earnings.append(0)
                i = i + 1
        
        prevMonth = date.month
        accumEarn = 0
        for index, stock in enumerate(stockData):
            if(prevMonth < stock.get("endDate").month):
                # Append previous Month and acculated earnings
                columns.append(datetime.date(stock.get("endDate").year, prevMonth, 28))
                earnings.append(accumEarn)

                # FIXME Next end month
                # Append empty months if any
                prevMonth = prevMonth + 1
                accumEarn = 0
                # TODO Append filler months
                while(prevMonth != stock.get("endDate").month):
                    columns.append(datetime.date(stock.get("endDate").year, prevMonth, 28))
                    earnings.append(0)
                    # FIXME Next end month
                    prevMonth = prevMonth + 1

                # Set current stock info as previous
                accumEarn = 0 if stock.get("earnings") is None else stock.get("earnings")
                prevMonth = stock.get("endDate").month
            elif(prevMonth == stock.get("endDate").month) :
                sEarn = 0 if stock.get("earnings") is None else stock.get("earnings")
                accumEarn = accumEarn + sEarn
            else:
                raise Exception("Trades are not ascending order.")

            if(index == len(stockData)-1):
                columns.append(datetime.date(stock.get("endDate").year, prevMonth, 28))
                earnings.append(accumEarn)

        # Appends padding to end
        if(not dataOnly):
            eDate = columns[len(columns)-1]
            endDate = datetime.date(eDate.year, 12, 31)

            # FIXME: find a beter way to get the next month
            eDate = eDate + relativedelta(weeks=+4)
            while(eDate.year <= endDate.year):
                earnings.append(0)
                columns.append(datetime.date(eDate.year,eDate.month,1))
                eDate = eDate + relativedelta(weeks=+4)

        return {
            "name" : stockName,
            "earnings" : earnings,
            "columns" : columns
        }

    def _getAnnualEarnings(self, stockName, data, start, end):
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
            "name" : stockName,
            "earnings" : earnings,
            "columns" : columns
        }

class Stock(Asset):
    """Stock(principal, rate, time, start). Compounds daily

    Parameters:

    - ticker: a valid US ticker symbol
    """

    assetType = "stock"

    def __init__(self, ticker):
        self.ticker = ticker
        self.buys = []
        self.sells = []
        self.histData = None
        self.monthEnds = []
        self.hasDrip = False

    def addBuy(self, shares, price, date):
        """ Saves a buy trade

        Parameters:

        - shares: number shares bought
        - price: the cost paid
        - date: valid date (datetime.date) on the stock exchange
        """
        newBuy = self._createTrade(shares, price, date, "buy")

        if(self.isValidUSDate(date)) :

            buyLength = len(self.buys)

            # Insert buy trade in sorted order
            if(buyLength == 0) : 
                self.buys.append(newBuy)
            else :
                for index in range(buyLength):
                    if(date < self.buys[index].get("date")) :
                        self.buys.insert(index, newBuy)
                        break
                    if(index == len(self.buys)-1):
                        self.buys.append(newBuy)
   
    def addSell(self, shares, price, date):
        """ Saves a sell trade

        Parameters:

        - shares: number shares bought
        - price: the cost paid
        - date: valid date (datetime) on the stock exchange
        """
        newSell = self._createTrade(shares, price, date, "sell")
        
        if(self.isValidUSDate(date) and self._isValidSell(newSell)) :

            sellLength = len(self.sells)

            # Insert sell trade in sorted order
            if(sellLength == 0) : 
                self.sells.append(newSell)
            else :
                for index in range(sellLength):
                    if(date < self.sells[index].get("date")) :
                        self.sells.insert(index,newSell)
                        break
                    if(index == len(self.sells)-1):
                        self.sells.append(newSell)

    def addDrip(self, date):
        """DRIP or Dividend Reinvestment Program"""
        newDrip = self._createTrade("*", "*", date, "drip")
        #TODO: Possibly add a flag to automatically add dividends if set
        pass

    def addSplit(self):
        """Stock split"""
        # You can calculate your cost basis per share in two ways:
        # Take the original investment amount ($10,000) and divide it by the new number of shares you hold (2,000 shares) to arrive at the new per share cost basis ($10,000/2,000=$5.00).
        # Take your previous cost basis per share ($10) and divide it by the split factor of 2:1 ($10.00/2 =$5.00).
        pass

    def getDailyGrowth(month):
        """Retrieves the growth percentage for each day of a given month
        
        Parameters:

        - month (int): a month from 1 - 12
        """
        pass

    def getMonthlyGrowth(self, year=2018):
        """Retrieves the growth percentage for each month of the give year

        Parameters:

        - year (int): year of interest
        """
        self._updateStockData(year)
        trades = self._getAllTrades()
        trades = self._generateCostBasis(trades)

        startYear = self.histData.index.date[0].year
        monthlyGrowth = []
        currentMonth = 1
        costBasis = 0
        value = 0

        for index, trade in enumerate(trades):
            while(currentMonth < trade.get("date").month and trade.get("date").year == year):
                if(costBasis == 0) :
                    growth = 0
                else :
                    offset = (year - startYear) * 12 - 1
                    eod = self.monthEnds[offset + currentMonth - 1]
                    eodValue = self.histData.iat[eod, 3]
                    value = self._calculateValue(eodValue, costBasis)

                period = self._createPeriod(value, trade.get("date"), trade.get("date"), trade.get("earnings"))
                monthlyGrowth.append(period)
                currentMonth = trade.get("date").month
            
            costBasis = trade.get("costBasis")

        return monthlyGrowth
    
    def getAnnualGrowth(self, startYear, endYear):
        """Retrieves the growth percentage for each year given a year range
        
        Parameters:

        - month (int): a month from 1 - 12
        """
        self._updateStockData(startYear, endYear)
        trades = self._getAllTrades()
        trades = self._generateCostBasis(trades)

        stockDataYear = self.histData.index.date[0].year
        annuallyGrowth = []
        currentYear = startYear
        costBasis = 0

        for index, trade in enumerate(trades):
        
            while(currentYear < trade.get("date").year):
                if(costBasis == 0) :
                    growth = 0
                else :
                    # Get offset to the begin of the current year
                    offset = 12 + ((currentYear - stockDataYear)*12)
                    eoy = self.monthEnds[offset-1]
                    eoyValue = self.histData.iat[eoy, 3]
                    value = self._calculateValue(eoyValue, costBasis)

                annuallyGrowth.append(value)
                currentYear = currentYear + 1
            
            costBasis = trade.get("costBasis")

            if(index == len(trades)-1) :
                # Get offset to the begin of the current year
                offset = ((currentYear - stockDataYear) * 12)
                remainingMonths = len(self.monthEnds)-offset
                month = 0

                if(remainingMonths > 12) :
                    month = 12
                else :
                    month = remainingMonths

                while(remainingMonths > 0):

                    eoy = self.monthEnds[offset + month - 1]
                    eoyValue = self.histData.iat[eoy, 3]
                    value = self._calculateValue(eoyValue, costBasis)
                    annuallyGrowth.append(value)
                    if(remainingMonths <= 12) :
                        offset = offset + remainingMonths
                        remainingMonths = remainingMonths - 12
                        month = 12
                    else :
                        offset = offset + 12
                        remainingMonths = remainingMonths - 12
                        month = remainingMonths%12
                    

        return annuallyGrowth

    def _get_last_day(self, dt):
        return get_first_day(dt, 0, 1) + datetime.timedelta(-1)

    def _get_first_day(self, dt, d_years=0, d_months=0):
        # d_years, d_months are "deltas" to apply to dt
        y, m = dt.year + d_years, dt.month + d_months
        a, m = divmod(m-1, 12)
        return datetime.date(y+a, m+1, 1)

    # TODO: Handle case if application does not have the year in stockData
    def isValidUSDate(self, date) :
        """ Test to see if the datetime date is a date the NYSE was open for trading stocks
        """
        if(not isinstance(date, datetime.date)) :
            raise TypeError("Date parameter should be of type datetime.date")

        self._updateStockData(date.year)
        validDates = self.histData.index.date
        result = date in validDates
        return result

    def _updateStockData(self, yearStart, yearEnd=None):
        """Updates historical data and ending months indicies
        """
        update = True
        if(yearEnd == None): 
            yearEnd = yearStart

        # Sets the bounds for stock data if not included in currently stored stock data
        if(self.histData is not None) :
            oldYearStart = self.histData.index.date[0].year
            oldYearEnd = self.histData.index.date[len(self.histData.index)-1].year

            update = yearStart < oldYearStart or yearEnd > oldYearEnd

            if(update) :
                if(yearStart > oldYearStart):
                    yearStart = oldYearStart

                if(yearEnd < oldYearEnd):
                    yearEnd = oldYearEnd 

        if(update) :
            self._updateHistData(yearStart, yearEnd)
            self._updateMonthEnds()

    def _updateHistData(self, yearStart, yearEnd):
        start = datetime.date(yearStart, 1,1)
        end = datetime.date(yearEnd, 12, 31)
        self.histData = web.get_data_yahoo(self.ticker, get_actions=True, start=start, end=end)

    def _updateMonthEnds(self):
        month = 1
        self.monthEnds = []
        for index, date in enumerate(self.histData.index.date):
            if(date.month != month) :
                self.monthEnds.append(index-1)
                month = month + 1
                if(month > 12) : month = 1
            if(index ==  len(self.histData.index)-1):
                self.monthEnds.append(index)

    # TODO: handle the case when sell trades are appended
    def _getAllTrades(self) :
        """Sorts all stock trades in ascending order
        """
        iBuy = 0
        iSell = 0
        maxBuy = len(self.buys)
        maxSell = len(self.sells)

        trades = []

        # Stock has both buys and sells
        while(iBuy < maxBuy and iSell < maxSell):

            buyDate = self.buys[iBuy].get("date")
            sellDate = self.sells[iSell].get("date")

            if(buyDate <= sellDate) :
                trades.append(self.buys[iBuy])
                iBuy = iBuy + 1

            elif(sellDate < buyDate) :
                trades.append(self.sells[iSell])
                iSell = iSell + 1

            else :
                raise Exception()
            
        # Appends trades when only one has trades
        if(iBuy < maxBuy):
            while(iBuy < maxBuy):
                trades.append(self.buys[iBuy])
                iBuy = iBuy + 1
        elif(iSell < maxSell):
            while(iSell < maxSell):
                trades.append(self.sells[iSell])
                iSell = iSell + 1

        newTrades = self._insertDividends(trades)

        return newTrades

    def _insertDividends(self, trades):
        done = False
        ti = di = 0
        twd = []
        if('Dividends' in self.histData) :
            dividends = self.histData[self.histData.Dividends.notnull()]
            #TODO: Figure out better way
            dValues = self.histData[self.histData.Dividends.notnull()].values.tolist()
            dDates = self.histData[self.histData.Dividends.notnull()].index.tolist()

            while(ti < len(trades) and di < len(dValues)):
                tDate = trades[ti].get("date")
                dDate = dDates[di].date()

                if(tDate > dDate):
                    dTrade = self._createTrade("*", dValues[di][6], dDate, "dividend")
                    if(len(twd) != 0) : 
                        twd.append(dTrade)
                    di = di + 1
                    if(di == len(dValues)):
                        while(ti < len(trades)):
                            twd.append(trades[ti])
                            ti = ti + 1
                else :
                    twd.append(trades[ti])
                    ti = ti + 1
                    if(ti == len(trades)):
                        while(di < len(dValues)):
                            dTrade = self._createTrade("*", dValues[di][6], dDates[di].date(), "dividend")
                            twd.append(dTrade)
                            di = di + 1

            return twd
        else :
            return trades


    # TODO: Include sells, drip, splits into costbasis
    # FIXME Costbasis broken
    def _generateCostBasis(self, trades):
        """Calucates the cost basis for all trades. Cost basis does not include profit.

        Parameters:

        - trades (array): collection of trades
        """
        totCost = 0
        totShares = 0
        costbasis = 0

        for index, trade in enumerate(trades):

            shares = trade.get("shares")
            price = trade.get("price")

            if(trade.get("type") == "buy") :
                totCost = totCost + (shares * price)
                totShares = totShares + shares
                costbasis = totCost/totShares
                trade["costBasis"] = costbasis

            # TODO: Figure out how to append profit to sell trade
            elif(trade.get("type") == "sell"):

                shares2Sell = shares

                # Sell trades using the FIFO method
                for i, t in enumerate(trades):
                    if(t.get("type") != "sell"):
                        remainingShares = None
                        if(t.get("sold") is None):
                            prevShares = t["shares"]
                            remainingShares = prevShares - shares2Sell
                            t["sold"] = { 
                                "tradeIndex" : [],
                                "remainingShares" : None
                            }
                        elif(t.get("sold").get("remainingShares") > 0) :
                            prevShares = t.get("sold").get("remainingShares")
                            if(prevShares == 0) : continue
                            remainingShares = prevShares - shares2Sell
                        elif(t.get("sold").get("remainingShares") == 0):
                            continue
                        else :
                            print("Previous trade type has invalid remaining shares")
                            print(t)

                        # Previous shares are sold in full
                        if(remainingShares == 0) :
                            t["sold"]["tradeIndex"].append(index)
                            t["sold"]["remainingShares"] = 0 

                            totShares = totShares - prevShares
                            #trade["earnings"] = prevShares * t.get("price") - (prevShares * trade.get("price"))
                            totCost = totCost - (prevShares * t["price"])

                            prevEarn = 0 if trade.get("earnings") is None else trade.get("earnings")
                            trade["earnings"] = prevEarn + shares2Sell * trade.get("price") - (shares2Sell * costbasis)
                            
                            if(totShares == 0) :
                                costbasis = 0
                                trade["costBasis"] = costbasis
                            elif(totShares > 0) :
                                costbasis = totCost/totShares
                                trade["costBasis"] = costbasis
                            else:
                                print("ERROR")
                            break

                        # Previous shares are completely sold with more shares to be sold
                        elif(remainingShares < 0) :
                            t["sold"]["tradeIndex"].append(index)
                            t["sold"]["remainingShares"] = 0 

                            shares2Sell = abs(remainingShares)

                            totShares = totShares - prevShares
                            totCost = totCost - (prevShares * t["price"])
                            prevEarn = 0 if trade.get("earnings") is None else trade.get("earnings")
                            trade["earnings"] = prevEarn + prevShares * trade.get("price") - (prevShares * costbasis)
                            #trade["earnings"] = ((prevShares * trade.get("price")) - (prevShares * t.get("price")))

                            if(totShares == 0) :
                                costbasis = 0
                                trade["costBasis"] = costbasis
                            elif(totShares > 0) :
                                #costbasis = totCost/totShares
                                trade["costBasis"] = totCost/totShares
                                pass
                            else:
                                print("ERROR")

                        # Previous shares are more than shares to sell. Shares remain
                        else:
                            t["sold"]["tradeIndex"].append(index)
                            t["sold"]["remainingShares"] = remainingShares

                            #TODO: Compute costbasis for current trade
                            
                            totShares = totShares - shares2Sell
                            totCost = totCost - (shares2Sell * t["price"])
                            prevEarn = 0 if trade.get("earnings") is None else trade.get("earnings")
                            trade["earnings"] = prevEarn + shares2Sell * trade.get("price") - (shares2Sell * costbasis)
                            #trade["earnings"] = ((shares2Sell * trade.get("price")) - (shares2Sell * t.get("price")))

                            shares2Sell = 0

                            if(totShares == 0) :
                                costbasis = 0
                                trade["costBasis"] = costbasis
                            elif(totShares > 0) :
                                costbasis = totCost/totShares
                                trade["costBasis"] = costbasis
                            else:
                                print("ERROR")

                            break
                        
                        if(i == index-1) : 
                            if(shares2Sell != 0):
                                print("Reached the last trade without selling all shares.")
                            break

            # TODO: Figure out how to append profit to dividend trade
            elif(trade.get("type") == "dividend") :
                # Costbasis should be adjusted
                trade["costBasis"] = totCost/totShares
                trade["shares"] = totShares
                if(self.hasDrip):
                    pass
                else:
                    trade["earnings"] = trade.get("price") * totShares

            elif(trade.get("type") == "split") :
                pass

            else :
                pass
        # FIXME: Do not need profit anymore
        return trades

    def _isValidSell(self, sell) :
        result = False
        sharesOwned = self._getTotalShares(self.buys)
        sharesSold = self._getTotalShares(self.sells)
        remainingShares = sharesOwned - sharesSold

        for buy in self.buys:
            sharesOwned = sharesOwned + buy.get("shares")
            if(remainingShares >= sell.get("shares") and sell.get("date") > buy.get("date")) : 
                result = True
                break
        
        return result

    def _getTotalShares(self, trades):
        total = 0

        for trade in trades:
            total = total + trade.get("shares")
        
        return total

    def _createTrade(self, shares, price, date, tradeType) :
        return {
            "shares" : shares,
            "price" : price,
            "date" : date,
            "type" : tradeType
        }

    def _createPeriod(self, value, startDate, endDate, earnings): 
        return { 
            "value" : value, 
            "startDate" : startDate, 
            "endDate" : endDate, 
            "earnings" : earnings 
        }

    def _calculateGrowth(self, present, past) :
        return (present - past) / past

    def _calculateValue(self, shares, price):
        return shares * price

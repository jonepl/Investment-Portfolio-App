import pytest, datetime
import pandas as pd
from app.Stocks import Stock
import test.test_stock_data as testData


def setup_module(module):
    pass

def setup_function(function):
    global stock
    stock = Stock("TSLA")

def test_stock_constructor():
    assert(stock.ticker == "TSLA")
    assert(stock.buys == [])
    assert(stock.sells == [])
    assert(stock.histData == None)
    assert(stock.sells == [])

def test_stock_addBuy_withValidDate():

    shares = 50
    price = 185.00
    date = datetime.date(2019,6,13)
    
    testData.setUpStock(stock, testData.TSLA2019)

    expected = {
        "shares" : shares,
        "price" : price,
        "date" : date,
        "type" : "buy"
    }

    stock.addBuy(shares, price, date)

    assert(len(stock.buys) == 1)
    assert(stock.buys[0] == expected)

def test_stock_addBuy_noTradingDayDate():
    shares = 50
    price = 185.00
    date = datetime.date(2019,7,4)

    setUpStock(stock, testData.TSLA2019)

    expected = {
        "shares" : shares,
        "price" : price,
        "date" : date
    }

    stock.addBuy(shares, price, date)

    assert(len(stock.buys) == 0)

def test_stock_addBuy_withInvalidDateType():
    shares = 50
    price = 185.00
    date = datetime.datetime(2019,6,13)

    setUpStock(stock, testData.TSLA2019)

    with pytest.raises(TypeError) as e:
        stock.addBuy(shares, price, "date")

def test_stock_addBuy_ensureBuysAreSorted():
    shares0 = 50
    price0 = 185.00
    date0 = datetime.date(2019,1,7)

    shares1 = 50
    price1 = 185.00
    date1 = datetime.date(2019,6,13)

    shares2 = 50
    price2 = 185.00
    date2 = datetime.date(2019,8,12)

    setUpStock(stock, testData.TSLA2019)

    stock.addBuy(shares1, price1, date1)  
    stock.addBuy(shares2, price2, date2)
    stock.addBuy(shares0, price0, date0)

    assert(len(stock.buys) == 3)
    assert(stock.buys[0] == { "shares" : shares0, "price" : price0, "date" : date0, "type" : "buy" })
    assert(stock.buys[1] == { "shares" : shares1, "price" : price1, "date" : date1, "type" : "buy"})
    assert(stock.buys[2] == { "shares" : shares2, "price" : price2, "date" : date2, "type" : "buy"})

def test_stock_addSell_withValidDate():
    buyShares = 100
    buyPrice = 85.00
    buyDate = datetime.date(2019,6,13)

    soldShares = 50
    soldPrice = 185.00
    soldDate = datetime.date(2019,7,15)

    setUpStock(stock, testData.TSLA2019)

    expected = {
        "shares" : soldShares,
        "price" : soldPrice,
        "date" : soldDate,
        "type" : "sell"
    }

    stock.addBuy(buyShares, buyPrice, buyDate)
    stock.addSell(soldShares, soldPrice, soldDate)

    assert(len(stock.sells) == 1)
    assert(stock.sells[0] == expected)

def test_stock_getMonthlyGrowth_BaseTest():

    stock = Stock("SIX")
    testData.setUpStock(stock, testData.SIX2018)

    # FIXME: test these values. None not a thing
    expected = [{
        "earnings" : None,
        "endDate" : datetime.date(2018,9,13),
        "startDate" : datetime.date(2018,9,13),
        "value" : 0
    },
    {
        "earnings" : 16.5886,
        "endDate" : datetime.date(2018,11,28),
        "startDate" : datetime.date(2018,11,28),
        "value" : 4721.9613733276365
    }]

    stock.addBuy(20.23, 69.9032, datetime.date(2018,9,13))
    actual = stock.getMonthlyGrowth(2018)

    assert(expected == actual)

def test_stock_getAnnualGrowth_BaseTest():

    stock = Stock("SIX")
    setUpStock(stock, testData.SIX2018)

    expected = [3888.715090664673]

    stock.addBuy(20.23, 69.9032, datetime.date(2018,9,13))

    actual = stock.getAnnualGrowth(2018, 2018)

    assert(expected == actual)

# FIXME: Need data that increases gradually for this test case
def test_stock_updateStockData_expandingRange():

    setUpStock(stock, testData.TSLA2018)
    stock.addBuy(50, 100, datetime.date(2018,6,13))     

    assert(stock.histData.index.date[0].year == 2018) 
    assert(stock.histData.index.date[len(stock.histData.index)-1].year == 2018)

    setUpStock(stock, testData.TSLA2)
    stock.addBuy(50, 100, datetime.date(2017,6,13))

    assert(stock.histData.index.date[0].year == 2017)
    assert(stock.histData.index.date[len(stock.histData.index)-1].year == 2018)

    setUpStock(stock, testData.TSLA3)
    stock.addBuy(50, 100, datetime.date(2019,6,13))

    assert(stock.histData.index.date[0].year == 2017)
    assert(stock.histData.index.date[len(stock.histData.index)-1].year == 2019)

def test_stock_getAllTrades_happyPath():
    
    setUpStock(stock, testData.TSLA3)

    buy0 = createTrade(25, 150, datetime.date(2019,6,13), "buy")
    buy1 = createTrade(100, 100, datetime.date(2018,6,13), "buy")
    buy2 = createTrade(200, 200, datetime.date(2017,3,24), "buy")
    sell0 = createTrade(200, 175, datetime.date(2017,9,25), "sell")
    sell1 = createTrade(125, 75, datetime.date(2019,6,14), "sell")

    expected = [buy2, sell0, buy1, buy0, sell1]

    stock.addBuy(buy0.get("shares"), buy0.get("price"), buy0.get("date"))
    stock.addBuy(buy1.get("shares"), buy1.get("price"), buy1.get("date"))
    stock.addBuy(buy2.get("shares"), buy2.get("price"), buy2.get("date"))
    stock.addSell(sell0.get("shares"), sell0.get("price"), sell0.get("date"))
    stock.addSell(sell1.get("shares"), sell1.get("price"), sell1.get("date"))

    actual = stock._getAllTrades()

    assert(expected == actual)

def test_stock_getAllTrades_sellBeforeBuy():

    setUpStock(stock, testData.TSLA3)

    buy0 = createTrade(25, 150, datetime.date(2019,6,13), "buy")
    sell0 = createTrade(200, 175, datetime.date(2017,9,25), "sell")

    expected = [buy0]

    stock.addSell(sell0.get("shares"), sell0.get("price"), sell0.get("date"))
    stock.addBuy(buy0.get("shares"), buy0.get("price"), buy0.get("date"))

    actual = stock._getAllTrades()

    assert(expected == actual)

def test_stock_getAllTrades_sellMoreThanBuy():

    setUpStock(stock, testData.TSLA3)

    buy0 = createTrade(25, 175, datetime.date(2017,9,25), "buy")
    sell0 = createTrade(200, 150, datetime.date(2019,6,13), "sell")

    expected = [buy0]

    stock.addBuy(buy0.get("shares"), buy0.get("price"), buy0.get("date"))
    stock.addSell(sell0.get("shares"), sell0.get("price"), sell0.get("date"))

    actual = stock._getAllTrades()

    assert(expected == actual)

def test_stock_generateCostBasis_multipleBuys():

    setUpStock(stock, testData.TSLA3)

    buy0 = createTrade(25, 150, datetime.date(2019,6,13), "buy")
    buy1 = createTrade(200, 200, datetime.date(2017,3,24), "buy")
    buy2 = createTrade(100, 100, datetime.date(2018,6,13), "buy")

    buy1["costBasis"] = 200
    buy2["costBasis"] = 166.66666666666666
    buy0["costBasis"] = 165.3846153846154

    expected = [buy1, buy2, buy0]

    stock.addBuy(buy0.get("shares"), buy0.get("price"), buy0.get("date"))
    stock.addBuy(buy1.get("shares"), buy1.get("price"), buy1.get("date"))
    stock.addBuy(buy2.get("shares"), buy2.get("price"), buy2.get("date"))

    trades = stock._getAllTrades()
    actual = stock._generateCostBasis(trades)

    assert(expected == actual)

def test_stock_generateCostBasis_multipleBuysAndSell0TradesRemaining():
    setUpStock(stock, testData.TSLA3)

    trade1 = createTrade(10, 250, datetime.date(2017,3,24), "buy")
    trade2 = createTrade(5, 300, datetime.date(2017,9,25), "sell")
    trade3 = createTrade(10, 200, datetime.date(2018,6,13), "buy")
    trade4 = createTrade(10, 150, datetime.date(2019,6,13), "buy")
    trade5 = createTrade(25, 350, datetime.date(2019,6,14), "sell")

    # TODO: convert tradeIndex into array
    trade1["costBasis"] = 250.0
    trade1["sold"] = { "tradeIndex" : [1, 4], "remainingShares" : 0 }
    trade2["costBasis"] = 250.0
    trade2["earnings"] = 250 # Validate
    trade3["costBasis"] = 216.66666666666666
    trade3["sold"] = { "tradeIndex" : [4], "remainingShares" : 0 }
    trade4["costBasis"] = 190.0
    trade4["sold"] = { "tradeIndex" : [4], "remainingShares" : 0 }
    trade5["costBasis"] = 0.0
    trade5["earnings"] = 4000.0

    expectedCostbasis = [trade1, trade2, trade3, trade4, trade5]

    stock.addBuy(trade4.get("shares"), trade4.get("price"), trade4.get("date"))
    stock.addBuy(trade3.get("shares"), trade3.get("price"), trade3.get("date"))
    stock.addBuy(trade1.get("shares"), trade1.get("price"), trade1.get("date"))
    stock.addSell(trade2.get("shares"), trade2.get("price"), trade2.get("date"))
    stock.addSell(trade5.get("shares"), trade5.get("price"), trade5.get("date"))

    trades = stock._getAllTrades()
    actualCostBasis = stock._generateCostBasis(trades)

    assert(expectedCostbasis == actualCostBasis)

def test_stock_generateCostBasis_multipleBuysAndSellsPartialTradesRemaining():
    setUpStock(stock, testData.TSLA3)

    trade1 = createTrade(10, 250, datetime.date(2017,3,24), "buy")
    trade2 = createTrade(5, 300, datetime.date(2017,9,25), "sell")
    trade3 = createTrade(10, 200, datetime.date(2018,6,13), "buy")
    trade4 = createTrade(10, 150, datetime.date(2019,6,13), "buy")
    trade5 = createTrade(20, 350, datetime.date(2019,6,14), "sell")

    # TODO: convert tradeIndex into array
    trade1["costBasis"] = 250.0
    trade1["sold"] = { "tradeIndex" : [1, 4], "remainingShares" : 0 }
    trade2["costBasis"] = 250.0
    trade2["earnings"] = 250 # Validate
    trade3["costBasis"] = 216.66666666666666
    trade3["sold"] = { "tradeIndex" : [4], "remainingShares" : 0 }
    trade4["costBasis"] = 190.0
    trade4["sold"] = { "tradeIndex" : [4], "remainingShares" : 5 }
    trade5["costBasis"] = 150.0
    trade5["earnings"] = 3200.0

    expectedCostbasis = [trade1, trade2, trade3, trade4, trade5]

    stock.addBuy(trade4.get("shares"), trade4.get("price"), trade4.get("date"))
    stock.addBuy(trade3.get("shares"), trade3.get("price"), trade3.get("date"))
    stock.addBuy(trade1.get("shares"), trade1.get("price"), trade1.get("date"))
    stock.addSell(trade2.get("shares"), trade2.get("price"), trade2.get("date"))
    stock.addSell(trade5.get("shares"), trade5.get("price"), trade5.get("date"))

    trades = stock._getAllTrades()
    actualCostBasis = stock._generateCostBasis(trades)

    assert(expectedCostbasis == actualCostBasis)

def createTrade(shares, price, date, tradeType) :
    return {
        "shares" : shares,
        "price" : price,
        "date" : date,
        "type" : tradeType
    }

def setUpStock(stock, histData):
    df = pd.DataFrame(histData.get("data"), index=pd.to_datetime(histData.get("index")))
    df.index.name = "Date"

    stock.histData = df
    stock._updateMonthEnds()
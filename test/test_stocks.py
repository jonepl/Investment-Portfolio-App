import datetime, pytest
import test.test_stock_data as testData
from unittest import mock
from app.Stocks import Stock, Stocks
import test.test_stock_data as testData

def setup_module(module):
    pass

def setup_function(function):
    global stocks
    stocks = Stocks()

def test_stocks_constructor():
    assert(stocks.stocks == [])

@mock.patch("app.Stocks.Stock")
def test_stocks_addBuy_whenStockDoesNotExist(mock_class):

    ticker = "TSLA"
    trade = createTrade(200, 150, datetime.date(2019,6,13), "buy")
    
    stocks.addBuy(ticker, trade.get("shares"), trade.get("price"), trade.get("date"))

    mock_class.assert_called_with("TSLA")
    assert(len(stocks.stocks) == 1)

@mock.patch("app.Stocks.Stock")
def test_stocks_addBuy_multipleOfSameStock(mockStock):
    
    ticker = "TSLA"

    trade0 = createTrade(200, 200, datetime.date(2017,3,24), "buy")
    trade1 = createTrade(100, 100, datetime.date(2018,6,13), "buy")
    trade2 = createTrade(125, 75, datetime.date(2019,6,13), "buy")

    stocks.addBuy(ticker, trade0.get("shares"), trade0.get("price"), trade0.get("date"))
    stocks.addBuy(ticker, trade1.get("shares"), trade1.get("price"), trade1.get("date"))
    stocks.addBuy(ticker, trade2.get("shares"), trade2.get("price"), trade2.get("date"))

    assert(mockStock.call_count == 3)
    mockStock.assert_called_with("TSLA")

    assert(mockStock.return_value.addBuy.call_count == 3)
    mockStock.return_value.addBuy.assert_any_call(trade0.get("shares"), trade0.get("price"), trade0.get("date"))
    mockStock.return_value.addBuy.assert_any_call(trade1.get("shares"), trade1.get("price"), trade1.get("date"))
    mockStock.return_value.addBuy.assert_any_call(trade2.get("shares"), trade2.get("price"), trade2.get("date"))

def test_stocks_addBuys():
    pass

def test_stocks_addSells():
    pass

def test_stocks_bulkLoad():
    pass

@mock.patch("app.Stocks.Stock")
def test_stocks_getMonthlyEarningsAll(mockStock):

    mockStock1 = mock.Mock(Stock)
    mockStock1.ticker = "SIX"
    data = [{'earnings': None, 'endDate': datetime.date(2018, 6, 13), 'startDate': datetime.date(2018, 6, 13), 'value': 0}, {'earnings': 39.0, 'endDate': datetime.date(2018, 8, 29), 'startDate': datetime.date(2018, 8, 29), 'value': 6451.999664306641}, {'earnings': 41.0, 'endDate': datetime.date(2018, 11, 28), 'startDate': datetime.date(2018, 11, 28), 'value': 6494.999694824219}, {'earnings': 41.0, 'endDate': datetime.date(2018, 11, 28), 'startDate': datetime.date(2018, 11, 28), 'value': 6136.000061035156}, {'earnings': 41.0, 'endDate': datetime.date(2018, 11, 28), 'startDate': datetime.date(2018, 11, 28), 'value': 5563.000106811523}]
    mockStock1.getMonthlyGrowth.return_value = data

    mockStock2 = mock.Mock(Stock)
    mockStock2.ticker = "TSLA"
    data = [{'earnings': None, 'endDate': datetime.date(2018, 6, 13), 'startDate': datetime.date(2018, 6, 13), 'value': 0}, {'earnings': None, 'endDate': datetime.date(2018, 6, 13), 'startDate': datetime.date(2018, 6, 13), 'value': 34295.001220703125}, {'earnings': None, 'endDate': datetime.date(2018, 6, 13), 'startDate': datetime.date(2018, 6, 13), 'value': 29814.00146484375}, {'earnings': None, 'endDate': datetime.date(2018, 6, 13), 'startDate': datetime.date(2018, 6, 13), 'value': 30166.000366210938}, {'earnings': None, 'endDate': datetime.date(2018, 6, 13), 'startDate': datetime.date(2018, 6, 13), 'value': 26476.998901367188}, {'earnings': None, 'endDate': datetime.date(2018, 6, 13), 'startDate': datetime.date(2018, 6, 13), 'value': 33732.000732421875}, {'earnings': None, 'endDate': datetime.date(2018, 6, 13), 'startDate': datetime.date(2018, 6, 13), 'value': 35048.00109863281}, {'earnings': None, 'endDate': datetime.date(2018, 6, 13), 'startDate': datetime.date(2018, 6, 13), 'value': 33279.998779296875}]
    mockStock2.getMonthlyGrowth.return_value = data

    stocks.stocks.append(mockStock1)
    stocks.stocks.append(mockStock2)

    actual = stocks.getMonthlyEarningsAll(2018)

    assert(isinstance(actual, list))
    assert(len(actual) == 2)
    
    assert(actual[0].get("columns") != None)
    assert(actual[0].get("earnings") != None)
    assert(actual[0].get("name") == "SIX")

    assert(actual[1].get("columns") != None)
    assert(actual[1].get("earnings") != None)
    assert(actual[1].get("name") == "TSLA")


def test_stocks_getStock_whenStockExist():
    mockStock = mock.Mock(Stock)
    mockStock.ticker = "Some ticker"
    stocks.stocks.append(mockStock)

    actual = stocks._getStock("Some ticker")

    assert(isinstance(actual, mock.Mock) == True)

def test_stocks_getStock_whenStockDoesNotExist():

    actual = stocks._getStock("Some ticker")
    assert(actual == None)

@mock.patch("app.Stocks.Stock")
def test_stocks_getMonthlyEarningsById(mockStock):
    mockStock.ticker = "AAPL"
    data = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 3, 12), 'endDate': datetime.date(2018, 3, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 4, 1), 'endDate': datetime.date(2018, 4, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 5, 1), 'endDate': datetime.date(2018, 5, 31), 'interest': 8.818791107204106}, {'value': 3031.547349545009, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.558879975867058}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.869634313645747}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.946870841586133}, {'value': 3075.576034948166, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.683184890292068}, {'value': 3084.574487417627, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.998452469460972}]
    mockStock.getMonthlyGrowth.return_value = data
    stocks.stocks.append(mockStock)

    actual = stocks.getMonthlyEarningsById("AAPL", 2019)

    mockStock.getMonthlyGrowth.assert_called_with(2019)
    assert(isinstance(actual, list))
    assert(actual[0].get("name") is not None)
    assert(actual[0].get("columns") is not None)
    assert(actual[0].get("earnings") is not None)

@mock.patch("app.Stocks.Stock")
def test_stocks_getAnnualEarningsAll(mockStock):
    
    mockStock.ticker = "AAPL"
    data = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 3, 12), 'endDate': datetime.date(2018, 3, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 4, 1), 'endDate': datetime.date(2018, 4, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 5, 1), 'endDate': datetime.date(2018, 5, 31), 'interest': 8.818791107204106}, {'value': 3031.547349545009, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.558879975867058}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.869634313645747}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.946870841586133}, {'value': 3075.576034948166, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.683184890292068}, {'value': 3084.574487417627, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.998452469460972}]
    mockStock.getAnnualGrowth.return_value = data
    stocks.stocks.append(mockStock)

    actual = stocks.getAnnualEarningsAll(2018,2019)

    mockStock.getAnnualGrowth.assert_called_with(2018,2019)
    assert(isinstance(actual, list))
    assert(actual[0].get("name") is not None)
    assert(actual[0].get("columns") is not None)
    assert(actual[0].get("earnings") is not None)

def test_stocks_getAnnualEarningsById_whenStockExists():
    
    mockStock = mock.Mock(Stock)
    mockStock.ticker = "Some ticker"
    data = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 3, 12), 'endDate': datetime.date(2018, 3, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 4, 1), 'endDate': datetime.date(2018, 4, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 5, 1), 'endDate': datetime.date(2018, 5, 31), 'interest': 8.818791107204106}, {'value': 3031.547349545009, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.558879975867058}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.869634313645747}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.946870841586133}, {'value': 3075.576034948166, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.683184890292068}, {'value': 3084.574487417627, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.998452469460972}]
    mockStock.getAnnualGrowth.return_value = data
    stocks.stocks.append(mockStock)

    actual = stocks.getAnnualEarningsById("Some ticker", 2018,2019)
    
    mockStock.getAnnualGrowth.assert_called_with(2018,2019)
    assert(isinstance(actual, list))
    assert(actual[0].get("name") is not None)
    assert(actual[0].get("columns") is not None)
    assert(actual[0].get("earnings") is not None)

def test_stocks_getAnnualEarningsById_whenStockDoesNotExist():
    with pytest.raises(TypeError) as e:
        stocks.getAnnualEarningsById("Some ticker", 2018,2019)

def createTrade(shares, price, date, tradeType) :
    return {
        "shares" : shares,
        "price" : price,
        "date" : date,
        "type" : tradeType
    }
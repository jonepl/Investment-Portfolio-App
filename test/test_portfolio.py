import tempfile, pytest, datetime
from unittest import mock
from app.Portfolio import Portfolio
from app.Stocks import Stocks, Stock
from app.Certificates import Certificate, Certificates
import test.test_stock_data as testData

def setup_module(module):
    pass

def setup_function(function):
    global portfolio
    portfolio = Portfolio()

@pytest.fixture(scope="session")
def image_file(tmpdir_factory):
    img = compute_expensive_image()
    fn = tmpdir_factory.mktemp("data").join("img.png")
    img.save(str(fn))
    return fn

def test_portfolio_constructor():
    assert(isinstance(portfolio.investments[0], Certificates))
    assert(isinstance(portfolio.investments[1], Stocks))

@mock.patch("builtins.open", new_callable=mock.mock_open, read_data="data")
def test_generateMonthlyEarningsReportAll(tmpdir):

    c1 = Certificate("3K Max CD", 3000.0, 3.44, 12, datetime.date(2018, 3, 12))
    cs = Certificates()
    cs.certificates.append(c1)
 
    stock = Stock("SIX")
    testData.setUpStock(stock, testData.SIX2018)
    stock.addBuy(50, 150, datetime.date(2018,1,12))
    stock.addSell(25, 175, datetime.date(2018,9,20))
    stock.addSell(25, 200, datetime.date(2018,12,13))
    
    ss = Stocks()
    ss.stocks.append(stock)

    portfolio.investments.append(cs)
    portfolio.investments.append(ss)

    result = portfolio.generateMonthlyEarningsReportAll(2018)
    tmpdir.return_value.write.assert_called_with('Investment Name,JANUARY 2018,FEBRUARY 2018,MARCH 2018,APRIL 2018,MAY 2018,JUNE 2018,JULY 2018,AUGUST 2018,SEPTEMBER 2018,OCTOBER 2018,NOVEMBER 2018,DECEMBER 2018,Total\n3K Max CD,0,0,5.66,8.51,8.82,8.56,8.87,8.9,8.63,8.95,8.68,9.0,84.58\nSIX,0,39.0,0,0,39.0,0,0,39.0,625.0,0,20.5,1250.0,2012.5\nTotals,0.0,39.0,5.66,8.51,47.82,8.56,8.87,47.9,633.63,8.95,29.18,1259.0,2097.08')

def test_portfolio_loadInvestments():
    
    mockStocks = mock.Mock(Stocks)
    mockCertificates = mock.Mock(Certificates)
    portfolio.investments = [mockCertificates, mockStocks]

    test_investments = {
        "cds" : [],
        "stocks" : []
    }

    portfolio.loadInvestments(test_investments)
    
    mockStocks.bulkLoad.assert_called_with([])
    mockCertificates.bulkLoad.assert_called_with([])

def test_portfolio_generateMonthlyCSVData():
    expected = "3K Max CD,0,0,5.59,8.41,8.72,8.46,8.77,8.79,8.53,8.84,8.58,8.89,83.58\n"
    earningData = [{'name': '3K Max CD', 'earnings': [0, 0, 5.593989779840285, 8.410548697545437, 8.715626149914897, 8.458472844335574, 8.765288658509235, 8.790635328718054, 8.531268888023988, 8.840725247107002, 8.579880910520387, 8.89110058285587], 'columns': [datetime.date(2019, 1, 31), datetime.date(2019, 2, 28), datetime.date(2019, 3, 31), datetime.date(2019, 4, 30), datetime.date(2019, 5, 31), datetime.date(2019, 6, 30), datetime.date(2019, 7, 31), datetime.date(2019, 8, 31), datetime.date(2019, 9, 30), datetime.date(2019, 10, 31), datetime.date(2019, 11, 30), datetime.date(2019, 12, 31)]}]

    actual = portfolio._generateMonthlyCSVData(earningData)

    assert(actual == expected)

@mock.patch("builtins.open", new_callable=mock.mock_open, read_data="data")
def test_createReport(mock_file):
    portfolio._createReport("hello", "someFile.csv")

def test_portfolio_appendTotals():
    
    csv = "Investment Name,JANUARY 2018,FEBRUARY 2018,MARCH 2018,APRIL 2018,MAY 2018,JUNE 2018,JULY 2018,AUGUST 2018,SEPTEMBER 2018,OCTOBER 2018,NOVEMBER 2018,DECEMBER 2018,Total\n3K Max CD,1.0,0,0,4.00,6.00,0,8.77,8.79,8.53,8.84,8.58,8.89,63.4\n5K Max CD,0,2.0,0,5.00,0,8.00,0,0,0,8.25,9.19,9.51,41.95\nSIX,0,0,3.0,0,7.0,9.00,0,7.0,0,0,16.59,0,42.59\n"
    totals = "Totals,1.0,2.0,3.0,9.0,13.0,17.0,8.77,15.79,8.53,17.09,34.36,18.4,147.94"
    expected = csv + totals

    actual = portfolio._appendTotals(csv)
    assert(actual == expected)

def test_portfolio_getCSVHeader():
    expected = "Investment Name,JANUARY 2019,FEBRUARY 2019,MARCH 2019,APRIL 2019,MAY 2019,JUNE 2019,JULY 2019,AUGUST 2019,SEPTEMBER 2019,OCTOBER 2019,NOVEMBER 2019,DECEMBER 2019,Total\n"
    actual = portfolio._getCSVHeader(2019)
    assert(actual == expected)


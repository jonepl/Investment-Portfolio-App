import datetime
from app.Portfolio import Portfolio
from config.examplePortfolio import investments

portfolio = Portfolio()
portfolio.loadInvestments(investments)
portfolio.investments[0].getMonthlyAssetValueAll(2019)
portfolio.generateMonthlyEarningsReportAll(2019, "PersonalGrowth")

print("complete")

from abc import ABC, abstractmethod 

class Asset(ABC):
    
    @property
    @abstractmethod
    def assetType(self):
        pass

    @abstractmethod
    def getDailyGrowth(month):
        pass

    @abstractmethod
    def getMonthlyGrowth(year):
        pass

    @abstractmethod
    def getAnnualGrowth(yearStart, yearEnd):
        pass

    @abstractmethod
    def _createPeriod(value, startDate, endDate, earnings):
        pass
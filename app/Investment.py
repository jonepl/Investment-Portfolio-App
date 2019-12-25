from abc import ABC, abstractmethod 

class Investment(ABC):
    
    @abstractmethod
    def getMonthlyEarningsAll(year=None):
        pass

    @abstractmethod
    def getMonthlyEarningsById(id, year=None, ytd=None):
        pass

    @abstractmethod
    def getAnnualEarningsAll(yearStart, yearEnd):
        pass

    @abstractmethod
    def getAnnualEarningsById(id, yearStart, yearEnd):
        pass

    @abstractmethod
    def bulkLoad(self, investment):
        pass
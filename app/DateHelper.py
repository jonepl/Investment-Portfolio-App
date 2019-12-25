from enum import Enum
import datetime
from dateutil import relativedelta

class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12
 
def getFirstDay(currDate, plusMonths=0, plusYears=0):
    y, m = currDate.year + plusYears, currDate.month + plusMonths
    a, m = divmod(m-1, 12)
    return datetime.date(y+a, m+1, 1)

def getLastDay(currDate, plusMonths=0, plusYears=0):
    y, m = currDate.year + plusYears, currDate.month + plusMonths
    a, m = divmod(m, 12)
    return datetime.date(y+a, m+1, 1) + datetime.timedelta(-1)

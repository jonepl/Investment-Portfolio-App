import datetime, pytest
from app.Certificates import Certificate

def setup_module(module):
    pass

def setup_function(function):
    global certificate
    certificate = Certificate("3K Max CD", 3000, 3.44, 12, datetime.date(2018, 3, 12))

def test_certficate_constructor():
    assert(certificate.principal == 3000)
    assert(certificate.rate == 0.0344)
    assert(certificate.time == 12)
    assert(certificate.start == datetime.date(2018, 3, 12))

def test_certficate_updateCd():

    principal = 5000
    rate = 2.25
    time = 15
    start = datetime.date(2019, 2, 1)

    certificate.updateCd(principal, rate, time, start)

    assert(certificate.principal == principal)
    assert(certificate.rate == rate/100)
    assert(certificate.time == time)
    assert(certificate.start == start)

def test_certficate_getMonthlyGrowth_withOverlappingYear_noYearGiven():

    expected = [
        createPeriod(3005.65986036237, datetime.date(2018, 3, 12), datetime.date(2018, 3, 31), 5.659860362370182),
        createPeriod(3014.169678461938, datetime.date(2018, 4, 1), datetime.date(2018, 4, 30), 8.509818099567838) ,
        createPeriod(3022.988469569142, datetime.date(2018, 5, 1), datetime.date(2018, 5, 31), 8.818791107204106) ,
        createPeriod(3031.547349545009, datetime.date(2018, 6, 1), datetime.date(2018, 6, 30), 8.558879975867058) ,
        createPeriod(3040.416983858655, datetime.date(2018, 7, 1), datetime.date(2018, 7, 31), 8.869634313645747) ,
        createPeriod(3049.312568752577, datetime.date(2018, 8, 1), datetime.date(2018, 8, 31), 8.895584893922205) ,
        createPeriod(3057.945979216288, datetime.date(2018, 9, 1), datetime.date(2018, 9, 30), 8.633410463710788),
        createPeriod(3066.892850057874, datetime.date(2018, 10, 1), datetime.date(2018, 10, 31), 8.946870841586133),
        createPeriod(3075.576034948166, datetime.date(2018, 11, 1), datetime.date(2018, 11, 30), 8.683184890292068),
        createPeriod(3084.574487417627, datetime.date(2018, 12, 1), datetime.date(2018, 12, 31), 8.998452469460972),
        createPeriod(3093.5992673606825, datetime.date(2019, 1, 1), datetime.date(2019, 1, 31), 9.024779943055364),
        createPeriod(3101.7733745952105, datetime.date(2019, 2, 1), datetime.date(2019, 2, 28), 8.174107234528037),
        createPeriod(3104.990537040658, datetime.date(2019, 3, 1), datetime.date(2019, 3, 12), 3.217162445447684)
    ]

    actual = certificate.getMonthlyGrowth()

    assert(expected == actual)

def test_certficate_getMonthlyGrowth_withOverlappingYear_yearGiven():

    expected = [
        createPeriod(3005.65986036237, datetime.date(2018, 3, 12), datetime.date(2018, 3, 31), 5.659860362370182),
        createPeriod(3014.169678461938, datetime.date(2018, 4, 1), datetime.date(2018, 4, 30), 8.509818099567838) ,
        createPeriod(3022.988469569142, datetime.date(2018, 5, 1), datetime.date(2018, 5, 31), 8.818791107204106) ,
        createPeriod(3031.547349545009, datetime.date(2018, 6, 1), datetime.date(2018, 6, 30), 8.558879975867058) ,
        createPeriod(3040.416983858655, datetime.date(2018, 7, 1), datetime.date(2018, 7, 31), 8.869634313645747) ,
        createPeriod(3049.312568752577, datetime.date(2018, 8, 1), datetime.date(2018, 8, 31), 8.895584893922205) ,
        createPeriod(3057.945979216288, datetime.date(2018, 9, 1), datetime.date(2018, 9, 30), 8.633410463710788),
        createPeriod(3066.892850057874, datetime.date(2018, 10, 1), datetime.date(2018, 10, 31), 8.946870841586133),
        createPeriod(3075.576034948166, datetime.date(2018, 11, 1), datetime.date(2018, 11, 30), 8.683184890292068),
        createPeriod(3084.574487417627, datetime.date(2018, 12, 1), datetime.date(2018, 12, 31), 8.998452469460972)
    ]

    actual = certificate.getMonthlyGrowth(2018)

    assert(expected == actual)

def test_certficate_getMonthlyGrowth_withOverlappingYear_yearOutOfRange():

    expected = []

    actual = certificate.getMonthlyGrowth(2017)

    assert(expected == actual)

def test_certficate_getMonthlyGrowth_withOverlappingYear_invalidYearGiven():
    with pytest.raises(TypeError) as e:
        actual = certificate.getMonthlyGrowth("2018") 

def test_certficate_getAnnualGrowth_withOverlappingYear():

    expected = [
        createPeriod(3084.574487417627, datetime.date(2018, 3, 12), datetime.date(2018, 12, 31), 84.5744874176271),
        createPeriod(3104.990537040658, datetime.date(2019, 1, 1), datetime.date(2019, 3, 12), 20.416049623031086)
    ]

    actual = certificate.getAnnualGrowth(2017, 2019)

    assert(expected == actual)

def test_certficate_getAnnualGrowth_withOverlappingYear_yearOutOfRange():
    expected = []

    actual = certificate.getAnnualGrowth(2014, 2016)

    assert(expected == actual)

def test_certficate_getAnnualGrowth_withOverlappingYear_invalidYear():
    with pytest.raises(TypeError) as e:
        actual = certificate.getAnnualGrowth("2017", 2019) 

def createPeriod(value, startDate, endDate, interest):
    return {
        "value" : value, 
        "startDate" : startDate, 
        "endDate" : endDate, 
        "interest" : interest
    }
import datetime, pytest
from unittest import mock
from app.Certificates import Certificate, Certificates

def setup_module(module):
    pass

def setup_function(function):
    global certificates
    certificates = Certificates()

def test_certficates_constructor():
    assert(certificates.certificates == [])

def test_certficates_addCertificate_withValidName():
    
    principal = 5000
    rate = 2.25
    time = 15
    start = datetime.date(2019, 2, 1)
    
    certificates.addCertificate("5K Max CD", principal, rate, time, start)

    assert(certificates.certificates[0].principal == principal)
    assert(certificates.certificates[0].rate == rate/100)
    assert(certificates.certificates[0].time == time)
    assert(certificates.certificates[0].start == start)

def test_certficates_addCertificate_withInvalidName():
    pass
    

def test_certficates_addCertificate_multipleCertExist():
    
    principal = 5000
    rate = 2.25
    time = 15
    start = datetime.date(2019, 2, 1)
    
    certificates.addCertificate("5K Max CD", principal, rate, time, start)
    with pytest.raises(TypeError) as e:
        certificates.addCertificate("5K Max CD", principal, rate, time, start)

def test_certficates_getMonthlyEarningsAll_withYear():

    # Mock Certificate 3.44% 12 month 3/12/18 - 3/12/19
    mockCertificate1 = mock.Mock(Certificate)
    mockCertificate1.name = "3K Max CD"
    data1 = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 3, 12), 'endDate': datetime.date(2018, 3, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 4, 1), 'endDate': datetime.date(2018, 4, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 5, 1), 'endDate': datetime.date(2018, 5, 31), 'interest': 8.818791107204106}, {'value': 3031.547349545009, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.558879975867058}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.869634313645747}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.946870841586133}, {'value': 3075.576034948166, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.683184890292068}, {'value': 3084.574487417627, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.998452469460972}]
    mockCertificate1.getMonthlyGrowth.return_value = data1

    # Mock Certificate 3.44% 12 month 5/12/18 - 5/12/19
    mockCertificate2 = mock.Mock(Certificate)
    mockCertificate2.name = "Other 3K Max CD"
    data2 = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 5, 12), 'endDate': datetime.date(2018, 5, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.818791107204106}, {'value': 3031.8330625006924, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.844592931550324}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.583921357962481}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.946870841586133}]
    mockCertificate2.getMonthlyGrowth.return_value = data2

    certificates.certificates.append(mockCertificate1)
    certificates.certificates.append(mockCertificate2)

    actual = certificates.getMonthlyEarningsAll(year=2018, dataOnly=False)

    assert(isinstance(actual, list))
    assert(len(actual) == 2)
    assert(isinstance(actual[0], dict))
    assert(isinstance(actual[1], dict))
    assert(actual[0].get("name") == "3K Max CD")
    assert(actual[1].get("name") == "Other 3K Max CD")
    assert(len(actual[0].get("earnings")) == 12)
    assert(len(actual[1].get("earnings")) == 12)

def test_certficates_getMonthlyEarningsAll_noYear():

    # Mock Certificate 3.44% 12 month 3/12/18 - 3/12/19
    mockCertificate1 = mock.Mock(Certificate)
    mockCertificate1.name = "3K Max CD"
    data1 = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 3, 12), 'endDate': datetime.date(2018, 3, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 4, 1), 'endDate': datetime.date(2018, 4, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 5, 1), 'endDate': datetime.date(2018, 5, 31), 'interest': 8.818791107204106}, {'value': 3031.547349545009, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.558879975867058}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.869634313645747}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.946870841586133}, {'value': 3075.576034948166, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.683184890292068}, {'value': 3084.574487417627, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.998452469460972}, {'value': 3093.5992673606825, 'startDate': datetime.date(2019, 1, 1), 'endDate': datetime.date(2019, 1, 31), 'interest': 9.024779943055364}, {'value': 3101.7733745952105, 'startDate': datetime.date(2019, 2, 1), 'endDate': datetime.date(2019, 2, 28), 'interest': 8.174107234528037}, {'value': 3104.990537040658, 'startDate': datetime.date(2019, 3, 1), 'endDate': datetime.date(2019, 3, 12), 'interest': 3.217162445447684}]
    mockCertificate1.getMonthlyGrowth.return_value = data1

    # Mock Certificate 3.44% 12 month 5/12/18 - 5/12/19
    mockCertificate2 = mock.Mock(Certificate)
    mockCertificate2.name = "Other 3K Max CD"
    data2 = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 5, 12), 'endDate': datetime.date(2018, 5, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.818791107204106}, {'value': 3031.8330625006924, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.844592931550324}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.583921357962481}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.946870841586133}, {'value': 3075.865897456665, 'startDate': datetime.date(2019, 1, 1), 'endDate': datetime.date(2019, 1, 31), 'interest': 8.973047398791095}, {'value': 3083.993148439075, 'startDate': datetime.date(2019, 2, 1), 'endDate': datetime.date(2019, 2, 28), 'interest': 8.127250982409805}, {'value': 3093.0162275133794, 'startDate': datetime.date(2019, 3, 1), 'endDate': datetime.date(2019, 3, 31), 'interest': 9.023079074304405}, {'value': 3101.7733745952105, 'startDate': datetime.date(2019, 4, 1), 'endDate': datetime.date(2019, 4, 30), 'interest': 8.757147081831135}, {'value': 3104.990537040658, 'startDate': datetime.date(2019, 5, 1), 'endDate': datetime.date(2019, 5, 12), 'interest': 3.217162445447684}]
    mockCertificate2.getMonthlyGrowth.return_value = data2

    certificates.certificates.append(mockCertificate1)
    certificates.certificates.append(mockCertificate2)

    actual = certificates.getMonthlyEarningsAll(year=None, dataOnly=False)
    print(actual)

    assert(isinstance(actual, list))
    assert(len(actual) == 2)
    assert(isinstance(actual[0], dict))
    assert(isinstance(actual[1], dict))
    assert(actual[0].get("name") == "3K Max CD")
    assert(actual[1].get("name") == "Other 3K Max CD")
    assert(len(actual[0].get("earnings")) == 24)
    assert(len(actual[1].get("earnings")) == 24)

def test_certficates_getMonthlyEarningsAll_noYearDataOnly():

    mockCertificate1 = mock.Mock(Certificate)
    mockCertificate1.name = "3K Max Stock"
    data1 = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 3, 12), 'endDate': datetime.date(2018, 3, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 4, 1), 'endDate': datetime.date(2018, 4, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 5, 1), 'endDate': datetime.date(2018, 5, 31), 'interest': 8.818791107204106}, {'value': 3031.547349545009, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.558879975867058}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.869634313645747}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.946870841586133}, {'value': 3075.576034948166, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.683184890292068}, {'value': 3084.574487417627, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.998452469460972}, {'value': 3093.5992673606825, 'startDate': datetime.date(2019, 1, 1), 'endDate': datetime.date(2019, 1, 31), 'interest': 9.024779943055364}, {'value': 3101.7733745952105, 'startDate': datetime.date(2019, 2, 1), 'endDate': datetime.date(2019, 2, 28), 'interest': 8.174107234528037}, {'value': 3104.990537040658, 'startDate': datetime.date(2019, 3, 1), 'endDate': datetime.date(2019, 3, 12), 'interest': 3.217162445447684}]
    mockCertificate1.getMonthlyGrowth.return_value = data1

    mockCertificate2 = mock.Mock(Certificate)
    mockCertificate2.name = "Other 3K Max Stock"
    data2 = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 5, 12), 'endDate': datetime.date(2018, 5, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.818791107204106}, {'value': 3031.8330625006924, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.844592931550324}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.583921357962481}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.946870841586133}, {'value': 3075.865897456665, 'startDate': datetime.date(2019, 1, 1), 'endDate': datetime.date(2019, 1, 31), 'interest': 8.973047398791095}, {'value': 3083.993148439075, 'startDate': datetime.date(2019, 2, 1), 'endDate': datetime.date(2019, 2, 28), 'interest': 8.127250982409805}, {'value': 3093.0162275133794, 'startDate': datetime.date(2019, 3, 1), 'endDate': datetime.date(2019, 3, 31), 'interest': 9.023079074304405}, {'value': 3101.7733745952105, 'startDate': datetime.date(2019, 4, 1), 'endDate': datetime.date(2019, 4, 30), 'interest': 8.757147081831135}, {'value': 3104.990537040658, 'startDate': datetime.date(2019, 5, 1), 'endDate': datetime.date(2019, 5, 12), 'interest': 3.217162445447684}]
    mockCertificate2.getMonthlyGrowth.return_value = data2

    certificates.certificates.append(mockCertificate1)
    certificates.certificates.append(mockCertificate2)

    actual = certificates.getMonthlyEarningsAll(dataOnly=True)
    
    assert(isinstance(actual, list))
    assert(len(actual) == 2)
    assert(isinstance(actual[0], dict))
    assert(isinstance(actual[1], dict))
    assert(actual[0].get("name") == "3K Max Stock")
    assert(actual[1].get("name") == "Other 3K Max Stock")
    assert(len(actual[0].get("earnings")) == 13)
    assert(len(actual[1].get("earnings")) == 13)

def test_certficates_getMonthlyEarningsAll_withYearWithYTD():
    mockCertificate1 = mock.Mock(Certificate)
    mockCertificate1.name = "3K Max Stock"
    data1 = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 3, 12), 'endDate': datetime.date(2018, 3, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 4, 1), 'endDate': datetime.date(2018, 4, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 5, 1), 'endDate': datetime.date(2018, 5, 31), 'interest': 8.818791107204106}, {'value': 3031.547349545009, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.558879975867058}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.869634313645747}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.946870841586133}, {'value': 3075.576034948166, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.683184890292068}, {'value': 3084.574487417627, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.998452469460972}]
    mockCertificate1.getMonthlyGrowth.return_value = data1

    mockCertificate2 = mock.Mock(Certificate)
    mockCertificate2.name = "Other 3K Max Stock"
    data2 = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 5, 12), 'endDate': datetime.date(2018, 5, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.818791107204106}, {'value': 3031.8330625006924, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.844592931550324}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.583921357962481}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.946870841586133}]
    mockCertificate2.getMonthlyGrowth.return_value = data2

    certificates.certificates.append(mockCertificate1)
    certificates.certificates.append(mockCertificate2)

    actual = certificates.getMonthlyEarningsAll(year=2018, dataOnly=True)
    
    assert(isinstance(actual, list))
    assert(len(actual) == 2)
    assert(isinstance(actual[0], dict))
    assert(isinstance(actual[1], dict))
    assert(actual[0].get("name") == "3K Max Stock")
    assert(actual[1].get("name") == "Other 3K Max Stock")
    assert(len(actual[0].get("earnings")) == 10)
    assert(len(actual[1].get("earnings")) == 8)

def test_certficates_getMonthlyEarningsById_noYear():

    mockCertificate = mock.Mock(Certificate)
    mockCertificate.name = "3K Max Stock"
    data = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 3, 12), 'endDate': datetime.date(2018, 3, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 4, 1), 'endDate': datetime.date(2018, 4, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 5, 1), 'endDate': datetime.date(2018, 5, 31), 'interest': 8.818791107204106}, {'value': 3031.547349545009, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.558879975867058}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.869634313645747}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.946870841586133}, {'value': 3075.576034948166, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.683184890292068}, {'value': 3084.574487417627, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.998452469460972}, {'value': 3093.5992673606825, 'startDate': datetime.date(2019, 1, 1), 'endDate': datetime.date(2019, 1, 31), 'interest': 9.024779943055364}, {'value': 3101.7733745952105, 'startDate': datetime.date(2019, 2, 1), 'endDate': datetime.date(2019, 2, 28), 'interest': 8.174107234528037}, {'value': 3104.990537040658, 'startDate': datetime.date(2019, 3, 1), 'endDate': datetime.date(2019, 3, 12), 'interest': 3.217162445447684}]
    mockCertificate.getMonthlyGrowth.return_value = data
    certificates.certificates.append(mockCertificate)

    actual = certificates.getMonthlyEarningsById("3K Max Stock")

    assert(isinstance(actual, list))
    assert(len(actual) == 1)
    assert(isinstance(actual[0], dict))
    assert(actual[0].get("name") == "3K Max Stock")
    assert(len(actual[0].get("earnings")) == 24)

def test_certficates_getMonthlyEarningsById_withYear():

    mockCertificate = mock.Mock(Certificate)
    mockCertificate.name = "3K Max Stock"
    data = [{'value': 3005.65986036237, 'startDate': datetime.date(2018, 3, 12), 'endDate': datetime.date(2018, 3, 31), 'interest': 5.659860362370182}, {'value': 3014.169678461938, 'startDate': datetime.date(2018, 4, 1), 'endDate': datetime.date(2018, 4, 30), 'interest': 8.509818099567838}, {'value': 3022.988469569142, 'startDate': datetime.date(2018, 5, 1), 'endDate': datetime.date(2018, 5, 31), 'interest': 8.818791107204106}, {'value': 3031.547349545009, 'startDate': datetime.date(2018, 6, 1), 'endDate': datetime.date(2018, 6, 30), 'interest': 8.558879975867058}, {'value': 3040.416983858655, 'startDate': datetime.date(2018, 7, 1), 'endDate': datetime.date(2018, 7, 31), 'interest': 8.869634313645747}, {'value': 3049.312568752577, 'startDate': datetime.date(2018, 8, 1), 'endDate': datetime.date(2018, 8, 31), 'interest': 8.895584893922205}, {'value': 3057.945979216288, 'startDate': datetime.date(2018, 9, 1), 'endDate': datetime.date(2018, 9, 30), 'interest': 8.633410463710788}, {'value': 3066.892850057874, 'startDate': datetime.date(2018, 10, 1), 'endDate': datetime.date(2018, 10, 31), 'interest': 8.946870841586133}, {'value': 3075.576034948166, 'startDate': datetime.date(2018, 11, 1), 'endDate': datetime.date(2018, 11, 30), 'interest': 8.683184890292068}, {'value': 3084.574487417627, 'startDate': datetime.date(2018, 12, 1), 'endDate': datetime.date(2018, 12, 31), 'interest': 8.998452469460972}]
    mockCertificate.getMonthlyGrowth.return_value = data
    certificates.certificates.append(mockCertificate)

    actual = certificates.getMonthlyEarningsById("3K Max Stock", 2018)

    assert(isinstance(actual, list))
    assert(len(actual) == 1)
    assert(isinstance(actual[0], dict))
    assert(actual[0].get("name") == "3K Max Stock")
    assert(len(actual[0].get("earnings")) == 12)

@mock.patch("app.Certificates.Certificate")
def test_certficates_getMonthlyEarningsById_whenCertDoesNotExist(mockCertificate):

    with pytest.raises(TypeError) as e:
        actual = certificates.getMonthlyEarningsById("3K Max Stock", 2019)

def test_certficates_getAnnualEarningsAll():

    cert1 = Certificate("3K Max Stock", 3000, 3.44, 12, datetime.date(2018, 3, 12))
    cert2 = Certificate("6K Max Stock", 6000, 3.44, 12, datetime.date(2018, 3, 12))
    certificates.certificates.append(cert1)
    certificates.certificates.append(cert2)

    actual = certificates.getAnnualEarningsAll(2017,2020)

    assert(isinstance(actual, list))
    assert(len(actual) == 2)
    assert(actual[0].get("name") == "3K Max Stock")
    assert(actual[1].get("name") == "6K Max Stock")
    assert(isinstance(actual[0], dict))
    assert(isinstance(actual[1], dict))
    assert(len(actual[0].get("earnings")) == 4)
    assert(len(actual[1].get("earnings")) == 4)

@mock.patch("app.Certificates.Certificate")
def test_certificates_getAnnualEarningsById(mockCertificate):

    mockCertificate.name = "3K Max Stock"
    data = [{'endDate': datetime.date(2018, 12, 31), 'interest': 84.5744874176271, 'startDate': datetime.date(2018, 3, 12), 'value': 3084.574487417627}, {'endDate': datetime.date(2019, 3, 12), 'interest': 20.416049623031086, 'startDate': datetime.date(2019, 1, 1), 'value': 3104.990537040658}]
    mockCertificate.getAnnualGrowth.return_value = data
    certificates.certificates.append(mockCertificate)

    actual = certificates.getAnnualEarningsById("3K Max Stock", 2018, 2019)

    mockCertificate.getAnnualGrowth.assert_called_with(2018, 2019)
    assert(isinstance(actual[0], dict))
    assert(len(actual[0].get("earnings")) == 2)

@mock.patch("app.Certificates.Certificate")
def test_certificates_getAnnualEarningsById_whenCertDoesNotExist(mockCertificate):
    with pytest.raises(TypeError) as e:
        actual = certificates.getAnnualEarningsById("3K Max Stock", 2018, 2019)
import datetime

investments = {
    "cds" : [{
            "name" : "3K Max CD",
            "principal" : 3000,
            "rate" : 3.40,
            "time" : 12,
            "start" : datetime.date(2018,3,12) 
        },
        {
            "name" : "5K Max CD",
            "principal" : 5000,
            "rate" : 2.230,
            "time" : 9,
            "start" : datetime.date(2018,10,5)
        }
    ],
    "stocks" :[{
        "ticker" : "SIX",
        "buys" : [{
            "shares" : 0.23356,
            "price" : 64.1372,
            "date" : datetime.date(2018,9,14)
        },{
            "shares" : 20.0,
            "price" : 69.9705,
            "date" : datetime.date(2018,3,5)
        }],
        "sells" : []
    }]
}
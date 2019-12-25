# Investments

## Types of Investments

* cds - Array of certificate of deposits values
    * name: a unqiue string value for identifying the CD
    * principal: integer dollar value greater that 0
    * rate: float percentage value greater that 0.0
    * time: integer number of months greater that 0
    * start: datetime.date
* stocks
    * ticker: a valid US ticker symbol
    * buys: trade information
    * sells: trade information

NOTE: trade information consist an array of dictionay containing shares (integer), price (integer), date (datetime)

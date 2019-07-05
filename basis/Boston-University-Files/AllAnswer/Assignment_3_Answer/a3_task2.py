# Stock Returns and Statistice

# Mission 1.
def calc_returns(prices):
    # Function will process a list of stock prices
    # and calculate the periodic returns(1 to n).
    # Assume the oldest price is in prices[0]
    # and latest price in prices[-1].

    # The periodic rate of return is calculate as the
    # rate of change in price from the previous period.
    # Ri = (Pi / Pi_1) - 1
    period = []
    for period_n in range(1,len(prices)):
        period.append(prices[period_n] / prices[period_n - 1] - 1)

    return period

# Mission 2.
def process_stock_prices_csv(filename):
    # Function will process a data file containing
    # stock price data, and return a list of stock prices,
    # File was recorded in Comma Separate Values(CSV) format(ps).
    # prices = [['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    prices = []
    priceHolder = ['']
    i = 0
    splitTag = True                # As a tag for discard date
    with open(filename, "r") as priceDateFile:
        priceDateFile.readline()
        for Date in priceDateFile.read():
            if Date == '\n' :       # Line end, append priceHolder to prices list
                priceHolder[-1] = float(priceHolder[-1])
                prices.append(priceHolder)
                priceHolder = ['']   # Then clear the priceHolder
                i = 0
                splitTag = True      # Discard tag reset
            elif Date == ',':
                if splitTag == True: # Close the split door
                    splitTag = False
                    continue
                priceHolder[i] = eval(priceHolder[i])
                priceHolder.append('')
                i += 1
            elif splitTag == False: # splitTag disappear, add price data
                priceHolder[i] += Date
    return prices

def Test():
    prices = [100, 110, 105, 112, 115]
    print(calc_returns(prices))

    fileName = "L:\WeeklyHomeworks\Assignment 3 — MF 703, Boston University_files\AAPL.csv"
    print(process_stock_prices_csv(fileName))


# Mission 3.
from a3_task1 import *
def stock_report():
    # Function as a client program to process stock
    # prices and display descriptive statistics about
    # the stocks. This program will process several CSV
    # files to obtain stock prices (for the same time periods)
    # for 5 different stocks, and produce several outputs.
    stockMarketIndex = []
    stock_close_price = []
    myFileRutine = "L:\WeeklyHomeworks\Assignment 3 — MF 703, Boston University_files\\"
    while True:
        stock = input("Entry a list of Stock Market Index, split by enter key, " + '\n' \
                      + "End with word(quit) -> : ").strip().upper()
        if stock == 'QUIT':
            break
        stockMarketIndex.append(stock)

    # Print format
    print("\t\t{}\t{}\t{}\t{}\t{}\t{}".format('Descriptive', 'statistics', 'for', 'annual', 'stock', 'returns : '))
    print("Symbol:\t\t", end = '')

    # Process and append the prices data into stockData list
    # Here using function stock_data_process, and calc_returns
    for stockMarketIndexName in stockMarketIndex:
        stock_data_process = process_stock_prices_csv(myFileRutine + stockMarketIndexName + '.csv')
        stock_close_price_temp = []
        for i in range(len(stock_data_process)):
            # Only get Adj Close positon in [i][-2]
            stock_close_price_temp.append(stock_data_process[i][-2])

        if stockMarketIndexName == 'VTMSX':
            # We want to compare each stock to the stock market index(VTMSX)
            # So I make a independent List
            VTMSX = calc_returns(stock_close_price_temp)   # Get a Adj Close Prices, Return a list
            continue

        # Get a Adj Close Prices, Return a list
        stock_close_price.append(calc_returns(stock_close_price_temp))

    # Deal with the Mean, Varianve, Stdev, Covariance, Correlation,
    # Rsq, Beta, Alpha and Returns of each Stock
    stock_descriptive = []
    for i in range(len(stockMarketIndex) - 1):  # No including VTMSX stock
        stock_descriptive_temp = []
        stock_descriptive_temp.append(mean(stock_close_price[i]))
        stock_descriptive_temp.append(variance(stock_close_price[i]))
        stock_descriptive_temp.append(stdev(stock_close_price[i]))
        stock_descriptive_temp.append(covariance(stock_close_price[i], VTMSX))
        stock_descriptive_temp.append(correlation(stock_close_price[i], VTMSX))
        stock_descriptive_temp.append(rsq(stock_close_price[i], VTMSX))

        # Append the above information into stock_descriptive
        stock_descriptive.append(stock_descriptive_temp)

    VTMSX_temp = VTMSX
    VTMSX[0] = mean(VTMSX_temp)
    VTMSX[1] = variance(VTMSX_temp)
    VTMSX[2] = stdev(VTMSX_temp)

    # Print the Stock Name
    for eachStock in stockMarketIndex:
        print(eachStock + '  \t\t', end = '')

    print()
    # Print data
    Descriptive = ['Mead: ', 'Varia: ', 'StDev: ', 'Covar: ', 'Correl:', 'R-SQ: ']
    for i in range(len(Descriptive)):
        print(Descriptive[i] + '\t\t', end = '')
        for j in range(len(stock_descriptive)):
            print("{:.4f}\t\t".format(stock_descriptive[j][i]), end = '')

        # For print data of VTMSX
        if i < 3:
            print("{:.4f}\t\t".format(VTMSX[i]))
        else:
            print()

if __name__ == '__main__':
    stock_report()














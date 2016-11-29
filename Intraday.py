from bs4 import BeautifulSoup
try:
	from urllib2 import urlopen
except:
	from urllib.request import urlopen
import sys
import datetime
import matplotlib.pyplot as plt


url = 'https://www.google.com/finance/getprices?q=%s&i=%s&p=%sd&f=d,o,h,l,c,v'
#ticker, seconds, days

class Intraday(object):
    '''
    This class retrieves the intraday stock values and then uses the data to calculate timely fluxuations
    '''

    def __init__(self, ticker, seconds, days, url):
        self.ticker = ticker
        self.seconds = seconds
        self.days = days
        self.url = url
        self.intra = []

    def gather(self):
        '''
        Retrives page source data from the given url.
        All data should be written in page source.
        '''
        try:
            html = urlopen(self.url % (self.ticker, self.seconds, self.days)).read()
            return(BeautifulSoup(html, 'lxml'))
        except:
            print('404 Error: %s' % self.ticker)

    def printOut(self):
        '''
        Takes the data from gather and prints out a readable version
        '''
        answer =  self.gather()
        return(str(answer)[15:-18])

    def UnixTimeConverter(self, time):
        """
        Useless
        """
        print(datetime.datetime.fromtimestamp(int('%s' % time)).strftime('%Y-%m-%d %H:%M:%S'))

    def saveData(self):
        '''
        In oder to write the data into a text file, it needs to take in a printed statement.
        '''
        """sys.stdout = open('rawData.txt', 'w')
                                self.printOut()"""
        with open("rawData.txt", "w") as myfile:
            myfile.write('%s' % self.printOut())

    def readData(self, printExchange = False, printData = True):
        '''
        It retrieves the saved data from data.txt and reads it.
        It will output the Exhange (NYSE, NASDAQ, or what not) if requested.
        The function also takes the input of the jumbled data, and turns it into organized lists
        so the lists is capable of being parced easily.
        '''
        priceList = []
        with open("rawData.txt") as f:
            content = f.readlines()
            Exchange = ('Exchange: ' + content[0][11:])
            if printExchange == True:
                print(Exchange)
            data = content[7:-1]
            for priceRow in data:
                prices = priceRow.split(',')[1:-1]
                priceList.append(float(prices[-1]))
        if printData == True:
            print(priceList)
        else:
            return(priceList)

    def priceChange(self, printChange = True):
        '''
        Calculates the change between daily stock values.
        '''
        priceList = self.readData(printData = False)
        changeList = []
        for stockPoint in range(len(priceList)-1):
            changeList.append(float('%.4f' % ((priceList[stockPoint+1] - priceList[stockPoint])*\
                (100/priceList[stockPoint]))))
        if printChange == True:
            print(len(changeList))
        else:
            return(changeList)

    def countChangeRecurrences(self, gapVar):
        '''
        Counts the number of times that a stock has a gapup above a given amount
        '''
        Counter = 0
        changeList = self.priceChange(printChange=False)
        for stockPoint in changeList:
            if stockPoint >= gapVar:
                Counter += 1
                print(stockPoint)
        print(Counter)

    def readStartTime(self):
        '''
        Prints the starts time (the date as of x-days ago)
        ****Useless****
        '''
        with open("rawData.txt") as f:
            StartTime = data[0][1:11]

    def createPlot(self, Change = True):
        '''
        Creates graphs for the function.  The x-axis is time intervals and the y-axis is price change.
        '''
        if Change == True:
            dataList = self.priceChange(printChange=False)
        else:
            dataList = self.readData(printData = False)
        plt.figure()
        x_series = [i for i in range(len(dataList))]
        y_series = dataList
        plt.plot(x_series, y_series)
        plt.savefig("%s.png" % self.ticker)
        plt.close()

    def saveTickerData(self):
        priceList = self.readData(printData = False)
        changeList = self.priceChange(printChange=False)
        allData = [self.ticker, priceList, changeList]
        sys.stdout = open('%s.txt' % self.ticker, 'w')
        print(allData)
        
def createMasterDictionary(Exchange, printTicker = True):
    '''
    Iterates through every stock in the Exchange list, and
    '''
    masterDict = {}
    for ticker in Exchange[1:]:
        if ticker[-1] == ":":
            ticker = ticker[:-1]
        I = Intraday("%s" % ticker, 1800, 10, url)
        I.saveData()
        masterDict[ticker] = I.readData(printData = False)
    return(masterDict)

if __name__ == '__main__':
    #1800 seconds = 30 minutes
    def chooseExchangeList(Exchange):
        exchange = open("%s.txt" % Exchange).read().splitlines()[0:]
        exchange = [ticker.split(' ')[0] for ticker in exchange]
        print(createMasterDictionary(exchange))

    chooseExchangeList("15BelowNASDAQ")

    
    #I = Intraday("AAPL", 3600, 10, url)
    #I.saveData()
    #I.printOut()
    

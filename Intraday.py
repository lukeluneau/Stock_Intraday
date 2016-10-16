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
        answer =  self.gather()
        print(str(answer)[15:-18])

    def UnixTimeConverter(self, time):
        print(datetime.datetime.fromtimestamp(int('%s' % time)).strftime('%Y-%m-%d %H:%M:%S'))

    def saveData(self):
        sys.stdout = open('data.txt', 'w')
        self.printOut()

    def readData(self, printExchange = False, printData = True):
        priceList = []
        with open("data.txt") as f:
            content = f.readlines()
            Exchange = ('Exchange: ' + content[0][11:])
            if printExchange == True:
                print(Exchange)
            data = content[7:-1]
            for priceRow in data:
                for price in priceRow.split(',')[1:-1]:
                    priceList.append(float(price))
        if printData == True:
            print(priceList)
        else:
            return(priceList)

    def priceChange(self, printChange = True):
        priceList = self.readData(printData = False)
        changeList = []
        for price in range(len(priceList)-1):
            changeList.append(float('%.4f' % ((priceList[price+1] - priceList[price])*\
                (100/priceList[price]))))
        if printChange == True:
            print(changeList)
        else:
            return(changeList)

    def readStartTime(self):
        with open("data.txt") as f:
            StartTime = data[0][1:11]

    def createPlot(self):
        changeList = self.priceChange(printChange=False)
        plt.figure()
        x_series = [i for i in range(len(changeList))]
        y_series = changeList
        plt.plot(x_series, y_series)
        plt.savefig("%s.png" % self.ticker)


if __name__ == '__main__':
    I = Intraday("GOOGL", 1800, 10, url)
    #I.printOut()
    #I.saveData()
    #I.readData()
    #I.priceChange()
    I.createPlot()

'''
Robot Web-Scraping Etiquette Compiler
'''

from bs4 import BeautifulSoup
try:
	from urllib2 import urlopen
except:
	from urllib.request import urlopen

import sys

import datetime

from math import ceil


Companies = ['https://www.google.com/finance/getprices?q=%s&i=600&p=10d&f=d,o,h,l,c,v']


def Gather(url):
	'''
	Retrives page source data from the given url.
	All data should be written in page source.
	'''
	try:
		html = urlopen(url).read()
		return BeautifulSoup(html, 'lxml')
	except:
		print('404 Error')

def PrintOut(ticker):
	'''
	Initiates the Gather function on all companies.
	'''
	for company in Companies:
		answer =  Gather(company % ticker)
		print(str(answer)[15:-18])

def UnixTimeConverter(time):
	print(datetime.datetime.fromtimestamp(int('%s' % time)).strftime('%Y-%m-%d %H:%M:%S'))

def DeltaCount():
	global Change
	count = 0
	for i in Change:
		if i[1] >= .1:
			count += 1
	print(count)

def Execute(Company):
	PrintOut("%s" % Company)
	sys.stdout = open('data.txt', 'w')
	PrintOut("%s" % Company)

Price = []
Change = []

def Execute():
	global Price
	global Change

	with open("data.txt") as f:
		content = f.readlines()
		Exchange = ('Exchange: ' + content[0][11:])
		print(Exchange)
		Data = content[7:-1]
		StartTime = Data[0][1:11]
		UnixTimeConverter(StartTime)
		for i in Data:
			dateSet = i.split(",")[1:-1]
			for d in dateSet:
				Price.append(d)
		for i in range(len(Price)-1):
			dollar_change = (float(Price[i+1]))-float(Price[i])
			dollar_change = ceil(dollar_change*100)/100.0
			percent = ceil(float(dollar_change/float(Price[i])) * 100) / 100.0
			Change.append([dollar_change, percent])
		
def Printable():
	global Price
	global Change
	#print(Price)
	print('There were --%s-- data points taken.' % len(Price))
	print(Change)


Execute()
Printable()
DeltaCount()



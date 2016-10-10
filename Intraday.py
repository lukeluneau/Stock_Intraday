import requests
import csv
import datetime
import re

def get_intraday(ticker, interval, days):

	url = 'https://www.google.com/finance/getprices?q=%s&i=%s&p=%sd&f=d,o,h,l,c,v' % (ticker, interval, days)

	page = requests.get(url)
	reader = csv.reader(page.content.splitlines())
	columns = ['Open', 'High', 'Low', 'Close', 'Volume']
	rows = []
	times = []
	print(reader)
	'''
	for row in reader:
		if re.match('^[a\d]', row[0]):
			if row[0].startswith('a'):
				start = datetime.datetime.fromtimestamp(int(row[0][1:]))
				times.append(start)
			else:
				times.append(start+datetime.timedelta(seconds=period*int(row[0])))
			rows.append(map(float, row[1:]))
	'''
get_intraday("APPL", 30000, 10)
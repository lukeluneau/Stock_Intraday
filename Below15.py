from yahoo_finance import Share
import sys

NYSE = ['NYSE'] + open('NYSE.txt').read().splitlines()
NASDAQ = ['NASDAQ'] + open("NASDAQ.txt").read().splitlines()
AMEX = ['AMEX'] + open("AMEX.txt").read().splitlines()


class Below15(object):

	def __init__(self, Exchange):
		self.ExchangeName = Exchange[0]
		self.Exchange = sorted(Exchange[1:])

	def makeList(self):
		Stock_list = []
		for stock in self.Exchange:
			try:
				yahoo = Share("%s" % stock)
				price_open = yahoo.get_open()
				if price_open is not None:
					if float(price_open) < 15:
						change = yahoo.get_change()
						try:
							stock = stock.split(" ")[0]
						except:
							pass
						info = ("%s: $%s, %s" % (stock, price_open, change))
						print(info)
						Stock_list.append([stock, price_open])
			except:
				pass

		Stock_list = sorted(Stock_list)
		## Creates Text File
		sys.stdout = open('15Below%s.txt' % self.ExchangeName, 'w')


if __name__ == '__main__':

	Exchanges = [NYSE, NASDAQ, AMEX]
	for E in Exchanges:
		print(E)
		print(Below15(E).makeList())
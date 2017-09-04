import re
import requests


def sortByMarketCup(list):
	return sorted(list, key=lambda crypto: crypto[0], reverse=True)

def sortByCurentPrice(list):
	return sorted(list, key=lambda crypto: crypto[1])

def getListCryptos():
	return requests.get('https://coinmarketcap.com/all/views/all/')


def processResponseAndGetText(response):
	text = response.text.encode('utf-8')
	return text.split('tbody')[1]
	

def getRelevantSortedCryptosList():
	text = processResponseAndGetText(getListCryptos())
	return parseCryptos(text)

def parseCryptos(inputText):

	cryptoListParse = []

	cryptos = inputText.split('\n')

	crypto = ''
	shouldAppend = False

	for line in cryptos:
		# line = cryptos[i]
		
		if "</tr>" in line:
			shouldAppend = False
			cryptoListParse.append(crypto)
			crypto = ''

		if "<tr id" in line:
			shouldAppend = True

		if shouldAppend:
			crypto += line

	cryptoList = []


	for cryptoData in cryptoListParse:
		mFound = re.findall(r'market-cap\stext-right\"\sdata-usd=\"\d+\.?\d+', cryptoData)

		if len(mFound) == 0:
			break

		marketCup = float(mFound[0][33:])

		if marketCup < 1000000:
			continue

		curPrice = float(re.findall(r'class=\"price\"\sdata-usd=\"\d+\.?\d+', cryptoData)[0][24:])


		totalSup = re.findall(r'data-supply=\"\d+\.?\d+', cryptoData)
		
		if len(totalSup) == 0:
			break

		totalSupply = float(totalSup[0][13:])

		name = re.findall(r'id=\"id-.+\"\s\sc', cryptoData)[0][7:-4]
	

		posReg = re.findall(r'text-center\"\>\s+\d+', cryptoData)

		positionInCoinMarket = posReg[0][14:].strip()


		if totalSupply > 10000000 and totalSupply < 100000000:
			cryptoList.append((marketCup, curPrice, str(totalSupply / 1000000) + 'm' , name, positionInCoinMarket))



	return sortByCurentPrice(cryptoList)
	

def printList(list, rangeNum):
	for i in range(rangeNum):
		print('\r\nName: %s, Price: %s, Market: %d, Position in coinmarket: %s' % (list[i][3], str(list[i][1]), list[i][0], list[i][4]))

def printTitle():
    print("|=========================================================|")
    print("|                 Cryptocurrency Parser                   |")
    print("|              Developed by Maxim Pogorelov               |")
    print("|  LinkedIn: https://www.linkedin.com/in/pogorelovmaxim   |")
    print("|    Facebook: https://www.facebook.com/pohorielov.max    |")
    print("|=========================================================|\n\n")

printTitle()

list = getRelevantSortedCryptosList()

printList(list, 20)
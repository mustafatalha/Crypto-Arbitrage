from JSONAnalysis import JSONAnalysis
from CoinObject import CoinObject
from requests import get
import logging

logging.basicConfig(filename='App.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

#Create a CoinObject list for every coin in ArbitrageList
def setCoinList(jsonAnalysis):
    coinList = []
    try:
        for item in jsonAnalysis.getArbitrageMarketList():
            poloBid = jsonAnalysis.getPoloniexJson()["BTC_"+item]["highestBid"]
            poloAsk = jsonAnalysis.getPoloniexJson()["BTC_"+item]["lowestAsk"]

            id = jsonAnalysis.getBittrexResultArrIndexList()[item]
            bitBid = jsonAnalysis.getBitrexJson()["result"][id]["Bid"]
            bitAsk = jsonAnalysis.getBitrexJson()["result"][id]["Ask"]

            coinList.append(CoinObject(item,poloBid,poloAsk,bitBid,bitAsk))
    except Exception as ex:
        logging.error("Error: %s"%getattr(ex, 'message', repr(ex)))
    logging.info("coinList has been set")
    return coinList

#Arbitrage Volume Calculator
def calculateVolume(name, buyPlatform):
    try:
        bittrexLink = "https://bittrex.com/api/v1.1/public/getorderbook?market=BTC-%s&type=both" % name
        poloniexLink = "https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_%s&depth=10000" % name
        bJson = get(bittrexLink).json()
        pJson = get(poloniexLink).json()
        i = 0
        volume = 0
        volume_btc = 0
        if buyPlatform == 'Bittrex':
            buy = float(bJson['result']['sell'][0]['Rate'])
            while True:
                bid = float(pJson['bids'][i][0])
                if bid < buy:
                    break
                volume += float(pJson['bids'][i][1])
                volume_btc += float(pJson['bids'][i][1])*float(pJson['bids'][i][0])
                i += 1
        elif buyPlatform == 'Poloniex':
            buy = float(pJson['asks'][0][0])
            while True:
                bid = float(bJson['result']['buy'][i]['Rate'])
                if bid < buy:
                    break
                volume += float(bJson['result']['buy'][i]['Quantity'])
                volume_btc += float(bJson['result']['buy'][i]['Quantity'])*float(bJson['result']['buy'][i]['Rate'])
                i += 1
        return {'Volume': volume, 'BtcVolume': volume_btc}
    except Exception as ex:
        logging.error("Error: %s"%getattr(ex, 'message', repr(ex)))
        return {'Volume': 0, 'BtcVolume': 0}

#All magic comes true in here
def arbitrageManager(jsonAnalysis):
    arbitrageList = []
    dict = {}
    for coin in coinList:
        #Check if coin market is active or not
        if (jsonAnalysis.isActiveOnBit(coin.getName())) and (jsonAnalysis.isActiveOnPolo(coin.getName())):
            poloSellRate = 100 * (coin.getPoloBid() - coin.getBitAsk()) / coin.getBitAsk()
            bittSellRate = 100 * (coin.getBitBid() - coin.getPoloAsk()) / coin.getPoloAsk()

            if(poloSellRate > 0.5):
                volDict = calculateVolume(coin.getName(),'Bittrex')
                cDict = {"Name" : coin.getName(),
                    "BuyPlatform" : 'Bittrex',
                    "SellPlatform" : 'Poloniex',
                    "BuyPrice" : "%.8f"%coin.getBitAsk(),
                    "SellPrice" : "%.8f"%coin.getPoloBid(),
                    "ProfitRate" : "%.2f"%poloSellRate,
                    "Volume:" : "%.2f"%volDict['Volume'],
                    "BtcVolume" : "%.2f"%volDict['BtcVolume']}
                arbitrageList.append(cDict)
            elif(bittSellRate > 0.5):
                volDict = calculateVolume(coin.getName(),'Poloniex')
                cDict = {"Name" : coin.getName(),
                    "BuyPlatform" : 'Poloniex',
                    "SellPlatform" : 'Bittrex',
                    "BuyPrice" : "%.8f"%coin.getPoloAsk(),
                    "SellPrice" : "%.8f"%coin.getBitBid(),
                    "ProfitRate" : "%.2f"%bittSellRate,
                    "Volume:" : "%.2f"%volDict['Volume'],
                    "BtcVolume" : "%.2f"%volDict['BtcVolume']}
                arbitrageList.append(cDict)
    logging.info("arbitrageManager has been completed")
    return arbitrageList


while True:
    try:
        jsonAnalysis = JSONAnalysis()
        coinList = setCoinList(jsonAnalysis)
        List = arbitrageManager(jsonAnalysis)
        #You can do with this List whatever you want, Here I just print
        for i in List:
            print(i)
        logging.info("Arbitrage data has been printed")
        print("Waiting for next update")
        #You may add here a wait statement
    except Exception as ex:
        logging.error("Error: %s"%getattr(ex, 'message', repr(ex)))



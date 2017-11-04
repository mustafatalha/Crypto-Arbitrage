from requests import get
import logging

logging.basicConfig(filename='App.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

class JSONAnalysis:
    '''Exchange API links,
    MarketSummaries and Ticker to do market works, Currencies to look if market is active'''
    BIITREX_URL = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
    BITTREX_CUR_URL = "https://bittrex.com/api/v1.1/public/getmarkets"
    POLONIEX_URL = "https://poloniex.com/public?command=returnTicker"
    POLONIEX_CUR_URL = "https://poloniex.com/public?command=returnCurrencies"

    __bittrexJson = {}
    __bitCurJson = {}
    __poloniexJson = {}
    __poloCurJson = {}

    __bitMarketList = []
    __poloMarketList = []
    __bitActiveList = {}
    __poloActiveList = {}

    #There is a index problem in BittrexJson Result Array, so we need Coin : IndexNum dicitonary to handle it
    __bittrexJsonResultArrIndexList = {}
    __arbitrageMarketList = []

    def __init__(self):
        try:
            self.__bittrexJson = get(self.BIITREX_URL).json()
            self.__bitCurJson = get(self.BITTREX_CUR_URL).json()
            self.__poloniexJson = get(self.POLONIEX_URL).json()
            self.__poloCurJson = get(self.POLONIEX_CUR_URL).json()
        except Exception as ex:
            logging.error("Error: %s"%getattr(ex, 'message', repr(ex)))

        logging.info("Market jsons has been taken")
        self.__bitMarketList = self.setBittrexMarketList()
        self.__poloMarketList = self.setPoloniexMarketList()
        self.__arbitrageMarketList = self.setArbitrageMarketList()
        self.__bitActiveList = self.setBittrexActiveList()
        self.__poloActiveList = self.setPoloniexActiveList()
        self.__bittrexJsonResultArrIndexList = self.setResultArrIndexList()
        logging.info("jsonAnalysis object is created")

    #Set Bittrex Btc-Coin market lists (Coin List)
    def setBittrexMarketList(self):
        bitBtcMarketList = []
        try:
            for item in self.__bitCurJson["result"]:
                if item["BaseCurrency"] == "BTC":
                    bitBtcMarketList.append(item["MarketCurrency"])
            return bitBtcMarketList
        except Exception as ex:
            logging.error("Error: %s"%getattr(ex, 'message', repr(ex)))


    #Set Poloniex Btc-Coin market lists (Coin List)
    def setPoloniexMarketList(self):
        poloBtcMarketList = []
        try:
            for item in self.__poloniexJson.keys():
                if item[0:3] == "BTC":
                    poloBtcMarketList.append(item[4:])
            return poloBtcMarketList
        except Exception as ex:
            logging.error("Error: %s"%getattr(ex, 'message', repr(ex)))
    #Set list of coins that arbitrage can be happen
    def setArbitrageMarketList(self):

        #List of coins that exist on both Bittrex and Poloniex
        arbitrageMarketList = []
        for item in self.__poloMarketList:
            if item in self.__bitMarketList:
                arbitrageMarketList.append(item)

        return arbitrageMarketList

    #Set List of coin's activity on Bittrex as dictionary
    def setBittrexActiveList(self):
        activeList = {}
        try:
            for item in self.__bitCurJson['result']:
                if item['MarketCurrency'] in self.__arbitrageMarketList:
                    activeList[item['MarketCurrency']] = item['IsActive']
            return activeList
        except Exception as ex:
            logging.error("Error: %s"%getattr(ex, 'message', repr(ex)))

    #Set List of coin's activity on Poloniex as dicitionary
    def setPoloniexActiveList(self):
        activeList = {}
        try:
            keys = self.__poloCurJson.keys()
            for item in keys:
                if item in self.__arbitrageMarketList:
                    if not self.__poloCurJson[item]["delisted"]:
                        activeList[item] = self.__poloCurJson[item]["disabled"]
            return activeList
        except Exception as ex:
            logging.error("Error: %s"%getattr(ex, 'message', repr(ex)))

    def setResultArrIndexList(self):
        i = 0
        resultArrIndexList = {}
        try:
            for item in self.__bittrexJson["result"]:
                if item["MarketName"][0:3] == 'BTC':
                    resultArrIndexList[item["MarketName"][4:]] = i
                    i += 1
            return resultArrIndexList
        except Exception as ex:
            logging.error("Error: %s"%getattr(ex, 'message', repr(ex)))

    #Check if a coin's market active on Bittrex
    def isActiveOnBit(self, name):
        if name in self.__bitActiveList:
            return self.__bitActiveList[name]
        else:
            return False

    #Check if a coin's market active on Poloniex
    def isActiveOnPolo(self, name):
        if name in self.__poloActiveList:
            return not self.__poloActiveList[name]
        else:
            return False

    def getArbitrageMarketList(self):
        return self.__arbitrageMarketList

    def getBitrexJson(self):
        return self.__bittrexJson

    def getPoloniexJson(self):
        return self.__poloniexJson

    def getBittrexResultArrIndexList(self):
        return self.__bittrexJsonResultArrIndexList




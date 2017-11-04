class CoinObject:
    def __init__(self, name, poloBid, poloAsk, bitBid, bitAsk):
        self.__name = str(name);
        self.__poloBid = float(poloBid)
        self.__poloAsk = float(poloAsk)
        self.__bitBid = float(bitBid)
        self.__bitAsk = float(bitAsk)

    def getPoloniexType(self):
        return "BTC_"+self.__name

    def getBittrexType(self):
        return "BTC-"+self.__name

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getPoloBid(self):
        return self.__poloBid

    def setPoloBid(self, poloBid):
        self.__poloBid = poloBid

    def getPoloAsk(self):
        return self.__poloAsk

    def setPoloAsk(self, poloAsk):
        self.__poloAsk = poloAsk

    def getBitBid(self):
        return self.__bitBid

    def setBitBid(self, bitBid):
        self.__bitBid = bitBid

    def getBitAsk(self):
        return self.__bitAsk

    def setBitAsk(self, bitAsk):
        self.__poloAsk = bitAsk

    def toString(self):
        return ("Name: %s PoloniexBid: %.8f PoloniexAsk: %.8f BittrexBid: %.8f BittrexAsk %.8f" %
                (self.__name, self.__poloBid, self.__poloAsk, self.__bitBid, self.__bitAsk))


class ModelSokoban:
    def __init__(self):
        self.__view = None
        self.__ground = []
        self.__crates = []
        self.__stars = []
        self.__walls = []
        self.__player = []
        self.__traps = []
        self.__activeTraps = []
        self.__teleport = []
        self.__level = 1
        self.__nbStep = 0
        self.__win = False
        self.__crateOnStar = []
        self.__size = [0,0]
    
    def getSize(self):
        return self.__size
    
    def getGround(self):
        return self.__ground

    def getCrates(self):
        return self.__crates

    def getStars(self):
        return self.__stars

    def getWalls(self):
        return self.__walls

    def getPlayer(self):
        return self.__player

    def getTraps(self):
        return self.__traps

    def getActiveTraps(self):
        return self.__activeTraps
    
    def getTeleport(self):
        return self.__teleport
    
    def getLevel(self):
        return self.__level

    def getNbStep(self):
        return self.__nbStep

    def getGameOn(self):
        return self.__gameOn

    def getWin(self):
        return self.__win
    
    def getCrateOnStar(self):
        return self.__crateOnStar
            
    def setGround(self,ground):
        self.__ground = ground

    def setCrates(self, crates):
        self.__crates = crates
    
    def setStars(self, stars):
        self.__stars = stars

    def setWalls(self, walls):
        self.__walls = walls

    def setPlayer(self, player):
        self.__player = player
    
    def setTraps(self, traps):
        self.__traps = traps

    def setActiveTraps(self,activeTraps):
        self.__activeTraps = activeTraps

    def setTeleport(self,teleport):
        self.__teleport = teleport

    def setLevel(self, level):
        self.__level = level
    
    def setNbStep(self, nbStep):
        self.__nbStep = nbStep

    def setGameOn(self, gameOn):
        self.__gameOn = gameOn

    def setWin(self, win):
        self.__win = win

    def setCrateOnStar(self, crateOnStar):
        self.__crateOnStar = crateOnStar
        
    def setView(self,view) :
        self.__view = view
        
    def setSize(self,size):
        self.__size = size


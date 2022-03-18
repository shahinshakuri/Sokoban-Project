import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.Qt import QSound

class ControllerSokoban :
    def __init__(self):
        self.__model = None
        self.__view = None
        self.__countTP = 0
        
    def setModel(self,model):
        self.__model = model
    
    def setView(self,view):
        self.__view = view
      
    def checkWin(self):

        if len(self.__model.getCrateOnStar())==len(self.__model.getCrates()):
            self.__model.setWin(True)

      
    def pushCrates(self,direction, crate):

        init = self.__model.getCrates().copy() #Initial crate array position

        move = direction
        move = (move[0] + int(self.__model.getCrates()[crate][0]),move[1] + int(self.__model.getCrates()[crate][1])) # Futur crate position
        tmp = self.__model.getCrates().copy() #Futur crate array position
        tmp.remove(init[crate])
        tmp.append(move)
        self.__model.setCrates(tmp)

        if(move in self.__model.getStars()):
            tmp = self.__model.getCrateOnStar().copy()
            tmp.append(move)
            self.__model.setCrateOnStar(tmp)

            

        #Actions if on wall or if crate on crate
        if (move in self.__model.getWalls() or move in init):
            move = (move[0] - direction[0],move[1] - direction[1])
            self.__model.setCrates(init)
            return False

        self.checkOnStar()

        return True
    
    def teleportOn(self):

        if(self.__model.getTeleport()[1] not in self.__model.getCrates() and self.__countTP == 0):
            if(self.__model.getTeleport()[0] in self.__model.getCrates()):
                copy = self.__model.getCrates().copy()
                copy.remove(self.__model.getTeleport()[0])
                copy.append(self.__model.getTeleport()[1])
                self.__model.setCrates(copy)
                self.__countTP += 1
                self.sound.play()
            elif(self.__model.getTeleport()[0] == self.__model.getPlayer()):
                self.__model.setPlayer(self.__model.getTeleport()[1])
                self.__countTP += 1

            

            
        if(self.__model.getTeleport()[0] not in self.__model.getCrates() and self.__countTP == 0):
            if(self.__model.getTeleport()[1] in self.__model.getCrates()): 
                copy = self.__model.getCrates().copy()
                copy.remove(self.__model.getTeleport()[1])
                copy.append(self.__model.getTeleport()[0])
                self.__model.setCrates(copy)
                self.__countTP += 1
                self.sound.play()
            elif(self.__model.getTeleport()[1] == self.__model.getPlayer()):
                self.__model.setPlayer(self.__model.getTeleport()[0])
                self.__countTP += 1



    
    def movePlayer(self,direction):
        if self.__model is not None :

            assert abs(direction[0] + direction[1]) ==1
            move = direction
            move = (move[0] + self.__model.getPlayer()[0],move[1] + self.__model.getPlayer()[1])
            self.__model.setPlayer(move)
            
            #Check player on crate
            for i in range(len(self.__model.getCrates())):
                    if (self.__model.getCrates()[i][0] == self.__model.getPlayer()[0] and self.__model.getCrates()[i][1] == self.__model.getPlayer()[1]):
                        if (not self.pushCrates(direction,i)):
                            move = (move[0] - direction[0],move[1] - direction[1])
                            self.__model.setPlayer(move)
            
            #Check player on wall            
            if (move in self.__model.getWalls()):
                move = (move[0] - direction[0],move[1] - direction[1])
                self.__model.setPlayer(move)
                return
             
             
            if (self.__model.getNbStep()%2 != 0): #If player have activated a trap
                self.__model.setActiveTraps([])
            elif( self.__model.getNbStep()%2 == 0):
                copy = self.__model.getTraps().copy()
                self.__model.setActiveTraps(copy)

            
                    
            #Teleporter Gestion
            if(self.__countTP > 0):
                self.__countTP += 1
            if(self.__countTP == 4):
                self.__countTP = 0
            if(len(self.__model.getTeleport()) == 2):
                self.teleportOn()

            #UI check
            
            self.__model.setNbStep(self.__model.getNbStep() + 1)
            if (self.__model.getPlayer() in self.__model.getActiveTraps()):
                self.setGame()
                self.__view.majInterface()
            self.checkWin()

    def checkOnStar(self):
        for i in range(len(self.__model.getStars())):
            if (self.__model.getStars()[i] in self.__model.getCrates() and self.__model.getStars()[i] not in self.__model.getCrateOnStar()):
                tmp = self.__model.getCrateOnStar().copy()
                tmp.append(self.__model.getStars()[i])
                self.__model.setCrateOnStar(tmp)
                
                self.sound.play()
            elif (self.__model.getStars()[i] not in self.__model.getCrates() and self.__model.getStars()[i] in self.__model.getCrateOnStar()) :
                tmp = self.__model.getCrateOnStar().copy()
                tmp.remove(self.__model.getStars()[i])
                self.__model.setCrateOnStar(tmp)

    
    def setGame(self):
        #Reset
        self.__model.setWalls([])
        self.__model.setGround([])
        self.__model.setStars([])
        self.__model.setPlayer([])
        self.__model.setCrates([])
        self.__model.setStars([])
        self.__model.setTraps([])
        self.__model.setActiveTraps([])
        self.__model.setCrateOnStar([])
        self.__model.setTeleport([])
        self.__model.setWin(False)
        self.__model.setNbStep(0)
        
        mainPath = os.getcwd()+"/Assets/Levels"
        l = 0
        c = 0
        file = open(mainPath + "/levelSize_"+ str(self.__model.getLevel()) +".txt", "r")
        for line in file:
            for i in range(len(line)):
                if(line[i] == ","):
                    self.__model.setSize([int(line[:i]),int(line[i+1:-1])])
        
        file = open(mainPath + "/level_"+ str(self.__model.getLevel()) +".txt", "r")
        for line in file:
            c=0
            for character in line:
                if character == "w" : #Wall
                    tmp = self.__model.getWalls().copy()
                    tmp.append((l,c))
                    self.__model.setWalls(tmp)
                    
                elif character == "g" : #Ground
                    tmp = self.__model.getGround().copy()
                    tmp.append((l,c))
                    self.__model.setGround(tmp)
                    
                    
                elif character == "s" : #Stars
                    tmp = self.__model.getStars().copy()
                    tmp.append((l,c))
                    self.__model.setStars(tmp)
                    
                elif character == "p" : #Player
                    self.__model.setPlayer((l,c))
                    
                    tmp = self.__model.getGround().copy()
                    tmp.append((l,c))
                    self.__model.setGround(tmp)
                    
                elif character == "c" : #Crate
                    tmp = self.__model.getCrates().copy()
                    tmp.append((l,c))
                    self.__model.setCrates(tmp)
                    
                    tmp = self.__model.getGround().copy()
                    tmp.append((l,c))
                    self.__model.setGround(tmp)
                    
                elif character == "x" : #Crate On Star
                    tmp = self.__model.getCrateOnStar().copy()
                    tmp.append((l,c))
                    self.__model.setCrateOnStar(tmp)
                    
                    tmp = self.__model.getStars().copy()
                    tmp.append((l,c))
                    self.__model.setStars(tmp)
                    
                    tmp = self.__model.getCrates().copy()
                    tmp.append((l,c))
                    self.__model.setCrates(tmp)
                    
                elif character == "t" : #Trap
                    tmp = self.__model.getTraps().copy()
                    tmp.append((l,c))
                    self.__model.setTraps(tmp)
                                
                elif character == "o" : #teleport
                    tmp = self.__model.getTeleport().copy()
                    tmp.append((l,c))
                    self.__model.setTeleport(tmp)
                c +=1
            l+=1

        
        
    def goNextLevel(self):
        self.__model.setLevel(self.__model.getLevel()+1)
        
        
        
    
        
        

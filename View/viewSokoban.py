from PyQt5.QtWidgets import QMainWindow,QWidget,QGridLayout,QLabel,QVBoxLayout,QPushButton,QMenu,QAction

from PyQt5.QtGui import QFont,QPixmap
from PyQt5.QtCore import Qt,QRect
import os

class ViewSokoban(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.__model = None
        self.__controller = None
        self.__dirPlayer = None
        
        self.setWindowTitle("Projet : Sokoban 0.1 !!")
        self.__window = QWidget()
        self.setCentralWidget(self.__window)


        self.__menuBar = self.menuBar()
        self.__gameMenu = QMenu("&Game",self)
        self.__menuBar.addMenu(self.__gameMenu)
        
        self.__exitProgram = QAction(self)
        self.__exitProgram.setText("&Quit")
        self.__gameMenu.addAction(self.__exitProgram)
        self.__exitProgram.triggered.connect(self.close)
        


        # Main Layout to put elements in column
        self.__mainLayout = QVBoxLayout()
        
        #First initialisation Game
        # grid WidgetType creation 
        self.__gridWidget = QWidget()
        self.__gridLayout = QGridLayout()
        self.__gridLayout.setSpacing(0)

        self.__gridLabel = [];
        self.__gridWidget.setLayout(self.__gridLayout)
        
        # Adding different widget to the main Layout
        self.__mainLayout.addWidget(self.__gridWidget)
        self.__window.setLayout(self.__mainLayout)

    
    def restartLevel(self):
        if (not self.__model.getWin()):
            self.__controller.setGame()
            self.majInterface()
    
    def setModel(self,model):
        self.__model = model
        
        counter = 0
        # Creation of the different cases
        for i in range(72):
            case = QLabel("",parent = self.__window)
            case.setFixedSize(72, 72)
            case.setFont(QFont("Arial",50,QFont.Bold))
            case.setAlignment(Qt.AlignCenter)
            self.__gridLabel.append(case)

        for i in range(9):
            for j in range(8):
                self.__gridLayout.addWidget(self.__gridLabel[counter],i,j)
                counter += 1   
        # label for scoring 
        self.__labelNbStep = QLabel("Number of steps : " + str(self.__model.getNbStep()))
        self.__labelNbStep.setFont(QFont("Arial",24,QFont.Bold))
        self.__labelNbStep.setAlignment(Qt.AlignCenter)
        self.__mainLayout.addWidget(self.__labelNbStep)
        

        
    def initGame(self): # Initalize the game UI to play
        # grid WidgetType creation
        self.__controller.setGame()
        self.__gridWidget = QWidget()
        self.__gridLayout = QGridLayout()
        self.__gridLayout.setSpacing(0)

        self.__gridLabel = [];
        self.__gridWidget.setLayout(self.__gridLayout)
        
        self.__labelNbStep = QLabel("Number of steps : " + str(self.__model.getNbStep()))
        self.__labelNbStep.setFont(QFont("Arial",24,QFont.Bold))
        self.__labelNbStep.setAlignment(Qt.AlignCenter)
        self.__mainLayout.addWidget(self.__labelNbStep)
        
        # Creation of the different cases
        counter = 0
        print(self.__model.getSize()[0]*self.__model.getSize()[1])
        for i in range(self.__model.getSize()[0]*self.__model.getSize()[1]):
            case = QLabel("",parent = self.__window)
            case.setFixedSize(72, 72)
            case.setFont(QFont("Arial",50,QFont.Bold))
            case.setAlignment(Qt.AlignCenter)
            self.__gridLabel.append(case)

        for i in range(self.__model.getSize()[1]):
            for j in range(self.__model.getSize()[0]):
                self.__gridLayout.addWidget(self.__gridLabel[counter],i,j)
                counter += 1
        self.setFixedSize(72*self.__model.getSize()[0]+25, 72*self.__model.getSize()[1] + 100)      
        self.__mainLayout.addWidget(self.__gridWidget)
        self.__mainLayout.addWidget(self.__labelNbStep)
        
 
    def setController(self,controller):
        self.__controller = controller
        self.__controller.setGame()
        self.setFixedSize(72*self.__model.getSize()[0]+25, 72*self.__model.getSize()[1] + 100)
        self.__restartLevel = QAction(self)
        self.__restartLevel.setText("&Restart")
        self.__gameMenu.addAction(self.__restartLevel)
        self.__restartLevel.triggered.connect(self.restartLevel)

    def majInterface(self):
        counter = 0
        self.__gridLabel[0].setFont(QFont("Arial",12,QFont.Bold))
        self.__gridLabel[0].setText("Press R  <br/>to retry")
        mainPath = os.getcwd()+"/Assets/Sprites" 
        for i in range(self.__model.getSize()[1]):
            for j in range(self.__model.getSize()[0]):
                if((i,j) in self.__model.getCrateOnStar()):
                    self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/CrateOnStar.jpg"))
                elif((i,j) == self.__model.getPlayer()):
                    self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/Player_Idle.jpg"))
                elif((i,j) in self.__model.getWalls()):
                    self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/Wall.jpg"))
                elif(len(self.__model.getTeleport()) != 0 and (i,j) == self.__model.getTeleport()[0]) :
                    self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/teleporter.jpg"))
                elif(len(self.__model.getTeleport()) != 0 and (i,j) == self.__model.getTeleport()[1]):
                    self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/teleporter.jpg"))
                elif((i,j) in self.__model.getCrates()):
                    self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/Crate.jpg"))
                elif((i,j) in self.__model.getStars()):
                    self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/Star.jpg"))
                elif((i,j) in self.__model.getActiveTraps()):
                     self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/spikeOn.jpg"))
                elif((i,j) in self.__model.getTraps()):
                     self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/spikeOff.jpg"))
                elif((i,j) in self.__model.getGround()):
                    self.__gridLabel[counter].setPixmap(QPixmap(mainPath + "/Ground.jpg"))
                else :
                    self.__gridLabel[counter].setStyleSheet("background-color : black; color : white;")
                counter+=1
                
        if not self.__model.getWin() :
            self.__labelNbStep.setText("Number of steps : " + str(self.__model.getNbStep()))
        elif self.__model.getWin() :
            self.__labelNbStep.setText("Level " + str(self.__model.getLevel()) + " : Complete !! <br/> Number of steps : " + str(self.__model.getNbStep()))
            self.__gridWidget.deleteLater()
            if self.__model.getLevel() == 5 :
                self.__nextLevel = QPushButton("Au revoir !")
            else :
                self.__nextLevel = QPushButton("Next Level !")
            self.__nextLevel.setFont(QFont("Arial",32,QFont.Bold))
            self.__nextLevel.setStyleSheet("color : black;background : green;")
            self.__nextLevel.clicked.connect(self.nextLevel)
            self.__mainLayout.addWidget(self.__nextLevel)
            self.setFixedSize(500,200)

            
    def keyPressEvent(self,event):
        if(not self.__model.getWin()):
            if(event.key() == 16777235 or event.key() == 90 ): #Top
                self.__controller.movePlayer((-1,0))
                self.majInterface()
            elif(event.key() == 16777236 or event.key() == 68 ) : #Right
                self.__controller.movePlayer((0,1))
                self.majInterface()
            elif(event.key() == 16777237 or event.key() == 83 ): #Bottom
                self.__controller.movePlayer((1,0))
                self.majInterface()
            elif(event.key() == 16777234 or event.key() == 81 ): #Left
                self.__controller.movePlayer((0,-1))
                self.majInterface()
            elif(event.key() == 82 or event.key() == 32):
                self.restartLevel()

    def nextLevel(self):
        self.__nextLevel.deleteLater()
        self.__labelNbStep.deleteLater()
        self.__controller.goNextLevel()
        if(self.__model.getLevel() <= 5):   
            self.__controller.setGame()
            self.initGame()
            self.majInterface()
        else :
            self.close()
        
    

    
        
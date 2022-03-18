import sys
from PyQt5.QtWidgets import QApplication
from Controller.controllerSokoban import ControllerSokoban
from Model.modelSokoban import ModelSokoban
from View.viewSokoban import ViewSokoban

app = QApplication(sys.argv)

model = ModelSokoban()
controller = ControllerSokoban()
basicView = ViewSokoban()

model.setView(basicView)
controller.setView(basicView)
controller.setModel(model)
basicView.setModel(model)
basicView.setController(controller)
basicView.majInterface()

basicView.show()

sys.exit(app.exec_())

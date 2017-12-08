# The code is placed into public domain by anatoly techtonik
# Feel free to copy/paste wherever you like

# Minimal PySide application with button for choosing color to paint itself
#
# NOTE: Setting color for a button may destroy default system
#       theme for the element - like rounded corners etc. because
#       OS theme engine may not support setting colors for buttons:
#       http://qt-project.org/doc/qt-4.8/stylesheet-examples.html#customizing-a-qpushbutton-using-the-box-model


from PySide.QtGui import QApplication, QPushButton, QColorDialog, QMessageBox


class ButtonPainter(object):
  def __init__(self, button):
    self.button = button

  def choose_color(self):
    # Select color
    color  = QColorDialog().getColor()
    
    if color.isValid():
        self.button.setStyleSheet(u'background-color:' + color.name())
    else:
        msgbox = QMessageBox()
        msgbox.setWindowTitle(u'No Color was Selected')
        msgbox.exec_()


app = QApplication([])
    
# Create top level window/button
button = QPushButton('Choose Color')
# button.clicked.connect() doesn't support passing custom parameters to
# handler function (reference to the  button that we want to paint), so we
# create object that will hold this parameter
button_painter = ButtonPainter(button)
button.clicked.connect(button_painter.choose_color)
button.show()

app.exec_()

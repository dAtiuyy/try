import win32gui
import win32con
from PyQt6 import QtWidgets, QtGui, QtCore

class Overlay(QtWidgets.QWidget ):
    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(255,255,255,0.5);")

    def paintEvent(self, event):
        print('draws')
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        painter.setPen(QtCore.Qt.GlobalColor.red)
        painter.setFont(QtGui.QFont('Arial', 30))
        painter.drawText(self.rect() ,QtCore.Qt.AlignmentFlag.AlignLeft, 'Hello World')

    """
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        # Draw live data here using painter.
    """


def main():
    # Find the handle of the window.
    hwnd = win32gui.FindWindow(None, "Valor")
    # find a way to call it multiple times as to redraw stuff incase something changes, also add a basic button
    if hwnd:
        # Get the dimensions of the window.
        rect = win32gui.GetClientRect(hwnd)
        print(rect)
        x, y, width, height = rect
        # Create the overlay window.
        app = QtWidgets.QApplication([])
        overlay = Overlay()
        overlay.resize(width, height)
        overlay.move(x, y)

        # Make the overlay window a child of the window.
        win32gui.SetParent(int(overlay.winId()), hwnd)

        overlay.show()
        app.exec()

    else:
        print("no window")

if __name__ == "__main__":
    main()
__author__ = 'Pontsho Maseko'
__version__ = 1.0
__all__ = ['UI']

import os

from PySide2 import QtWidgets, QtGui, QtCore

from svg_to_qt.ui import header, color, browser, listview, addbutton, qt_root_browser, rcc_type
from svg_to_qt.core import converter


class UI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)

        # Set
        self._glob_pos = QtCore.QPoint()

        # Set attributes
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setMinimumSize(1000, 600)

        # Set Attributes
        self.radius = 2
        self.background = QtGui.QColor(51, 51, 51)
        self.foreground = QtGui.QColor(51, 51, 51)

        # Main Layout
        m_layout = QtWidgets.QVBoxLayout()
        self.setLayout(m_layout)

        # Header
        _header = header.Header(title='SVG To Qt - Convert')
        m_layout.addWidget(_header)

        # Seperator
        seperator = QtWidgets.QSplitter()
        m_layout.addWidget(seperator)

        # Left widget
        left_wid = QtWidgets.QWidget()
        seperator.addWidget(left_wid)
        left_lay = QtWidgets.QVBoxLayout()
        left_wid.setLayout(left_lay)

        # Build browser
        self._qt_build = qt_root_browser.QtRootBrowser()
        left_lay.addWidget(self._qt_build)

        # Output
        out_wid = QtWidgets.QWidget()
        out_lay = QtWidgets.QGridLayout()
        out_wid.setLayout(out_lay)
        left_lay.addWidget(out_wid)

        out_icon = QtGui.QIcon(':file-upload.png')
        out_btn = QtWidgets.QPushButton()
        out_btn.clicked.connect(self._out_browse)
        out_btn.setFixedSize(35, 35)
        out_btn.setIcon(out_icon)
        out_btn.setIconSize(QtCore.QSize(30, 30))

        output_label = QtWidgets.QLabel('Output Folder : ')
        self._out_edit = QtWidgets.QLineEdit()
        out_lay.addWidget(output_label, 0, 0)
        out_lay.addWidget(self._out_edit, 0, 1)
        out_lay.addWidget(out_btn, 0, 2)

        # Color
        self._color = color.Color()
        left_lay.addWidget(self._color)

        # Type
        self._rcc_type = rcc_type.RCC_Type()
        left_lay.addWidget(self._rcc_type)

        # Browser
        _browser = browser.Browser()
        left_lay.addWidget(_browser)

        # List
        self._list = listview.ListView()
        _browser.gotFiles.connect(self._list.set_items)
        left_lay.addWidget(self._list)

        # Add
        add = addbutton.AddButton()
        add.gotFiles.connect(self._list.set_items)
        seperator.addWidget(add)

        # Footer
        footer = QtWidgets.QWidget()
        footer.setFixedHeight(60)
        footer_lay = QtWidgets.QHBoxLayout()
        footer_lay.setAlignment(QtCore.Qt.AlignCenter)
        footer.setLayout(footer_lay)
        m_layout.addWidget(footer)

        # Convert
        convert_btn = QtWidgets.QPushButton('Convert to PNG')
        convert_btn.clicked.connect(self._convert)
        convert_btn.setFixedSize(200, 50)
        footer_lay.addWidget(convert_btn)

        # Make rcc
        rcc_btn = QtWidgets.QPushButton('Make Qt RCC')
        rcc_btn.clicked.connect(self._make_rcc)
        rcc_btn.setFixedSize(200, 50)
        footer_lay.addWidget(rcc_btn)

    def _out_browse(self):

        # File dialog
        dialog = QtWidgets.QFileDialog()
        folder = dialog.getExistingDirectory()

        # Check the folder
        if os.path.isdir(folder):
            self._out_edit.setText(folder)

    def set_qt_build_dir(self, path: str):
        self._qt_build.set(path)

    def _convert(self):

        """Convert the svg(s) that are given"""

        # Get files and check for list of files
        files = self._list.get_files()
        if len(files) == 0:
            return

        # Color
        color = self._color.get()
        if color == '':
            color = '#1f1f1f'

        # Out folder
        out_folder = self._out_edit.text()
        out = ''

        # For each file
        for f in files:

            # Check if the out folder is a directory
            if os.path.isdir(out_folder):
                out = os.path.join(out_folder, os.path.basename(f))

            # Convert
            converter.convert(f, color, output=out)

    def _make_rcc(self):

        # Check file
        files = self._list.get_files()
        if len(files) == 0:
            return

        # Color
        color = self._color.get()
        if color == '':
            color = '#1f1f1f'

        # Out folder
        out_folder = self._out_edit.text()
        if not os.path.isdir(out_folder):
            print('Please specify out folder for RCC file.')
            return

        # Qt build dir
        qt_build_dir = self._qt_build.get()

        # Compile type
        compile_type = self._rcc_type.get()

        # Make rcc file
        converter.generate_rcc(files, out_folder, color, qt_build_dir, compile_type)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, color):
        self._background = color

    @property
    def foreground(self):
        return self._foreground

    @foreground.setter
    def foreground(self, color):
        self._foreground = color

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    def mouseMoveEvent(self, event):

        """Mouse is moveing
        :type event: QMouseMoveEvent
        :return: None.
        """

        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + (event.globalPos() - self._glob_pos))
            self._glob_pos = event.globalPos()

        # Event
        super(UI, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):

        """Mouse press
        :type event: QMousePressEvent
        :return: None.
        """

        # Left Mouse
        if event.buttons() == QtCore.Qt.LeftButton:
            self._pos = event.pos()
            self._glob_pos = event.globalPos()
        
        # Mouse press
        super(UI, self).mousePressEvent(event)

    def paintEvent(self, event):

        """Paint event
        :return event: QPaintEvent()
        :return: None.
        """

        # Size of the widget
        size = self.size()

        # Paint
        painter = QtGui.QPainter()
        painter.begin(self)

        painter.setBrush(self._background)
        painter.setPen(self._foreground)
        painter.drawRoundRect(0, 0, size.width(), size.height(), self._radius, self._radius)

        painter.end()

        # Super
        #super(UI, self).paintEvent(event)
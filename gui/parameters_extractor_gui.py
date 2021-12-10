# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Code\Qt\cnn-eia\form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


# noinspection PyAttributeOutsideInit,SpellCheckingInspection
class ParametersExtractorGUI(object):
    def __init__(self, main_window):
        main_window.setObjectName("ParametersExtractor")
        main_window.resize(640, 160)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(size_policy)
        main_window.setMinimumSize(QtCore.QSize(640, 160))
        main_window.setMaximumSize(QtCore.QSize(640, 160))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.modelLocationGB = QtWidgets.QGroupBox(self.centralwidget)
        self.modelLocationGB.setGeometry(QtCore.QRect(10, 10, 421, 71))
        self.modelLocationGB.setObjectName("modelLocationGB")
        self.modelLocation = QtWidgets.QLineEdit(self.modelLocationGB)
        self.modelLocation.setGeometry(QtCore.QRect(19, 30, 341, 20))
        self.modelLocation.setFrame(True)
        self.modelLocation.setReadOnly(True)
        self.modelLocation.setObjectName("modelLocation")
        self.browseButton = QtWidgets.QPushButton(self.modelLocationGB)
        self.browseButton.setGeometry(QtCore.QRect(370, 30, 31, 21))
        self.browseButton.setObjectName("browseButton")
        self.modelLibraryGB = QtWidgets.QGroupBox(self.centralwidget)
        self.modelLibraryGB.setGeometry(QtCore.QRect(440, 10, 181, 71))
        self.modelLibraryGB.setObjectName("modelLibraryGB")
        self.modelLibrary = QtWidgets.QComboBox(self.modelLibraryGB)
        self.modelLibrary.setGeometry(QtCore.QRect(20, 30, 141, 22))
        self.modelLibrary.setObjectName("modelLibrary")
        self.modelLibrary.addItem("")
        self.modelLibrary.addItem("")
        self.modelLibrary.addItem("")
        self.extractButton = QtWidgets.QPushButton(self.centralwidget)
        self.extractButton.setGeometry(QtCore.QRect(440, 90, 181, 31))
        self.extractButton.setObjectName("extractButton")
        self.generateButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateButton.setGeometry(QtCore.QRect(250, 90, 181, 31))
        self.generateButton.setObjectName("generateButton")
        self.generateButton.setEnabled(False)
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.set_text(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def set_text(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle("Parameters Extractor")
        self.modelLocationGB.setTitle("Model Location")
        self.browseButton.setText("...")
        self.modelLibraryGB.setTitle("Model Library")
        self.modelLibrary.setItemText(0, "ONNX")
        self.modelLibrary.setItemText(1, "PyTorch (DEBUG)")
        self.modelLibrary.setItemText(2, "TensorFlow (DEBUG)")
        self.extractButton.setText("Extract Parameters")
        self.generateButton.setText("Generate A Model")

    def attach_functionality(self, p_e):
        self.browse_model_location = p_e.browse_model_location
        self.browseButton.clicked.connect(self.browse_model_location)
        self.training_library_changed = p_e.model_library_changed
        self.modelLibrary.currentIndexChanged.connect(self.training_library_changed)
        self.generate_model = p_e.generate_model
        self.generateButton.clicked.connect(self.generate_model)
        self.extract_model_parameters = p_e.extract_model_parameters
        self.extractButton.clicked.connect(self.extract_model_parameters)

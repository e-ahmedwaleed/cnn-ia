# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Code\Qt\cnn-eia\requiem.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


# noinspection SpellCheckingInspection
class InterstellarGUI(object):

    def __init__(self, main_window, browser, model_file):
        main_window.resize(960, 640)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(size_policy)
        main_window.setMinimumSize(QtCore.QSize(960, 640))
        main_window.setMaximumSize(QtCore.QSize(960, 640))
        icon = QtGui.QIcon()
        project_dir = __file__.replace("\\", "/").replace("/gui/requiem/interstellar_gui.py", "")
        icon.addPixmap(QtGui.QPixmap(project_dir + "/imgs/stand-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_window.setWindowIcon(icon)

        self.model_name = model_file.replace(".onnx", "")
        self.centralwidget = QtWidgets.QWidget(main_window)

        self.model_preview_group = QtWidgets.QGroupBox(self.centralwidget)
        self.model_preview_group.setGeometry(QtCore.QRect(10, 10, 321, 621))

        self.gridLayout = QtWidgets.QGridLayout(self.model_preview_group)
        self.gridLayout.addWidget(browser, 0, 0, 0, 0)
        browser.page().runJavaScript('this.__view__._updateZoom(0);')

        self.model_layer_group = QtWidgets.QGroupBox(self.centralwidget)
        self.model_layer_group.setGeometry(QtCore.QRect(340, 10, 451, 51))

        self.layer_type = QtWidgets.QComboBox(self.model_layer_group)
        self.layer_type.setGeometry(QtCore.QRect(70, 20, 81, 22))
        self.layer_type_label = QtWidgets.QLabel(self.model_layer_group)
        self.layer_type_label.setGeometry(QtCore.QRect(10, 20, 55, 21))

        self.layer_name = QtWidgets.QComboBox(self.model_layer_group)
        self.layer_name.setGeometry(QtCore.QRect(224, 20, 107, 22))
        self.layer_name_label = QtWidgets.QLabel(self.model_layer_group)
        self.layer_name_label.setGeometry(QtCore.QRect(160, 20, 59, 21))

        self.batch_size = QtWidgets.QSpinBox(self.model_layer_group)
        self.batch_size.setGeometry(QtCore.QRect(375, 20, 66, 21))
        self.batch_size.setMinimum(1)
        self.batch_size.setMaximum(2 ** 20)
        self.batch_size.setAccelerated(True)
        self.batch_size_label = QtWidgets.QLabel(self.model_layer_group)
        self.batch_size_label.setGeometry(QtCore.QRect(340, 20, 30, 21))

        self.memory_arch_group = QtWidgets.QGroupBox(self.centralwidget)
        self.memory_arch_group.setGeometry(QtCore.QRect(340, 70, 611, 261))

        self.memory_arch_table = QtWidgets.QTableWidget(self.memory_arch_group)
        self.memory_arch_table.setGeometry(QtCore.QRect(10, 20, 591, 201))
        self.memory_arch_table.setColumnCount(6)
        self.memory_arch_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.memory_arch_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.memory_arch_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.memory_arch_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.memory_arch_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.memory_arch_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.memory_arch_table.setHorizontalHeaderItem(5, item)
        self.memory_arch_table.verticalHeader().setDefaultSectionSize(40)
        self.memory_arch_table.horizontalHeader().setDefaultSectionSize(83)
        self.memory_arch_table.horizontalHeader().setStretchLastSection(True)
        self.memory_arch_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        delegate = InterstellarGUI.NumericDelegate(self.memory_arch_table)
        self.memory_arch_table.setItemDelegate(delegate)

        self.add_memory_level = QtWidgets.QPushButton(self.memory_arch_group)
        self.add_memory_level.setGeometry(QtCore.QRect(12, 22, 21, 21))
        self.add_memory_level.clicked.connect(self.add_memory_arch_table_row)

        self.remove_memory_level = QtWidgets.QPushButton(self.memory_arch_group)
        self.remove_memory_level.setGeometry(QtCore.QRect(32, 22, 21, 21))
        self.remove_memory_level.clicked.connect(self.remove_memory_arch_table_row)

        self.precision = QtWidgets.QSpinBox(self.memory_arch_group)
        self.precision.setGeometry(QtCore.QRect(10, 230, 71, 21))
        self.precision.setMaximum(2 ** 10)
        self.precision.setProperty("value", 16)
        self.precision.setAccelerated(True)

        self.utilization_threshold = QtWidgets.QSpinBox(self.memory_arch_group)
        self.utilization_threshold.setGeometry(QtCore.QRect(195, 230, 46, 21))
        self.utilization_threshold.setMaximum(100)
        self.utilization_threshold.setAccelerated(True)
        self.utilization_threshold_label = QtWidgets.QLabel(self.memory_arch_group)
        self.utilization_threshold_label.setGeometry(QtCore.QRect(100, 230, 91, 21))

        self.parallel_cost = QtWidgets.QLineEdit(self.memory_arch_group)
        self.parallel_cost.setGeometry(QtCore.QRect(385, 230, 46, 21))
        self.parallel_cost.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+(\\.[0-9]+)?")))
        self.parallel_cost_label = QtWidgets.QLabel(self.memory_arch_group)
        self.parallel_cost_label.setGeometry(QtCore.QRect(260, 230, 121, 21))

        self.replication = QtWidgets.QCheckBox(self.memory_arch_group)
        self.replication.setGeometry(QtCore.QRect(450, 230, 71, 21))

        self.mac_capacity = QtWidgets.QCheckBox(self.memory_arch_group)
        self.mac_capacity.setGeometry(QtCore.QRect(525, 230, 76, 21))

        self.output_queue_group = QtWidgets.QGroupBox(self.centralwidget)
        self.output_queue_group.setGeometry(QtCore.QRect(340, 340, 611, 291))

        self.output_queue_table = QtWidgets.QTableWidget(self.output_queue_group)
        self.output_queue_table.setGeometry(QtCore.QRect(10, 20, 591, 261))
        self.output_queue_table.setColumnCount(3)
        self.output_queue_table.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.output_queue_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.output_queue_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        self.output_queue_table.setHorizontalHeaderItem(2, item)
        self.output_queue_table.horizontalHeader().setDefaultSectionSize(98)
        self.output_queue_table.horizontalHeader().setStretchLastSection(True)
        self.output_queue_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.output_queue_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.clear_output_queue = QtWidgets.QPushButton(self.output_queue_group)
        self.clear_output_queue.setGeometry(QtCore.QRect(538, 22, 61, 21))

        self.add_to_output_queue = QtWidgets.QPushButton(self.centralwidget)
        self.add_to_output_queue.setGeometry(QtCore.QRect(800, 20, 31, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(project_dir + "/imgs/queue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_to_output_queue.setIcon(icon)
        self.add_to_output_queue.setEnabled(False)

        self.run_output_queue = QtWidgets.QPushButton(self.centralwidget)
        self.run_output_queue.setGeometry(QtCore.QRect(840, 20, 111, 41))
        self.run_output_queue.setEnabled(False)

        main_window.setCentralWidget(self.centralwidget)

        self.set_text(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        main_window.show()

    def set_text(self, main_window):
        main_window.setWindowTitle("Inference Analyzer [" + self.model_name + ']')
        self.model_preview_group.setTitle("Model Preview")

        self.model_layer_group.setTitle("Model Layer")
        self.layer_type_label.setText("Layer type:")
        self.layer_type.setToolTip("Supported layer type")
        self.layer_name_label.setText("Layer name:")
        self.layer_name.setToolTip("Extracted layer file")
        self.batch_size_label.setText("Batch:")
        self.batch_size.setToolTip("Number of inputs in a batch")

        self.memory_arch_group.setTitle("Memory Architecture")
        item = self.memory_arch_table.horizontalHeaderItem(0)
        item.setText("Capacity")
        item.setToolTip("Memory capacity in bytes")
        item = self.memory_arch_table.horizontalHeaderItem(1)
        item.setText("Access cost")
        item.setToolTip("Cost per access")
        item = self.memory_arch_table.horizontalHeaderItem(2)
        item.setText("Static cost")
        item.setToolTip("Cost per time unit")
        item = self.memory_arch_table.horizontalHeaderItem(3)
        item.setText("Parallel count")
        item.setToolTip("Number of parallel processing elements")
        item = self.memory_arch_table.horizontalHeaderItem(4)
        item.setText("Parallel dim")
        item.setToolTip("Layout dimension (1D & square-2D)")
        item = self.memory_arch_table.horizontalHeaderItem(5)
        item.setText("Parallel mode")
        item.setToolTip("Hardware parallel template (hierarchical & neighbour & broadcast)")
        for i in range(3):
            self.add_memory_arch_table_row()
        self.precision.setSuffix(" bit(s)")
        self.precision.setToolTip("Number of bits (precision)")
        self.utilization_threshold_label.setText("Minimum utilization:")
        self.utilization_threshold.setSuffix("%")
        self.utilization_threshold.setToolTip(
            "At paralleled level: utilized units / total units")
        self.parallel_cost_label.setText("Intercommunication cost:")
        self.parallel_cost.setText("0.0")
        self.parallel_cost.setToolTip(
            "Per access cost of fetching data from neighborhood processing elements (parallel cost)")
        self.replication.setText("Replication")
        self.replication.setToolTip(
            "Allow another loop dimension (3rd) to be spatially unrolled")
        self.replication.setChecked(True)
        self.mac_capacity.setText("MAC buffer")
        self.mac_capacity.setToolTip("Determines whether MAC can buffer 1 output")
        self.mac_capacity.setChecked(True)
        self.add_memory_level.setText("+")
        self.add_memory_level.setToolTip("Add memory level")
        self.remove_memory_level.setText("-")
        self.remove_memory_level.setToolTip("Remove memory level")

        self.output_queue_group.setTitle("Output Queue")
        self.clear_output_queue.setText("Clear")
        self.clear_output_queue.setToolTip("Clear output queue")
        item = self.output_queue_table.horizontalHeaderItem(0)
        item.setText("Layer name")
        item = self.output_queue_table.horizontalHeaderItem(1)
        item.setText("Status")
        item = self.output_queue_table.horizontalHeaderItem(2)
        item.setText("Output")

        self.add_to_output_queue.setToolTip("Add current layer to the queue")
        self.run_output_queue.setText("Run Optimizer")
        self.run_output_queue.setToolTip("CNN scheduler (interstellar)")

    def add_supported_layers(self, layers):
        i = 0
        for lib in layers:
            self.layer_type.addItem("")
            self.layer_type.setItemText(i, lib)
            i += 1

        if i == 1:
            self.layer_type.setEnabled(False)

    def add_memory_arch_table_row(self):
        row_index = self.memory_arch_table.rowCount()
        self.memory_arch_table.insertRow(row_index)

        item = QtWidgets.QTableWidgetItem()
        self.memory_arch_table.setVerticalHeaderItem(row_index, item)
        item = QtWidgets.QTableWidgetItem()
        self.memory_arch_table.setItem(row_index, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.memory_arch_table.setItem(row_index, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.memory_arch_table.setItem(row_index, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.memory_arch_table.setItem(row_index, 3, item)
        item = InterstellarGUI.ParallelDim(self.memory_arch_table)
        self.memory_arch_table.setCellWidget(row_index, 4, item)
        item = InterstellarGUI.ParallelMode(self.memory_arch_table)
        self.memory_arch_table.setCellWidget(row_index, 5, item)

        item = self.memory_arch_table.verticalHeaderItem(row_index)
        item.setText("Memory L" + str(row_index))
        item = self.memory_arch_table.item(row_index, 0)
        item.setText("1")
        item = self.memory_arch_table.item(row_index, 1)
        item.setText("0.0")
        item = self.memory_arch_table.item(row_index, 2)
        item.setText("0.0")
        item = self.memory_arch_table.item(row_index, 3)
        item.setText("1")

    def remove_memory_arch_table_row(self):
        if self.memory_arch_table.rowCount() > 1:
            self.memory_arch_table.setRowCount(self.memory_arch_table.rowCount() - 1)
        else:
            item = self.memory_arch_table.item(0, 0)
            item.setText("1")
            item = self.memory_arch_table.item(0, 1)
            item.setText("0.0")
            item = self.memory_arch_table.item(0, 2)
            item.setText("0.0")
            item = self.memory_arch_table.item(0, 3)
            item.setText("1")
            item = self.memory_arch_table.cellWidget(0, 4)
            item.setCurrentIndex(0)
            item = self.memory_arch_table.cellWidget(0, 5)
            item.setCurrentIndex(0)

    def update_output_queue_table(self, output_queue):
        self.output_queue_table.clearContents()

        row_count = max(1, len(output_queue))
        if row_count < 8:
            self.clear_output_queue.setGeometry(QtCore.QRect(538, 22, 61, 21))
        else:
            self.clear_output_queue.setGeometry(QtCore.QRect(520, 22, 61, 21))
        self.output_queue_table.setRowCount(row_count)

        row_index = 0
        for key in output_queue:
            output = output_queue[key][1]
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            self.output_queue_table.setItem(row_index, 0, item)
            item = QtWidgets.QTableWidgetItem()
            if output:
                if isinstance(output, str):
                    if (':' in output) or ('/' == output[0]):
                        item.setText("Finished")
                    else:
                        item.setText("Failure")
                else:
                    item.setText("Running")
            else:
                item.setText("Ready")
            self.output_queue_table.setItem(row_index, 1, item)
            item = QtWidgets.QTableWidgetItem()
            if isinstance(output, str):
                item.setText(output)
            self.output_queue_table.setItem(row_index, 2, item)
            row_index += 1

        QtCore.QCoreApplication.processEvents()

    def toggle_edit(self, edit):
        self.clear_output_queue.setEnabled(edit)
        self.run_output_queue.setEnabled(edit)
        self.add_to_output_queue.setEnabled(edit)
        self.model_layer_group.setEnabled(edit)
        self.memory_arch_group.setEnabled(edit)

    def attach_functionality(self, i):
        self.layer_type.currentIndexChanged.connect(i.identify_supported_layers)
        self.run_output_queue.clicked.connect(i.run)
        self.add_to_output_queue.clicked.connect(i.add_layer_to_output_queue)
        self.clear_output_queue.clicked.connect(i.clear_output_queue)

    class NumericDelegate(QtWidgets.QStyledItemDelegate):
        def createEditor(self, parent, option, index):
            editor = super(InterstellarGUI.NumericDelegate, self).createEditor(parent, option, index)
            if isinstance(editor, QtWidgets.QLineEdit):
                if index.column() % 3:
                    reg_ex = QtCore.QRegExp("[0-9]+(\\.[0-9]+)?")
                else:
                    reg_ex = QtCore.QRegExp("[1-9][0-9]*")
                validator = QtGui.QRegExpValidator(reg_ex, editor)
                editor.setValidator(validator)
            return editor

    class TableComboBox(QtWidgets.QComboBox):
        def __init__(self, parent):
            super().__init__(parent)
            style = " QComboBox {"
            style += " border: none;"
            style += " background: white;"
            style += "}"
            self.setStyleSheet(style)

    class ParallelDim(TableComboBox):
        def __init__(self, parent):
            super().__init__(parent)
            self.addItems(["1D", "square-2D"])

    class ParallelMode(TableComboBox):
        def __init__(self, parent):
            super().__init__(parent)
            self.addItems(["hierarchical", "neighbour", "broadcast"])

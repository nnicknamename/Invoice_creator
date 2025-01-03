# Form implementation generated from reading ui file 'C:\Users\pc\Documents\programming\personal_projects\invoice_creator\ui\clients_info_template.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_clients_info(object):
    def setupUi(self, clients_info):
        clients_info.setObjectName("clients_info")
        clients_info.setEnabled(True)
        clients_info.resize(416, 321)
        self.verticalLayout = QtWidgets.QVBoxLayout(clients_info)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Info_layout = QtWidgets.QVBoxLayout()
        self.Info_layout.setObjectName("Info_layout")
        self.header_bar = QtWidgets.QHBoxLayout()
        self.header_bar.setObjectName("header_bar")
        spacerItem = QtWidgets.QSpacerItem(16, 16, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.header_bar.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(parent=clients_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.header_bar.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.header_bar.addItem(spacerItem1)
        self.pushButton_3 = QtWidgets.QPushButton(parent=clients_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.header_bar.addWidget(self.pushButton_3)
        spacerItem2 = QtWidgets.QSpacerItem(16, 16, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.header_bar.addItem(spacerItem2)
        self.Info_layout.addLayout(self.header_bar)
        self.search_box = QtWidgets.QComboBox(parent=clients_info)
        self.search_box.setEditable(True)
        self.search_box.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.search_box.setObjectName("search_box")
        self.Info_layout.addWidget(self.search_box)
        self.line_2 = QtWidgets.QFrame(parent=clients_info)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.Info_layout.addWidget(self.line_2)
        self.info_table = QtWidgets.QTableView(parent=clients_info)
        self.info_table.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_table.sizePolicy().hasHeightForWidth())
        self.info_table.setSizePolicy(sizePolicy)
        self.info_table.setObjectName("info_table")
        self.Info_layout.addWidget(self.info_table)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem3 = QtWidgets.QSpacerItem(16, 16, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.save_button = QtWidgets.QPushButton(parent=clients_info)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_6.addWidget(self.save_button)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.Info_layout.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addLayout(self.Info_layout)

        self.retranslateUi(clients_info)
        self.search_box.currentIndexChanged['int'].connect(clients_info.selection_changed) # type: ignore
        self.pushButton_3.clicked.connect(clients_info.load) # type: ignore
        self.save_button.clicked.connect(clients_info.save) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(clients_info)

    def retranslateUi(self, clients_info):
        _translate = QtCore.QCoreApplication.translate
        clients_info.setWindowTitle(_translate("clients_info", "Form"))
        self.label_2.setText(_translate("clients_info", "Client info"))
        self.pushButton_3.setText(_translate("clients_info", "..."))
        self.save_button.setText(_translate("clients_info", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    clients_info = QtWidgets.QWidget()
    ui = Ui_clients_info()
    ui.setupUi(clients_info)
    clients_info.show()
    sys.exit(app.exec())

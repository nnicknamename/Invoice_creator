# Form implementation generated from reading ui file 'C:\Users\pc\Documents\programming\personal_projects\invoice_creator\ui\actor_info_template.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(405, 322)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Info_layout = QtWidgets.QVBoxLayout()
        self.Info_layout.setObjectName("Info_layout")
        self.header_bar = QtWidgets.QHBoxLayout()
        self.header_bar.setObjectName("header_bar")
        spacerItem = QtWidgets.QSpacerItem(16, 16, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.header_bar.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(parent=Form)
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
        self.pushButton_3 = QtWidgets.QPushButton(parent=Form)
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
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.Info_layout.addItem(spacerItem3)
        self.line_2 = QtWidgets.QFrame(parent=Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.Info_layout.addWidget(self.line_2)
        self.info_table = QtWidgets.QTableView(parent=Form)
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
        spacerItem4 = QtWidgets.QSpacerItem(16, 16, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.save_button = QtWidgets.QPushButton(parent=Form)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_6.addWidget(self.save_button)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.Info_layout.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addLayout(self.Info_layout)

        self.retranslateUi(Form)
        self.pushButton_3.clicked.connect(Form.load) # type: ignore
        self.save_button.clicked.connect(Form.save) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Client info"))
        self.pushButton_3.setText(_translate("Form", "..."))
        self.save_button.setText(_translate("Form", "save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())

# -*- encoding: utf-8 -*-
# Date Calculator v0.1.1
# A simple date calculator.
# Copyright © 2016, Chris Warrick.
# See /LICENSE for licensing information.

"""
Date Calculator GUI interface (PyQt5).

:Copyright: © 2016, Chris Warrick.
:License: BSD (see /LICENSE).
"""

import datecalc
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from datecalc import utils

__all__ = ('main',)


class MainWindow(QtWidgets.QMainWindow):
    """Date Calculator main window."""

    def __init__(self, app):
        """Initialize the GUI."""
        super(MainWindow, self).__init__()
        self.app = app

        # Set icon and title
        self.setWindowIcon(QtGui.QIcon.fromTheme("office-calendar"))
        self.setWindowTitle("Date Calculator v" + datecalc.__version__)

        # Create form layout
        self.centralWidget = QtWidgets.QWidget(self)
        self.formLayout = QtWidgets.QFormLayout(self.centralWidget)
        self.setCentralWidget(self.centralWidget)

        # Add labels
        self.labelStartDate = QtWidgets.QLabel("Start Date", self)
        self.labelOperation = QtWidgets.QLabel("Operation", self)
        self.labelEndDate = QtWidgets.QLabel("End Date", self)
        self.labelOperand = QtWidgets.QLabel("Operand", self)
        self.labelResult = QtWidgets.QLabel("Result", self)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelStartDate)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelOperation)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelEndDate)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelOperand)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.labelResult)

        # Add input fields
        dateSizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        # dateSizePolicy.setHorizontalStretch(0)
        # dateSizePolicy.setVerticalStretch(0)
        # dateSizePolicy.setHeightForWidth(startDate.sizePolicy().hasHeightForWidth())

        self.startDate = QtWidgets.QDateTimeEdit(self, dateTimeChanged=self.recompute)
        self.startDate.setSizePolicy(dateSizePolicy)
        # self.startDate.setMaximumDate(QtWidgets.QDate(7999, 12, 31))
        self.startDate.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.startDate.setCalendarPopup(True)

        self.endDate = QtWidgets.QDateTimeEdit(self, dateTimeChanged=self.recompute)
        self.endDate.setSizePolicy(dateSizePolicy)
        self.endDate.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.endDate.setCalendarPopup(True)

        self.operationLayout = QtWidgets.QHBoxLayout()

        self.radioDiff = QtWidgets.QRadioButton("Time &difference", self, toggled=self.radioChange)
        self.radioAdd = QtWidgets.QRadioButton("&Add", self, toggled=self.radioChange)
        self.radioSubtract = QtWidgets.QRadioButton("&Subtract", self, toggled=self.radioChange)

        self.operationLayout.addWidget(self.radioDiff)
        self.operationLayout.addWidget(self.radioAdd)
        self.operationLayout.addWidget(self.radioSubtract)

        self.operandLayout = QtWidgets.QHBoxLayout()

        self.daysBox = QtWidgets.QSpinBox(self, valueChanged=self.recompute)
        self.daysBox.setMaximum(999999)
        self.labelDaysWord = QtWidgets.QLabel("days", self)
        self.timeBox = QtWidgets.QTimeEdit(self, timeChanged=self.recompute)
        self.timeBox.setSizePolicy(dateSizePolicy)
        self.timeBox.setDisplayFormat("HH:mm:ss")

        self.operandLayout.addWidget(self.daysBox)
        self.operandLayout.addWidget(self.labelDaysWord)
        self.operandLayout.addWidget(self.timeBox)

        resultSizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        self.result = QtWidgets.QLabel("0", self)
        rfont = self.result.font()
        rfont.setBold(True)
        self.result.setFont(rfont)
        self.result.setSizePolicy(resultSizePolicy)
        self.result.setFrameShape(QtWidgets.QFrame.Box)
        self.result.setAlignment(QtCore.Qt.AlignCenter)
        self.result.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.startDate)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.operationLayout)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.endDate)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.operandLayout)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.result)

        # Disable operand fields by default and do the math
        self.radioDiff.setChecked(True)
        self.switchOperations()

        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()

    def radioChange(self, status):
        if status:
            self.switchOperations()

    def switchOperations(self):
        """Switch operations."""
        if self.radioDiff.isChecked():
            self.endDate.setEnabled(True)
            self.operandLayout.setEnabled(False)
            self.daysBox.setEnabled(False)
            self.labelDaysWord.setEnabled(False)
            self.timeBox.setEnabled(False)
        elif self.radioAdd.isChecked() or self.radioSubtract.isChecked():
            self.endDate.setEnabled(False)
            self.operandLayout.setEnabled(True)
            self.daysBox.setEnabled(True)
            self.labelDaysWord.setEnabled(True)
            self.timeBox.setEnabled(True)
        else:
            raise Exception("Unknown operation")
        self.recompute()

    def recompute(self, event=None):
        """Recompute and update the field."""
        try:
            date1 = self.startDate.dateTime().toPyDateTime()
            if self.radioDiff.isChecked():
                date2 = self.endDate.dateTime().toPyDateTime()
                difference = utils.date_difference(date1, date2)
                self.result.setText(str(difference))
            elif self.radioAdd.isChecked() or self.radioSubtract.isChecked():
                tbox = self.timeBox.time()
                date2 = utils.TimeSplit.from_dhms(
                    self.daysBox.value(),
                    tbox.hour(),
                    tbox.minute(),
                    tbox.second(),
                    self.radioSubtract.isChecked()
                )
                new = date1 + date2.to_timedelta()
                self.result.setText(str(new))
            else:
                raise Exception("Unknown operation")
        except OverflowError:
            self.result.setText("OVERFLOW")


def main():
    """The main routine for the UI."""
    # if '-h' in sys.argv or '--help' in sys.argv:
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(app)  # NOQA
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

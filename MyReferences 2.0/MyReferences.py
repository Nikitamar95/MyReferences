# -*- coding: utf-8 -*-
#
#  MyReferences.py
#
#  Copyright 2022 Nikita Marchenko
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import os
from PyQt5 import QtWidgets, QtCore
import Main_window_ui
import String_preparing


class ConvertionProcessThread(QtCore.QThread):

    def string_convertion(self):
        self.main_string = window.main_window_ui.text_before_convertion.toPlainText()
        self.tempfile_plain_text = open("Ref_Rus.txt", 'w+')
        self.tempfile_plain_text.write(self.main_string)
        self.tempfile_plain_text.close()
        String_preparing.Batch_process()
        os.remove(r'Ref_Rus.txt')
        self.tempfile = open("Ref_Eng.txt", 'r')
        global string_text
        string_text = self.tempfile.read()
        self.tempfile.close()
        os.remove(r'Ref_Eng.txt')

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        self.string_convertion()


class MainWindow(QtWidgets.QMainWindow):
    def on_clicked(self):
        self.main_window_ui.convert_button.setDisabled(True)
        app.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.convertion_thread.start()

    def on_finished(self):
        self.main_window_ui.text_after_convertion.setPlainText(string_text)
        self.main_window_ui.convert_button.setDisabled(False)
        app.restoreOverrideCursor()
        if String_preparing.google_warning_is_shown is True:
            QtWidgets.QMessageBox.information(window, "",
                                              String_preparing.google_warning_text
                                              )
            String_preparing.google_warning_is_shown = False
        if String_preparing.internet_warning_is_shown is True:
            QtWidgets.QMessageBox.information(window, "",
                                              String_preparing.internet_warning_text
                                              )
            String_preparing.internet_warning_is_shown = False

    def ClearTheTextField(self, name_of_the_field):
        eval(f"self.main_window_ui.{name_of_the_field}.clear()")

    def OpenTextFile(self):
        self.file_selection = QtWidgets.QFileDialog.getOpenFileName(
            caption="Открыть файл", filter="Text files (*.txt)", initialFilter="Text files (*.txt)"
            )
        self.file_path = self.file_selection[0]
        if self.file_path != "":
            self.file = open(self.file_path, "r+")
            self.file_text = self.file.read()
            self.file.close()
            self.main_window_ui.text_before_convertion.setPlainText(self.file_text)
    def SaveTextFile(self):
        self.file_selection = QtWidgets.QFileDialog.getSaveFileName(
            caption="Сохранить файл", filter="Text files (*.txt)", initialFilter="Text files (*.txt)"
        )
        self.text = self.main_window_ui.text_after_convertion.toPlainText()
        self.file_path = self.file_selection[0]
        if self.file_path != "":
            self.file_path += ".txt"
            self.file = open(self.file_path, "w+")
            self.file.write(self.text)
            self.file.close()
    def PlaceToClipboard(self):
        self.text = self.main_window_ui.text_after_convertion.toPlainText()
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.clipboard.setText(self.text)
    def SetHelpText(self):
        self.url = QtCore.QUrl("Help.html")
        self.main_window_ui.Help_text.setSource(self.url)
        self.main_window_ui.Help_text.setOpenExternalLinks(True)

    def SetAboutText(self):
        self.url = QtCore.QUrl("About_the_program.html")
        self.main_window_ui.About_the_program_text.setSource(self.url)
        self.main_window_ui.About_the_program_text.setOpenExternalLinks(True)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.main_window_ui = Main_window_ui.Ui_MainWindow()
        self.main_window_ui.setupUi(self)
        self.SetHelpText()
        self.SetAboutText()
        self.convertion_thread = ConvertionProcessThread()
        self.main_window_ui.convert_button.clicked.connect(self.on_clicked)
        self.convertion_thread.finished.connect(self.on_finished)
        self.main_window_ui.place_to_clipboard_button.clicked.connect(self.PlaceToClipboard)
        self.main_window_ui.open_txt_file_button.clicked.connect(self.OpenTextFile)
        self.main_window_ui.save_txt_file_button.clicked.connect(self.SaveTextFile)
        self.main_window_ui.clear_the_before_field_button.clicked.connect(lambda: self.ClearTheTextField(
            "text_before_convertion")
            )
        self.main_window_ui.clear_the_after_field_button.clicked.connect(lambda: self.ClearTheTextField(
            "text_after_convertion")
        )

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

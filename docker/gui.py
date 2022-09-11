import logging
logger = logging.getLogger()

import os
import sys
import time
import datetime
import traceback
import subprocess
from pathlib import Path
from argparse import ArgumentParser
from jinja2 import Environment, FileSystemLoader
import pydicom
from launcher import parse_uri

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
LAUNCHER_EXE = os.path.join(THIS_DIR,"launcher.py")

from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, QMainWindow, 
    QVBoxLayout, 
    QMessageBox,
    QPushButton, QLabel, QTextEdit
)

# ref https://realpython.com/python-pyqt-layout
class RoiManager(QWidget):
    def __init__(self,custom_uri,app,parent=None):
        super(RoiManager, self).__init__(parent,QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.app = app
        self.setWindowTitle("RoiManager")
        self.resize(270, 110)        
        
        self.mainLabel = QLabel("status:")
        self.myRichText = QTextEdit()

        self.myRichText.setHtml('hohoho')
        self.myRichText.setReadOnly(True)
        self.helpButton = QPushButton("show me protocol")
        self.doneButton = QPushButton("done")
        self.notdoneButton = QPushButton("not done")

        self.helpButton.clicked.connect(self.on_help_button_clicked)
        self.doneButton.clicked.connect(self.on_done_button_clicked)
        self.notdoneButton.clicked.connect(self.on_notdone_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.helpButton)
        layout.addWidget(self.mainLabel)
        layout.addWidget(self.myRichText)        
        layout.addWidget(self.doneButton)
        layout.addWidget(self.notdoneButton)
        layout.addStretch()
        # Set the layout on the application's window
        self.setLayout(layout)

        self.custom_uri = custom_uri
        self.dicom_folder, self.segmentation_file, self.workdir = parse_uri(self.custom_uri)
        
        self.user = os.environ.get("USER","anon")
        self.edit_file = os.path.join(self.workdir,f"editing.{self.user}.status")
        self.done_file = os.path.join(self.workdir,f"reviewed.{self.user}.status")
        self.done_clicked = False
        self.notdone_clicked = False
        self.start_process()

    def start_process(self):        
        status_file_list = [x for x in os.listdir(self.workdir) if x.endswith('.status')]
        reviewed_file_list = [x for x in os.listdir(self.workdir) if x.startswith('reviewed') and x.endswith('.status')]
        edit_file_list = [x for x in os.listdir(self.workdir) if x.startswith('editing') and x.endswith('.status')]
        if len(status_file_list) != 0:
            msgBox = QMessageBox()
            if len(reviewed_file_list) == 1 and len(edit_file_list)==0:
                tmpuser = reviewed_file_list[0].split('.')[1]
                status_text = f"case has been reviewed by {tmpuser}, do you wish to proceed and overwrite?"
                detail_text = f"click Yes to continue, Cancel to exit"
                icon = QMessageBox.Icon.Warning
                msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            elif len(edit_file_list) == 1 and len(reviewed_file_list)==0:
                tmpuser = edit_file_list[0].split('.')[1]
                status_text = f"case is being edited by {tmpuser}"
                detail_text = f"click Yes to continue, Cancel to exit"
                icon = QMessageBox.Icon.Warning
                msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            else:
                status_text = f"unexpected status, please goahead and review, {status_file_list}"
                detail_text = f"just click Yes."
                icon = QMessageBox.Icon.Information
                msgBox.setStandardButtons(QMessageBox.StandardButton.Yes)
                
            msgBox.setIcon(icon)
            msgBox.setText(status_text)
            msgBox.setInformativeText(detail_text)
            
            msgBox.setDefaultButton(QMessageBox.StandardButton.Yes)
            retval = msgBox.exec()
            if retval == QMessageBox.StandardButton.Yes:
                is_launch = True
                for x in status_file_list:
                    os.remove(os.path.join(self.workdir,x))
            elif retval == QMessageBox.StandardButton.Cancel:
                is_launch = False
        
        if is_launch:            
            with open(self.edit_file,'w') as f:
                f.write("editing")
            self.myRichText.setHtml("please wait, launching itksnap... remember to click `Save->Save *.nii.gz` before closing itksnap")
            self.p = QtCore.QProcess()
            self.p.start("python3", [LAUNCHER_EXE,self.custom_uri])
        else:
            self.myRichText.setHtml("user clicked Cancel, exiting...")
            self.app.quit()

    def close_clicked(self):
        if self.done_clicked:
            self.done_clicked = False
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Icon.Question)
            msgBox.setText("Have you saved the contours in itksnap, are you done with the edit and review?")
            msgBox.setInformativeText("Click Yes if you are done with edit and review.")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Cancel)
            retval = msgBox.exec()
            if retval == QMessageBox.StandardButton.Yes:
                with open(self.done_file,'w') as f:
                    f.write("done")
                if os.path.exists(self.edit_file):
                    os.remove(self.edit_file)
            elif retval == QMessageBox.StandardButton.Cancel:
                return
        if self.notdone_clicked:
            self.notdone_clicked = False
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Icon.Question)
            msgBox.setText("Are you sure you want to exit?")
            msgBox.setInformativeText("Click Close if want to exit, status will remain at editing.")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Close | QMessageBox.StandardButton.Cancel)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Cancel)
            retval = msgBox.exec()
            if retval == QMessageBox.StandardButton.Close:
                with open(self.edit_file,'w') as f:
                    f.write("notdone")
                if os.path.exists(self.done_file):
                    os.remove(self.done_file)
            elif retval == QMessageBox.StandardButton.Cancel:
                return
        self.close()

    def on_help_button_clicked(self):        
        logger.info("middle!")
        protocol_content = """
        + review and edit contours in itksnap.\n
        + periodically and at the end of session, click `Save->Save *.nii.gz`.\n
        + click `done` when you are done with contour.\n
        + click `not done` when you are not done with contour, but want to exit.\n
        """
        self.myRichText.setHtml(protocol_content)

    def on_done_button_clicked(self):
        logger.info("bottom!")
        self.done_clicked = True
        self.close_clicked()
        

    def on_notdone_button_clicked(self):
        logger.info("bottom!")
        self.notdone_clicked = True
        self.close_clicked()
        

if __name__ == "__main__":

    print(f'{sys.argv}')
    parser = ArgumentParser(description="")
    parser.add_argument("custom_uri", type=str)
    args = parser.parse_args()
    custom_uri = args.custom_uri

    _,_, workdir = parse_uri(custom_uri)
    tstamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    log_file = os.path.join(workdir,f"gui-{tstamp}.log")
    os.makedirs(workdir,exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    app = QApplication([])
    main = RoiManager(custom_uri,app)
    main.show()
    app.exec()

'''
python3 gui.py $CITKSNAP_URI
'''

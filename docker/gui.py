import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

import os
import sys
import time
import traceback
import subprocess
from pathlib import Path
from argparse import ArgumentParser
from jinja2 import Environment, FileSystemLoader
import pydicom


from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton    
)
from PyQt6.QtCore import QProcess
from PyQt6 import QtCore

class MyWindow(QMainWindow):
    def __init__(self,custom_uri,output_folder,parent=None):
        super(MyWindow, self).__init__(parent,QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.pushButton = QPushButton("click me")
        self.setCentralWidget(self.pushButton)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.custom_uri = custom_uri
        self.output_folder = output_folder
        self.start_process()

    def start_process(self):
        self.p = QProcess()
        self.p.start("python3", ['launcher.py',self.custom_uri,self.output_folder])
        
    def close_clicked(self):
        self.close()

    def on_pushButton_clicked(self):
        logger.info("clicked!")        

if __name__ == "__main__":
    logger.debug(f'{sys.argv}')
    parser = ArgumentParser(description="")
    parser.add_argument("custom_uri", type=str)
    parser.add_argument("output_folder", type=str)
    args = parser.parse_args()
    custom_uri = args.custom_uri
    output_folder = args.output_folder

    app = QApplication([])
    main0 = MyWindow(custom_uri,output_folder)
    main0.show()
    app.exec()

'''
python3 gui.py $CITKSNAP_URI /tmp/ok
'''
'''
always on top window
monitor if itksnap is launched
if no itksnap, then enable button to launch

`verify button` to check basic segmentation info.

`push button` to push segmentation to db
`lock push button` to do one way sync with db
`un/lock button` 

'''
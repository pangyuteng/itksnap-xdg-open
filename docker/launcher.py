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

class ITKSnapLauncher(object):

    def __init__(self,custom_uri,output_folder):

        self.custom_uri = custom_uri
        self.output_folder = output_folder
        self.dicom_folder = None
        self.segmentation_file = None
        self.itksnap_workspace_file = None

    # no need to do this if you just save you images as nitfi files!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # alternatively update itksnap to take in dicom directory via cli
    def prepare(self):

        try:
            mydict = {}
            for item_str in custom_uri.replace('citksnap://','').split(','):
                key,value = item_str.split('=')
                mydict[key]=value

            self.dicom_folder = mydict["dicom_folder"]
            self.segmentation_file = mydict["segmentation_file"]

        except:
            traceback.print_exc()
            raise ValueError("segmentation_file or dicom_folder not specified!")

        # find dicom via glob
        s0 = time.time()    
        dicom_file_list = [x for x in Path(self.dicom_folder).rglob('*.dcm')]

        primary_dicom_file = dicom_file_list[0]
        ds = pydicom.dcmread(primary_dicom_file)

        s1 = time.time()
        logger.debug(f'image prep time: {s1-s0}')
        
        orientation_str = "RAI" # ??
        
        roi_dict = {}
        for idx in range(5):
            roi_dict[idx] = dict(
                element_idx=idx,
                color_str='255 0 0',
                label_str=f'mylabel_{idx}',
            )

        self.itksnap_workspace_file = os.path.join(self.output_folder,'workspace.itksnap')
        os.makedirs(os.path.dirname(self.itksnap_workspace_file),exist_ok=True)

        content_dict = dict(
            itksnap_workspace_folder=self.output_folder,
            primary_dicom_file=primary_dicom_file,
            segmentation_file=self.segmentation_file,
            series_instance_uid=ds.SeriesInstanceUID,
            slice_thickness=ds.SliceThickness,
            series_number= str(ds.SeriesNumber) if hasattr(ds,'SeriesNumber') else '',
            rows=ds.Rows,
            columns=ds.Columns,
            depth=len(dicom_file_list),
            roi_dict=roi_dict,
            orientation_str=orientation_str,
            segmentation_alpha=0.3,
        )
        logger.debug(f'{content_dict}')
        THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        j2_env = Environment(loader=FileSystemLoader(THIS_DIR),trim_blocks=True)    
        with open(self.itksnap_workspace_file,'w') as f:
            content = j2_env.get_template('template.itksnap').render(**content_dict)
            f.write(content)

    def post(self):
        logger.info('running post steps')

    def launch_itksnap(self):
        cmd_list = ["itksnap","-w",self.itksnap_workspace_file]
        out =subprocess.check_output(cmd_list)
        logger.debug(out)

    def run(self):
        # before logic
        self.prepare()
        # launch snap to review and edit segmentations
        self.launch_itksnap()
        # after logic
        self.post()

def main(custom_uri,output_folder):
    inst = ITKSnapLauncher(custom_uri,output_folder)
    inst.run()

if __name__ == "__main__":
    logger.debug(f'{sys.argv}')
    parser = ArgumentParser(description="")
    parser.add_argument("custom_uri", type=str)
    parser.add_argument("output_folder", type=str)
    args = parser.parse_args()
    custom_uri = args.custom_uri
    output_folder = args.output_folder

    main(custom_uri,output_folder)

'''
python3 launcher.py $CITKSNAP_URI /tmp/ok
'''
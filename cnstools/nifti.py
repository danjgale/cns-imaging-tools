import sys
import os
import re
import numpy as np
import nipype
from nipype.interfaces.dcm2nii import Dcm2niix
from traitlets import TraitError


def _convert_to_nifti(input_dir, output_dir, compress=True):

    os.makedirs(output_dir, exist_ok=True)
    compress_flag = 'i' if compress else 'n'

    try:
        Dcm2niix(
            source_dir=input_dir,
            output_dir=output_dir,
            out_filename='%t%p%s',
            compress=compress_flag,
            single_file=False
        ).run()
    except Exception as e:
        # Will get an innocuous trait error after each participant
        print('{} occured; passing...'.format(e))
        pass


class NiftiConvert(object):

    def __init__(self, data_path, output_path, compress=True):
        self.data_path = data_path
        self.output_path = output_path
        self.compressed = compress

    def convert(self):
        _convert_to_nifti(self.data_path, self.output_path, self.compressed)


class BidsFormat(object):

    def __init__(self):
        pass
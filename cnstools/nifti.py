"""NIfTI management tools.

This module is designed to handle NIfTI file management, which includes
conversion, sorting, and BIDS formatting.

"""
import os
from nipype.interfaces.dcm2nii import Dcm2niix
from traitlets import TraitError


class NiftiConvert(object):
    def __init__(self, data_path, output_path):
        """Convert raw DICOMs into useable NIfTI files for a given
        dataset/participant.

        Parameters
        ----------
        data_path : [type]
            Raw DICOM directory for a single participant.
        output_path : [type]
            Output directory for NIfTI files.

        """
        self.data_path = data_path
        self.output_path = output_path


    def convert(self, compress=True, ignore_exceptions=True):
        """Runs DICOM to NIfTI conversion.

        Parameters
        ----------
        compress : bool, optional
            Generate compressed or uncompressed nifti images (the default is
            True, which returns `*.nii.gz`)

        """
        os.makedirs(self.output_path, exist_ok=True)
        compress_flag = 'i' if compress else 'n'
        try:
            Dcm2niix(
                source_dir=self.data_path,
                output_dir=self.output_path,
                out_filename='%t%p%s',
                compress=compress_flag,
                single_file=False
            ).run()
        except Exception as e:
            # Will get an innocuous trait error after each participant
            if ignore_exceptions:
                print('{} occured; passing...'.format(e))
            else:
                raise e


class BidsFormat(object):
    def __init__(self):
        pass
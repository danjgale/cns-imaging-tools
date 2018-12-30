"""NIfTI management tools.

This module is designed to handle NIfTI file management, which includes
conversion, sorting, and BIDS formatting.

"""
import os
from dcm2bids.dcm2bids import Dcm2bids
from traitlets import TraitError



class BidsData(object):
    def __init__(self, data_path):
        self.data_path = data_path


    def create(self, dicom_path, pid, config):

        self.config = config
        bids = Dcm2bids(dicom_path, pid, self.config)
        bids.run()


    def set_events(self):
        pass

    def set_participants(self):
        pass

    def set_task(self):
        pass




# def _is_moco(fn):
#     """Checks if data is Siemens Motion Corrected data. If so, returns True."""
#     with open(fn) as f:
#         metadata = json.load(f)
#     try:
#         if metadata['SeriesDescription'] == 'MoCoSeries':
#             return True
#         else:
#             return False
#     except KeyError:
#         print("Please verify JSON key.")


# class NiftiData(object):
#     def __init__(self, data_path, compressed=True):
#         """Class to convert and format a Nifti dataset.

#         Parameters
#         ----------
#         data_path : [type]
#             Path to Nifti dataset.

#         """
#         self.data_path = data_path
#         self.compressed = compressed
#         os.makedirs(self.data_path, exist_ok=True)


#     def convert(self, raw_path, ignore_exceptions=True):
#         """Converts DICOM to NIfTI data using Dcm2niix.

#         Parameters
#         ----------
#         compress : bool, optional
#             Generate compressed or uncompressed nifti images (the default is
#             True, which returns `*.nii.gz`)

#         """
#         compress_flag = 'i' if self.compressed else 'n'
#         try:
#             Dcm2niix(
#                 source_dir=raw_path,
#                 output_dir=self.data_path,
#                 out_filename='%t%p%s',
#                 compress=compress_flag,
#                 single_file=False
#             ).run()
#         except Exception as e:
#             # Will get an innocuous trait error after each participant
#             if ignore_exceptions:
#                 print('{} occured; passing...'.format(e))
#             else:
#                 raise e


#     def get_runs(self, n_vols, use_moco=True):
#         """Identify experimental runs in chronological order.

#         Parameters
#         ----------
#         n_vols : int or list of int
#             Number of volumes of experimental runs. If all the same, specify
#             one value, otherwise a list of values for multiple numbers of runs.
#         use_moco : bool, optional
#             Use Siemens Motion Corrected data (the default is True).

#         Returns
#         -------
#         list of str
#             File list of experimental runs in the order of collection.

#         """

#         # identify moco/non moco data

#         # select files with appropriate number of runs

#         # sort files by acquisition time

#         # return file_list
#         pass


#     def to_bids(self):
#         pass


# class BidsFormat(object):
#     def __init__(self):
#         pass
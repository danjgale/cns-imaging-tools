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

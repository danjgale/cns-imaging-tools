"""NIfTI management tools.

This module is designed to handle NIfTI file management, which includes
conversion, sorting, and BIDS formatting.

"""
import os
import pandas as pd
import subprocess
from traitlets import TraitError


def _num_format(x):
    x = int(x)
    return '0{}'.format(x) if x < 10 else str(x)


def _make_event_files(data, pid, out_path):
    df = data.copy()
    run, task = (df['run'].iloc[0], df['task'].iloc[0])
    pid = _num_format(pid)
    fname = 'sub-{pid}_task-{task}_run-{run}_events.tsv'
    df.drop('run', axis=1, inplace=True).to_csv(os.path.join(out_path, fname),
                                                sep='\t')


class BidsData(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.sub_id_pairs = []
        self.__sub_id_list = []


    def add_subject(self, raw_id, sub_id, dicom_path, config, session=None):
        
        
        cmd = "dcm2bids -p {} -c {} -o {}".format(sub_id, config, self.data_path)
        
        if len(dicom_path.split(" ")) > 1:
            # space in path
            cmd += " -d '{}'".format(dicom_path)
        else:
            cmd += " -d {}".format(dicom_path)
            
        if session is not None:
            cmd += " -s {}".format(session)
        
        print(cmd)
        subprocess.run(cmd, shell=True)
        
        self.__sub_id_list.append(sub_id)
        if sub_id not in self.__sub_id_list:
            # only add one pair for a subject; prevent duplicates arising
            # from multiple sessions
            sub_id_pair = {
                'participant_original': raw_id,
                'participant_id': sub_id
            }
            self.sub_id_pairs.append(sub_id_pair)


    def add_event_files(self, fname):
        df = pd.read_csv(fname)
        col_list = ['run', 'onset', 'duration', 'trial_type', 'task']

        if not set(col_list).issubset(df.columns):
            raise ValueError('Event file must contain columns {}'
                             .format(col_list))

        for i in self.sub_id_pairs:
            _, sub_id = list(i.items())[0]
            df.groupby(['run', 'task']).apply(_make_event_files, sub_id)


    def set_participant_file(self, fname):

        df = pd.read_csv(fname)
        try:
            df = df[['participant_id', 'sex', 'age']]
            df.to_csv(os.path.join(self.data_path, 'participants.tsv'), sep='\t')
        except KeyError:
            print("Participant data incomplete or incorrect. Must include "
                  "columns 'participant_id', 'sex', and 'age'")

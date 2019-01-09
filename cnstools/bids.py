"""NIfTI management tools.

This module is designed to handle NIfTI file management, which includes
conversion, sorting, and BIDS formatting.

"""
import os
import pandas as pd
import subprocess
from traitlets import TraitError


def _num_format(x):
    return '0{}'.format(x) if int(x) < 10 else str(x)


def _make_event_file(data, pid, out_path, session=None):
    df = data.copy()
    run, task = (df['run'].iloc[0], df['task'].iloc[0])
    pid = _num_format(pid)

    if session is not None:
        fname = 'sub-{}_ses-{}_task-{}_run-{}_events.tsv'
        fname.format(pid, session, task, run)
    else:
        fname = 'sub-{}_task-{}_run-{}_events.tsv'
        fname.format(pid, task, run)

    df.drop('run', axis=1, inplace=True).to_csv(os.path.join(out_path, fname),
                                                sep='\t')


def _set_event_files(event_df, sub_id, output_path, session=None):
    df = event_df.copy()
    df = pd.read_csv(fname)
    cols = ['run', 'onset', 'duration', 'trial_type', 'task']

    if not set(cols).issubset(df.columns):
        raise ValueError('Event file columns must include {}'.format(cols))

    df.groupby(['run', 'task']).apply(_make_event_files, sub_id, output_path,
                                      session)


def _run_dcm2bids(sub_id, config, output_path, dicom_path, session=None):
    cmd_str = "dcm2bids -p {} -c {} -o {} -d '{}'"
    cmd_str.format(sub_id, config, output_path, dicom_path)
    if session is not None:
        cmd_str += " -s {}".format(session)
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)


class Bids(object):
    def __init__(self, data_path):
        """Class to generate a BIDS formatted dataset.

        Parameters
        ----------
        data_path : str
            Top-level BIDS directory. Each subject will be immediate
            sub-directories.

        """
        self.data_path = data_path
        self.sub_id_pairs = []
        self.__sub_id_list = []
        self.__sub_id_sessions = {}


    def add_subject(self, raw_id, sub_id, dicom_path, config):
        """Adds a subject to the dataset.

        `dicom_path` can be a list of folders if the subject has multiple
        dicom directories. If so, then each directory will be treated as
        separate sessions belonging to the subject.

        Parameters
        ----------
        raw_id : str
            The alphanumeric ID provided originally with the dataset
        sub_id : str or int
            The subject ID number. Can either be a number or a string.
        dicom_path : str or list of str
            Dicom directory path(s). If there are a multiple directories for a
            single subject, each dirctory is treated as a separate session for
            the subject.
        config : str
            Name/path of a dcm2bids configuration .json file. See dcm2bids
            documentation for details.

        """
        # zero-pad if not done already
        sub_id = _num_format(sub_id) if isinstance(sub_id, int) | len(a) == 1

        if isinstance(dicom_path, list) & len(dicom_path) > 1:
            session_list = []
            for i, path in enumerate(dicom_path):
                # make a new session for each directory
                session_num = _num_format(i)
                _run_dcm2bids(sub_id, config, self.data_path, path,
                              session=session_num)
                session_list.append(session_num)
            # keep track of number of sessions for subject
            self.__sub_id_sessions[sub_id] = session_list
        elif isinstance(dicom_path, str):
            _run_dcm2bids(sub_id, config, self.data_path, path)
        else:
            raise ValueError('dicom_path must either be a string or a list '
                             'of strings')

        self.__sub_id_list.append(sub_id)
        if sub_id not in self.__sub_id_list:
            # only add one pair for a subject; prevent duplicates arising
            # from multiple sessions
            sub_id_pair = {
                'participant_original': raw_id,
                'participant_id': sub_id
            }
            self.sub_id_pairs.append(sub_id_pair)


    def add_event_files(self, event_files):
        """Add run-specific event files.

        Parameters
        ----------
        event_files : str or list of str
            Filename(s) of master event file(s), which must include the
            following columns: 'run', 'onset', 'duration', 'trial_type', and
            'task'. The file must be in columnar format (i.e. in 'tidy data'
            format). Therefore, mapping each event to each column, we get each
            row as an event occuring at 'onset' (in seconds) within a specified
            'run' and 'task'. The event is of a particular 'trial_type' and
            lasts a certain 'duration' (in seconds). Extra columns for
            parameters of the events can also be included. If a list is
            provided, then they must appear in the order of the sessions.

        Raises
        ------
        ValueError
            Raised if any of the necessary columns are missing.

        """

        for i in self.sub_id_pairs:
            _, sub_id = list(i.items())[0]
            if isinstance(event_file, str):
                _set_event_files(
                    event_file,
                    sub_id,
                    os.path.join(self.data_path, 'sub-{}'.format(sub_id))
                )
            elif isinstance(event_file, list):
                # loop through multiple sessions
                for i, f in enumerate(event_file):
                    ses_num = _num_format(i + 1)
                    out_path = os.path.join(self.data_path,
                                            'sub-{}'.format(sub_id),
                                            'ses-{}'.format(ses_num))
                    _set_event_files(f, sub_id, out_path, ses_num)


    def set_participant_file(self, fname, include_columns=None):
        """Creates a participants.tsv file in main directory.

        Parameters
        ----------
        fname : str
            Name of file containing demographic information. Must include the
            following columns: 'participant_id', 'sex', 'age'. Extra columns
            can exist within the file. They are only included in
            participants.tsv if specified by `include_columns`.
        include_columns : list of str
            List of extra columns to include in participants.tsv (e.g.,
            condition)

        """
        df = pd.read_csv(fname)
        try:
            cols = ['participant_id', 'sex', 'age']
            cols += include_columns if include_columns is not None
            df = df[cols]
            df.to_csv(os.path.join(self.data_path, 'participants.tsv'),
                      sep='\t')
        except KeyError:
            print("Participant data incomplete or incorrect. Must include "
                  "columns 'participant_id', 'sex', and 'age'")

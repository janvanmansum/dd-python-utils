import argparse
import os

import utils.config as CONFIG

from utils.common.batch_processing import batch_process
from utils.common.ds_metadatafile import construct_filename_base_from_pid
from utils.common.ds_pidsfile import load_pids


def convert_dataset_metadata_action(server_url, pid, input_dir, output_dir):
    # find input metadata file
    input_filename_ext = 'json'  # assume json, but maybe detect this?
    input_full_name = os.path.join(input_dir, construct_filename_base_from_pid(pid) + '.' + input_filename_ext)
    if not os.path.isfile(input_full_name):
        raise ValueError("Could not find input: " + input_full_name)
    print("Found input: " + input_full_name)
    #
    # TODO implement conversion with XSLT file (maybe with Saxon-HE ?)


def convert_dataset_metadata_command(pids_file, input_dir, output_dir):
    print('Args: ' + input_dir + ',  ' + output_dir)
    print("Example using server URL: " + CONFIG.SERVER_URL)

    # detect if input dir exists?
    load_path = os.path.join(CONFIG.OUTPUT_DIR, input_dir)

    # create output dir if not exists!
    save_path = os.path.join(CONFIG.OUTPUT_DIR, output_dir)
    if os.path.isdir(save_path):
        print("Skipping dir creation, because it already exists: " + save_path)
    else:
        print("Creating output dir: " + save_path)
        os.makedirs(save_path)

    # look for inputfile in configured OUTPUT_DIR
    full_name = os.path.join(CONFIG.OUTPUT_DIR, pids_file)
    pids = load_pids(full_name)

    batch_process(pids, lambda pid: convert_dataset_metadata_action(CONFIG.SERVER_URL, pid, load_path, save_path), CONFIG.OUTPUT_DIR, delay=0.0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieves the metadata for all published datasets with the pids in the given inputfile')
    parser.add_argument('-p', '--pids_file', default='dataset_pids.txt', help='The input file with the dataset pids')
    parser.add_argument('-i', '--input_dir', default='dataset_metadata', help='The input dir with the dataset metadata files')
    parser.add_argument('-o', '--output_dir', default='converted_dataset_metadata', help='The output dir, for storing the converted metadata files')
    args = parser.parse_args()

    convert_dataset_metadata_command(args.pids_file, args.input_dir, args.output_dir)

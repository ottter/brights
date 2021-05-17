# Purpose: parse through .csv files gotten from DiscordChatExporter for desired person
# https://github.com/Tyrrrz/DiscordChatExporter

import os
import sys
import csv
import glob
import pandas as pd
# from main import author_id, author_name, create_master
from pathlib import Path

# variables
parse_path = "text/parsed-csv/"
master_path = "text/master-csv/"
input_path = "text/INPUT_FILES_HERE/"
input_csv = [i for i in glob.glob(f'{input_path}*.csv')]    # list of all files to be parsed through


# ensures required directories exist
def create_directories(author_name):
    dir_list = [parse_path, input_path, master_path, parse_path+author_name]
    for create_dir in dir_list:
        if not os.path.exists(create_dir):
            print(f"Creating '{create_dir}' directory...")
            os.mkdir(create_dir)
    return


def initialize_dataset(author_name):
    dataset_size = sum(f.stat().st_size for f in Path(input_path).glob('**/*') if f.is_file())
    dataset_size = round(dataset_size / (1024 * 1024), 2)

    print(f"Creating files for training.\n"
          f"\tauthor: {author_name}\n"
          f"\t# of files: {len(input_csv)}\n"
          f"\ttotal size: {dataset_size} MB")

    # decrease the max_int value by factor of 10 if OverflowError occurs
    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            print(f"Lowered max_int to {max_int}")
            break
        except OverflowError:
            max_int = int(max_int/10)
    return


def create_dataset(author_name, author_id, create_master):
    print(f"Creating individual csv for {author_name}...")

    try:
        for file in input_csv:
            filename = Path(file)
            output_csv = file.lstrip(input_path).lstrip('\\')

            df = pd.read_csv(filename)
            author_df = df[df["AuthorID"] == author_id]
            author_df.loc[:, "Content"].to_csv(f"{parse_path}{author_name}/{output_csv}", index=False, encoding="utf-8")

        if create_master:
            print(f"Creating master csv of {author_name}...")
            master_csv = [i for i in glob.glob(f"{parse_path}{author_name}/*.csv")]
            concat_csv = pd.concat([pd.read_csv(file) for file in master_csv])
            concat_csv.to_csv(f"{master_path}{author_name}-master.csv", index=False, encoding="utf-8")
    except ValueError as e:
        print(f"{'='*5} Invalid Input. Aborting. {'='*5}")
        exit()

    if create_master:
        final_size = round(Path(f"{master_path}{author_name}-master.csv").stat().st_size / (1024 * 1024), 2)
        print(f"Final size: {final_size} MB")
    print(f"{'=' * 5} Done! {'=' * 5}")
    return

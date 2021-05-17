from scripts.csv_parse import create_directories, initialize_dataset, create_dataset
from training import train_model
import os

# author_id must be an int from AuthorID col from input csv files
author_id = 146121659571634177

# author_name string can be anything. Will be where output is placed
author_name = 'lights'

# make one concatenated file out of parsed input files
create_master = True

# Don't make edits below here unless you know what you're doing.
# ==============================================================


def run():
    if not os.path.exists(f"text/master-csv/{author_name}-master.csv"):
        create_directories(author_name)
        initialize_dataset(author_name)
        create_dataset(author_name, author_id, create_master)
    train_model(author_name)


if __name__ == "__main__":
    run()

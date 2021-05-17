import logging

import gpt_2_simple as gpt2
import tensorflow as tf
import os
import requests

model_name = "124M"     # 124M, 355M, 774M, 1558M
file_name = "text/master-csv/lights-master.csv"
training_steps = 1000
print_every = 10
batch_size = 1

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'    # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)

if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(model_name=model_name)  # model is saved into current directory under /models/124M/

if not os.path.isfile(file_name):
    url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
    data = requests.get(url)

    with open(file_name, 'w') as f:
        f.write(data.text)

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
print(f"Starting finetune using: {file_name}...")
gpt2.finetune(sess, file_name,
              model_name=model_name,
              steps=training_steps,
              print_every=print_every,
              batch_size=batch_size)  # steps is max number of training steps
gpt2.generate(sess)
print("Finetune complete.")

from __future__ import absolute_import, division, print_function, unicode_literals
import glob
import os
import numpy as np
import argparse
import json
import torch
from scipy.io.wavfile import write
from .env import AttrDict
from .meldataset import MAX_WAV_VALUE
from .models import Generator

h = None
device = None


def load_checkpoint(filepath, device):
    assert os.path.isfile(filepath)
    print("Loading '{}'".format(filepath))
    checkpoint_dict = torch.load(filepath, map_location=device)
    print("Complete.")
    return checkpoint_dict


def scan_checkpoint(cp_dir, prefix):
    pattern = os.path.join(cp_dir, prefix + '*')
    cp_list = glob.glob(pattern)
    if len(cp_list) == 0:
        return ''
    return sorted(cp_list)[-1]


def inference(a, wav_name):
    generator = Generator(h).to(device)

    state_dict_g = load_checkpoint('tts/audio/backend/data/g_02517000', device)
    generator.load_state_dict(state_dict_g['generator'])

    generator.eval()
    generator.remove_weight_norm()
    with torch.no_grad():
            x = torch.FloatTensor(a).to(device)
            x = x.unsqueeze(1)
            y_g_hat = generator(x.permute(1,  0, 2))
            audio = y_g_hat.squeeze()
            audio = audio * MAX_WAV_VALUE
            audio = audio.cpu().numpy().astype('int16')
            output_file = os.path.join('static/wavs', wav_name)
            write(output_file, h.sampling_rate, audio)
            print(output_file)


def main(mel, wav_name):
    config_file = os.path.join(os.path.split('tts/audio/backend/data/g_02517000')[0], 'config.json')
    with open(config_file) as f:
        data = f.read()

    global h
    json_config = json.loads(data)
    h = AttrDict(json_config)

    torch.manual_seed(h.seed)
    global device
    if torch.cuda.is_available():
        torch.cuda.manual_seed(h.seed)
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    inference(mel, wav_name)


# if __name__ == '__main__':
#     main()


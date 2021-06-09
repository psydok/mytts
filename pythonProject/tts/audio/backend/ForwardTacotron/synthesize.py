import torch
import numpy as np
from typing import Callable
from .models.forward_tacotron import ForwardTacotron
from tts.audio.backend.dsp import DSP
from .utils.text.cleaners import Cleaner
from .utils.text import text_to_sequence
from .utils import hparams as hp
from .utils.text.symbols import phonemes
from datetime import datetime
from pathlib import Path


class Synthesizer:

    def __init__(self,
                 tts_path: str,
                 voc_path: str,
                 device='cpu'):
        self.device = torch.device(device)
        path_to_config = Path(__file__).parent.absolute().__str__() + '\\hparams.py'
        hp.configure(path_to_config)
        tts_model = ForwardTacotron(embed_dims=hp.forward_embed_dims,
                                    num_chars=len(phonemes),
                                    durpred_rnn_dims=hp.forward_durpred_rnn_dims,
                                    durpred_conv_dims=hp.forward_durpred_conv_dims,
                                    durpred_dropout=hp.forward_durpred_dropout,
                                    pitch_rnn_dims=hp.forward_pitch_rnn_dims,
                                    pitch_conv_dims=hp.forward_pitch_conv_dims,
                                    pitch_dropout=hp.forward_pitch_dropout,
                                    pitch_emb_dims=hp.forward_pitch_emb_dims,
                                    pitch_proj_dropout=hp.forward_pitch_proj_dropout,
                                    rnn_dim=hp.forward_rnn_dims,
                                    postnet_k=hp.forward_postnet_K,
                                    postnet_dims=hp.forward_postnet_dims,
                                    prenet_k=hp.forward_prenet_K,
                                    prenet_dims=hp.forward_prenet_dims,
                                    highways=hp.forward_num_highways,
                                    dropout=hp.forward_dropout,
                                    n_mels=hp.num_mels).to(device)

        tts_model.load(tts_path)
        self.tts_model = tts_model
        # self.wavernn = WaveRNN.from_checkpoint(voc_path)
        # self.melgan = torch.hub.load('seungwonpark/melgan', 'melgan')
        # self.melgan.to(device).eval()
        self.cleaner = Cleaner.from_config(hp)
        self.dsp = DSP(hp.num_mels,
                       hp.sample_rate,
                       hp.hop_length,
                       hp.win_length,
                       hp.n_fft,
                       hp.fmin,
                       hp.fmax,
                       hp.peak_norm,
                       hp.trim_start_end_silence,
                       hp.trim_silence_top_db,
                       hp.pitch_max_freq,
                       hp.trim_long_silences,
                       hp.vad_sample_rate,
                       hp.vad_window_length,
                       hp.vad_moving_average_width,
                       hp.vad_max_silence_length,
                       hp.bits,
                       hp.mu_law,
                       hp.voc_mode,
                       )
        self.tts_config = hp

    def dsp(self):
        return self.dsp

    def __call__(self,
                 text: str,
                 voc_model: str,
                 alpha=1.0,
                 pitch_function: Callable[[torch.tensor], torch.tensor] = lambda x: x,
                 ) -> np.array:
        x = self.cleaner(text)
        x = text_to_sequence(x)
        x = torch.tensor(x).unsqueeze(0)
        _, gen, _, _ = self.tts_model.generate(x,
                                               alpha=alpha,
                                               pitch_function=pitch_function)

        return gen
        # now = datetime.now()
        # dt_string = now.strftime("%Y%m%d_%H-%M-%S")
        #
        # if voc_model == 'griffinlim':
        #     wav_name = f'{dt_string}_forward_alpha{alpha}_amp_{voc_model}.wav'
        #     # np.save("C:\\Users\\max\\Downloads\\mel_forward.npy", gen)
        #     wav = self.dsp.griffinlim(gen, n_iter=32)
        #     DSP.save_wav(wav, out_path / f'{wav_name}', sample_rate=self.tts_config.sample_rate)
        # else:
        #     wav_name = f'none'
        #     # m = torch.tensor(gen).unsqueeze(0).cpu()
        #     # with torch.no_grad():
        #     #     wav = self.melgan.inference(m).cpu().numpy()
        #
        # return wav_name

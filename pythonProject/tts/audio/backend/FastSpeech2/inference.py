import torch
from .fastspeech import FeedForwardTransformer
from .utils.texts import phonemes_to_sequence
import numpy as np
from .utils.texts import valid_symbols
from .utils.hparams import load_hparam_str
from .utils.texts.cleaners import punctuation_removers
from tts.audio.backend.dsp import DSP


class SynthenizerFastSpeech:
    def __init__(self):
        """Run deocding."""

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        checkpoint_path = 'tts/audio/backend/data/fastspeech2_72k_steps.pyt'
        checkpoint = torch.load(checkpoint_path, map_location=device)

        self.hp = load_hparam_str(checkpoint["hp_str"])
        self.hp.train.ngpu = 0

        self.dsp = DSP(self.hp.audio.num_mels,
                       self.hp.audio.sample_rate,
                       self.hp.audio.hop_length,
                       self.hp.audio.win_length,
                       self.hp.audio.n_fft,
                       self.hp.audio.fmin,
                       self.hp.audio.fmax,
                       self.hp.audio.peak_norm,
                       True,
                       self.hp.audio.ref_level_db,
                       self.hp.data.p_max,
                       False,
                       16000,
                       30,
                       8,
                       12,
                       self.hp.audio.bits,
                       self.hp.audio.mu_law,
                       'RAW')

        idim = len(valid_symbols)
        odim = self.hp.audio.num_mels
        self.model = FeedForwardTransformer(
            idim, odim, self.hp
        )

        self.model.load_state_dict(checkpoint["model"])

    def __call__(self, text: str):
        para_mel = []
        text = self.process_paragraph(text)
        print(text)
        for i in range(0, len(text)):
            phomenes = self.preprocess(text[i])

            audio = self.synth(phomenes, self.model, self.hp)
            m = audio.T
            para_mel.append(m)

        m = torch.cat(para_mel, dim=1)
        return m.cpu().numpy()
        # now = datetime.now()
        # creation_date = now.strftime("%Y%m%d_%H-%M-%S")
        # if voc_model == "":
        #     voc_model = 'griffinlim'
        # wav_name = f'{creation_date}_fastspeech2_amp_{voc_model}.wav'
        # if voc_model == 'hifigan':
        #     voc(m, wav_name)
        # else:
        #     wav = self.dsp.griffinlim(m.cpu().numpy(), 30)
        #
        # return m

    @staticmethod
    def dsp(self):
        return self.dsp()

    @staticmethod
    def preprocess(text):
        # input - line of phonemes
        # output - list of phonemes
        clean_phonemes = punctuation_removers(text)
        print(clean_phonemes)
        phonemes = clean_phonemes.split() #to_russian_phonemes(clean_text)
        phonemes = ["" if x == " " else x for x in phonemes]
        phonemes = ["sp" if x == "," else x for x in phonemes]
        phonemes = ["sp" if x == "." else x for x in phonemes]
        phonemes = ' '.join(phonemes)
        return phonemes + ' ~'

    @staticmethod
    def process_paragraph(para):
        # input - paragraph with lines seperated by "."
        # output - list with each item as lines of paragraph seperated by suitable padding
        text = []
        for lines in para.split("."):
            text.append(lines)
        return text

    @staticmethod
    def synth(text, model, hp):
        """Decode with E2E-TTS model."""
        print("TTS synthesis")
        model.eval()
        # set torch device
        device = torch.device("cuda" if hp.train.ngpu > 0 else "cpu")
        model = model.to(device)

        input = np.asarray(phonemes_to_sequence(text))
        text = torch.LongTensor(input)
        text = text.to(device)

        with torch.no_grad():
            print("predicting")
            outs = model.inference(text)  # model(text) for jit script
            mel = outs
        return mel


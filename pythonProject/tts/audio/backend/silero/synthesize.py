import torch
from tts.audio.backend.dsp import DSP
from utils.files import out_path
from datetime import datetime


def generator(text):
    language = 'ru'
    speaker = 'ruslan_16khz'
    device = torch.device('cpu')
    model, symbols, sample_rate, _, apply_tts = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                          model='silero_tts',
                                                                          language=language,
                                                                          speaker=speaker)
    model = model.to(device)
    audio = apply_tts(texts=[text],
                      model=model,
                      sample_rate=sample_rate,
                      symbols=symbols,
                      device=device)
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H-%M-%S")
    wav_name = f'{dt_string}_silero.wav'

    DSP.save_wav(audio[0].numpy(), out_path / f'{wav_name}', sample_rate=sample_rate)
    return wav_name

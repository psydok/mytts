import torch
from tts.audio.backend.dsp import DSP
from utils.files import out_path
from datetime import datetime
from omegaconf import OmegaConf
from .tts_utils import init_jit_model as init_jit_model_tts
from .tts_utils import apply_tts


def generator(text):
    path_to_models = 'tts/audio/backend/silero/latest_silero_models.yml'
    language = 'ru'
    speaker = 'ruslan_16khz'
    device = torch.device('cpu')
    torch.hub.download_url_to_file('https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml',
                                   path_to_models,
                                   progress=False)
    models = OmegaConf.load(path_to_models)
    model_conf = models.tts_models[language][speaker].latest
    model = init_jit_model_tts(model_conf.jit)
    symbols = model_conf.tokenset
    sample_rate = model_conf.sample_rate

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

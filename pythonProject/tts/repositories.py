from abc import ABC, abstractmethod
from datetime import datetime
from tts.audio.backend.hifigan.inference_e2e import main as vocoder
from .audio.backend.dsp import DSP
from .models import saved_models
from .audio.backend.ForwardTacotron.synthesize import Synthesizer
from .audio.backend.FastSpeech2.inference import SynthenizerFastSpeech
from .audio.backend.silero.synthesize import generator
from utils.files import out_path


class Repository(ABC):
    @property
    @abstractmethod
    def name_model(self):
        pass

    def get_tts_path(self) -> str:
        path = saved_models['path']
        return path + saved_models['synthesizers'][self.name_model]

    @abstractmethod
    def generate(self, text: str, voc_model: str):
        pass

    def get_audio(self, mel, voc_model, dsp: DSP, sample_rate=22050):
        now = datetime.now()
        creation_date = now.strftime("%Y%m%d_%H-%M-%S")
        wav_name = f'{creation_date}_{self.name_model}_amp_{voc_model}.wav'
        if voc_model == 'hifigan':
            wav = vocoder(mel, wav_name)
        else:
            wav = dsp.griffinlim(mel, 30)
            dsp.save_wav(wav, out_path / f'{wav_name}', sample_rate=sample_rate)
        return wav_name


class ForwardTacotronRepository(Repository):

    @property
    def name_model(self):
        return 'forward_tacotron'

    def generate(self, text: str, voc_model: str):
        synthesizer = Synthesizer(tts_path=self.get_tts_path(),
                                  device='cpu')
        mel = synthesizer(text, alpha=0.9)
        wav_name = self.get_audio(mel, voc_model, synthesizer.dsp)

        return wav_name


class FastSpeech2Repository(Repository):

    @property
    def name_model(self):
        return 'fast_speech2'

    def generate(self, text: str, voc_model: str):
        synthesizer = SynthenizerFastSpeech()
        mel = synthesizer(text)
        wav_name = self.get_audio(mel, voc_model, synthesizer.dsp)
        return wav_name


class SileroRepository(Repository):
    """
    Пример входного текста для генерации такой же как у SovaTTS:
    д+обрый в+ечер! ч+ем мог+у пом+очь?
    """

    @property
    def name_model(self):
        return 'silero'

    def generate(self, text: str, voc_model: str):
        text_new_accent = ""
        for ch in text:
            if ch == "+":
                text_new_accent = text_new_accent[:-1] + "+" + text_new_accent[-1:]
                continue
            text_new_accent += ch
        print(text_new_accent)
        wav_name = generator(text_new_accent)
        return wav_name

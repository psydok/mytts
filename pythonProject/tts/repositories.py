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
            wav = dsp.griffinlim(mel.cpu().numpy(), 30)
            dsp.save_wav(wav, out_path / f'{wav_name}', sample_rate=sample_rate)
        return wav_name, wav


class ForwardTacotronRepository(Repository):

    @property
    def name_model(self):
        return 'forward_tacotron'

    def generate(self, text: str, voc_model: str):
        synthesizer = Synthesizer(tts_path=self.get_tts_path(),
                                  voc_path='',
                                  device='cpu')
        mel = synthesizer(text, voc_model=voc_model, alpha=0.9)
        wav_name = self.get_audio(mel, voc_model, synthesizer.dsp)

        return wav_name


class FastSpeech2Repository(Repository):

    @property
    def name_model(self):
        return 'fast_speech2'

    def generate(self, text: str, voc_model: str):
        synthesizer = SynthenizerFastSpeech()
        mel = synthesizer(text, voc_model=voc_model)
        wav_name = self.get_audio(mel, voc_model, synthesizer.dsp)
        return wav_name


class SileroRepository(Repository):

    @property
    def name_model(self):
        return 'silero'

    def generate(self, text: str, voc_model: str):
        wav_name = generator(text)
        return wav_name

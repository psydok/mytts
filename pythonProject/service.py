from typing import Dict
import time
from tts.models import saved_models
from tts.repositories import ForwardTacotronRepository, FastSpeech2Repository, SileroRepository
from tts.text import ProcessedText


class SpeechSynthesisService(object):
    __repositories_all = {
        "forward_tacotron": ForwardTacotronRepository,
        "fast_speech2": FastSpeech2Repository,
        "silero": SileroRepository
    }

    def __init__(self, repository: str) -> None:
        self._repository = self._check_exists_repository(repository)

    def _check_exists_repository(self, repository):
        for model in saved_models['synthesizers']:
            if model == repository:
                return self.__repositories_all[repository]()
        raise ValueError('Model not supported yet')

    @property
    def repository(self):
        return self._repository

    @repository.setter
    def repository(self, repository: str):
        self._repository = self._check_exists_repository(repository)

    def generate(self, text, vocoder='griffinlim') -> Dict[str, str]:
        if vocoder == "":
            vocoder = 'griffinlim'
        use_accent = True
        if '+' in text:
            use_accent = False
        processed_text = ProcessedText(text, use_accent)
        norm_text = processed_text.process_text()
        print(norm_text)
        len_text = 0
        start = time.time()
        if norm_text:
            len_text = len(norm_text)
            wav_name = self._repository.generate(norm_text, vocoder)
        else:
            len_text = len(processed_text.text)
            wav_name = self._repository.generate(processed_text.text, vocoder)
        end = time.time()
        return {
            "wav_name": wav_name,
            "speed_synthesis": round(end - start, 5),
            "len_text": len_text
        }

    # def wav_to_bytes(self, path):
    #     with open("static/wavs/test.wav", "rb") as wavfile:
    #         input_wav = wavfile.read()
    #     rate, data = read(io.BytesIO(input_wav))
    #     reversed_data = data[::-1]  # reversing it
    #
    #     return reversed_data

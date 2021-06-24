from typing import Dict
import time
from tts.models import saved_models
from tts.repositories import ForwardTacotronRepository, FastSpeech2Repository, SileroRepository
from tts.text import ProcessedText
import re


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

    def generate(self, text, vocoder) -> Dict[str, str]:
        # убираем лишние ударения перед гласными, если есть
        text = re.sub(r'(?i)(([^аеёиоуыэюя\s])\++)', r'\2', text)
        # проверяем наличие расставленных ударений
        use_accent = True
        if re.findall(r'(?i)([аеёиоуыэюя])\+', text):
            use_accent = False

        processed_text = ProcessedText(text, use_accent)
        norm_text = processed_text.process_text()
        print(norm_text)
        phonemes = processed_text.to_russian_phonemes()
        print(phonemes)
        len_text = len(norm_text)

        start = time.time()
        wav_name = self._repository.generate({"phonemes": phonemes, "text": text}, vocoder)
        end = time.time()

        return {
            "wav_name": wav_name,
            "speed_synthesis": round(end - start, 5),
            "len_text": len_text
        }
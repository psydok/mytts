from russian_g2p.Transcription import Transcription
from ..text.normalizator.normalizer import Normalizer
from russian_g2p.Accentor import Accentor
from collections import deque
import re


class ProcessedText(object):
    def __init__(self, text: str, use_accent=False):
        if not text:
            raise ValueError('Text must not be empty')
        self._use_accent = use_accent
        self._text = text

    def to_russian_phonemes(self):
        text = self._text
        text = text.replace('-', '—')
        text = text.replace('…', '.')
        punctuation_marks = ';:,.!?¡¿—…"«»“”()'
        transcriptor = Transcription()
        phonemes = ''
        queue = deque()
        for i in text:
            if i in punctuation_marks:
                queue.append(' ' + i + ' ')
        for it in transcriptor.transcribe([text]):
            for seq in it:
                if len(queue) == 0:
                    phonemes += ' '.join(seq)
                    continue
                phonemes += ' '.join(seq) + queue.popleft()
        return phonemes

    @staticmethod
    def _replace_on_word(match):
        return match.group('word') if match.group('word') else ' равно '

    @staticmethod
    def preprocessing_abbreviations(text: str) -> str:
        preprocessing_text = []
        for word in text.split():
            if word.isupper() and '.' not in word:
                word = ''.join([ch + '.' for ch in word])
            preprocessing_text.append(word)
        return ' '.join(preprocessing_text)

    @staticmethod
    def normalizing(text: str) -> str:
        normalizer = Normalizer()
        norm_text = normalizer.norm_text(text)
        return norm_text

    @staticmethod
    def replace(text, replaceable_chars, new_char):
        for punctuation in replaceable_chars:
            text = text.replace(punctuation, new_char)
        return text

    @staticmethod
    def accenting(text: str) -> str:
        text = ProcessedText.replace(text, ['«', '»', '“', '”', '”', ], '"')
        text = ProcessedText.replace(text, ['(', '[', ')', ']'], '.')
        punctuations = {';', ':', ',', '.', '!', '?', '¡', '¿', '—', '"'}

        # Создаем синтагмы
        temp_text = ProcessedText.replace(text, punctuations, '.')
        syntagmas = [syntagma.strip() for syntagma in temp_text.split('.') if len(syntagma.strip()) != 0]

        # Запоминаем знаки препинания для восстановления после обработки
        queue_punctuation = deque()
        for ch in text:
            if ch in punctuations:
                queue_punctuation.append(ch)

        # Создаем сингамны с расстановкой ударений
        processed_syntagmas = []
        accentor = Accentor()
        for syntagma in syntagmas:
            preprocessing_text = []
            for word in syntagma.split():
                clean_word = ''
                for ch in word:
                    if ch in punctuations:
                        continue
                    clean_word += ch
                preprocessing_text.append([clean_word])
            # Получить ударения
            accent_words = accentor.do_accents(preprocessing_text)
            accent_words = accent_words[0]
            if len(accent_words) == 0:
                continue
            processed_syntagmas.append(' '.join(accent_words))

        pro_text = ''
        for syntagma in processed_syntagmas:
            pro_text += syntagma
            if len(queue_punctuation) > 0:
                pro_text += queue_punctuation.popleft() + ' '

        return pro_text.strip()

    @property
    def text(self):
        return self._text

    def process_text(self) -> str:
        text = self._text.lower()
        clean_text = re.sub(r"(?i)([а-яё])\+", r'\1', text)
        clean_text = re.sub(r'(?=\w\=)(?P<word>\w)\=|\s(\=)\s', self._replace_on_word, clean_text)
        if self._use_accent:
            text = \
                self.accenting(
                    self.normalizing(
                        self.preprocessing_abbreviations(clean_text)))
        else:
            # [[['сло', 'во'], 'сло+во'], [...]]
            accenting_list = [[i.split('+'), i] for i in text.split() if '+' in i and i.split('+')[0] != '']
            text = \
                self.normalizing(
                    self.preprocessing_abbreviations(clean_text))
            for word in text.split():
                for chunks in accenting_list:
                    if str(chunks[0][0] + chunks[0][1]).strip() == word:
                        text = text.replace(word, chunks[1])
                        accenting_list.remove(chunks)
                    break
        if text != "":
            self._text = text
        return self._text

import re
from typing import Dict, Any

from ...utils.text.numbers import normalize_numbers
from ...utils.text.symbols import phonemes_set
from unidecode import unidecode
from russian_g2p.Transcription import Transcription
from queue import Queue
# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
    ('mrs', 'misess'),
    ('mr', 'mister'),
    ('dr', 'doctor'),
    ('st', 'saint'),
    ('co', 'company'),
    ('jr', 'junior'),
    ('maj', 'major'),
    ('gen', 'general'),
    ('drs', 'doctors'),
    ('rev', 'reverend'),
    ('lt', 'lieutenant'),
    ('hon', 'honorable'),
    ('sgt', 'sergeant'),
    ('capt', 'captain'),
    ('esq', 'esquire'),
    ('ltd', 'limited'),
    ('col', 'colonel'),
    ('ft', 'fort'),
]]


def expand_abbreviations(text):
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text


def collapse_whitespace(text):
    return re.sub(_whitespace_re, ' ', text)


def no_cleaners(text):
    return text


def english_cleaners(text):
    text = unidecode(text)
    text = normalize_numbers(text)
    text = expand_abbreviations(text)
    return text


def russian_cleaners(text):
    text = collapse_whitespace(text)
    text = text.strip()
    return text


def to_russian_phonemes(text):
    text = text.replace('-', '—')
    text = text.replace('…', '.')
    punctuation_marks = ';:,.!?¡¿—…"«»“”()'
    transcriptor = Transcription()
    phonemes = ''
    queue = Queue()
    for i in text:
        if i in punctuation_marks:
            queue.put(' ' + i + ' ')
    for it in transcriptor.transcribe([text]):
        for seq in it:
            if queue.empty():
                phonemes += ' '.join(seq)
                continue
            phonemes += ' '.join(seq) + queue.get()
    return phonemes


class Cleaner:

    def __init__(self,
                 cleaner_name: str,
                 use_phonemes: bool,
                 lang: str) -> None:
        if cleaner_name == 'russian_cleaners':
            self.clean_func = russian_cleaners
        elif cleaner_name == 'no_cleaners':
            self.clean_func = no_cleaners
        else:
            raise ValueError(f'Cleaner not supported: {cleaner_name}! '
                             f'Currently supported: [\'english_cleaners\', \'no_cleaners\']')
        self.use_phonemes = use_phonemes
        self.lang = lang

    def __call__(self, text: str) -> str:
        text = self.clean_func(text)
        if self.use_phonemes:
            text = to_russian_phonemes(text)
        text = collapse_whitespace(text)
        text = text.strip()
        return text

    @classmethod
    def from_config(cls, config) -> 'Cleaner':
        return Cleaner(
            cleaner_name=config.tts_cleaner_name,
            use_phonemes=config.use_phonemes,
            lang=config.language
        )

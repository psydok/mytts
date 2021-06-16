""" from https://github.com/keithito/tacotron """
import re
from ...utils.texts import cleaners
from ...utils.texts.symbols import (
    symbols,
    _eos,
    phonemes_symbols,
    PAD,
    EOS,
    _PHONEME_SEP,
)
from ...utils.texts.dict_ import symbols_

from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r"(.*?)\{(.+?)\}(.*)")

valid_symbols = phonemes_symbols


def pad_with_eos_bos(_sequence):
    return _sequence + [_symbol_to_id[_eos]]


def text_to_sequence(text, cleaner_names, eos):
    """Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    The text can optionally have ARPAbet sequences enclosed in curly braces embedded
    in it. For example, "Turn left on {HH AW1 S S T AH0 N} Street."
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
    """
    sequence = []
    if eos:
        text = text + "~"
    try:
        sequence += _symbols_to_sequence(_clean_text(text, cleaner_names))
    except KeyError:
        print("text : ", text)
        exit(0)

    return sequence


def sequence_to_text(sequence):
    """Converts a sequence of IDs back to a string"""
    result = ""
    for symbol_id in sequence:
        if symbol_id in _id_to_symbol:
            s = _id_to_symbol[symbol_id]
            # Enclose ARPAbet back in curly braces:
            if len(s) > 1 and s[0] == "@":
                s = "{%s}" % s[1:]
            result += s
    return result.replace("}{", " ")


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception("Unknown cleaner: %s" % name)
        text = cleaner(text)
    return text


def _symbols_to_sequence(symbols):
    return [symbols_[s.upper()] for s in symbols]


def _arpabet_to_sequence(text):
    return _symbols_to_sequence(["@" + s for s in text.split()])


def _should_keep_symbol(s):
    return s in _symbol_to_id and s != "_" and s != "~"


# For phonemes
_phoneme_to_id = {s: i for i, s in enumerate(valid_symbols)}
_id_to_phoneme = {i: s for i, s in enumerate(valid_symbols)}


def _should_keep_token(token, token_dict):
    return (
            token in token_dict
            and token != PAD
            and token != EOS
            and token != _phoneme_to_id[PAD]
            and token != _phoneme_to_id[EOS]
    )


def phonemes_to_sequence(phonemes):
    string = phonemes.split() if isinstance(phonemes, str) else phonemes
    # string.append(EOS)
    # sequence = list(map(convert_phoneme_CMU, string))
    try:
        sequence = []
        for s in string:
            if s in _phoneme_to_id:
                sequence.append(_phoneme_to_id[s])
            else:
                for i in s:
                    if i in _phoneme_to_id:
                        sequence.append(_phoneme_to_id[i])
        # sequence = [_phoneme_to_id[s] for s in string if s in _phoneme_to_id]
    except Exception as e:
        print(string)
        raise e
    return sequence


def sequence_to_phonemes(sequence, use_eos=False):
    string = [_id_to_phoneme[idx] for idx in sequence]
    # if _should_keep_token(idx, _id_to_phoneme)]
    string = _PHONEME_SEP.join(string)
    if use_eos:
        string = string.replace(EOS, "")
    return string


def text_to_phonemes(text, custom_words={}):
    """
    Convert text into ARPAbet.
    For known words use CMUDict; for the rest try 'espeak' (to IPA) followed by 'listener'.
    :param text: str, input text.
    :param custom_words:
        dict {str: list of str}, optional
        Pronounciations (a list of ARPAbet phonemes) you'd like to override.
        Example: {'word': ['W', 'EU1', 'R', 'D']}
    :return: list of str, phonemes
    """
    g2p = Grapheme2Phoneme()

    words = text.lower().split()

    phonemes = []
    PUNCTUATION = "!?.,-:;\"'()"
    for word in words:
        if all(c in PUNCTUATION for c in word):
            pronounciation = ["pau"]
        else:
            pronounciation = g2p.word_to_phonemes(word)
            pronounciation = list(
                pronounciation
            )  # (map(convert_phoneme_CMU, pronounciation))

        phonemes += pronounciation

    return phonemes

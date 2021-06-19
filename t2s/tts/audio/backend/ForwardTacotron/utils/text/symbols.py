""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. '''

_vocals_phonemes = {
    'U0', 'U', 'O0', 'O', 'A0', 'A', 'E0', 'E', 'Y0', 'Y', 'I0', 'I',
    'U0l', 'Ul', 'O0l', 'Ol', 'A0l', 'Al', 'E0l', 'El', 'Y0l', 'Yl', 'I0l', 'Il'
}

_voiced_weak_phonemes = {
    'J0', 'V0', 'V', 'N0', 'N', 'L0', 'L', 'M0', 'M', 'R0', 'R',
    'J0l', 'V0l', 'Vl', 'N0l', 'Nl', 'L0l', 'Ll', 'M0l', 'Ml', 'R0l', 'Rl'
}

_voiced_strong_phonemes = {
    'B', 'B0', 'G', 'G0', 'D', 'D0', 'Z', 'Z0', 'ZH', 'ZH0',
    'GH', 'GH0', 'DZ', 'DZ0', 'DZH', 'DZH0',
    'Bl', 'B0l', 'Gl', 'G0l', 'Dl', 'D0l', 'Zl', 'Z0l', 'ZHl', 'ZH0l',
    'GHl', 'GH0l', 'DZl', 'DZ0l', 'DZHl', 'DZH0l'
}

_deaf_phonemes = {
    'K', 'K0', 'P', 'P0', 'S', 'S0', 'T', 'T0', 'F', 'F0', 'KH', 'KH0',
    'TS', 'TS0', 'TSH', 'TSH0', 'SH', 'SH0',
    'Kl', 'K0l', 'Pl', 'P0l', 'Sl', 'S0l', 'Tl', 'T0l', 'Fl', 'F0l', 'KHl', 'KH0l',
    'TSl', 'TS0l', 'TSHl', 'TSH0l', 'SHl', 'SH0l'
}
_punctuation = {';', ':', ',', '.', '!', '?', '¡', '¿', '—', '"', '«', '»', '“', '”', '(', ')'}
sos = '#s'
eos = '#e'

phonemes = sorted(list(
    _vocals_phonemes | _voiced_weak_phonemes | _voiced_strong_phonemes | _deaf_phonemes | _punctuation | {'sli'}))

phonemes_set = set(phonemes)

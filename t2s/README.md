Модуль синтеза речи
======

Требования
----
Python 3.6.2

Коды
----
      model_name          model
      ------------------|-----------------
      fast_speech2        FastSpeech2
      forward_tacotron    ForwardTacotron
     
      vocoder_name        vocoder
      ------------------|-----------------
      hifigan             HifiGAN
      griffinlim          Griffin-Lim


Тестирование
----
Чтобы сгенерировать аудиозапись, отправьте POST-запрос:

`
$ curl --request POST 'http://localhost:5000/synth' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "До+брый вечер! Я могу вам чем-то помо+чь?",
    "model_name": "fast_speech2",
    "vocoder_name": "hifigan"
}'`

Аудиозапись сохраниться по пути _static/wavs_
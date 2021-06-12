<template>
  <div class="v-about">
    <div class="v-about-info container-lg px-3 my-5 markdown-body">
      <h1>Результаты исследования</h1>
      <p>
      </p>
      <ul class="list-unstyled">
        <li>Синтез речи - технология перевода текста в речевой сигнал при помощи различных подходов.</li>
        <li>На данном сайте представлены модели архитектур синтеза речи, основанные на машинном обучении.</li>
        <li>Данный подход к синтезу речи именуется параметрическим и основан на нейросетях.</li>
      </ul>

      <ul class="list-unstyled">
        <li>На данный момент для генерации доступны следующие модели:
          <ul>
            <li>ForwardTacotron + <a href="https://github.com/nsu-ai/russian_g2p">russian_g2p</a></li>
            <li>FastSpeech2 + <a href="https://github.com/nsu-ai/russian_g2p">russian_g2p</a></li>
            <li>Silero (Tacotron2 + потоковый вокодер WaveGlow)</li>
          </ul>
        </li>
      </ul>

    </div>
    <div class="container-lg px-3 my-5 markdown-body">
      <p>Все образцы генерируются моделями, обученными на датасете <a
          href="http://dataset.sova.ai/SOVA-TTS/ruslan/ruslan_dataset.tar">RUSLAN (SOVA TTS)</a>.</p>

      <h2>ForwardTacotron + Griffin-Lim</h2>
      <p>Образцы генерируются с помощью модели <a href="https://github.com/as-ideas/ForwardTacotron">ForwardTacotron</a>, обученной 90К шагов на алгоритмическом способе получения аудио из
        мел-спектрограммы - <a href="https://arxiv.org/pdf/2007.05764.pdf">Griffin-Lim</a>. Скорость речи: 0,9.</p>
      <p class="text">Начал думать - реши, решил - действуй.</p>
      <footer class="blockquote-footer">М.Б. Литвак</footer>
      <audio src="/wavs/ftg/1_alpha09.wav" controls preload></audio>
      <p class="text">Смерть никогда не обманешь, хотя жизнь обмануть можно.</p>
      <footer class="blockquote-footer">«Ад для Джеффри Темпеста»</footer>
      <audio src="/wavs/ftg/2_alpha09.wav" controls preload></audio>

      <h2>ForwardTacotron + HifiGAN</h2>
      <p>Образцы генерируются с помощью модели <a href="https://github.com/as-ideas/ForwardTacotron">ForwardTacotron</a>, обученной 90К шагов с дообученным вокодером
        HifiGAN, представленным в репозитории <a href="https://github.com/jik876/hifi-gan">Hifi-GAN repo</a>.</p>

      <p class="text">Оказалось, что люди замечают не так уж и много, если не приглядываются специально.</p>
      <footer class="blockquote-footer">«Дом, в котором»</footer>
      <audio src="/wavs/fth/3_alpha09.wav" controls preload></audio>
      <p class="text">Вокруг нас разбросаны ответы на любые вопросы, надо только суметь отыскать их.</p>
      <footer class="blockquote-footer">«Дом, в котором»</footer>
      <audio src="/wavs/fth/4_alpha09.wav" controls preload></audio>

      <h2>FastSpeech2 + Griffin-Lim</h2>
      <p>Образцы генерируются с помощью модели <a href="https://github.com/rishikksh20/FastSpeech2">FastSpeech2</a>, обученной 72К шагов, и озвучиваются алгоритмом Griffin-Lim.</p>
      <p class="text">Мы совсем не хотим завоевывать космос, мы просто хотим расширить Землю до его пределов.</p>
      <footer class="blockquote-footer">«Солярис»</footer>
      <audio src="/wavs/fs2g/5.wav" controls preload></audio>

      <p class="text">Наука занимается только тем, как происходит что-то, а не тем, почему происходит.</p>
      <footer class="blockquote-footer">«Солярис»</footer>
      <audio src="/wavs/fs2g/6.wav" controls preload></audio>

      <h2>FastSpeech2 + HifiGAN</h2>
      <p>Образцы генерируются с помощью модели <a href="https://github.com/rishikksh20/FastSpeech2">FastSpeech2</a>, обученной 72К шагов, и озвучиваются вокодером HifiGAN.</p>
      <p class="text">Знаю одно: между нулем и единицей есть бесконечное множество чисел.</p>
      <footer class="blockquote-footer">«Виноваты звезды»</footer>
      <audio src="/wavs/fs2h/7.wav" controls preload></audio>

      <p class="text">Они еще трудятся, ибо труд – развлечение. Но они заботятся, чтобы развлечение не утомляло их.</p>
      <footer class="blockquote-footer">«Так говорил Заратустра»</footer>
      <audio src="/wavs/fs2h/8.wav" controls preload></audio>
      <div class="footer border-top border-gray-light mt-5 pt-3 text-gray text-right">
        © MAXIKON. Student CSU. 2021.
      </div>
    </div>


  </div>
</template>

<script>
export default {
  name: "v-about"
}
</script>

<style>
.v-about {
  text-align: justify;
}

.markdown-body h2 {
  margin-top: 16px;
  padding-bottom: 0.3em;
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
}

.text {
  font-size: 20px;
  margin-top: 16px;
}

.text-right {
  text-align: right !important;
}

.text-gray {
  color: #586069 !important;
}
</style>
<template>
  <div class="v-about">

    <div class="v-about-info container-lg px-3 my-5 markdown-body">
      <h1>Результаты исследования</h1>
      <p>
      </p>
      <ul class="list-unstyled">
        <li>Синтез речи - технология перевода текста в речевой сигнал при помощи различных подходов.</li>
        <li>На данном сайте представлены архитектуры синтеза речи, основанные на машинном обучении.</li>
        <li>Данный подход к синтезу речи именуется параметрическим и основан на нейросетях.</li>
      </ul>

      <ul class="list-unstyled">
        <li>На данный момент на сайте представлены следующие обученные модели:
          <ul>
            <li>ForwardTacotron с фонемами russian_g2p</li>
            <li>FastSpeech2 с фонемами russian_g2p</li>
            <li>Silero</li>
          </ul>
        </li>
      </ul>

    </div>
    <div class="container-lg px-3 my-5 markdown-body">

      <h2>ForwardTacotron + Griffin-Lim</h2>
      <p>Образцы генерируются с помощью модели, обученной 90К шагов на датасете <a
          href="http://dataset.sova.ai/SOVA-TTS/ruslan/ruslan_dataset.tar">RUSLAN (SOVA TTS)</a> с дообученным вокодером
        HifiGAN, представленным в репозитории <a href="https://github.com/jik876/hifi-gan">Hifi-GAN repo</a>.</p>
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
  padding-bottom: 0.3em;
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
}
</style>
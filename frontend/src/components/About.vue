<template>
<div class="v-about">
  <p class="h3 mb-4">Теория синтеза речи</p>
  <div class="v-about-info">
    <ul class="list-unstyled">
      <li>Синтез речи - технология перевода текста в речевой сигнал при помощи различных подходов.</li>
      <li>На данном сайте представлены архитектуры синтеза речи, основанные на машинном обучении.</li>
      <li>Данный подход к синтезу речи именует параметрическим и основан на нейросетях.</li>
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
</div>
</template>

<script>
export default {
  name: "v-about"
}
</script>

<style>
.v-about-info {
  text-align: left;
  margin-left: 24px;;
}
</style>
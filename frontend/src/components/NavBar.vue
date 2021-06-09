<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand mytitle" href="#">TTS</a>
<!--    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"-->
<!--            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">-->
<!--      <span class="navbar-toggler-icon"></span>-->
<!--    </button>-->
    <div class=" navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item active">
          <router-link
              class="nav-link"
              :to="{name:'tts'}"
          >Синтез речи
          </router-link>
        </li>
        <li class="nav-item">
          <router-link
              class="nav-link"
              :to="{name:'rating'}"
          >Рейтинг моделей
          </router-link>
        </li>
        <li class="nav-item">
          <router-link
              class="nav-link"
              :to="{name:'about'}"
          >О технологии
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  mounted() {
  }
}
</script>

<style>
.mytitle {
  margin-left: 1rem;
}
</style>
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand mytitle" href="#">TTS</a>
    <button class="navbar-toggler mytitle" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
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
  data () {
    return {
    }
  }
}
</script>

<style>
.mytitle {
  margin-left: 1rem;
  margin-right: 1rem;
}
</style>
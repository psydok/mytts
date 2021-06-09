<template>
  <div class="v-main-wrapper">
    <router-view></router-view>
  </div>

</template>

<script>
export default {
  name: "MainWrapper",
  mounted() {
    document.title = 'Исследования синтеза речи';
  }
}
</script>

<style>
.v-main-wrapper {
  margin-top: 24px;
}
</style>
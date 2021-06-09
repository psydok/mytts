<template>
    <vNavBar/>
    <vMainWrapper/>
</template>

<script>
import vMainWrapper from './components/MainWrapper'
import vNavBar from './components/NavBar'

export default {
  name: 'App',
  components: {
    vMainWrapper,
    vNavBar
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: auto;
}
</style>

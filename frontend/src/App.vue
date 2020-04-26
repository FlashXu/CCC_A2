<template>
  <div id='app' class="bg">
    <Navbar />
    <Home />
    <router-view></router-view>
  </div>
</template>


<script>
import Home from './views/Home'
import Navbar from './views/Navbar'
import Landing from './views/Landing'

export default {
  name:"app",
  components: {
    Home,
    Navbar,
    Landing
  }
}
</script>


<style scoped src="./assets/styles/mystyles.css"></style>
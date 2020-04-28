<template>
  <div id="app">
    <google-map />
    <router-view name="header" />
    <div class="wrapper">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {};
</script>
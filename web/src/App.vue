<template>
<div id="app">
<!--
    <router-link to='/'>Home</router-link>
    <router-link to='/login'>Login</router-link>
   -->
    <router-view />
  </div>

</template>

<script>
export default {
  name: 'App',
  data: () => ({
    //
  }),
};
</script>

<style>
#app {
  padding-left: 30px;
  padding-right: 30px;
  padding-top: 30px;
}
</style>

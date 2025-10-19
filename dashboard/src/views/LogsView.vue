<script setup lang="ts">
import { ref } from 'vue';
const logs = ref<string[]>([
  "Example database log 1",
  "Example ML Service log 1"
])
</script>
<template>
  <main>
    <h1>Logs </h1>
    <p>backend logs will appear below</p>
    <ol>
      <li v-for="log in logs">{{ log }}</li>
    </ol>
  </main>
</template>
<style lang="css" scoped>
</style>

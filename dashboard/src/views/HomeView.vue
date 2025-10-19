<script setup lang="ts">
import { useAPIGateway } from '@/composables/useAPIGateway';
import { watch } from 'vue';

const {ws} = useAPIGateway()

const sendMessage = () => {
  ws.send("some message")
}

watch(ws.data, (newData) => {
  console.info('new data: ', newData)
})
</script>

<template>
  <main>
    <h1></h1>
    <button @click="sendMessage">Send message</button>
  </main>
</template>

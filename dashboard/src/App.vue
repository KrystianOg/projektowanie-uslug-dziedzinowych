<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ConfigProvider } from 'reka-ui';

import Header from './components/Header.vue';
</script>

<template>
  <ConfigProvider>
    <Header />
    <RouterView />
  </ConfigProvider>
</template>

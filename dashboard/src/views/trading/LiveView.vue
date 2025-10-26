<script setup lang="ts">
import { usePositions } from '@/composables/usePositions';

const {closeAllPositions} = usePositions()
</script>
<template>
  <main>
    <div class="wrapper">
      <!-- TODO: prompt if user is sure -->
      <button class="destructive" @click="closeAllPositions">
        Close all positions
      </button>
    </div>
  </main>

</template>
<style lang="css" scoped>
.wrapper {
  display: flex;
}

.desctructive {}
</style>

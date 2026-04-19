<script setup>
import {ref, watch} from "vue";

const props = defineProps(['username'])
const myUsername = ref(props.username)

watch(() => props.username, newVal =>{
  myUsername.value = newVal
})
defineExpose({
  myUsername,
})
</script>

<template>
  <fieldset class="filedset">
    <lable class="label  text-base">用户名</lable>
    <input v-model="myUsername" type="text" class="input w-108">
  </fieldset>
</template>

<style scoped>

</style>
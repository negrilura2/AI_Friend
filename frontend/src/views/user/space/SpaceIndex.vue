<script setup>
import {useRoute, useRouter} from "vue-router";

const route = useRoute()//取当前url里的信息
// const router = useRouter()//打开一个页面或者后退
// router.push({
//   name:'homepage-index'
// })
</script>

<template>
个人空间:{{route.params.user_id }}
</template>

<style scoped>

</style>
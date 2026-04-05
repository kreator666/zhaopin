<template>
  <div class="my-items-page">
    <Navbar />
    <div class="container">
      <h2>我的发布</h2>
      <el-empty description="您还没有发布任何物品" />
      <el-button type="primary" @click="$router.push('/flea/publish')">发布闲置</el-button>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.my-items-page { min-height: 100vh; background: #f5f7fa; padding: 100px 0 40px; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; text-align: center; }
</style>

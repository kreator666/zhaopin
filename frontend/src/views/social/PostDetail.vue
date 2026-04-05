<template>
  <Navbar />
  <div class="post-detail-page">
    <div class="container">
      <el-empty description="帖子详情开发中..." />
      <el-button @click="$router.back()">返回</el-button>
    </div>
  </div>
</template>

<style scoped>
.post-detail-page { min-height: 100vh; background: #f5f7fa; padding: 100px 0 40px; }
.container { max-width: 800px; margin: 0 auto; padding: 0 20px; text-align: center; }
</style>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

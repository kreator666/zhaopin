<template>
  <div class="publish-item-page">
    <Navbar />
    <div class="container">
      <h2>发布闲置</h2>
      <el-empty description="发布功能开发中..." />
      <el-button @click="$router.back()">返回</el-button>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.publish-item-page { min-height: 100vh; background: #f5f7fa; padding: 100px 0 40px; }
.container { max-width: 800px; margin: 0 auto; padding: 0 20px; text-align: center; }
</style>

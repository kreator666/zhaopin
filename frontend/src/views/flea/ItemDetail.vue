<template>
  <div class="item-detail-page">
    <Navbar />
    <div class="container">
      <el-empty description="物品详情开发中..." />
      <el-button @click="$router.back()">返回</el-button>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.item-detail-page { min-height: 100vh; background: #f5f7fa; padding: 100px 0 40px; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; text-align: center; }
</style>

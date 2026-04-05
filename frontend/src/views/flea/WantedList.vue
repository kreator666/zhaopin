<template>
  <div class="wanted-list-page">
    <Navbar />
    <div class="container">
      <h2>求购信息</h2>
      <el-empty description="求购模块开发中..." />
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.wanted-list-page { min-height: 100vh; background: #f5f7fa; padding: 100px 0 40px; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; text-align: center; }
</style>

<template>
  <Navbar />
  <div class="event-list-page">
    <div class="page-header">
      <h1>活动约伴</h1>
      <p>学习、运动、娱乐，一起约起来</p>
    </div>
    <div class="container">
      <el-empty description="活动模块开发中，敬请期待..." />
    </div>
  </div>
</template>

<style scoped>
.event-list-page { min-height: 100vh; background: #f5f7fa; padding-top: 60px; }
.page-header { background: linear-gradient(135deg, #67C23A 0%, #E6A23C 100%); color: #fff; padding: 40px 0; text-align: center; }
.container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
</style>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

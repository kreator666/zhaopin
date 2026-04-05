<template>
  <Navbar />
  <div class="course-detail-page" style="padding-top: 60px;">
    <div class="container">
      <el-empty description="课程详情开发中..." />
      <el-button @click="$router.back()">返回</el-button>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.course-detail-page { min-height: 100vh; background: #f5f7fa; padding: 40px 0; }
.container { max-width: 1000px; margin: 0 auto; padding: 0 20px; text-align: center; }
</style>

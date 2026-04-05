<template>
  <Navbar />
  <div class="material-list-page" style="padding-top: 60px;">
    <div class="page-header">
      <div class="container">
        <h1>学习资料</h1>
        <p>课件、笔记、真题，助力学习</p>
      </div>
    </div>
    <div class="container main-content">
      <el-empty description="资料模块开发中，敬请期待..." />
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.material-list-page { min-height: 100vh; background: #f5f7fa; }
.page-header { background: linear-gradient(135deg, #67C23A 0%, #409EFF 100%); color: #fff; padding: 40px 0; text-align: center; }
.main-content { padding: 40px 20px; }
</style>

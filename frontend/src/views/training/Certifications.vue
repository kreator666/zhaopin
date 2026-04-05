<template>
  <Navbar />
  <div class="certifications-page" style="padding-top: 60px;">
    <div class="page-header">
      <div class="container">
        <h1>考证信息</h1>
        <p>四六级、计算机等级、职业资格考试</p>
      </div>
    </div>
    <div class="container main-content">
      <el-empty description="考证模块开发中，敬请期待..." />
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.certifications-page { min-height: 100vh; background: #f5f7fa; }
.page-header { background: linear-gradient(135deg, #E6A23C 0%, #F56C6C 100%); color: #fff; padding: 40px 0; text-align: center; }
.main-content { padding: 40px 20px; }
</style>

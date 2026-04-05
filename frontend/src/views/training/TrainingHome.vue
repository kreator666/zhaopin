<template>
  <Navbar />
  <div class="training-home" style="padding-top: 60px;">
    <div class="page-header">
      <h1>培训学习</h1>
      <p>提升技能，成就未来</p>
    </div>
    <div class="container">
      <el-row :gutter="20">
        <el-col :xs="24" :md="8">
          <el-card shadow="hover" @click="$router.push('/training/courses')">
            <el-icon :size="48" color="#409EFF"><Reading /></el-icon>
            <h3>精品课程</h3>
            <p>编程、设计、职场技能全覆盖</p>
          </el-card>
        </el-col>
        <el-col :xs="24" :md="8">
          <el-card shadow="hover" @click="$router.push('/training/materials')">
            <el-icon :size="48" color="#67C23A"><Document /></el-icon>
            <h3>学习资料</h3>
            <p>课件、笔记、真题免费下载</p>
          </el-card>
        </el-col>
        <el-col :xs="24" :md="8">
          <el-card shadow="hover" @click="$router.push('/training/certifications')">
            <el-icon :size="48" color="#E6A23C"><Trophy /></el-icon>
            <h3>考证信息</h3>
            <p>四六级、计算机、职业资格</p>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import { Reading, Document, Trophy } from '@element-plus/icons-vue'
</script>

<style scoped>
.training-home {
  min-height: 100vh;
  background: #f5f7fa;
}
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 60px 0;
  text-align: center;
}
.page-header h1 {
  font-size: 36px;
  margin-bottom: 16px;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}
.el-card {
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s;
}
.el-card:hover {
  transform: translateY(-5px);
}
</style>

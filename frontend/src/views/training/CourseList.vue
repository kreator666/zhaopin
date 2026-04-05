<template>
  <Navbar />
  <div class="course-list-page" style="padding-top: 60px;">
    <div class="page-header">
      <div class="container">
        <h1>精品课程</h1>
        <el-input v-model="searchQuery" placeholder="搜索课程" clearable class="search-input">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
      </div>
    </div>
    <div class="container main-content">
      <el-empty description="课程模块开发中，敬请期待..." />
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
const searchQuery = ref('')
</script>

<style scoped>
.course-list-page { min-height: 100vh; background: #f5f7fa; }
.page-header { background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%); color: #fff; padding: 40px 0; text-align: center; }
.page-header h1 { margin-bottom: 20px; }
.search-input { width: 400px; margin: 0 auto; display: block; }
.main-content { padding: 40px 20px; }
</style>

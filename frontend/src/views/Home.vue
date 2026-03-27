<template>
  <div class="home">
    <Navbar />
    
    <!-- Banner 区域 -->
    <div class="banner">
      <div class="banner-content">
        <h1>找到理想的工作</h1>
        <p>连接优秀人才与优质企业</p>
        
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索职位、公司"
            size="large"
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button type="primary" @click="handleSearch">
                <el-icon><Search /></el-icon>
                搜索
              </el-button>
            </template>
          </el-input>
        </div>
        
        <div class="hot-keywords">
          <span>热门搜索：</span>
          <el-tag 
            v-for="tag in hotTags" 
            :key="tag"
            class="keyword-tag"
            @click="searchKeyword = tag; handleSearch()"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </div>
    
    <!-- 最新职位 -->
    <div class="section">
      <div class="container">
        <div class="section-header">
          <h2>最新职位</h2>
          <router-link to="/jobs" class="more">查看更多 <el-icon><ArrowRight /></el-icon></router-link>
        </div>
        
        <el-row :gutter="20">
          <el-col :span="8" v-for="job in latestJobs" :key="job.id">
            <el-card class="job-card" shadow="hover" @click="goToJobDetail(job.id)">
              <div class="job-title">{{ job.title }}</div>
              <div class="job-salary" v-if="job.salary_min || job.salary_max">
                {{ job.salary_min || '面议' }} - {{ job.salary_max || '面议' }}
              </div>
              <div class="job-company">{{ job.company?.name }}</div>
              <div class="job-tags">
                <el-tag size="small">{{ job.location }}</el-tag>
                <el-tag size="small">{{ job.experience || '经验不限' }}</el-tag>
                <el-tag size="small">{{ job.education || '学历不限' }}</el-tag>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { jobsApi } from '@/api/jobs'

const router = useRouter()
const searchKeyword = ref('')
const latestJobs = ref([])

const hotTags = ['Java', 'Python', '前端', '产品经理', '运营', 'UI设计']

const handleSearch = () => {
  router.push({
    path: '/jobs',
    query: { keyword: searchKeyword.value }
  })
}

const goToJobDetail = (id) => {
  router.push(`/jobs/${id}`)
}

const fetchLatestJobs = async () => {
  try {
    const res = await jobsApi.getList({ per_page: 6 })
    latestJobs.value = res.items
  } catch (error) {
    console.error('获取职位失败', error)
  }
}

onMounted(() => {
  fetchLatestJobs()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.banner {
  margin-top: 60px;
  height: 400px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.banner-content {
  text-align: center;
  max-width: 700px;
  padding: 0 20px;
}

.banner h1 {
  font-size: 48px;
  margin-bottom: 16px;
}

.banner p {
  font-size: 20px;
  margin-bottom: 40px;
  opacity: 0.9;
}

.search-box {
  margin-bottom: 20px;
}

.search-box :deep(.el-input__wrapper) {
  padding: 5px;
}

.search-box :deep(.el-input__inner) {
  height: 50px;
  font-size: 16px;
}

.hot-keywords {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.hot-keywords span {
  opacity: 0.8;
}

.keyword-tag {
  cursor: pointer;
}

.section {
  padding: 60px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.section-header h2 {
  font-size: 28px;
  color: #333;
}

.more {
  color: #409EFF;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 5px;
}

.job-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s;
}

.job-card:hover {
  transform: translateY(-5px);
}

.job-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.job-salary {
  color: #f56c6c;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.job-company {
  color: #666;
  margin-bottom: 10px;
}

.job-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.job-tags .el-tag {
  background-color: #f5f7fa;
  border: none;
  color: #666;
}
</style>

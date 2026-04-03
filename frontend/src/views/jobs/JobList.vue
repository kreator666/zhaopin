<template>
  <div class="job-list-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <!-- 搜索栏 -->
        <div class="search-section">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索职位、公司"
            size="large"
            class="search-input"
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button type="primary" @click="handleSearch">
                <el-icon><Search /></el-icon>
                搜索
              </el-button>
            </template>
          </el-input>
          
          <el-input
            v-model="searchForm.location"
            placeholder="工作地点"
            size="large"
            class="location-input"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Location /></el-icon>
            </template>
          </el-input>
        </div>
        
        <!-- 职位列表 -->
        <div class="job-list">
          <el-card v-for="job in jobs" :key="job.id" class="job-item" shadow="hover">
            <div class="job-header">
              <div class="job-info">
                <h3 class="job-title" @click="goToDetail(job.id)">{{ job.title }}</h3>
                <div class="job-tags">
                  <el-tag size="small" type="info">{{ job.location || '地点不限' }}</el-tag>
                  <el-tag size="small" type="info">{{ job.experience || '经验不限' }}</el-tag>
                  <el-tag size="small" type="info">{{ job.education || '学历不限' }}</el-tag>
                  <el-tag size="small" type="info">{{ formatJobType(job.job_type) }}</el-tag>
                </div>
              </div>
              <div class="job-salary" v-if="job.salary_min || job.salary_max">
                {{ formatSalary(job.salary_min, job.salary_max) }}
              </div>
            </div>
            
            <div class="job-company" @click="goToDetail(job.id)">
              <el-icon><OfficeBuilding /></el-icon>
              <span>{{ job.company?.name }}</span>
              <span class="company-info" v-if="job.company?.industry">{{ job.company.industry }}</span>
            </div>
            
            <div class="job-footer">
              <span class="publish-time">{{ formatTime(job.created_at) }}发布</span>
              <el-button type="primary" size="small" @click="handleApply(job.id)">立即投递</el-button>
            </div>
          </el-card>
        </div>
        
        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            v-model:current-page="searchForm.page"
            v-model:page-size="searchForm.per_page"
            :total="total"
            :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { jobsApi } from '@/api/jobs'
import { applicationsApi } from '@/api/applications'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const jobs = ref([])
const total = ref(0)

const searchForm = reactive({
  keyword: '',
  location: '',
  page: 1,
  per_page: 10
})

const formatSalary = (min, max) => {
  if (!min && !max) return '薪资面议'
  return `${min || 0}K - ${max || 0}K`
}

const formatJobType = (type) => {
  const map = {
    full_time: '全职',
    part_time: '兼职',
    intern: '实习'
  }
  return map[type] || '全职'
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 30) return `${days}天前`
  return `${Math.floor(days / 30)}个月前`
}

const fetchJobs = async () => {
  try {
    const res = await jobsApi.getList({
      keyword: searchForm.keyword,
      location: searchForm.location,
      page: searchForm.page,
      per_page: searchForm.per_page
    })
    const data = res.data || res
    jobs.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取职位失败', error)
  }
}

const handleSearch = () => {
  searchForm.page = 1
  fetchJobs()
}

const handlePageChange = (page) => {
  searchForm.page = page
  fetchJobs()
}

const handleSizeChange = (size) => {
  searchForm.per_page = size
  searchForm.page = 1
  fetchJobs()
}

const goToDetail = (id) => {
  router.push(`/jobs/${id}`)
}

const handleApply = async (jobId) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  if (!userStore.isJobSeeker) {
    ElMessage.warning('只有求职者才能投递简历')
    return
  }
  
  try {
    await ElMessageBox.confirm('确定要投递这个职位吗？', '确认投递', {
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    
    await applicationsApi.apply({ job_id: jobId })
    ElMessage.success('投递成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('投递失败', error)
    }
  }
}

// 监听路由参数变化
watch(() => route.query.keyword, (val) => {
  if (val) {
    searchForm.keyword = val
    fetchJobs()
  }
}, { immediate: true })

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
.job-list-page {
  min-height: 100vh;
}

.main-content {
  padding-top: 80px;
  padding-bottom: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.search-section {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.search-input {
  flex: 1;
}

.location-input {
  width: 250px;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.job-item {
  cursor: pointer;
}

.job-item:hover {
  border-color: #409EFF;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.job-title {
  font-size: 18px;
  color: #333;
  margin: 0 0 10px 0;
  cursor: pointer;
}

.job-title:hover {
  color: #409EFF;
}

.job-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.job-salary {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
}

.job-company {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  margin-bottom: 15px;
  cursor: pointer;
}

.company-info {
  color: #999;
  font-size: 13px;
}

.job-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.publish-time {
  color: #999;
  font-size: 13px;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>

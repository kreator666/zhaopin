<template>
  <div class="job-detail-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <!-- 职位信息 -->
        <el-card class="job-card" v-loading="loading">
          <div class="job-header">
            <div>
              <h1 class="job-title">{{ job.title }}</h1>
              <div class="job-tags">
                <el-tag>{{ job.location || '地点不限' }}</el-tag>
                <el-tag>{{ job.experience || '经验不限' }}</el-tag>
                <el-tag>{{ job.education || '学历不限' }}</el-tag>
                <el-tag>{{ formatJobType(job.job_type) }}</el-tag>
              </div>
            </div>
            <div class="job-salary" v-if="job.salary_min || job.salary_max">
              {{ formatSalary(job.salary_min, job.salary_max) }}
            </div>
          </div>
          
          <div class="company-info">
            <h3>{{ job.company?.name }}</h3>
            <p v-if="job.company?.industry">{{ job.company.industry }}</p>
            <p v-if="job.company?.location">{{ job.company.location }}</p>
          </div>
          
          <el-divider />
          
          <div class="job-section">
            <h3>职位描述</h3>
            <pre class="job-description">{{ job.description }}</pre>
          </div>
          
          <div class="job-section" v-if="job.requirements">
            <h3>任职要求</h3>
            <pre class="job-description">{{ job.requirements }}</pre>
          </div>
          
          <div class="job-footer">
            <span class="view-count">
              <el-icon><View /></el-icon>
              {{ job.view_count }} 浏览
            </span>
            <span class="publish-time">{{ formatTime(job.created_at) }}发布</span>
            <el-button 
              type="primary" 
              size="large" 
              @click="handleApply"
              :disabled="hasApplied"
            >
              {{ hasApplied ? '已投递' : '立即投递' }}
            </el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { jobsApi } from '@/api/jobs'
import { applicationsApi } from '@/api/applications'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const job = ref({})
const loading = ref(false)
const hasApplied = ref(false)

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
  return date.toLocaleDateString('zh-CN')
}

const fetchJobDetail = async () => {
  loading.value = true
  try {
    const res = await jobsApi.getDetail(route.params.id)
    const data = res.data || res
    job.value = data
  } catch (error) {
    console.error('获取职位详情失败', error)
    ElMessage.error('职位不存在')
    router.push('/jobs')
  } finally {
    loading.value = false
  }
}

const handleApply = async () => {
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
    
    await applicationsApi.apply({ job_id: job.value.id })
    ElMessage.success('投递成功')
    hasApplied.value = true
  } catch (error) {
    if (error !== 'cancel') {
      console.error('投递失败', error)
    }
  }
}

onMounted(() => {
  fetchJobDetail()
})
</script>

<style scoped>
.job-detail-page {
  min-height: 100vh;
}

.main-content {
  padding-top: 80px;
  padding-bottom: 40px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.job-card {
  padding: 20px;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.job-title {
  font-size: 28px;
  color: #333;
  margin: 0 0 15px 0;
}

.job-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.job-salary {
  color: #f56c6c;
  font-size: 24px;
  font-weight: bold;
}

.company-info {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.company-info h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.company-info p {
  margin: 5px 0;
  color: #666;
}

.job-section {
  margin-bottom: 30px;
}

.job-section h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
  border-left: 4px solid #409EFF;
  padding-left: 10px;
}

.job-description {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #555;
  font-family: inherit;
  font-size: 14px;
}

.job-footer {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.view-count {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #999;
}

.publish-time {
  flex: 1;
  color: #999;
}
</style>

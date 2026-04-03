<template>
  <div class="applications-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <h2 class="page-title">我的投递记录</h2>
        
        <el-empty v-if="applications.length === 0" description="暂无投递记录" />
        
        <div v-else class="application-list">
          <el-card v-for="app in applications" :key="app.id" class="application-item">
            <div class="app-header">
              <div class="job-info">
                <h3 class="job-title" @click="goToJob(app.job?.id)">{{ app.job?.title }}</h3>
                <p class="company-name">{{ app.job?.company?.name }}</p>
              </div>
              <el-tag :type="getStatusType(app.status)">{{ getStatusText(app.status) }}</el-tag>
            </div>
            
            <div class="app-footer">
              <span class="apply-time">投递时间：{{ formatTime(app.created_at) }}</span>
              <span class="update-time" v-if="app.updated_at !== app.created_at">
                更新时间：{{ formatTime(app.updated_at) }}
              </span>
            </div>
            
            <div class="hr-remark" v-if="app.hr_remark">
              <el-divider />
              <p><strong>HR备注：</strong>{{ app.hr_remark }}</p>
            </div>
          </el-card>
        </div>
        
        <div class="pagination" v-if="total > 0">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="perPage"
            :total="total"
            layout="prev, pager, next"
            @current-change="fetchApplications"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { applicationsApi } from '@/api/applications'

const router = useRouter()

const applications = ref([])
const page = ref(1)
const perPage = ref(10)
const total = ref(0)

const getStatusType = (status) => {
  const map = {
    pending: 'warning',
    accepted: 'success',
    rejected: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = {
    pending: '待处理',
    accepted: '已接受',
    rejected: '已拒绝'
  }
  return map[status] || status
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

const fetchApplications = async () => {
  try {
    const res = await applicationsApi.getMyApplications({
      page: page.value,
      per_page: perPage.value
    })
    const data = res.data || res
    applications.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取投递记录失败', error)
  }
}

const goToJob = (jobId) => {
  if (jobId) {
    router.push(`/jobs/${jobId}`)
  }
}

onMounted(() => {
  fetchApplications()
})
</script>

<style scoped>
.applications-page {
  min-height: 100vh;
}

.main-content {
  padding-top: 80px;
  padding-bottom: 40px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  margin-bottom: 30px;
  color: #333;
}

.application-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.application-item {
  margin-bottom: 0;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.job-title {
  font-size: 18px;
  color: #333;
  margin: 0 0 8px 0;
  cursor: pointer;
}

.job-title:hover {
  color: #409EFF;
}

.company-name {
  color: #666;
  margin: 0;
}

.app-footer {
  display: flex;
  gap: 20px;
  color: #999;
  font-size: 13px;
}

.hr-remark {
  margin-top: 10px;
  color: #666;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>

<template>
  <div class="dashboard">
    <h2 class="page-title">企业概览</h2>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon blue">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalJobs }}</div>
            <div class="stat-label">发布职位</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon green">
            <el-icon><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.activeJobs }}</div>
            <div class="stat-label">招聘中</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon orange">
            <el-icon><MessageBox /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalApplications }}</div>
            <div class="stat-label">收到简历</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon purple">
            <el-icon><Timer /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.pendingApplications }}</div>
            <div class="stat-label">待处理</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快速操作 -->
    <el-card class="quick-actions">
      <template #header>
        <span>快速操作</span>
      </template>
      <div class="action-list">
        <div class="action-item" @click="goToCreateJob">
          <div class="action-icon">
            <el-icon><Plus /></el-icon>
          </div>
          <div class="action-info">
            <h4>发布新职位</h4>
            <p>创建新的招聘岗位，吸引优秀人才</p>
          </div>
          <el-icon class="action-arrow"><ArrowRight /></el-icon>
        </div>
        
        <div class="action-item" @click="goToApplications">
          <div class="action-icon orange">
            <el-icon><MessageBox /></el-icon>
          </div>
          <div class="action-info">
            <h4>处理简历</h4>
            <p>查看并处理收到的候选人简历</p>
          </div>
          <el-icon class="action-arrow"><ArrowRight /></el-icon>
          <el-badge v-if="stats.pendingApplications > 0" :value="stats.pendingApplications" class="action-badge" />
        </div>
        
        <div class="action-item" @click="goToJobs">
          <div class="action-icon green">
            <el-icon><Management /></el-icon>
          </div>
          <div class="action-info">
            <h4>管理职位</h4>
            <p>编辑、上架/下架已发布的职位</p>
          </div>
          <el-icon class="action-arrow"><ArrowRight /></el-icon>
        </div>
      </div>
    </el-card>
    
    <!-- 招聘流程说明 -->
    <el-card class="process-guide">
      <template #header>
        <span>招聘流程指南</span>
      </template>
      <el-steps :active="0" simple>
        <el-step title="发布职位" description="创建岗位信息" :icon="Document" />
        <el-step title="接收简历" description="查看候选人" :icon="MessageBox" />
        <el-step title="筛选评估" description="评估匹配度" :icon="Filter" />
        <el-step title="接受/拒绝" description="处理申请" :icon="CircleCheck" />
        <el-step title="安排面试" description="联系候选人" :icon="Phone" />
      </el-steps>
    </el-card>
    
    <!-- 最新简历提醒 -->
    <el-card v-if="recentApplications.length > 0" class="recent-apps">
      <template #header>
        <div class="card-header">
          <span>最新投递</span>
          <el-link type="primary" @click="goToApplications">查看全部</el-link>
        </div>
      </template>
      <el-table :data="recentApplications" style="width: 100%">
        <el-table-column prop="seeker_profile.name" label="候选人" width="120" />
        <el-table-column prop="job.title" label="应聘职位" />
        <el-table-column label="投递时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="success" size="small" @click="handleAccept(row.id)">接受</el-button>
            <el-button type="danger" size="small" @click="handleReject(row.id)">拒绝</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { jobsApi } from '@/api/jobs'
import { applicationsApi } from '@/api/applications'
import { Document, MessageBox, CircleCheck, Timer, Plus, ArrowRight, Management, Filter, Phone } from '@element-plus/icons-vue'

const router = useRouter()

const stats = ref({
  totalJobs: 0,
  activeJobs: 0,
  totalApplications: 0,
  pendingApplications: 0
})

const recentApplications = ref([])

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

const fetchStats = async () => {
  try {
    // 获取职位统计
    const jobsRes = await jobsApi.getMyJobs({ per_page: 100 })
    const jobsData = jobsRes.data || jobsRes
    const jobs = jobsData.items || []
    stats.value.totalJobs = jobs.length
    stats.value.activeJobs = jobs.filter(j => j.status === 'active').length
    
    // 获取简历统计
    const appsRes = await applicationsApi.getReceivedApplications({ per_page: 100 })
    const appsData = appsRes.data || appsRes
    const apps = appsData.items || []
    stats.value.totalApplications = apps.length
    stats.value.pendingApplications = apps.filter(a => a.status === 'pending').length
    
    // 最新5条待处理简历
    recentApplications.value = apps.filter(a => a.status === 'pending').slice(0, 5)
  } catch (error) {
    console.error('获取统计数据失败', error)
  }
}

const goToCreateJob = () => {
  router.push('/company/jobs/create')
}

const goToJobs = () => {
  router.push('/company/jobs')
}

const goToApplications = () => {
  router.push('/company/applications')
}

const handleAccept = async (id) => {
  try {
    await applicationsApi.updateStatus(id, { status: 'accepted' })
    ElMessage.success('已接受该候选人')
    fetchStats()
  } catch (error) {
    console.error('操作失败', error)
  }
}

const handleReject = async (id) => {
  try {
    await applicationsApi.updateStatus(id, { status: 'rejected' })
    ElMessage.success('已拒绝该候选人')
    fetchStats()
  } catch (error) {
    console.error('操作失败', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.page-title {
  margin: 0 0 20px 0;
  font-size: 24px;
  color: #333;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 10px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-right: 15px;
}

.stat-icon.blue {
  background: #ecf5ff;
  color: #409EFF;
}

.stat-icon.green {
  background: #f0f9eb;
  color: #67c23a;
}

.stat-icon.orange {
  background: #fdf6ec;
  color: #e6a23c;
}

.stat-icon.purple {
  background: #f5f0ff;
  color: #9254de;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 5px;
}

.quick-actions {
  margin-bottom: 20px;
}

.action-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.action-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.action-item:hover {
  background: #ecf5ff;
  transform: translateX(5px);
}

.action-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  background: #409EFF;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}

.action-icon.orange {
  background: #e6a23c;
}

.action-icon.green {
  background: #67c23a;
}

.action-info {
  flex: 1;
}

.action-info h4 {
  margin: 0 0 5px 0;
  color: #333;
}

.action-info p {
  margin: 0;
  color: #999;
  font-size: 14px;
}

.action-arrow {
  font-size: 20px;
  color: #c0c4cc;
}

.action-badge {
  position: absolute;
  right: 50px;
  top: 50%;
  transform: translateY(-50%);
}

.process-guide {
  margin-bottom: 20px;
}

.process-guide :deep(.el-step__title) {
  font-size: 14px;
}

.recent-apps {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

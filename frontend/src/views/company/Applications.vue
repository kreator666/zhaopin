<template>
  <div class="received-applications">
    <div class="page-header">
      <h2>收到的简历</h2>
    </div>
    
    <el-card>
      <el-empty v-if="applications.length === 0" description="暂无收到的简历" />
      
      <div v-else class="application-list">
        <el-card v-for="app in applications" :key="app.id" class="app-item">
          <div class="app-header">
            <div class="seeker-info">
              <h3>{{ app.seeker_profile?.name || '未填写姓名' }}</h3>
              <p v-if="app.seeker_profile?.location">
                <el-icon><Location /></el-icon>
                {{ app.seeker_profile.location }}
              </p>
            </div>
            <div class="job-info">
              <span>应聘职位：{{ app.job?.title }}</span>
            </div>
          </div>
          
          <div class="app-body" v-if="app.seeker_profile">
            <div class="info-row">
              <span v-if="app.seeker_profile.gender">性别：{{ app.seeker_profile.gender }}</span>
              <span v-if="app.seeker_profile.skills">技能：{{ app.seeker_profile.skills }}</span>
            </div>
            
            <el-collapse v-if="app.seeker_profile.experience_text || app.seeker_profile.education_text">
              <el-collapse-item title="工作经历" v-if="app.seeker_profile.experience_text">
                <pre>{{ app.seeker_profile.experience_text }}</pre>
              </el-collapse-item>
              <el-collapse-item title="教育经历" v-if="app.seeker_profile.education_text">
                <pre>{{ app.seeker_profile.education_text }}</pre>
              </el-collapse-item>
            </el-collapse>
          </div>
          
          <div class="app-footer">
            <div class="status-section">
              <span>当前状态：</span>
              <el-tag :type="getStatusType(app.status)">{{ getStatusText(app.status) }}</el-tag>
            </div>
            
            <div class="actions" v-if="app.status === 'pending'">
              <el-button type="success" size="small" @click="handleAccept(app.id)">
                接受
              </el-button>
              <el-button type="danger" size="small" @click="handleReject(app.id)">
                拒绝
              </el-button>
            </div>
          </div>
          
          <div class="remark-section" v-if="app.hr_remark">
            <el-divider />
            <p><strong>备注：</strong>{{ app.hr_remark }}</p>
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
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { applicationsApi } from '@/api/applications'

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

const fetchApplications = async () => {
  try {
    const res = await applicationsApi.getReceivedApplications({
      page: page.value,
      per_page: perPage.value
    })
    applications.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('获取简历失败', error)
  }
}

const handleAccept = async (id) => {
  try {
    await applicationsApi.updateStatus(id, { status: 'accepted' })
    ElMessage.success('已接受该候选人')
    fetchApplications()
  } catch (error) {
    console.error('操作失败', error)
  }
}

const handleReject = async (id) => {
  try {
    await applicationsApi.updateStatus(id, { status: 'rejected' })
    ElMessage.success('已拒绝该候选人')
    fetchApplications()
  } catch (error) {
    console.error('操作失败', error)
  }
}

onMounted(() => {
  fetchApplications()
})
</script>

<style scoped>
.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.application-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.app-item {
  margin-bottom: 0;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.seeker-info h3 {
  margin: 0 0 8px 0;
  color: #333;
}

.seeker-info p {
  color: #666;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.job-info {
  color: #409EFF;
}

.app-body {
  margin-bottom: 15px;
}

.info-row {
  display: flex;
  gap: 30px;
  margin-bottom: 15px;
  color: #666;
}

.app-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.status-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.actions {
  display: flex;
  gap: 10px;
}

.remark-section {
  margin-top: 10px;
  color: #666;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

pre {
  white-space: pre-wrap;
  font-family: inherit;
  color: #555;
  line-height: 1.6;
}
</style>

<template>
  <div class="campus-talk-detail">
    <Navbar />
    
    <div class="main-content" style="padding-top: 60px;">
      <div class="container">
        <el-button text @click="$router.back()" class="back-btn">
          <el-icon><ArrowLeft /></el-icon> 返回列表
        </el-button>
        
        <el-card v-if="talk.id" shadow="hover" class="detail-card">
          <div class="talk-header">
            <h1>{{ talk.title }}</h1>
            <el-tag :type="statusType(talk.status)" size="large">{{ statusText(talk.status) }}</el-tag>
          </div>
          
          <div class="company-info" v-if="talk.company">
            <el-avatar :size="60" :src="talk.company.logo" />
            <div class="company-meta">
              <h3>{{ talk.company.name }}</h3>
              <p>{{ talk.company.industry }} · {{ talk.company.scale }}</p>
            </div>
          </div>
          
          <el-divider />
          
          <div class="info-list">
            <div class="info-item">
              <el-icon><School /></el-icon>
              <span class="label">目标学校：</span>
              <span>{{ talk.school_name }}</span>
            </div>
            <div class="info-item">
              <el-icon><Calendar /></el-icon>
              <span class="label">开始时间：</span>
              <span>{{ formatDateTime(talk.start_time) }}</span>
            </div>
            <div class="info-item" v-if="talk.end_time">
              <el-icon><Timer /></el-icon>
              <span class="label">结束时间：</span>
              <span>{{ formatDateTime(talk.end_time) }}</span>
            </div>
            <div class="info-item">
              <el-icon><Location /></el-icon>
              <span class="label">宣讲地点：</span>
              <span>{{ talk.location || '待定' }}</span>
            </div>
          </div>
          
          <el-divider />
          
          <div class="description-section">
            <h3>宣讲介绍</h3>
            <p class="description-content">{{ talk.description || '暂无介绍' }}</p>
          </div>
          
          <div class="actions" v-if="talk.status !== 'ended'">
            <el-button 
              v-if="talk.registration_url" 
              type="primary" 
              size="large"
              @click="openRegistration"
            >
              立即报名
            </el-button>
            <el-button type="success" size="large" @click="shareTalk">
              <el-icon><Share /></el-icon> 分享
            </el-button>
          </div>
          
          <div class="view-count">
            <el-icon><View /></el-icon>
            <span>{{ talk.view_count || 0 }} 次浏览</span>
          </div>
        </el-card>
        
        <el-skeleton v-else :rows="10" animated />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, School, Calendar, Timer, Location, Share, View } from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import { getCampusTalk } from '@/api/interview'

const route = useRoute()
const talk = ref({})

const fetchDetail = async () => {
  try {
    const res = await getCampusTalk(route.params.id)
    talk.value = res.data || res
  } catch (error) {
    ElMessage.error('获取详情失败')
  }
}

const statusType = (status) => {
  const types = { upcoming: 'primary', ongoing: 'success', ended: 'info' }
  return types[status] || 'info'
}

const statusText = (status) => {
  const texts = { upcoming: '即将开始', ongoing: '进行中', ended: '已结束' }
  return texts[status] || status
}

const formatDateTime = (datetime) => {
  if (!datetime) return ''
  return new Date(datetime).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const openRegistration = () => {
  if (talk.value.registration_url) {
    window.open(talk.value.registration_url, '_blank')
  }
}

const shareTalk = () => {
  ElMessage.success('链接已复制到剪贴板')
}

onMounted(fetchDetail)
</script>

<style scoped>
.campus-talk-detail {
  min-height: 100vh;
  background: #f5f7fa;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.back-btn {
  margin-bottom: 20px;
}

.detail-card {
  padding: 20px;
}

.talk-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.talk-header h1 {
  margin: 0;
  font-size: 28px;
}

.company-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.company-meta h3 {
  margin: 0 0 4px 0;
}

.company-meta p {
  margin: 0;
  color: #666;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
}

.info-item .label {
  color: #666;
  min-width: 80px;
}

.description-section h3 {
  margin-bottom: 12px;
}

.description-content {
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
}

.actions {
  margin-top: 32px;
  display: flex;
  gap: 16px;
  justify-content: center;
}

.view-count {
  margin-top: 24px;
  text-align: center;
  color: #999;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
</style>

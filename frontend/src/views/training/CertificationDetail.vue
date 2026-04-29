<template>
  <div class="cert-detail-page">
    <Navbar />
    
    <!-- 面包屑 -->
    <div class="breadcrumb-section">
      <div class="container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: '/training/certifications' }">考证信息</el-breadcrumb-item>
          <el-breadcrumb-item>{{ certification?.name || '详情' }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>
    
    <div class="main-content">
      <div class="container" v-loading="loading">
        <div v-if="!loading && certification" class="detail-content">
          <!-- 基本信息 -->
          <div class="basic-info">
            <div class="info-header">
              <div class="status-tags">
                <el-tag :type="getStatusTagType(certification.status)" size="large">
                  {{ getStatusName(certification.status) }}
                </el-tag>
                <el-tag type="info" size="large">
                  {{ getCategoryName(certification.category) }}
                </el-tag>
              </div>
              <h1 class="cert-name">{{ certification.name }}</h1>
              <p class="cert-organizer" v-if="certification.organizer">
                主办单位：{{ certification.organizer }}
              </p>
            </div>
            
            <!-- 时间信息卡片 -->
            <div class="info-cards">
              <div class="info-card">
                <div class="info-card-icon bg-warning">
                  <el-icon><Calendar /></el-icon>
                </div>
                <div class="info-card-content">
                  <div class="info-card-label">报名时间</div>
                  <div class="info-card-value">
                    {{ certification.registration_start || '待定' }} 
                    <span v-if="certification.registration_start && certification.registration_end">
                      ~ {{ certification.registration_end }}
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="info-card">
                <div class="info-card-icon bg-primary">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="info-card-content">
                  <div class="info-card-label">考试时间</div>
                  <div class="info-card-value">
                    {{ certification.exam_date || '待定' }}
                  </div>
                </div>
              </div>
              
              <div class="info-card">
                <div class="info-card-icon bg-success">
                  <el-icon><Money /></el-icon>
                </div>
                <div class="info-card-content">
                  <div class="info-card-label">报名费用</div>
                  <div class="info-card-value">
                    {{ certification.fee !== null && certification.fee !== undefined 
                      ? (certification.fee > 0 ? '¥' + certification.fee : '免费') 
                      : '待定' }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 操作按钮 -->
            <div class="action-buttons" v-if="certification.registration_url">
              <el-button 
                type="primary" 
                size="large"
                @click="openRegistration"
              >
                <el-icon><Link /></el-icon>
                立即报名
              </el-button>
              <el-button 
                size="large"
                @click="goToList"
              >
                返回列表
              </el-button>
            </div>
            
            <div class="action-buttons" v-else>
              <el-button size="large" @click="goToList">
                返回列表
              </el-button>
            </div>
          </div>
          
          <!-- 详细描述 -->
          <div class="detail-section" v-if="certification.description">
            <h3 class="section-title">
              <el-icon><Document /></el-icon>
              考试介绍
            </h3>
            <div class="section-content">
              <p class="desc-text">{{ certification.description }}</p>
            </div>
          </div>
          
          <!-- 报考条件 -->
          <div class="detail-section" v-if="certification.requirements">
            <h3 class="section-title">
              <el-icon><User /></el-icon>
              报考条件
            </h3>
            <div class="section-content">
              <p class="desc-text">{{ certification.requirements }}</p>
            </div>
          </div>
          
          <!-- 发布时间 -->
          <div class="publish-info">
            <span>发布时间：{{ certification.created_at ? formatTime(certification.created_at) : '-' }}</span>
          </div>
        </div>
        
        <!-- 空状态 -->
        <el-empty v-if="!loading && !certification" description="考证信息不存在" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { getCertification } from '@/api/training'
import { ElMessage } from 'element-plus'
import {
  Calendar, Clock, Money, Link, Document, User
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const certification = ref(null)

// 分类映射
const categoryMap = {
  language: '语言考试',
  computer: '计算机等级',
  professional: '职业资格',
  finance: '金融财会',
  other: '其他'
}

// 状态映射
const statusMap = {
  upcoming: { name: '即将开始', type: 'warning' },
  ongoing: { name: '报名中', type: 'success' },
  ended: { name: '已结束', type: 'info' }
}

// 获取分类名称
const getCategoryName = (category) => {
  return categoryMap[category] || '其他'
}

// 获取状态名称
const getStatusName = (status) => {
  return statusMap[status]?.name || status
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  return statusMap[status]?.type || 'info'
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

// 获取考证详情
const fetchCertification = async () => {
  const certId = route.params.id
  if (!certId) return
  
  loading.value = true
  try {
    const res = await getCertification(certId)
    const data = res.data || res
    certification.value = data
  } catch (error) {
    console.error('获取考证详情失败', error)
    ElMessage.error('获取考证信息失败')
  } finally {
    loading.value = false
  }
}

// 打开报名链接
const openRegistration = () => {
  if (certification.value?.registration_url) {
    window.open(certification.value.registration_url, '_blank')
  }
}

// 返回列表
const goToList = () => {
  router.push('/training/certifications')
}

onMounted(() => {
  fetchCertification()
})
</script>

<style scoped>
.cert-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 60px;
}

.breadcrumb-section {
  background: #fff;
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}

.main-content {
  padding: 30px 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.basic-info {
  background: #fff;
  border-radius: 12px;
  padding: 30px;
}

.info-header {
  margin-bottom: 30px;
}

.status-tags {
  margin-bottom: 16px;
  display: flex;
  gap: 10px;
}

.cert-name {
  font-size: 28px;
  color: #303133;
  margin: 0 0 12px 0;
  font-weight: 600;
}

.cert-organizer {
  font-size: 15px;
  color: #606266;
  margin: 0;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.info-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.info-card-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
  flex-shrink: 0;
}

.bg-warning {
  background: linear-gradient(135deg, #E6A23C 0%, #F56C6C 100%);
}

.bg-primary {
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
}

.bg-success {
  background: linear-gradient(135deg, #67C23A 0%, #909399 100%);
}

.info-card-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-card-label {
  font-size: 13px;
  color: #909399;
}

.info-card-value {
  font-size: 15px;
  color: #303133;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.detail-section {
  background: #fff;
  border-radius: 12px;
  padding: 24px 30px;
}

.section-title {
  font-size: 18px;
  color: #303133;
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.section-content {
  color: #606266;
}

.desc-text {
  font-size: 15px;
  line-height: 1.8;
  margin: 0;
  white-space: pre-wrap;
}

.publish-info {
  text-align: right;
  font-size: 14px;
  color: #909399;
}
</style>

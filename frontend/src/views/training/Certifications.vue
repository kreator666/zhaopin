<template>
  <div class="certifications-page">
    <Navbar />
    
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1>考证信息</h1>
            <p>四六级、计算机等级、职业资格考试，助您职业规划</p>
          </div>
          <div class="header-actions">
            <el-button 
              v-if="userStore.isLoggedIn && userStore.userInfo?.role === 'admin'" 
              type="primary" 
              size="large"
              @click="$router.push('/company/certifications')"
            >
              <el-icon><Plus /></el-icon>
              管理考证信息
            </el-button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="main-content">
      <div class="container">
        <!-- 筛选栏 -->
        <div class="filter-section">
          <div class="filter-row">
            <span class="filter-label">状态：</span>
            <el-radio-group v-model="filterForm.status" size="small" @change="handleFilterChange">
              <el-radio-button value="">全部</el-radio-button>
              <el-radio-button value="upcoming">即将开始</el-radio-button>
              <el-radio-button value="ongoing">报名中</el-radio-button>
              <el-radio-button value="ended">已结束</el-radio-button>
            </el-radio-group>
          </div>
          
          <div class="filter-row">
            <span class="filter-label">分类：</span>
            <el-radio-group v-model="filterForm.category" size="small" @change="handleFilterChange">
              <el-radio-button value="">全部</el-radio-button>
              <el-radio-button value="language">语言考试</el-radio-button>
              <el-radio-button value="computer">计算机等级</el-radio-button>
              <el-radio-button value="professional">职业资格</el-radio-button>
              <el-radio-button value="finance">金融财会</el-radio-button>
              <el-radio-button value="other">其他</el-radio-button>
            </el-radio-group>
          </div>
        </div>
        
        <!-- 考证列表 -->
        <div class="cert-list" v-loading="loading">
          <el-empty v-if="!loading && certifications.length === 0" description="暂无考证信息" />
          
          <el-card 
            v-for="cert in certifications" 
            :key="cert.id" 
            class="cert-card" 
            shadow="hover"
            @click="goToDetail(cert.id)"
          >
            <div class="cert-card-header">
              <div class="cert-status">
                <el-tag :type="getStatusTagType(cert.status)" size="small">
                  {{ getStatusName(cert.status) }}
                </el-tag>
              </div>
              <div class="cert-category">
                <el-tag type="info" size="small">
                  {{ getCategoryName(cert.category) }}
                </el-tag>
              </div>
            </div>
            
            <h3 class="cert-title">{{ cert.name }}</h3>
            
            <div class="cert-meta">
              <div class="meta-item" v-if="cert.organizer">
                <el-icon><OfficeBuilding /></el-icon>
                <span>{{ cert.organizer }}</span>
              </div>
              <div class="meta-item" v-if="cert.registration_start">
                <el-icon><Calendar /></el-icon>
                <span>报名: {{ cert.registration_start }} ~ {{ cert.registration_end || '-' }}</span>
              </div>
              <div class="meta-item" v-if="cert.exam_date">
                <el-icon><Clock /></el-icon>
                <span>考试: {{ cert.exam_date }}</span>
              </div>
              <div class="meta-item" v-if="cert.fee !== null && cert.fee !== undefined">
                <el-icon><Money /></el-icon>
                <span>费用: {{ cert.fee > 0 ? '¥' + cert.fee : '免费' }}</span>
              </div>
            </div>
            
            <div class="cert-desc" v-if="cert.description">
              {{ cert.description.length > 100 ? cert.description.substring(0, 100) + '...' : cert.description }}
            </div>
            
            <div class="cert-card-footer">
              <el-button type="primary" size="small">
                查看详情
              </el-button>
            </div>
          </el-card>
        </div>
        
        <!-- 分页 -->
        <div v-if="certifications.length > 0" class="pagination">
          <el-pagination
            v-model:current-page="filterForm.page"
            v-model:page-size="filterForm.per_page"
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import { useUserStore } from '@/stores/user'
import { getCertifications } from '@/api/training'
import {
  Plus, OfficeBuilding, Calendar, Clock, Money
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const certifications = ref([])
const total = ref(0)

// 筛选表单
const filterForm = reactive({
  category: '',
  status: '',
  page: 1,
  per_page: 12
})

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

// 获取考证列表
const fetchCertifications = async () => {
  loading.value = true
  try {
    const params = {
      page: filterForm.page,
      per_page: filterForm.per_page
    }
    if (filterForm.category) {
      params.category = filterForm.category
    }
    if (filterForm.status) {
      params.status = filterForm.status
    }
    
    const res = await getCertifications(params)
    const data = res.data || res
    certifications.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取考证信息失败', error)
  } finally {
    loading.value = false
  }
}

// 筛选变化
const handleFilterChange = () => {
  filterForm.page = 1
  fetchCertifications()
}

// 分页变化
const handleSizeChange = () => {
  filterForm.page = 1
  fetchCertifications()
}

const handlePageChange = () => {
  fetchCertifications()
}

// 跳转详情
const goToDetail = (id) => {
  router.push(`/training/certifications/${id}`)
}

onMounted(() => {
  fetchCertifications()
})
</script>

<style scoped>
.certifications-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 60px;
}

.page-header {
  background: linear-gradient(135deg, #E6A23C 0%, #F56C6C 100%);
  color: #fff;
  padding: 40px 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 32px;
}

.page-header p {
  margin: 0;
  font-size: 16px;
  opacity: 0.9;
}

.main-content {
  padding: 30px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.filter-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.filter-label {
  font-size: 14px;
  color: #606266;
  margin-right: 12px;
  width: 50px;
  flex-shrink: 0;
}

.cert-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.cert-card {
  cursor: pointer;
  transition: all 0.3s;
}

.cert-card:hover {
  transform: translateY(-4px);
}

.cert-card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.cert-title {
  font-size: 18px;
  color: #303133;
  margin: 0 0 15px 0;
  font-weight: 600;
}

.cert-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 20px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #606266;
}

.meta-item .el-icon {
  color: #909399;
}

.cert-desc {
  font-size: 14px;
  color: #909399;
  line-height: 1.6;
  margin-bottom: 15px;
}

.cert-card-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>

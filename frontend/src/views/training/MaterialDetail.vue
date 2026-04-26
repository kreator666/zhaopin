<template>
  <div class="material-detail-page">
    <Navbar />
    
    <div class="main-content" v-loading="loading">
      <div class="container" v-if="material">
        <!-- 面包屑导航 -->
        <el-breadcrumb separator="/" class="breadcrumb">
          <el-breadcrumb-item :to="{ path: '/training' }">培训学习</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: '/training/materials' }">学习资料</el-breadcrumb-item>
          <el-breadcrumb-item>{{ material.title }}</el-breadcrumb-item>
        </el-breadcrumb>
        
        <div class="detail-content">
          <!-- 左侧：资料信息 -->
          <div class="info-section">
            <div class="material-header">
              <div class="material-icon">
                <el-icon :size="64" :color="getFileIconColor(material.file_type)">
                  <component :is="getFileIcon(material.file_type)" />
                </el-icon>
              </div>
              <div class="material-basic">
                <h1 class="material-title">{{ material.title }}</h1>
                <div class="material-meta">
                  <el-tag size="small" type="info">{{ getCategoryName(material.category) }}</el-tag>
                  <span class="file-type-tag">{{ getFileTypeName(material.file_type) }}</span>
                  <span v-if="material.file_size" class="file-size">
                    {{ formatFileSize(material.file_size) }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- 资料描述 -->
            <div class="description-section" v-if="material.description">
              <h3 class="section-title">资料描述</h3>
              <div class="description-content">
                {{ material.description }}
              </div>
            </div>
            
            <!-- 统计信息 -->
            <div class="stats-section">
              <h3 class="section-title">资料统计</h3>
              <div class="stats-grid">
                <div class="stat-item">
                  <span class="stat-icon"><el-icon><Download /></el-icon></span>
                  <div class="stat-info">
                    <span class="stat-value">{{ material.download_count }}</span>
                    <span class="stat-label">下载次数</span>
                  </div>
                </div>
                <div class="stat-item">
                  <span class="stat-icon"><el-icon><Star /></el-icon></span>
                  <div class="stat-info">
                    <span class="stat-value">{{ material.like_count }}</span>
                    <span class="stat-label">点赞数</span>
                  </div>
                </div>
                <div class="stat-item">
                  <span class="stat-icon"><el-icon><Calendar /></el-icon></span>
                  <div class="stat-info">
                    <span class="stat-value">{{ formatDate(material.created_at) }}</span>
                    <span class="stat-label">上传时间</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 右侧：上传者信息和操作 -->
          <div class="action-section">
            <!-- 上传者信息 -->
            <div class="uploader-card" v-if="material.user">
              <div class="uploader-info" @click="goToProfile(material.user.id)">
                <el-avatar :size="56" :src="getUserAvatar(material.user.avatar_url)" />
                <div class="uploader-detail">
                  <span class="uploader-name">{{ material.user.username }}</span>
                  <span class="uploader-school" v-if="material.user.school_name">
                    {{ material.user.school_name }}
                  </span>
                </div>
              </div>
              
              <el-button 
                v-if="!isOwner" 
                type="primary" 
                size="large" 
                @click="contactUploader"
              >
                <el-icon><ChatDotRound /></el-icon>
                联系上传者
              </el-button>
            </div>
            
            <!-- 操作按钮 -->
            <div class="action-buttons">
              <el-button 
                type="primary" 
                size="large" 
                @click="handleDownload"
                :loading="downloading"
              >
                <el-icon><Download /></el-icon>
                下载资料
              </el-button>
              
              <el-button 
                size="large" 
                @click="handleLike"
                :loading="liking"
              >
                <el-icon><Star /></el-icon>
                点赞 ({{ material.like_count }})
              </el-button>
              
              <!-- 上传者操作 -->
              <template v-if="isOwner">
                <el-button 
                  type="danger" 
                  size="large" 
                  @click="handleDelete"
                >
                  <el-icon><Delete /></el-icon>
                  删除资料
                </el-button>
              </template>
            </div>
            
            <!-- 下载说明 -->
            <div class="download-tip">
              <el-alert
                title="下载说明"
                type="info"
                :closable="false"
              >
                <template #default>
                  <ul>
                    <li>下载资料后，请在 1 天内完成学习</li>
                    <li>资料仅供个人学习使用，请勿商用</li>
                    <li>如果资料对您有帮助，请点赞支持</li>
                  </ul>
                </template>
              </el-alert>
            </div>
          </div>
        </div>
        
        <!-- 相关推荐 -->
        <div class="recommend-section" v-if="recommendMaterials.length > 0">
          <h3 class="section-title">相关推荐</h3>
          <div class="recommend-grid">
            <el-card 
              v-for="rec in recommendMaterials" 
              :key="rec.id" 
              class="recommend-card"
              shadow="hover"
              @click="goToDetail(rec.id)"
            >
              <div class="recommend-icon">
                <el-icon :size="32" :color="getFileIconColor(rec.file_type)">
                  <component :is="getFileIcon(rec.file_type)" />
                </el-icon>
              </div>
              <h4 class="recommend-title">{{ rec.title }}</h4>
              <div class="recommend-stats">
                <span><el-icon><Download /></el-icon> {{ rec.download_count }}</span>
                <span><el-icon><Star /></el-icon> {{ rec.like_count }}</span>
              </div>
            </el-card>
          </div>
        </div>
      </div>
      
      <!-- 错误状态 -->
      <div class="error-container" v-else-if="!loading">
        <el-empty description="资料不存在或已被删除" />
        <el-button type="primary" @click="$router.push('/training/materials')">返回资料列表</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { useUserStore } from '@/stores/user'
import { getMaterial, downloadMaterial, likeMaterial, deleteMaterial, getMaterials } from '@/api/training'
import {
  Download, Star, ChatDotRound, Delete, Calendar,
  Document, Picture, Folder, Files
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const API_BASE_URL = 'http://localhost:5000'

const loading = ref(true)
const material = ref(null)
const recommendMaterials = ref([])
const downloading = ref(false)
const liking = ref(false)

// 是否是上传者
const isOwner = computed(() => {
  return userStore.isLoggedIn && material.value?.user_id === userStore.userInfo?.id
})

// 分类映射
const categoryMap = {
  notes: '课堂笔记',
  exam: '考试资料',
  book: '教材课件',
  homework: '作业答案',
  certificate: '考证资料',
  other: '其他'
}

// 文件类型映射
const fileTypeMap = {
  pdf: { icon: 'Document', name: 'PDF', color: '#f56c6c' },
  doc: { icon: 'Document', name: 'Word', color: '#409eff' },
  docx: { icon: 'Document', name: 'Word', color: '#409eff' },
  ppt: { icon: 'Files', name: 'PPT', color: '#e6a23c' },
  pptx: { icon: 'Files', name: 'PPT', color: '#e6a23c' },
  zip: { icon: 'Folder', name: '压缩包', color: '#67c23a' },
  rar: { icon: 'Folder', name: '压缩包', color: '#67c23a' },
  jpg: { icon: 'Picture', name: '图片', color: '#409eff' },
  jpeg: { icon: 'Picture', name: '图片', color: '#409eff' },
  png: { icon: 'Picture', name: '图片', color: '#409eff' },
  gif: { icon: 'Picture', name: '图片', color: '#409eff' },
  video: { icon: 'Files', name: '视频', color: '#909399' }
}

// 获取分类名称
const getCategoryName = (category) => {
  return categoryMap[category] || '其他'
}

// 获取文件图标
const getFileIcon = (fileType) => {
  if (!fileType) return 'Document'
  const type = fileType.toLowerCase()
  return fileTypeMap[type]?.icon || 'Document'
}

// 获取文件图标颜色
const getFileIconColor = (fileType) => {
  if (!fileType) return '#909399'
  const type = fileType.toLowerCase()
  return fileTypeMap[type]?.color || '#909399'
}

// 获取文件类型名称
const getFileTypeName = (fileType) => {
  if (!fileType) return '文件'
  const type = fileType.toLowerCase()
  return fileTypeMap[type]?.name || '文件'
}

// 格式化文件大小
const formatFileSize = (size) => {
  if (!size) return ''
  const bytes = parseInt(size)
  if (isNaN(bytes)) return size
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// 格式化日期
const formatDate = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 获取完整图片URL
const getFullImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${API_BASE_URL}${url}`
}

// 获取用户头像
const getUserAvatar = (avatarUrl) => {
  return getFullImageUrl(avatarUrl) || 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
}

// 获取资料详情
const fetchMaterialDetail = async () => {
  const materialId = route.params.id
  if (!materialId) {
    loading.value = false
    return
  }
  
  loading.value = true
  try {
    const res = await getMaterial(materialId)
    const data = res.data || res
    material.value = data
  } catch (error) {
    console.error('获取资料详情失败', error)
    ElMessage.error('获取资料详情失败')
  } finally {
    loading.value = false
  }
}

// 获取推荐资料
const fetchRecommendMaterials = async () => {
  if (!material.value) return
  
  try {
    const res = await getMaterials({
      category: material.value.category,
      page: 1,
      per_page: 6
    })
    const data = res.data || res
    recommendMaterials.value = (data.items || []).filter(m => m.id !== material.value.id)
  } catch (error) {
    console.error('获取推荐资料失败', error)
  }
}

// 下载资料
const handleDownload = async () => {
  if (!material.value?.file_url) {
    ElMessage.warning('该资料没有可下载的文件')
    return
  }
  
  downloading.value = true
  try {
    // 先调用下载计数接口
    await downloadMaterial(material.value.id)
    material.value.download_count += 1
    
    // 然后下载文件
    const downloadUrl = getFullImageUrl(material.value.file_url)
    
    // 创建临时链接下载
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = material.value.title || 'download'
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('开始下载')
  } catch (error) {
    console.error('下载失败', error)
    ElMessage.error('下载失败，请重试')
  } finally {
    downloading.value = false
  }
}

// 点赞
const handleLike = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  liking.value = true
  try {
    const res = await likeMaterial(material.value.id)
    material.value.like_count = res.data?.like_count || (material.value.like_count + 1)
    ElMessage.success('点赞成功')
  } catch (error) {
    console.error('点赞失败', error)
    ElMessage.error('点赞失败')
  } finally {
    liking.value = false
  }
}

// 删除资料
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除该资料吗？删除后无法恢复。', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteMaterial(material.value.id)
    ElMessage.success('删除成功')
    router.push('/training/materials')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败', error)
      ElMessage.error('删除失败')
    }
  }
}

// 联系上传者
const contactUploader = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  if (isOwner.value) {
    ElMessage.warning('不能联系自己')
    return
  }
  
  if (material.value?.user_id) {
    router.push(`/messages/${material.value.user_id}`)
  }
}

// 跳转到用户主页
const goToProfile = (userId) => {
  if (userId) {
    router.push(`/profile/${userId}`)
  }
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/training/materials/${id}`)
}

onMounted(async () => {
  await fetchMaterialDetail()
  fetchRecommendMaterials()
})
</script>

<style scoped>
.material-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.main-content {
  padding: 100px 0 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumb {
  margin-bottom: 20px;
}

.detail-content {
  display: flex;
  gap: 30px;
}

.info-section {
  flex: 1;
  min-width: 0;
}

.action-section {
  width: 320px;
  flex-shrink: 0;
}

.material-header {
  display: flex;
  gap: 24px;
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 20px;
}

.material-icon {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 8px;
  flex-shrink: 0;
}

.material-basic {
  flex: 1;
  min-width: 0;
}

.material-title {
  font-size: 24px;
  color: #333;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.material-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.file-type-tag {
  font-size: 14px;
  color: #909399;
}

.file-size {
  font-size: 14px;
  color: #909399;
}

.description-section, .stats-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  color: #333;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.description-content {
  color: #666;
  line-height: 1.8;
  white-space: pre-wrap;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #409eff;
  border-radius: 8px;
  color: #fff;
  font-size: 20px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 13px;
  color: #909399;
}

.uploader-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.uploader-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
  cursor: pointer;
}

.uploader-detail {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.uploader-name {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.uploader-school {
  font-size: 13px;
  color: #909399;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.download-tip {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}

.download-tip ul {
  margin: 0;
  padding-left: 20px;
}

.download-tip li {
  font-size: 13px;
  color: #666;
  line-height: 1.8;
}

.recommend-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.recommend-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.recommend-card {
  cursor: pointer;
  text-align: center;
}

.recommend-card :deep(.el-card__body) {
  padding: 20px;
}

.recommend-icon {
  margin-bottom: 12px;
}

.recommend-title {
  font-size: 14px;
  color: #333;
  margin: 0 0 10px 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recommend-stats {
  display: flex;
  justify-content: center;
  gap: 15px;
  font-size: 12px;
  color: #909399;
}

.recommend-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
}

@media (max-width: 992px) {
  .detail-content {
    flex-direction: column;
  }
  
  .action-section {
    width: 100%;
  }
  
  .recommend-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 80px 0 20px;
  }
  
  .material-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .material-meta {
    justify-content: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .recommend-grid {
    grid-template-columns: 1fr;
  }
}
</style>

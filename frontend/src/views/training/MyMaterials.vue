<template>
  <div class="my-materials-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <!-- 页面头部 -->
        <div class="page-header">
          <div class="header-left">
            <h1>我的资料</h1>
            <p>管理你上传的所有学习资料</p>
          </div>
          <el-button type="primary" size="large" @click="$router.push('/training/materials')">
            <el-icon><ArrowLeft /></el-icon>
            返回资料广场
          </el-button>
        </div>
        
        <!-- 筛选栏 -->
        <div class="filter-section">
          <el-radio-group v-model="currentStatus" size="large" @change="handleStatusChange">
            <el-radio-button value="">全部</el-radio-button>
            <el-radio-button value="active">公开</el-radio-button>
            <el-radio-button value="removed">已删除</el-radio-button>
          </el-radio-group>
          
          <el-select 
            v-model="currentCategory" 
            size="large" 
            placeholder="分类筛选" 
            clearable
            @change="handleCategoryChange"
            style="width: 150px"
          >
            <el-option label="课堂笔记" value="notes" />
            <el-option label="考试资料" value="exam" />
            <el-option label="教材课件" value="book" />
            <el-option label="作业答案" value="homework" />
            <el-option label="考证资料" value="certificate" />
            <el-option label="其他" value="other" />
          </el-select>
        </div>
        
        <!-- 资料列表 -->
        <div class="materials-list" v-loading="loading">
          <el-table 
            :data="materials" 
            style="width: 100%"
            v-if="materials.length > 0"
          >
            <el-table-column prop="title" label="资料名称" min-width="250">
              <template #default="{ row }">
                <div class="material-info" @click="goToDetail(row.id)">
                  <div class="material-icon-small">
                    <el-icon :size="28" :color="getFileIconColor(row.file_type)">
                      <component :is="getFileIcon(row.file_type)" />
                    </el-icon>
                  </div>
                  <div class="material-text">
                    <div class="material-title">{{ row.title }}</div>
                    <div class="material-desc" v-if="row.description">
                      {{ row.description }}
                    </div>
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="category" label="分类" width="120">
              <template #default="{ row }">
                <el-tag size="small">{{ getCategoryName(row.category) }}</el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="file_type" label="类型" width="100">
              <template #default="{ row }">
                {{ getFileTypeName(row.file_type) }}
              </template>
            </el-table-column>
            
            <el-table-column prop="download_count" label="下载" width="80">
              <template #default="{ row }">
                <span class="stat-text">
                  <el-icon><Download /></el-icon>
                  {{ row.download_count }}
                </span>
              </template>
            </el-table-column>
            
            <el-table-column prop="like_count" label="点赞" width="80">
              <template #default="{ row }">
                <span class="stat-text">
                  <el-icon><Star /></el-icon>
                  {{ row.like_count }}
                </span>
              </template>
            </el-table-column>
            
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusName(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="is_public" label="可见性" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_public ? 'success' : 'info'" size="small">
                  {{ row.is_public ? '公开' : '私有' }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="created_at" label="上传时间" width="120">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button 
                  type="primary" 
                  link 
                  size="small"
                  @click="handleDownload(row)"
                >
                  下载
                </el-button>
                
                <el-button 
                  type="primary" 
                  link 
                  size="small"
                  @click="toggleVisibility(row)"
                  v-if="row.status === 'active'"
                >
                  {{ row.is_public ? '设为私有' : '设为公开' }}
                </el-button>
                
                <el-button 
                  type="danger" 
                  link 
                  size="small"
                  @click="handleDelete(row)"
                  v-if="row.status === 'active'"
                >
                  删除
                </el-button>
                
                <el-button 
                  type="primary" 
                  link 
                  size="small"
                  @click="restoreMaterial(row)"
                  v-if="row.status === 'removed'"
                >
                  恢复
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="materials.length === 0 && !loading" description="暂无上传的资料">
            <el-button type="primary" @click="$router.push('/training/materials')">去上传</el-button>
          </el-empty>
        </div>
        
        <!-- 分页 -->
        <div class="pagination" v-if="total > 0">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { getMyMaterials, updateMaterial, downloadMaterial } from '@/api/training'
import {
  ArrowLeft, Download, Star,
  Document, Picture, Video, Folder, Files
} from '@element-plus/icons-vue'

const router = useRouter()

const API_BASE_URL = 'http://localhost:5000'

const loading = ref(false)
const materials = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const currentStatus = ref('')
const currentCategory = ref('')

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
  video: { icon: 'Video', name: '视频', color: '#909399' }
}

// 状态映射
const statusMap = {
  active: { name: '正常', type: 'success' },
  removed: { name: '已删除', type: 'danger' }
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

// 获取状态名称
const getStatusName = (status) => {
  return statusMap[status]?.name || '未知'
}

// 获取状态标签类型
const getStatusType = (status) => {
  return statusMap[status]?.type || 'info'
}

// 格式化日期
const formatDate = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleDateString('zh-CN')
}

// 获取完整URL
const getFullUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${API_BASE_URL}${url}`
}

// 获取资料列表
const fetchMaterials = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value
    }
    if (currentStatus.value) {
      params.status = currentStatus.value
    }
    
    const res = await getMyMaterials(params)
    const data = res.data || res
    materials.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取我的资料失败', error)
    ElMessage.error('获取资料列表失败')
  } finally {
    loading.value = false
  }
}

// 状态筛选变化
const handleStatusChange = () => {
  currentPage.value = 1
  fetchMaterials()
}

// 分类筛选变化
const handleCategoryChange = () => {
  currentPage.value = 1
  fetchMaterials()
}

// 分页变化
const handlePageChange = (page) => {
  currentPage.value = page
  fetchMaterials()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchMaterials()
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/training/materials/${id}`)
}

// 下载资料
const handleDownload = async (row) => {
  if (!row.file_url) {
    ElMessage.warning('该资料没有可下载的文件')
    return
  }
  
  try {
    // 先调用下载计数接口
    await downloadMaterial(row.id)
    
    // 然后下载文件
    const downloadUrl = getFullUrl(row.file_url)
    
    // 创建临时链接下载
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = row.title || 'download'
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    // 更新本地数据
    const item = materials.value.find(m => m.id === row.id)
    if (item) {
      item.download_count += 1
    }
    
    ElMessage.success('开始下载')
  } catch (error) {
    console.error('下载失败', error)
    ElMessage.error('下载失败，请重试')
  }
}

// 切换可见性
const toggleVisibility = async (row) => {
  try {
    const newVisibility = !row.is_public
    await updateMaterial(row.id, { is_public: newVisibility })
    row.is_public = newVisibility
    ElMessage.success(newVisibility ? '已设为公开' : '已设为私有')
  } catch (error) {
    console.error('操作失败', error)
    ElMessage.error('操作失败')
  }
}

// 删除资料
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该资料吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await updateMaterial(row.id, { status: 'removed' })
    row.status = 'removed'
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败', error)
      ElMessage.error('删除失败')
    }
  }
}

// 恢复资料
const restoreMaterial = async (row) => {
  try {
    await ElMessageBox.confirm('确定要恢复该资料吗？', '确认恢复', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    })
    
    await updateMaterial(row.id, { status: 'active' })
    row.status = 'active'
    ElMessage.success('恢复成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('恢复失败', error)
      ElMessage.error('恢复失败')
    }
  }
}

onMounted(() => {
  fetchMaterials()
})
</script>

<style scoped>
.my-materials-page {
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.header-left p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.filter-section {
  display: flex;
  gap: 20px;
  background: #fff;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
}

.materials-list {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.material-info {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  cursor: pointer;
}

.material-icon-small {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 6px;
  flex-shrink: 0;
}

.material-text {
  flex: 1;
  min-width: 0;
}

.material-title {
  font-size: 14px;
  color: #333;
  font-weight: 500;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.material-desc {
  font-size: 12px;
  color: #909399;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.stat-text {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .main-content {
    padding: 80px 0 20px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .filter-section {
    flex-wrap: wrap;
    overflow-x: auto;
  }
  
  .filter-section :deep(.el-radio-group) {
    white-space: nowrap;
  }
}
</style>

<template>
  <div class="material-list-page">
    <Navbar />
    
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1>学习资料</h1>
            <p>课件、笔记、真题，助力学习</p>
          </div>
          <div class="header-actions">
            <el-button 
              v-if="userStore.isLoggedIn" 
              type="primary" 
              size="large"
              @click="showPublishDialog = true"
            >
              <el-icon><Upload /></el-icon>
              上传资料
            </el-button>
            <el-button 
              v-if="userStore.isLoggedIn" 
              size="large"
              @click="$router.push('/training/my-materials')"
            >
              我的资料
            </el-button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="main-content">
      <div class="container">
        <!-- 搜索和筛选栏 -->
        <div class="search-section">
          <div class="search-row">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索资料名称、描述"
              size="large"
              class="search-input"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            
            <el-button type="primary" size="large" @click="handleSearch">
              搜索
            </el-button>
          </div>
          
          <div class="filter-row">
            <div class="category-filter">
              <span class="filter-label">分类：</span>
              <el-radio-group v-model="searchForm.category" size="small" @change="handleCategoryChange">
                <el-radio-button value="">全部</el-radio-button>
                <el-radio-button value="notes">课堂笔记</el-radio-button>
                <el-radio-button value="exam">考试资料</el-radio-button>
                <el-radio-button value="book">教材课件</el-radio-button>
                <el-radio-button value="homework">作业答案</el-radio-button>
                <el-radio-button value="certificate">考证资料</el-radio-button>
                <el-radio-button value="other">其他</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="sort-filter">
              <span class="filter-label">排序：</span>
              <el-select v-model="searchForm.sort" size="small" @change="handleSortChange" style="width: 120px">
                <el-option label="最新上传" value="newest" />
                <el-option label="最多下载" value="downloads" />
                <el-option label="最多点赞" value="likes" />
              </el-select>
            </div>
          </div>
        </div>
        
        <!-- 资料列表 -->
        <div class="materials-grid" v-loading="loading">
          <el-card 
            v-for="material in materials" 
            :key="material.id" 
            class="material-card" 
            shadow="hover"
            @click="goToDetail(material.id)"
          >
            <div class="material-icon">
              <el-icon :size="48" :color="getFileIconColor(material.file_type)">
                <component :is="getFileIcon(material.file_type)" />
              </el-icon>
              <span class="file-type-tag">{{ getFileTypeName(material.file_type) }}</span>
            </div>
            
            <div class="material-info">
              <h3 class="material-title">{{ material.title }}</h3>
              <p class="material-desc" v-if="material.description">{{ material.description }}</p>
              
              <div class="material-meta">
                <el-tag size="small" type="info">{{ getCategoryName(material.category) }}</el-tag>
                <span v-if="material.file_size" class="file-size">
                  {{ formatFileSize(material.file_size) }}
                </span>
              </div>
              
              <div class="material-stats">
                <span class="stat-item">
                  <el-icon><Download /></el-icon>
                  {{ material.download_count }} 下载
                </span>
                <span class="stat-item">
                  <el-icon><Star /></el-icon>
                  {{ material.like_count }} 点赞
                </span>
                <span class="publish-time">
                  {{ formatTime(material.created_at) }}
                </span>
              </div>
              
              <div class="uploader-info" v-if="material.user">
                <el-avatar :size="20" :src="getUserAvatar(material.user.avatar_url)" />
                <span class="uploader-name">{{ material.user.username }}</span>
              </div>
            </div>
          </el-card>
          
          <el-empty v-if="materials.length === 0 && !loading" description="暂无学习资料" />
        </div>
        
        <!-- 分页 -->
        <div class="pagination" v-if="total > 0">
          <el-pagination
            v-model:current-page="searchForm.page"
            v-model:page-size="searchForm.per_page"
            :total="total"
            :page-sizes="[12, 24, 48]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>
    
    <!-- 上传资料对话框 -->
    <el-dialog
      v-model="showPublishDialog"
      title="上传学习资料"
      width="600px"
      :close-on-click-modal="false"
      @closed="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="资料名称" prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入资料名称（如：计算机网络期末复习笔记）"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="资料描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请描述资料的内容、用途等信息"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="资料分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="课堂笔记" value="notes" />
            <el-option label="考试资料" value="exam" />
            <el-option label="教材课件" value="book" />
            <el-option label="作业答案" value="homework" />
            <el-option label="考证资料" value="certificate" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="上传文件" prop="file_url">
          <el-upload
            class="file-uploader"
            :action="uploadUrl"
            :headers="uploadHeaders"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :on-remove="handleRemove"
            :file-list="fileList"
            :limit="1"
            :auto-upload="true"
            accept=".pdf,.doc,.docx,.ppt,.pptx,.zip,.rar,.jpg,.jpeg,.png,.gif"
          >
            <el-button type="primary" :loading="uploading">
              <el-icon><Upload /></el-icon>
              选择文件
            </el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持 PDF、Word、PPT、图片、压缩包等格式，最大 16MB
              </div>
            </template>
          </el-upload>
          <p v-if="form.file_url" class="file-name">
            <el-icon><Document /></el-icon>
            {{ form.file_name || '已选择文件' }}
          </p>
        </el-form-item>
        
        <el-form-item label="公开可见">
          <el-switch v-model="form.is_public" active-text="是" inactive-text="否" />
          <span class="form-tip">（如果选择否，仅自己可见）</span>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showPublishDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          发布
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { useUserStore } from '@/stores/user'
import { getMaterials, uploadMaterial } from '@/api/training'
import { uploadApi } from '@/api/upload'
import {
  Search, Upload, Download, Star, Document,
  Picture, Video, Folder, Files
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const API_BASE_URL = 'http://localhost:5000'

const loading = ref(false)
const materials = ref([])
const total = ref(0)
const showPublishDialog = ref(false)
const uploading = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const fileList = ref([])

const searchForm = reactive({
  keyword: '',
  category: '',
  sort: 'newest',
  page: 1,
  per_page: 12
})

const form = reactive({
  title: '',
  description: '',
  category: '',
  file_url: '',
  file_type: '',
  file_size: '',
  file_name: '',
  is_public: true
})

const rules = {
  title: [
    { required: true, message: '请输入资料名称', trigger: 'blur' },
    { min: 2, max: 100, message: '名称长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入资料描述', trigger: 'blur' },
    { min: 5, max: 500, message: '描述长度在 5 到 500 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择资料分类', trigger: 'change' }
  ],
  file_url: [
    { required: true, message: '请上传资料文件', trigger: 'change' }
  ]
}

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

// 上传地址
const uploadUrl = computed(() => {
  return `${API_BASE_URL}/api/upload/file`
})

// 上传请求头
const uploadHeaders = computed(() => {
  const token = localStorage.getItem('token')
  return {
    Authorization: token ? `Bearer ${token}` : ''
  }
})

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

// 格式化时间
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

// 从文件名获取类型
const getFileTypeFromName = (filename) => {
  if (!filename) return ''
  const ext = filename.split('.').pop()?.toLowerCase() || ''
  return ext
}

// 获取资料列表
const fetchMaterials = async () => {
  loading.value = true
  try {
    const params = {
      page: searchForm.page,
      per_page: searchForm.per_page
    }
    if (searchForm.category) {
      params.category = searchForm.category
    }
    // TODO: 后端支持关键词搜索
    // if (searchForm.keyword) {
    //   params.keyword = searchForm.keyword
    // }
    
    const res = await getMaterials(params)
    const data = res.data || res
    materials.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取资料列表失败', error)
    ElMessage.error('获取资料列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchForm.page = 1
  fetchMaterials()
}

// 分类切换
const handleCategoryChange = () => {
  searchForm.page = 1
  fetchMaterials()
}

// 排序切换
const handleSortChange = () => {
  searchForm.page = 1
  fetchMaterials()
}

// 分页变化
const handlePageChange = (page) => {
  searchForm.page = page
  fetchMaterials()
}

const handleSizeChange = (size) => {
  searchForm.per_page = size
  searchForm.page = 1
  fetchMaterials()
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/training/materials/${id}`)
}

// 上传成功
const handleUploadSuccess = (response, file, fileListVal) => {
  if (response && response.url) {
    form.file_url = response.url
    form.file_name = response.filename
    if (response.size) {
      form.file_size = response.size.toString()
    }
    // 从文件名获取类型
    const ext = getFileTypeFromName(response.filename)
    form.file_type = ext
    ElMessage.success('文件上传成功')
  } else {
    ElMessage.error('文件上传失败')
  }
}

// 上传失败
const handleUploadError = (error) => {
  console.error('上传失败', error)
  ElMessage.error('文件上传失败，请重试')
}

// 移除文件
const handleRemove = () => {
  form.file_url = ''
  form.file_name = ''
  form.file_type = ''
  form.file_size = ''
}

// 重置表单
const resetForm = () => {
  form.title = ''
  form.description = ''
  form.category = ''
  form.file_url = ''
  form.file_name = ''
  form.file_type = ''
  form.file_size = ''
  form.is_public = true
  fileList.value = []
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const submitData = {
          title: form.title,
          description: form.description,
          category: form.category,
          file_url: form.file_url,
          file_type: form.file_type,
          is_public: form.is_public
        }
        
        if (form.file_size) {
          submitData.file_size = form.file_size
        }
        
        await uploadMaterial(submitData)
        ElMessage.success('上传成功！')
        showPublishDialog.value = false
        resetForm()
        // 刷新列表
        searchForm.page = 1
        fetchMaterials()
      } catch (error) {
        console.error('上传失败', error)
        ElMessage.error(error.response?.data?.error || '上传失败，请重试')
      } finally {
        submitting.value = false
      }
    }
  })
}

onMounted(() => {
  fetchMaterials()
})
</script>

<style scoped>
.material-list-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  background: linear-gradient(135deg, #67C23A 0%, #409EFF 100%);
  color: #fff;
  padding: 60px 0;
  margin-top: 60px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  margin: 0 0 10px 0;
  font-size: 32px;
}

.header-content p {
  margin: 0;
  font-size: 16px;
  opacity: 0.9;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.main-content {
  padding: 30px 0;
}

.search-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.search-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  align-items: center;
}

.filter-label {
  color: #666;
  font-size: 14px;
  margin-right: 8px;
}

.category-filter, .sort-filter {
  display: flex;
  align-items: center;
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.material-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.material-card:hover {
  transform: translateY(-4px);
}

.material-card :deep(.el-card__body) {
  padding: 20px;
}

.material-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 8px;
}

.file-type-tag {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.material-info {
  text-align: left;
}

.material-title {
  font-size: 16px;
  color: #333;
  margin: 0 0 8px 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.material-desc {
  font-size: 13px;
  color: #666;
  margin: 0 0 12px 0;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.material-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.file-size {
  font-size: 13px;
  color: #909399;
}

.material-stats {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
}

.publish-time {
  margin-left: auto;
  font-size: 12px;
  color: #c0c4cc;
}

.uploader-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.uploader-name {
  font-size: 13px;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.file-uploader {
  width: 100%;
}

.file-name {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #409eff;
  font-size: 14px;
}

.form-tip {
  margin-left: 10px;
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .page-header {
    padding: 40px 0;
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  
  .search-row {
    flex-direction: column;
  }
  
  .filter-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .materials-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
}
</style>

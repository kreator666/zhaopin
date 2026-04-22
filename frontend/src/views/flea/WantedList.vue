<template>
  <div class="wanted-list-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <div class="page-header">
          <div class="header-info">
            <h2>求购信息</h2>
            <p>寻找你需要的物品，或者发布求购信息</p>
          </div>
          <el-button 
            v-if="userStore.isLoggedIn" 
            type="primary" 
            @click="showPublishDialog = true"
          >
            <el-icon><Plus /></el-icon>
            发布求购
          </el-button>
        </div>
        
        <!-- 分类筛选 -->
        <div class="filter-section">
          <span class="filter-label">分类：</span>
          <el-radio-group v-model="currentCategory" size="large" @change="handleCategoryChange">
            <el-radio-button value="">全部</el-radio-button>
            <el-radio-button value="book">书籍教材</el-radio-button>
            <el-radio-button value="electronics">数码电子</el-radio-button>
            <el-radio-button value="bike">自行车</el-radio-button>
            <el-radio-button value="dorm">宿舍用品</el-radio-button>
            <el-radio-button value="ticket">票务卡券</el-radio-button>
            <el-radio-button value="clothing">服饰鞋包</el-radio-button>
            <el-radio-button value="other">其他</el-radio-button>
          </el-radio-group>
        </div>
        
        <!-- 求购列表 -->
        <div class="wanted-list" v-loading="loading">
          <el-card v-for="wanted in wanteds" :key="wanted.id" class="wanted-card" shadow="hover">
            <div class="wanted-header">
              <h3 class="wanted-title">{{ wanted.title }}</h3>
              <el-tag type="danger" size="large">求购</el-tag>
            </div>
            
            <div class="wanted-content">
              <p v-if="wanted.description" class="wanted-description">
                {{ wanted.description }}
              </p>
              
              <div class="wanted-meta">
                <div class="meta-item" v-if="wanted.category">
                  <span class="meta-label">分类：</span>
                  <el-tag size="small">{{ getCategoryName(wanted.category) }}</el-tag>
                </div>
                <div class="meta-item" v-if="wanted.max_price">
                  <span class="meta-label">预算：</span>
                  <span class="price-value">¥{{ wanted.max_price }}以内</span>
                </div>
              </div>
            </div>
            
            <div class="wanted-footer">
              <div class="publisher-info" @click="goToProfile(wanted.user_id)">
                <el-avatar :size="32" :src="getUserAvatar(wanted.user?.avatar_url)" />
                <div class="publisher-detail">
                  <span class="publisher-name">{{ wanted.user?.username || '发布者' }}</span>
                  <span class="publish-time">{{ formatTime(wanted.created_at) }}</span>
                </div>
              </div>
              
              <el-button 
                v-if="userStore.isLoggedIn" 
                type="primary" 
                size="small"
                @click="contactPublisher(wanted.user_id)"
              >
                <el-icon><ChatDotRound /></el-icon>
                联系卖家
              </el-button>
            </div>
          </el-card>
          
          <el-empty v-if="wanteds.length === 0 && !loading" description="暂无求购信息">
            <el-button 
              v-if="userStore.isLoggedIn" 
              type="primary" 
              @click="showPublishDialog = true"
            >
              发布求购
            </el-button>
            <p v-else>登录后可以发布求购信息</p>
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
    
    <!-- 发布求购对话框 -->
    <el-dialog
      v-model="showPublishDialog"
      title="发布求购信息"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="publishForm"
        :rules="publishRules"
        label-width="80px"
      >
        <el-form-item label="求购标题" prop="title">
          <el-input
            v-model="publishForm.title"
            placeholder="例如：求购一本二手《计算机网络》教材"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="详细描述" prop="description">
          <el-input
            v-model="publishForm.description"
            type="textarea"
            :rows="4"
            placeholder="请详细描述你需要的物品，包括物品的要求、期望的价格范围等"
            maxlength="300"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="物品分类" prop="category">
          <el-select v-model="publishForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="书籍教材" value="book" />
            <el-option label="数码电子" value="electronics" />
            <el-option label="自行车" value="bike" />
            <el-option label="宿舍用品" value="dorm" />
            <el-option label="票务卡券" value="ticket" />
            <el-option label="服饰鞋包" value="clothing" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="最高预算">
          <el-input-number
            v-model="publishForm.max_price"
            :min="0"
            :precision="2"
            placeholder="请输入最高预算（选填）"
            style="width: 200px"
          />
          <span class="price-unit">元</span>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showPublishDialog = false">取消</el-button>
        <el-button type="primary" :loading="publishing" @click="handlePublish">
          发布
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { useUserStore } from '@/stores/user'
import { getWanteds, createWanted } from '@/api/flea'
import { Plus, ChatDotRound } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const API_BASE_URL = 'http://localhost:5000'

const loading = ref(false)
const wanteds = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const currentCategory = ref('')

// 发布求购相关
const showPublishDialog = ref(false)
const publishing = ref(false)
const formRef = ref(null)

const publishForm = reactive({
  title: '',
  description: '',
  category: '',
  max_price: null
})

const publishRules = {
  title: [
    { required: true, message: '请输入求购标题', trigger: 'blur' },
    { min: 5, max: 50, message: '标题长度在 5 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入详细描述', trigger: 'blur' },
    { min: 10, max: 300, message: '描述长度在 10 到 300 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择物品分类', trigger: 'change' }
  ]
}

// 分类映射
const categoryMap = {
  book: '书籍教材',
  electronics: '数码电子',
  bike: '自行车',
  dorm: '宿舍用品',
  ticket: '票务卡券',
  clothing: '服饰鞋包',
  other: '其他'
}

// 获取分类名称
const getCategoryName = (category) => {
  return categoryMap[category] || '其他'
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

// 获取求购列表
const fetchWanteds = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value
    }
    if (currentCategory.value) {
      params.category = currentCategory.value
    }
    
    const res = await getWanteds(params)
    const data = res.data || res
    wanteds.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取求购列表失败', error)
    ElMessage.error('获取求购列表失败')
  } finally {
    loading.value = false
  }
}

// 分类筛选变化
const handleCategoryChange = () => {
  currentPage.value = 1
  fetchWanteds()
}

// 分页变化
const handlePageChange = (page) => {
  currentPage.value = page
  fetchWanteds()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchWanteds()
}

// 跳转到发布者主页
const goToProfile = (userId) => {
  if (userId) {
    router.push(`/profile/${userId}`)
  }
}

// 联系发布者
const contactPublisher = (userId) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  if (userId === userStore.userInfo?.id) {
    ElMessage.warning('不能联系自己')
    return
  }
  
  router.push(`/messages/${userId}`)
}

// 发布求购
const handlePublish = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      publishing.value = true
      try {
        const submitData = {
          title: publishForm.title,
          description: publishForm.description,
          category: publishForm.category
        }
        
        if (publishForm.max_price !== null) {
          submitData.max_price = publishForm.max_price
        }
        
        await createWanted(submitData)
        ElMessage.success('发布成功！')
        showPublishDialog.value = false
        
        // 重置表单
        publishForm.title = ''
        publishForm.description = ''
        publishForm.category = ''
        publishForm.max_price = null
        
        // 刷新列表
        currentPage.value = 1
        fetchWanteds()
      } catch (error) {
        console.error('发布失败', error)
        ElMessage.error(error.response?.data?.error || '发布失败，请重试')
      } finally {
        publishing.value = false
      }
    }
  })
}

onMounted(() => {
  fetchWanteds()
})
</script>

<style scoped>
.wanted-list-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.main-content {
  padding: 100px 0 40px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-info h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.header-info p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.filter-section {
  background: #fff;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.filter-label {
  color: #666;
  margin-right: 12px;
  flex-shrink: 0;
}

.wanted-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.wanted-card {
  transition: box-shadow 0.3s;
}

.wanted-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.wanted-card :deep(.el-card__body) {
  padding: 20px;
}

.wanted-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.wanted-title {
  font-size: 18px;
  color: #333;
  margin: 0;
  line-height: 1.4;
}

.wanted-content {
  margin-bottom: 20px;
}

.wanted-description {
  color: #666;
  line-height: 1.6;
  margin: 0 0 15px 0;
}

.wanted-meta {
  display: flex;
  gap: 30px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.meta-label {
  color: #999;
  font-size: 14px;
}

.price-value {
  color: #f56c6c;
  font-weight: bold;
}

.wanted-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.publisher-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.publisher-detail {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.publisher-name {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.publish-time {
  font-size: 12px;
  color: #999;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.price-unit {
  margin-left: 8px;
  color: #666;
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
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    overflow-x: auto;
  }
  
  .filter-section :deep(.el-radio-group) {
    white-space: nowrap;
  }
  
  .wanted-meta {
    flex-direction: column;
    gap: 10px;
  }
  
  .wanted-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
}
</style>

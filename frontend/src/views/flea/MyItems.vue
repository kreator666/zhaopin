<template>
  <div class="my-items-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <div class="page-header">
          <h2>我的闲置</h2>
          <el-button type="primary" @click="$router.push('/flea/publish')">
            <el-icon><Plus /></el-icon>
            发布新物品
          </el-button>
        </div>
        
        <!-- 状态筛选 -->
        <div class="filter-section">
          <el-radio-group v-model="currentStatus" size="large" @change="handleStatusChange">
            <el-radio-button value="">全部</el-radio-button>
            <el-radio-button value="on_sale">在售</el-radio-button>
            <el-radio-button value="reserved">已预定</el-radio-button>
            <el-radio-button value="sold">已售出</el-radio-button>
            <el-radio-button value="removed">已下架</el-radio-button>
          </el-radio-group>
        </div>
        
        <!-- 物品列表 -->
        <div class="items-list" v-loading="loading">
          <div v-for="item in items" :key="item.id" class="item-card">
            <div class="item-image" @click="goToDetail(item.id)">
              <img :src="getItemImage(item)" alt="物品图片" />
              <div class="price-tag">¥{{ item.price }}</div>
              <el-tag 
                :type="getStatusType(item.status)" 
                size="small" 
                class="status-tag"
              >
                {{ getStatusName(item.status) }}
              </el-tag>
            </div>
            
            <div class="item-info">
              <h3 class="item-title" @click="goToDetail(item.id)">{{ item.title }}</h3>
              <div class="item-meta">
                <el-tag size="small">{{ getCategoryName(item.category) }}</el-tag>
                <el-tag size="small" type="warning">{{ getConditionName(item.condition) }}</el-tag>
                <span class="view-count">
                  <el-icon><View /></el-icon>
                  {{ item.view_count }}
                </span>
                <span class="publish-time">
                  {{ formatTime(item.created_at) }}
                </span>
              </div>
              
              <div class="item-actions">
                <el-button 
                  v-if="item.status === 'on_sale'" 
                  type="success" 
                  size="small"
                  @click="markAsSold(item)"
                >
                  标记售出
                </el-button>
                <el-button 
                  v-if="item.status === 'on_sale'" 
                  type="danger" 
                  size="small"
                  @click="removeItem(item)"
                >
                  下架
                </el-button>
                <el-button 
                  v-if="item.status === 'sold' || item.status === 'removed'" 
                  type="primary" 
                  size="small"
                  @click="republishItem(item)"
                >
                  重新上架
                </el-button>
                <el-button size="small" @click="editItem(item)">
                  <el-icon><Edit /></el-icon>
                  编辑
                </el-button>
              </div>
            </div>
          </div>
          
          <el-empty v-if="items.length === 0 && !loading" description="暂无发布的物品">
            <el-button type="primary" @click="$router.push('/flea/publish')">去发布</el-button>
          </el-empty>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { getMyItems, updateItem } from '@/api/flea'
import { Plus, View, Edit } from '@element-plus/icons-vue'

const router = useRouter()

const API_BASE_URL = 'http://localhost:5000'

const loading = ref(false)
const items = ref([])
const currentStatus = ref('')

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

// 新旧程度映射
const conditionMap = {
  new: '全新',
  like_new: '几乎全新',
  good: '良好',
  fair: '一般',
  worn: '较旧'
}

// 状态映射
const statusMap = {
  on_sale: '在售',
  reserved: '已预定',
  sold: '已售出',
  removed: '已下架'
}

// 获取分类名称
const getCategoryName = (category) => {
  return categoryMap[category] || '其他'
}

// 获取新旧程度名称
const getConditionName = (condition) => {
  return conditionMap[condition] || '良好'
}

// 获取状态名称
const getStatusName = (status) => {
  return statusMap[status] || '未知'
}

// 获取状态标签类型
const getStatusType = (status) => {
  const typeMap = {
    on_sale: 'success',
    reserved: 'warning',
    sold: 'info',
    removed: 'danger'
  }
  return typeMap[status] || 'info'
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

// 获取物品图片
const getItemImage = (itemData) => {
  if (!itemData.images) {
    return 'https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png'
  }
  try {
    const imgList = JSON.parse(itemData.images)
    if (Array.isArray(imgList) && imgList.length > 0) {
      return getFullImageUrl(imgList[0])
    }
  } catch (e) {
    if (typeof itemData.images === 'string') {
      return getFullImageUrl(itemData.images)
    }
  }
  return 'https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png'
}

// 获取我的物品列表
const fetchMyItems = async () => {
  loading.value = true
  try {
    const params = currentStatus.value ? { status: currentStatus.value } : {}
    const res = await getMyItems(params)
    const data = res.data || res
    items.value = data.items || []
  } catch (error) {
    console.error('获取我的物品列表失败', error)
    ElMessage.error('获取物品列表失败')
  } finally {
    loading.value = false
  }
}

// 状态筛选变化
const handleStatusChange = () => {
  fetchMyItems()
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/flea/items/${id}`)
}

// 编辑物品
const editItem = (item) => {
  ElMessage.info('编辑功能开发中')
}

// 标记已售出
const markAsSold = async (item) => {
  try {
    await ElMessageBox.confirm('确定要标记为已售出吗？', '确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await updateItem(item.id, { status: 'sold' })
    item.status = 'sold'
    ElMessage.success('已标记为售出')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败', error)
      ElMessage.error('操作失败')
    }
  }
}

// 下架物品
const removeItem = async (item) => {
  try {
    await ElMessageBox.confirm('确定要下架该物品吗？', '确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await updateItem(item.id, { status: 'removed' })
    item.status = 'removed'
    ElMessage.success('已下架')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败', error)
      ElMessage.error('操作失败')
    }
  }
}

// 重新上架
const republishItem = async (item) => {
  try {
    await ElMessageBox.confirm('确定要重新上架吗？', '确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    })
    
    await updateItem(item.id, { status: 'on_sale' })
    item.status = 'on_sale'
    ElMessage.success('已重新上架')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败', error)
      ElMessage.error('操作失败')
    }
  }
}

onMounted(() => {
  fetchMyItems()
})
</script>

<style scoped>
.my-items-page {
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

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.filter-section {
  background: #fff;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.item-card {
  display: flex;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.3s;
}

.item-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.item-image {
  position: relative;
  width: 160px;
  height: 120px;
  flex-shrink: 0;
  cursor: pointer;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.price-tag {
  position: absolute;
  bottom: 8px;
  left: 8px;
  background: rgba(255, 87, 34, 0.95);
  color: #fff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
}

.status-tag {
  position: absolute;
  top: 8px;
  right: 8px;
}

.item-info {
  flex: 1;
  padding: 15px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.item-title {
  font-size: 16px;
  color: #333;
  margin: 0 0 10px 0;
  cursor: pointer;
  transition: color 0.3s;
}

.item-title:hover {
  color: #409EFF;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.view-count {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #999;
}

.publish-time {
  font-size: 13px;
  color: #999;
}

.item-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
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
    overflow-x: auto;
  }
  
  .filter-section :deep(.el-radio-group) {
    white-space: nowrap;
  }
  
  .item-card {
    flex-direction: column;
  }
  
  .item-image {
    width: 100%;
    height: 200px;
  }
  
  .item-info {
    padding: 15px;
  }
  
  .item-meta {
    gap: 10px;
  }
  
  .item-actions {
    flex-wrap: wrap;
  }
}
</style>

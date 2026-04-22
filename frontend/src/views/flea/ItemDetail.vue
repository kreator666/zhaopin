<template>
  <div class="item-detail-page">
    <Navbar />
    
    <div class="main-content" v-loading="loading">
      <div class="container" v-if="item">
        <el-breadcrumb separator="/" class="breadcrumb">
          <el-breadcrumb-item :to="{ path: '/flea' }">跳蚤市场</el-breadcrumb-item>
          <el-breadcrumb-item>{{ getCategoryName(item.category) }}</el-breadcrumb-item>
          <el-breadcrumb-item>{{ item.title }}</el-breadcrumb-item>
        </el-breadcrumb>
        
        <div class="detail-content">
          <!-- 左侧：图片轮播 -->
          <div class="image-section">
            <el-carousel 
              v-if="images.length > 0" 
              height="400px" 
              :autoplay="false"
              indicator-position="outside"
            >
              <el-carousel-item v-for="(img, index) in images" :key="index">
                <div class="carousel-image">
                  <img :src="getFullImageUrl(img)" alt="物品图片" />
                </div>
              </el-carousel-item>
            </el-carousel>
            <div class="no-image" v-else>
              <el-icon size="80" color="#999"><Picture /></el-icon>
              <p>暂无图片</p>
            </div>
          </div>
          
          <!-- 右侧：物品信息 -->
          <div class="info-section">
            <div class="item-header">
              <h1 class="item-title">{{ item.title }}</h1>
              <div class="item-status">
                <el-tag :type="getStatusType(item.status)">{{ getStatusName(item.status) }}</el-tag>
              </div>
            </div>
            
            <div class="price-section">
              <span class="current-price">¥{{ item.price }}</span>
              <span v-if="item.original_price" class="original-price">¥{{ item.original_price }}</span>
              <el-tag v-if="item.original_price && item.original_price > item.price" type="danger" size="small">
                省{{ Math.round((item.original_price - item.price) / item.original_price * 100) }}%
              </el-tag>
            </div>
            
            <div class="item-meta">
              <div class="meta-row">
                <span class="meta-label">分类：</span>
                <el-tag size="small">{{ getCategoryName(item.category) }}</el-tag>
              </div>
              <div class="meta-row">
                <span class="meta-label">新旧程度：</span>
                <el-tag size="small" type="warning">{{ getConditionName(item.condition) }}</el-tag>
              </div>
              <div class="meta-row" v-if="item.trade_location">
                <span class="meta-label">交易地点：</span>
                <span class="meta-value">{{ item.trade_location }}</span>
              </div>
              <div class="meta-row" v-if="item.trade_method">
                <span class="meta-label">交易方式：</span>
                <span class="meta-value">{{ formatTradeMethod(item.trade_method) }}</span>
              </div>
              <div class="meta-row">
                <span class="meta-label">议价：</span>
                <span class="meta-value">
                  {{ item.is_bargain_allowed ? '接受议价' : '不接受议价' }}
                </span>
              </div>
              <div class="meta-row">
                <span class="meta-label">浏览量：</span>
                <span class="meta-value">{{ item.view_count }}</span>
              </div>
              <div class="meta-row">
                <span class="meta-label">发布时间：</span>
                <span class="meta-value">{{ formatTime(item.created_at) }}</span>
              </div>
            </div>
            
            <!-- 卖家信息 -->
            <div class="seller-section" v-if="item.seller">
              <div class="seller-info" @click="goToSellerProfile">
                <el-avatar :size="48" :src="getUserAvatar(item.seller.avatar_url)" />
                <div class="seller-detail">
                  <span class="seller-name">{{ item.seller.username }}</span>
                  <span class="seller-school" v-if="item.seller.school_name">
                    {{ item.seller.school_name }}
                  </span>
                </div>
              </div>
              
              <div class="seller-actions" v-if="!isOwner">
                <el-button type="primary" size="large" @click="contactSeller">
                  <el-icon><ChatDotRound /></el-icon>
                  联系卖家
                </el-button>
                <el-button size="large" @click="handleFavorite">
                  <el-icon><Star :class="{ filled: isFavorited }" /></el-icon>
                  {{ isFavorited ? '已收藏' : '收藏' }}
                </el-button>
              </div>
              
              <!-- 卖家自己的操作 -->
              <div class="seller-actions" v-else>
                <el-button type="primary" size="large" @click="editItem">
                  <el-icon><Edit /></el-icon>
                  编辑
                </el-button>
                <el-button 
                  v-if="item.status === 'on_sale'" 
                  size="large" 
                  type="success"
                  @click="markAsSold"
                >
                  <el-icon><Check /></el-icon>
                  标记已售出
                </el-button>
                <el-button 
                  v-if="item.status === 'on_sale'" 
                  size="large" 
                  type="danger"
                  @click="removeItem"
                >
                  <el-icon><Delete /></el-icon>
                  下架
                </el-button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 物品描述 -->
        <div class="description-section" v-if="item.description">
          <h3 class="section-title">物品描述</h3>
          <div class="description-content">
            {{ item.description }}
          </div>
        </div>
        
        <!-- 更多推荐 -->
        <div class="recommend-section">
          <h3 class="section-title">更多推荐</h3>
          <div class="recommend-items">
            <el-card 
              v-for="rec in recommendItems" 
              :key="rec.id" 
              class="recommend-card"
              shadow="hover"
              @click="goToDetail(rec.id)"
            >
              <div class="recommend-image">
                <img :src="getItemImage(rec)" alt="" />
              </div>
              <div class="recommend-info">
                <h4 class="recommend-title">{{ rec.title }}</h4>
                <span class="recommend-price">¥{{ rec.price }}</span>
              </div>
            </el-card>
            <el-empty v-if="recommendItems.length === 0" description="暂无更多推荐" />
          </div>
        </div>
      </div>
      
      <!-- 错误状态 -->
      <div class="error-container" v-else-if="!loading">
        <el-empty description="物品不存在或已被删除" />
        <el-button type="primary" @click="$router.push('/flea')">返回跳蚤市场</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { useUserStore } from '@/stores/user'
import { getFleaItem, getFleaItems, favoriteItem, updateItem } from '@/api/flea'
import {
  Picture, ChatDotRound, Star, Edit, Check, Delete
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const API_BASE_URL = 'http://localhost:5000'

const loading = ref(true)
const item = ref(null)
const images = ref([])
const recommendItems = ref([])
const isFavorited = ref(false)

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

// 是否是物品所有者
const isOwner = computed(() => {
  return userStore.isLoggedIn && item.value?.seller_id === userStore.userInfo?.id
})

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
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 格式化交易方式
const formatTradeMethod = (method) => {
  if (!method) return ''
  const methodMap = {
    face_to_face: '面对面交易',
    campus_delivery: '校园配送',
    express: '快递邮寄'
  }
  return method.split(',').map(m => methodMap[m.trim()] || m).join('、')
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

// 获取物品图片（用于推荐列表）
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

// 解析图片列表
const parseImages = (imagesStr) => {
  if (!imagesStr) return []
  try {
    const imgList = JSON.parse(imagesStr)
    if (Array.isArray(imgList)) return imgList
  } catch (e) {
    if (typeof imagesStr === 'string') {
      return [imagesStr]
    }
  }
  return []
}

// 获取物品详情
const fetchItemDetail = async () => {
  const itemId = route.params.id
  if (!itemId) {
    loading.value = false
    return
  }
  
  loading.value = true
  try {
    const res = await getFleaItem(itemId)
    const data = res.data || res
    item.value = data
    images.value = parseImages(data.images)
  } catch (error) {
    console.error('获取物品详情失败', error)
    ElMessage.error('获取物品详情失败')
  } finally {
    loading.value = false
  }
}

// 获取推荐物品
const fetchRecommendItems = async () => {
  if (!item.value) return
  
  try {
    const res = await getFleaItems({
      category: item.value.category,
      page: 1,
      per_page: 4
    })
    const data = res.data || res
    recommendItems.value = (data.items || []).filter(i => i.id !== item.value.id)
  } catch (error) {
    console.error('获取推荐物品失败', error)
  }
}

// 联系卖家
const contactSeller = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  if (isOwner.value) {
    ElMessage.warning('不能联系自己')
    return
  }
  
  router.push(`/messages/${item.value.seller_id}`)
}

// 收藏物品
const handleFavorite = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  try {
    await favoriteItem(route.params.id)
    isFavorited.value = true
    ElMessage.success('收藏成功')
  } catch (error) {
    if (error.response?.status === 400) {
      ElMessage.warning('已收藏过该物品')
      isFavorited.value = true
    } else {
      console.error('收藏失败', error)
      ElMessage.error('收藏失败')
    }
  }
}

// 跳转到卖家主页
const goToSellerProfile = () => {
  if (item.value?.seller_id) {
    router.push(`/profile/${item.value.seller_id}`)
  }
}

// 编辑物品
const editItem = () => {
  ElMessage.info('编辑功能开发中')
}

// 标记已售出
const markAsSold = async () => {
  try {
    await ElMessageBox.confirm('确定要标记为已售出吗？', '确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await updateItem(route.params.id, { status: 'sold' })
    item.value.status = 'sold'
    ElMessage.success('已标记为售出')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败', error)
      ElMessage.error('操作失败')
    }
  }
}

// 下架物品
const removeItem = async () => {
  try {
    await ElMessageBox.confirm('确定要下架该物品吗？', '确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await updateItem(route.params.id, { status: 'removed' })
    item.value.status = 'removed'
    ElMessage.success('已下架')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('操作失败', error)
      ElMessage.error('操作失败')
    }
  }
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/flea/items/${id}`)
}

onMounted(async () => {
  await fetchItemDetail()
  fetchRecommendItems()
})
</script>

<style scoped>
.item-detail-page {
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
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.image-section {
  width: 400px;
  flex-shrink: 0;
}

.carousel-image {
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
}

.carousel-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.no-image {
  width: 400px;
  height: 400px;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.info-section {
  flex: 1;
  min-width: 0;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.item-title {
  font-size: 22px;
  color: #333;
  margin: 0;
  line-height: 1.4;
  flex: 1;
  margin-right: 20px;
}

.price-section {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.current-price {
  font-size: 28px;
  color: #f56c6c;
  font-weight: bold;
}

.original-price {
  font-size: 16px;
  color: #999;
  text-decoration: line-through;
}

.item-meta {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 25px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.meta-label {
  color: #999;
  width: 80px;
  flex-shrink: 0;
}

.meta-value {
  color: #333;
}

.seller-section {
  background: #fafafa;
  border-radius: 8px;
  padding: 20px;
}

.seller-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
  cursor: pointer;
}

.seller-detail {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.seller-name {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.seller-school {
  font-size: 13px;
  color: #999;
}

.seller-actions {
  display: flex;
  gap: 12px;
}

.section-title {
  font-size: 18px;
  color: #333;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #409EFF;
  display: inline-block;
}

.description-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.description-content {
  color: #666;
  line-height: 1.8;
  white-space: pre-wrap;
}

.recommend-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}

.recommend-items {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.recommend-card {
  cursor: pointer;
}

.recommend-card :deep(.el-card__body) {
  padding: 0;
}

.recommend-image {
  width: 100%;
  height: 150px;
  overflow: hidden;
}

.recommend-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.recommend-info {
  padding: 12px;
}

.recommend-title {
  font-size: 14px;
  color: #333;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recommend-price {
  font-size: 16px;
  color: #f56c6c;
  font-weight: bold;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
}

.filled {
  color: #f7ba2a;
  fill: #f7ba2a;
}

@media (max-width: 992px) {
  .detail-content {
    flex-direction: column;
  }
  
  .image-section {
    width: 100%;
  }
  
  .carousel-image,
  .no-image {
    width: 100%;
    height: 300px;
  }
  
  .recommend-items {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .main-content {
    padding: 80px 0 20px;
  }
  
  .item-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .item-title {
    margin-right: 0;
  }
  
  .seller-actions {
    flex-direction: column;
  }
  
  .recommend-items {
    grid-template-columns: 1fr;
  }
}
</style>

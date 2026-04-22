<template>
  <div class="flea-market-page">
    <Navbar />
    
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="container">
        <h1>跳蚤市场</h1>
        <p>校园二手交易，让闲置流动起来</p>
        <el-button v-if="userStore.isLoggedIn" type="primary" size="large" @click="$router.push('/flea/publish')">
          <el-icon><Plus /></el-icon>
          发布闲置
        </el-button>
      </div>
    </div>
    
    <div class="main-content">
      <div class="container">
        <!-- 搜索和筛选栏 -->
        <div class="search-section">
          <div class="search-row">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索物品名称、描述"
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
                <el-radio-button value="book">书籍教材</el-radio-button>
                <el-radio-button value="electronics">数码电子</el-radio-button>
                <el-radio-button value="bike">自行车</el-radio-button>
                <el-radio-button value="dorm">宿舍用品</el-radio-button>
                <el-radio-button value="ticket">票务卡券</el-radio-button>
                <el-radio-button value="clothing">服饰鞋包</el-radio-button>
                <el-radio-button value="other">其他</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="price-filter">
              <span class="filter-label">价格：</span>
              <el-input-number v-model="searchForm.min_price" :min="0" placeholder="最低价" size="small" style="width: 100px" />
              <span class="price-separator">-</span>
              <el-input-number v-model="searchForm.max_price" :min="0" placeholder="最高价" size="small" style="width: 100px" />
              <el-button size="small" type="primary" @click="handlePriceFilter">确定</el-button>
            </div>
            
            <div class="tab-switch">
              <el-radio-group v-model="activeTab" size="small" @change="handleTabChange">
                <el-radio-button value="items">闲置物品</el-radio-button>
                <el-radio-button value="wanted">求购信息</el-radio-button>
              </el-radio-group>
            </div>
          </div>
        </div>
        
        <!-- 物品列表 -->
        <div class="items-grid" v-if="activeTab === 'items'">
          <el-card v-for="item in items" :key="item.id" class="item-card" shadow="hover" @click="goToDetail(item.id)">
            <div class="item-image">
              <img :src="getItemImage(item)" alt="物品图片" />
              <div class="item-price">¥{{ item.price }}</div>
              <el-tag v-if="item.original_price" size="small" type="info" class="original-price-tag">
                原价¥{{ item.original_price }}
              </el-tag>
            </div>
            <div class="item-info">
              <h3 class="item-title">{{ item.title }}</h3>
              <div class="item-meta">
                <el-tag size="small" type="info">{{ getCategoryName(item.category) }}</el-tag>
                <el-tag size="small" type="warning">{{ getConditionName(item.condition) }}</el-tag>
              </div>
              <div class="item-seller">
                <el-avatar :size="24" :src="getUserAvatar(item.seller?.avatar_url)" />
                <span class="seller-name">{{ item.seller?.username || '卖家' }}</span>
                <span class="publish-time">{{ formatTime(item.created_at) }}</span>
              </div>
            </div>
          </el-card>
          
          <el-empty v-if="items.length === 0 && !loading" description="暂无闲置物品" />
        </div>
        
        <!-- 求购列表 -->
        <div class="wanted-list" v-else>
          <el-card v-for="wanted in wanteds" :key="wanted.id" class="wanted-card" shadow="hover">
            <div class="wanted-header">
              <h3 class="wanted-title">{{ wanted.title }}</h3>
              <el-tag type="danger" size="small">求购</el-tag>
            </div>
            <div class="wanted-content">
              <p v-if="wanted.description">{{ wanted.description }}</p>
              <div class="wanted-meta">
                <span v-if="wanted.max_price" class="max-price">
                  最高预算：<strong>¥{{ wanted.max_price }}</strong>
                </span>
                <span v-if="wanted.category" class="wanted-category">
                  分类：{{ getCategoryName(wanted.category) }}
                </span>
              </div>
            </div>
            <div class="wanted-footer">
              <div class="publisher-info">
                <el-avatar :size="24" :src="getUserAvatar(wanted.user?.avatar_url)" />
                <span class="publisher-name">{{ wanted.user?.username || '发布者' }}</span>
                <span class="publish-time">{{ formatTime(wanted.created_at) }}</span>
              </div>
              <el-button 
                v-if="userStore.isLoggedIn" 
                type="primary" 
                size="small"
                @click.stop="contactPublisher(wanted.user_id)"
              >
                联系卖家
              </el-button>
            </div>
          </el-card>
          
          <el-empty v-if="wanteds.length === 0 && !loading" description="暂无求购信息" />
        </div>
        
        <!-- 分页 -->
        <div class="pagination" v-if="(activeTab === 'items' && total > 0) || (activeTab === 'wanted' && wantedTotal > 0)">
          <el-pagination
            v-model:current-page="searchForm.page"
            v-model:page-size="searchForm.per_page"
            :total="activeTab === 'items' ? total : wantedTotal"
            :page-sizes="[12, 24, 48]"
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import Navbar from '@/components/Navbar.vue'
import { useUserStore } from '@/stores/user'
import {
  getFleaItems,
  getWanteds
} from '@/api/flea'
import { Search, Plus } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const API_BASE_URL = 'http://localhost:5000'

const activeTab = ref('items')
const items = ref([])
const wanteds = ref([])
const total = ref(0)
const wantedTotal = ref(0)
const loading = ref(false)

const searchForm = reactive({
  keyword: '',
  category: '',
  min_price: null,
  max_price: null,
  page: 1,
  per_page: 12
})

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

// 获取分类名称
const getCategoryName = (category) => {
  return categoryMap[category] || '其他'
}

// 获取新旧程度名称
const getConditionName = (condition) => {
  return conditionMap[condition] || '良好'
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
  if (days < 365) return `${Math.floor(days / 30)}个月前`
  return `${Math.floor(days / 365)}年前`
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

// 获取物品图片
const getItemImage = (item) => {
  if (!item.images) {
    return 'https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png'
  }
  try {
    const images = JSON.parse(item.images)
    if (Array.isArray(images) && images.length > 0) {
      return getFullImageUrl(images[0])
    }
  } catch (e) {
    // 解析失败，尝试直接使用
    if (typeof item.images === 'string' && item.images) {
      return getFullImageUrl(item.images)
    }
  }
  return 'https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png'
}

// 获取物品列表
const fetchItems = async () => {
  loading.value = true
  try {
    const params = {
      page: searchForm.page,
      per_page: searchForm.per_page
    }
    if (searchForm.keyword) params.keyword = searchForm.keyword
    if (searchForm.category) params.category = searchForm.category
    if (searchForm.min_price !== null) params.min_price = searchForm.min_price
    if (searchForm.max_price !== null) params.max_price = searchForm.max_price
    
    const res = await getFleaItems(params)
    const data = res.data || res
    items.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取物品列表失败', error)
    ElMessage.error('获取物品列表失败')
  } finally {
    loading.value = false
  }
}

// 获取求购列表
const fetchWanteds = async () => {
  loading.value = true
  try {
    const params = {
      page: searchForm.page,
      per_page: searchForm.per_page
    }
    if (searchForm.category) params.category = searchForm.category
    
    const res = await getWanteds(params)
    const data = res.data || res
    wanteds.value = data.items || []
    wantedTotal.value = data.total || 0
  } catch (error) {
    console.error('获取求购列表失败', error)
    ElMessage.error('获取求购列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchForm.page = 1
  if (activeTab.value === 'items') {
    fetchItems()
  } else {
    fetchWanteds()
  }
}

// 分类切换
const handleCategoryChange = () => {
  searchForm.page = 1
  if (activeTab.value === 'items') {
    fetchItems()
  } else {
    fetchWanteds()
  }
}

// 价格筛选
const handlePriceFilter = () => {
  searchForm.page = 1
  if (activeTab.value === 'items') {
    fetchItems()
  }
}

// Tab 切换
const handleTabChange = () => {
  searchForm.page = 1
  if (activeTab.value === 'items') {
    fetchItems()
  } else {
    fetchWanteds()
  }
}

// 分页变化
const handlePageChange = (page) => {
  searchForm.page = page
  if (activeTab.value === 'items') {
    fetchItems()
  } else {
    fetchWanteds()
  }
}

const handleSizeChange = (size) => {
  searchForm.per_page = size
  searchForm.page = 1
  if (activeTab.value === 'items') {
    fetchItems()
  } else {
    fetchWanteds()
  }
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/flea/items/${id}`)
}

// 联系发布者
const contactPublisher = (userId) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  router.push(`/messages/${userId}`)
}

onMounted(() => {
  fetchItems()
})
</script>

<style scoped>
.flea-market-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  background: linear-gradient(135deg, #E6A23C 0%, #F56C6C 100%);
  color: #fff;
  padding: 60px 0;
  margin-top: 60px;
}

.page-header .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
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
  gap: 20px;
  align-items: center;
}

.filter-label {
  color: #666;
  font-size: 14px;
  margin-right: 8px;
}

.category-filter {
  display: flex;
  align-items: center;
}

.price-filter {
  display: flex;
  align-items: center;
}

.price-separator {
  margin: 0 8px;
  color: #999;
}

.tab-switch {
  margin-left: auto;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.item-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  overflow: hidden;
}

.item-card:hover {
  transform: translateY(-4px);
}

.item-card :deep(.el-card__body) {
  padding: 0;
}

.item-image {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-price {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background: rgba(255, 87, 34, 0.95);
  color: #fff;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 18px;
  font-weight: bold;
}

.original-price-tag {
  position: absolute;
  top: 10px;
  right: 10px;
}

.item-info {
  padding: 15px;
}

.item-title {
  margin: 0 0 10px 0;
  font-size: 15px;
  color: #333;
  line-height: 1.4;
  height: 42px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.item-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.item-seller {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.seller-name {
  font-size: 13px;
  color: #666;
}

.publish-time {
  margin-left: auto;
  font-size: 12px;
  color: #999;
}

.wanted-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

.wanted-card {
  cursor: pointer;
}

.wanted-card :deep(.el-card__body) {
  padding: 20px;
}

.wanted-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.wanted-title {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.wanted-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.wanted-meta {
  display: flex;
  gap: 30px;
}

.max-price strong {
  color: #f56c6c;
  font-size: 16px;
}

.wanted-category {
  color: #666;
}

.wanted-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  margin-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.publisher-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.publisher-name {
  font-size: 14px;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

@media (max-width: 768px) {
  .page-header .container {
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
  }
  
  .tab-switch {
    margin-left: 0;
  }
  
  .items-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
}
</style>

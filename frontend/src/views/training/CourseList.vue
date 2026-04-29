<template>
  <div class="course-list-page">
    <Navbar />
    
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1>精品课程</h1>
            <p>海量优质课程，助力职业成长</p>
          </div>
          <div class="header-actions">
            <el-button 
              v-if="userStore.isLoggedIn && isAdminOrCompany" 
              type="primary" 
              size="large"
              @click="$router.push('/company/courses')"
            >
              <el-icon><Plus /></el-icon>
              管理课程
            </el-button>
            <el-button 
              v-if="userStore.isLoggedIn" 
              size="large"
              @click="$router.push('/training/my-courses')"
            >
              <el-icon><Document /></el-icon>
              我的课程
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
              placeholder="搜索课程名称、描述、讲师"
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
              <el-radio-group v-model="searchForm.category" size="small" @change="handleFilterChange">
                <el-radio-button value="">全部</el-radio-button>
                <el-radio-button value="programming">编程开发</el-radio-button>
                <el-radio-button value="language">语言学习</el-radio-button>
                <el-radio-button value="exam_prep">考试考证</el-radio-button>
                <el-radio-button value="career">职业技能</el-radio-button>
                <el-radio-button value="design">设计创意</el-radio-button>
                <el-radio-button value="data">数据科学</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="level-filter">
              <span class="filter-label">难度：</span>
              <el-select v-model="searchForm.level" size="small" clearable placeholder="全部" @change="handleFilterChange" style="width: 120px">
                <el-option label="入门" value="beginner" />
                <el-option label="进阶" value="intermediate" />
                <el-option label="高级" value="advanced" />
              </el-select>
            </div>
            
            <div class="online-filter">
              <span class="filter-label">形式：</span>
              <el-select v-model="searchForm.is_online" size="small" clearable placeholder="全部" @change="handleFilterChange" style="width: 120px">
                <el-option label="线上课程" value="true" />
                <el-option label="线下课程" value="false" />
              </el-select>
            </div>
          </div>
        </div>
        
        <!-- 课程列表 -->
        <div class="courses-grid" v-loading="loading">
          <el-card 
            v-for="course in courses" 
            :key="course.id" 
            class="course-card" 
            shadow="hover"
            @click="goToDetail(course.id)"
          >
            <template #header>
              <div class="course-cover">
                <img 
                  :src="getCoverImage(course.cover_image)" 
                  :alt="course.title"
                  class="cover-img"
                />
                <div class="course-tags">
                  <el-tag v-if="course.is_online" size="small" type="primary">线上</el-tag>
                  <el-tag v-else size="small" type="warning">线下</el-tag>
                  <el-tag v-if="course.price === 0" size="small" type="success">免费</el-tag>
                </div>
              </div>
            </template>
            
            <div class="course-info">
              <h3 class="course-title">{{ course.title }}</h3>
              <p class="course-desc" v-if="course.description">
                {{ course.description }}
              </p>
              
              <div class="course-meta">
                <span class="meta-item" v-if="course.instructor">
                  <el-icon><User /></el-icon>
                  {{ course.instructor }}
                </span>
                <span class="meta-item" v-if="course.provider">
                  <el-icon><OfficeBuilding /></el-icon>
                  {{ course.provider }}
                </span>
                <span class="meta-item" v-if="course.duration">
                  <el-icon><Clock /></el-icon>
                  {{ course.duration }}
                </span>
              </div>
              
              <div class="course-stats">
                <div class="stats-left">
                  <span class="stat-item">
                    <el-icon><UserFilled /></el-icon>
                    {{ course.enrolled_count || 0 }}人学习
                  </span>
                  <span class="stat-item">
                    <el-icon><Star /></el-icon>
                    {{ course.rating || 5.0 }}分
                  </span>
                  <el-tag 
                    v-if="course.level" 
                    :type="getLevelTagType(course.level)" 
                    size="small"
                  >
                    {{ getLevelName(course.level) }}
                  </el-tag>
                </div>
                
                <div class="course-price">
                  <span class="price-value" v-if="course.price > 0">
                    ¥{{ course.price }}
                  </span>
                  <span class="price-value free" v-else>
                    免费
                  </span>
                  <span class="original-price" v-if="course.original_price && course.original_price > course.price">
                    ¥{{ course.original_price }}
                  </span>
                </div>
              </div>
            </div>
          </el-card>
          
          <el-empty v-if="courses.length === 0 && !loading" description="暂无课程" />
        </div>
        
        <!-- 分页 -->
        <div class="pagination" v-if="total > 0">
          <el-pagination
            v-model:current-page="searchForm.page"
            v-model:page-size="searchForm.per_page"
            :total="total"
            :page-sizes="[9, 18, 36]"
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
import { getCourses } from '@/api/training'
import {
  Search, Plus, Document, User, OfficeBuilding, Clock,
  UserFilled, Star
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const API_BASE_URL = 'http://localhost:5000'

const loading = ref(false)
const courses = ref([])
const total = ref(0)

// 是否是管理员或企业用户
const isAdminOrCompany = computed(() => {
  const role = userStore.userInfo?.role
  return role === 'admin' || role === 'company'
})

const searchForm = reactive({
  keyword: '',
  category: '',
  level: '',
  is_online: '',
  page: 1,
  per_page: 9
})

// 分类映射
const categoryMap = {
  programming: '编程开发',
  language: '语言学习',
  exam_prep: '考试考证',
  career: '职业技能',
  design: '设计创意',
  data: '数据科学'
}

// 难度映射
const levelMap = {
  beginner: { name: '入门', type: 'success' },
  intermediate: { name: '进阶', type: 'warning' },
  advanced: { name: '高级', type: 'danger' }
}

// 获取难度名称
const getLevelName = (level) => {
  return levelMap[level]?.name || ''
}

// 获取难度标签类型
const getLevelTagType = (level) => {
  return levelMap[level]?.type || 'info'
}

// 获取封面图片
const getCoverImage = (coverImage) => {
  if (!coverImage) {
    return 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=online%20course%20education%20learning%20technology%20modern%20design&image_size=landscape_16_9'
  }
  if (coverImage.startsWith('http')) {
    return coverImage
  }
  return `${API_BASE_URL}${coverImage}`
}

// 获取课程列表
const fetchCourses = async () => {
  loading.value = true
  try {
    const params = {
      page: searchForm.page,
      per_page: searchForm.per_page
    }
    if (searchForm.category) {
      params.category = searchForm.category
    }
    if (searchForm.level) {
      params.level = searchForm.level
    }
    if (searchForm.is_online) {
      params.is_online = searchForm.is_online
    }
    if (searchForm.keyword) {
      params.keyword = searchForm.keyword
    }
    
    const res = await getCourses(params)
    const data = res.data || res
    courses.value = data.items || []
    total.value = data.total || 0
  } catch (error) {
    console.error('获取课程列表失败', error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchForm.page = 1
  fetchCourses()
}

// 筛选变化
const handleFilterChange = () => {
  searchForm.page = 1
  fetchCourses()
}

// 分页变化
const handlePageChange = (page) => {
  searchForm.page = page
  fetchCourses()
}

const handleSizeChange = (size) => {
  searchForm.per_page = size
  searchForm.page = 1
  fetchCourses()
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/training/courses/${id}`)
}

onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.course-list-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
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

.category-filter, .level-filter, .online-filter {
  display: flex;
  align-items: center;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 30px;
}

.course-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  overflow: hidden;
}

.course-card:hover {
  transform: translateY(-4px);
}

.course-card :deep(.el-card__header) {
  padding: 0;
}

.course-cover {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.course-tags {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  gap: 6px;
}

.course-card :deep(.el-card__body) {
  padding: 16px;
}

.course-info {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.course-title {
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

.course-desc {
  font-size: 13px;
  color: #909399;
  margin: 0 0 12px 0;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  flex-shrink: 0;
}

.course-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #909399;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.course-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  margin-top: auto;
}

.stats-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
}

.course-price {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-value {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}

.price-value.free {
  color: #67c23a;
}

.original-price {
  font-size: 13px;
  color: #c0c4cc;
  text-decoration: line-through;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

@media (max-width: 992px) {
  .courses-grid {
    grid-template-columns: repeat(2, 1fr);
  }
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
  
  .courses-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>

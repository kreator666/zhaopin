<template>
  <div class="topic-list-page">
    <Navbar />
    
    <div class="page-header" style="padding-top: 60px;">
      <div class="container">
        <h1>兴趣圈子</h1>
        <p>分享交流，找到志同道合的伙伴</p>
      </div>
    </div>
    
    <div class="container main-content">
      <!-- 工具栏：搜索 + 发布按钮 -->
      <div class="toolbar">
        <div class="search-filter">
          <el-input
            v-model="searchQuery"
            placeholder="搜索话题..."
            clearable
            class="search-input"
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-select
            v-model="selectedTag"
            placeholder="按标签筛选"
            clearable
            class="tag-filter"
            @change="handleTagFilter"
          >
            <el-option
              v-for="tag in availableTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </div>
        
        <el-button type="primary" @click="showPostDialog = true">
          <el-icon><Plus /></el-icon>
          发布话题
        </el-button>
      </div>
      
      <!-- 话题列表 -->
      <div v-loading="loading" class="topics-list">
        <el-empty v-if="!loading && topics.length === 0" description="暂无话题，来发布第一个吧！" />
        
        <div
          v-for="topic in topics"
          :key="topic.id"
          class="topic-card"
          @click="goToTopic(topic.id)"
        >
          <div class="topic-header">
            <el-avatar :size="40" :src="topic.user?.avatar_url" />
            <div class="topic-meta">
              <span class="username">{{ topic.user?.username || '匿名用户' }}</span>
              <span class="time">{{ formatTime(topic.created_at) }}</span>
            </div>
            <el-tag v-if="topic.is_pinned" type="danger" size="small" effect="dark">置顶</el-tag>
            <el-tag v-if="topic.status === 'solved'" type="success" size="small">已解决</el-tag>
            <el-tag v-if="topic.status === 'closed'" type="info" size="small">已关闭</el-tag>
          </div>
          
          <h3 class="topic-title">{{ topic.title }}</h3>
          <p class="topic-content">{{ topic.content }}</p>
          
          <div class="topic-tags" v-if="topic.tags && topic.tags.length > 0">
            <el-tag 
              v-for="tag in topic.tags.slice(0, 5)" 
              :key="tag" 
              size="small"
              class="tag-item"
            >
              {{ tag }}
            </el-tag>
          </div>
          
          <div class="topic-stats">
            <span><el-icon><View /></el-icon> {{ topic.view_count || 0 }}</span>
            <span><el-icon><ChatDotRound /></el-icon> {{ topic.reply_count || 0 }}</span>
          </div>
        </div>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-wrapper" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @change="handlePageChange"
        />
      </div>
    </div>
    
    <!-- 发布话题弹窗 -->
    <el-dialog
      v-model="showPostDialog"
      title="发布话题"
      width="600px"
      destroy-on-close
    >
      <el-form :model="postForm" label-position="top">
        <el-form-item label="标题">
          <el-input 
            v-model="postForm.title" 
            placeholder="请输入话题标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="内容">
          <el-input 
            v-model="postForm.content" 
            type="textarea" 
            :rows="6"
            placeholder="分享你的想法..."
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="标签">
          <el-select
            v-model="postForm.tags"
            multiple
            filterable
            allow-create
            placeholder="添加标签（可选）"
            class="tag-select"
          >
            <el-option
              v-for="tag in availableTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="可见范围">
          <el-radio-group v-model="postForm.visibility">
            <el-radio label="public">全站可见</el-radio>
            <el-radio label="school_only">仅本校可见</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showPostDialog = false">取消</el-button>
        <el-button type="primary" @click="submitTopic" :loading="submitLoading">
          发布
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Plus, View, ChatDotRound } from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import { socialApi } from '@/api/social'

const router = useRouter()

// 列表数据
const loading = ref(false)
const topics = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const searchQuery = ref('')
const selectedTag = ref('')
const availableTags = ref([])

// 发布弹窗
const showPostDialog = ref(false)
const submitLoading = ref(false)
const postForm = ref({
  title: '',
  content: '',
  tags: [],
  visibility: 'public'
})

// 获取话题列表
const fetchTopics = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      search: searchQuery.value || undefined,
      tag: selectedTag.value || undefined
    }
    const res = await socialApi.getTopics(params)
    topics.value = res.data.items || []
    total.value = res.data.total || 0
  } catch (err) {
    console.error('获取话题列表失败:', err)
    ElMessage.error('获取话题列表失败')
  } finally {
    loading.value = false
  }
}

// 获取标签列表
const fetchTags = async () => {
  try {
    const res = await socialApi.getTags()
    availableTags.value = res.data.tags || []
  } catch (err) {
    console.error('获取标签失败:', err)
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchTopics()
}

// 标签筛选
const handleTagFilter = () => {
  currentPage.value = 1
  fetchTopics()
}

// 分页
const handlePageChange = () => {
  fetchTopics()
}

// 跳转到话题详情
const goToTopic = (topicId) => {
  router.push(`/social/topics/${topicId}`)
}

// 发布话题
const submitTopic = async () => {
  if (!postForm.value.title.trim()) {
    ElMessage.warning('请输入标题')
    return
  }
  
  submitLoading.value = true
  try {
    await socialApi.createTopic({
      title: postForm.value.title,
      content: postForm.value.content,
      tags: postForm.value.tags,
      visibility: postForm.value.visibility
    })
    
    ElMessage.success('发布成功')
    showPostDialog.value = false
    
    // 重置表单
    postForm.value = {
      title: '',
      content: '',
      tags: [],
      visibility: 'public'
    }
    
    // 刷新列表
    fetchTopics()
  } catch (err) {
    console.error('发布失败:', err)
    ElMessage.error(err.response?.data?.error || '发布失败')
  } finally {
    submitLoading.value = false
  }
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchTopics()
  fetchTags()
})
</script>

<style scoped>
.topic-list-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px 0;
  text-align: center;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 32px;
}

.page-header p {
  margin: 0;
  opacity: 0.9;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.main-content {
  padding: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 16px;
}

.search-filter {
  display: flex;
  gap: 12px;
  flex: 1;
}

.search-input {
  width: 300px;
}

.tag-filter {
  width: 150px;
}

.topics-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.topic-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.topic-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.topic-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.topic-meta {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 500;
  color: #333;
}

.time {
  font-size: 12px;
  color: #999;
}

.topic-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #333;
  line-height: 1.4;
}

.topic-content {
  margin: 0 0 12px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.topic-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.tag-item {
  margin-right: 0;
}

.topic-stats {
  display: flex;
  gap: 20px;
  color: #999;
  font-size: 13px;
}

.topic-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination-wrapper {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

.tag-select {
  width: 100%;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-filter {
    flex-direction: column;
  }
  
  .search-input,
  .tag-filter {
    width: 100%;
  }
}
</style>

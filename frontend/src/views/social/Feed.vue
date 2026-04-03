<template>
  <div class="social-feed-page">
    <Navbar />
    
    <div class="main-content">
      <div class="container">
        <el-row :gutter="24">
          <!-- 左侧栏 -->
          <el-col :xs="24" :md="6" class="left-sidebar">
            <el-card class="user-card" shadow="hover">
              <div class="user-brief" @click="goToProfile">
                <el-avatar :size="50" :src="userAvatar" />
                <div class="user-info">
                  <h4>{{ userStore.userInfo?.username }}</h4>
                  <p>{{ userStore.userInfo?.school_name || '未设置学校' }}</p>
                </div>
              </div>
              <div class="user-stats">
                <div class="stat-item">
                  <span class="num">{{ userStore.userInfo?.following_count || 0 }}</span>
                  <span class="label">关注</span>
                </div>
                <div class="stat-item">
                  <span class="num">{{ userStore.userInfo?.follower_count || 0 }}</span>
                  <span class="label">粉丝</span>
                </div>
                <div class="stat-item">
                  <span class="num">{{ userStore.userInfo?.post_count || 0 }}</span>
                  <span class="label">动态</span>
                </div>
              </div>
            </el-card>
            
            <el-card class="nav-card" shadow="hover">
              <div class="nav-menu">
                <div class="nav-item active" @click="$router.push('/social')">
                  <el-icon><ChatDotRound /></el-icon>
                  <span>动态广场</span>
                </div>
                <div class="nav-item" @click="$router.push('/social/alumni')">
                  <el-icon><School /></el-icon>
                  <span>校友圈</span>
                </div>
                <div class="nav-item" @click="$router.push('/social/circles')">
                  <el-icon><CircleCheck /></el-icon>
                  <span>兴趣圈子</span>
                </div>
                <div class="nav-item" @click="$router.push('/social/events')">
                  <el-icon><Calendar /></el-icon>
                  <span>活动约伴</span>
                </div>
                <div class="nav-item" @click="$router.push('/messages')">
                  <el-icon><Message /></el-icon>
                  <span>私信消息</span>
                  <el-badge v-if="unreadCount > 0" :value="unreadCount" class="msg-badge" />
                </div>
              </div>
            </el-card>
          </el-col>
          
          <!-- 中间动态流 -->
          <el-col :xs="24" :md="12" class="feed-content">
            <!-- 发布框 -->
            <el-card class="publish-card" shadow="hover" v-if="userStore.isLoggedIn">
              <div class="publish-header">
                <el-avatar :size="40" :src="userAvatar" />
                <div class="publish-input" @click="showPublishDialog">
                  <span>分享你的校园生活...</span>
                </div>
              </div>
              <div class="publish-actions">
                <el-button text @click="showPublishDialog('image')">
                  <el-icon color="#67C23A"><Picture /></el-icon>
                  图片
                </el-button>
                <el-button text @click="showPublishDialog('topic')">
                  <el-icon color="#409EFF"><ChatLineRound /></el-icon>
                  话题
                </el-button>
                <el-button text @click="showPublishDialog('poll')">
                  <el-icon color="#E6A23C"><PieChart /></el-icon>
                  投票
                </el-button>
              </div>
            </el-card>
            
            <!-- 筛选标签 -->
            <div class="filter-tabs">
              <el-radio-group v-model="activeFilter" size="small" @change="handleFilterChange">
                <el-radio-button label="all">全部</el-radio-button>
                <el-radio-button label="following">关注</el-radio-button>
                <el-radio-button label="school" v-if="userStore.userInfo?.school_name">同校</el-radio-button>
                <el-radio-button label="hot">热门</el-radio-button>
              </el-radio-group>
            </div>
            
            <!-- 动态列表 -->
            <div class="post-list" v-loading="loading">
              <div v-for="post in posts" :key="post.id" class="post-card">
                <div class="post-header">
                  <el-avatar :size="44" :src="getFullImageUrl(post.user?.avatar_url)" @click="goToUserProfile(post.user_id)" />
                  <div class="post-info">
                    <h4 @click="goToUserProfile(post.user_id)">{{ post.user?.username }}</h4>
                    <p>{{ formatTime(post.created_at) }}</p>
                  </div>
                  <el-button 
                    v-if="post.user_id !== userStore.userInfo?.id" 
                    :type="post.is_following ? 'default' : 'primary'"
                    size="small"
                    @click="toggleFollow(post.user_id, post)"
                  >
                    {{ post.is_following ? '已关注' : '+ 关注' }}
                  </el-button>
                </div>
                
                <div class="post-content">
                  <p class="post-text" v-html="formatContent(post.content)"></p>
                  
                  <!-- 图片网格 -->
                  <div v-if="post.images" class="post-images">
                    <div 
                      v-for="(img, idx) in parseImages(post.images)" 
                      :key="idx"
                      :class="['img-item', getImageClass(parseImages(post.images).length)]"
                      @click="previewImage(parseImages(post.images), idx)"
                    >
                      <img :src="getFullImageUrl(img)" alt="" />
                    </div>
                  </div>
                  
                  <!-- 投票 -->
                  <div v-if="post.post_type === 'poll' && post.poll_options" class="post-poll">
                    <div 
                      v-for="(option, idx) in parsePollOptions(post.poll_options)" 
                      :key="idx"
                      class="poll-option"
                      @click="votePoll(post.id, idx)"
                    >
                      <span class="option-text">{{ option.text }}</span>
                      <span class="option-count">{{ option.votes || 0 }}票</span>
                    </div>
                  </div>
                </div>
                
                <div class="post-tags" v-if="post.tags">
                  <el-tag v-for="tag in parseTags(post.tags)" :key="tag" size="small" effect="plain">#{{ tag }}</el-tag>
                </div>
                
                <div class="post-footer">
                  <div class="action-item" :class="{ active: post.is_liked }" @click="toggleLike(post)">
                    <el-icon><Star /></el-icon>
                    <span>{{ post.like_count || '点赞' }}</span>
                  </div>
                  <div class="action-item" @click="showComments(post)">
                    <el-icon><ChatDotRound /></el-icon>
                    <span>{{ post.comment_count || '评论' }}</span>
                  </div>
                  <div class="action-item" @click="sharePost(post)">
                    <el-icon><Share /></el-icon>
                    <span>分享</span>
                  </div>
                </div>
                
                <!-- 评论区 -->
                <div v-if="post.showComments" class="comment-section">
                  <div class="comment-list">
                    <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
                      <el-avatar :size="32" :src="getFullImageUrl(comment.user?.avatar_url)" />
                      <div class="comment-content">
                        <h5>{{ comment.user?.username }}</h5>
                        <p>{{ comment.content }}</p>
                        <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
                      </div>
                    </div>
                    <el-empty v-if="!post.comments || post.comments.length === 0" description="暂无评论" />
                  </div>
                  <div class="comment-input">
                    <el-input 
                      v-model="post.commentText" 
                      placeholder="写下你的评论..."
                      @keyup.enter="submitComment(post)"
                    >
                      <template #append>
                        <el-button @click="submitComment(post)">发送</el-button>
                      </template>
                    </el-input>
                  </div>
                </div>
              </div>
              
              <el-empty v-if="posts.length === 0 && !loading" description="暂无动态" />
              
              <div class="load-more" v-if="hasMore">
                <el-button text @click="loadMore">加载更多</el-button>
              </div>
            </div>
          </el-col>
          
          <!-- 右侧栏 -->
          <el-col :xs="24" :md="6" class="right-sidebar">
            <el-card class="topic-card" shadow="hover">
              <template #header>
                <span>热门话题</span>
              </template>
              <div class="topic-list">
                <div v-for="(topic, idx) in hotTopics" :key="idx" class="topic-item" @click="searchTopic(topic)">
                  <span class="topic-rank" :class="{ top: idx < 3 }">{{ idx + 1 }}</span>
                  <span class="topic-name">#{{ topic.name }}</span>
                  <span class="topic-count">{{ topic.count }}热度</span>
                </div>
              </div>
            </el-card>
            
            <el-card class="suggest-card" shadow="hover">
              <template #header>
                <span>可能认识的人</span>
              </template>
              <div class="suggest-list">
                <div v-for="user in suggestedUsers" :key="user.id" class="suggest-item">
                  <el-avatar :size="40" :src="getFullImageUrl(user.avatar_url)" @click="goToUserProfile(user.id)" />
                  <div class="suggest-info">
                    <h5 @click="goToUserProfile(user.id)">{{ user.username }}</h5>
                    <p>{{ user.school_name }}</p>
                  </div>
                  <el-button type="primary" size="small" @click="followUser(user)">+</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
    
    <!-- 发布动态弹窗 -->
    <el-dialog v-model="publishVisible" title="发布动态" width="600px" destroy-on-close>
      <PublishPost 
        :type="publishType"
        @success="onPublishSuccess"
        @cancel="publishVisible = false"
      />
    </el-dialog>
    
    <!-- 图片预览 -->
    <el-image-viewer
      v-if="imagePreview.visible"
      :url-list="imagePreview.urls"
      :initial-index="imagePreview.index"
      @close="imagePreview.visible = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import {
  ChatDotRound,
  School,
  CircleCheck,
  Calendar,
  Message,
  Picture,
  ChatLineRound,
  PieChart,
  Star,
  Share
} from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import PublishPost from './components/PublishPost.vue'
import { socialApi } from '@/api/social'
import { followUser as followUserApi, unfollowUser as unfollowUserApi, searchUsers } from '@/api/user'

const router = useRouter()
const userStore = useUserStore()
const API_BASE_URL = 'http://localhost:5000'

// 数据
const posts = ref([])
const loading = ref(false)
const page = ref(1)
const perPage = ref(10)
const hasMore = ref(true)
const activeFilter = ref('all')
const unreadCount = ref(0)
const hotTopics = ref([
  { name: '春招经验分享', count: 12580 },
  { name: '考研复试交流', count: 8960 },
  { name: '实习内推', count: 7650 },
  { name: '毕业季', count: 5420 },
  { name: '校园生活', count: 3890 }
])
const suggestedUsers = ref([])

// 发布弹窗
const publishVisible = ref(false)
const publishType = ref('text')

// 图片预览
const imagePreview = ref({
  visible: false,
  urls: [],
  index: 0
})

const userAvatar = computed(() => {
  if (!userStore.userInfo?.avatar_url) return ''
  if (userStore.userInfo.avatar_url.startsWith('http')) return userStore.userInfo.avatar_url
  return `${API_BASE_URL}${userStore.userInfo.avatar_url}`
})

const getFullImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${API_BASE_URL}${url}`
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 30) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
}

const formatContent = (content) => {
  if (!content) return ''
  // 高亮话题标签
  return content.replace(/#([^#\s]+)/g, '<span class="topic-tag">#$1</span>')
                .replace(/@([^\s]+)/g, '<span class="mention-tag">@$1</span>')
}

const parseImages = (images) => {
  if (!images) return []
  try {
    return JSON.parse(images)
  } catch {
    return []
  }
}

const parseTags = (tags) => {
  if (!tags) return []
  try {
    return JSON.parse(tags)
  } catch {
    return tags.split(',')
  }
}

const parsePollOptions = (options) => {
  if (!options) return []
  try {
    return JSON.parse(options)
  } catch {
    return []
  }
}

const getImageClass = (count) => {
  if (count === 1) return 'single'
  if (count === 2 || count === 4) return 'double'
  return 'triple'
}

// 方法
const fetchPosts = async () => {
  if (loading.value) return
  loading.value = true
  try {
    const res = await socialApi.getFeed({
      page: page.value,
      per_page: perPage.value,
      filter: activeFilter.value
    })
    const data = res.data || res
    if (page.value === 1) {
      posts.value = data.items || []
    } else {
      posts.value.push(...(data.items || []))
    }
    hasMore.value = (data.items || []).length === perPage.value
  } catch (error) {
    console.error('获取动态失败', error)
  } finally {
    loading.value = false
  }
}

const fetchSuggestedUsers = async () => {
  try {
    const res = await searchUsers({ per_page: 5 })
    suggestedUsers.value = (res.data?.items || []).filter(u => u.id !== userStore.userInfo?.id)
  } catch (error) {
    console.error('获取推荐用户失败', error)
  }
}

const handleFilterChange = () => {
  page.value = 1
  posts.value = []
  fetchPosts()
}

const loadMore = () => {
  page.value++
  fetchPosts()
}

const showPublishDialog = (type = 'text') => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  publishType.value = type
  publishVisible.value = true
}

const onPublishSuccess = () => {
  publishVisible.value = false
  page.value = 1
  fetchPosts()
  ElMessage.success('发布成功')
}

const toggleLike = async (post) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    if (post.is_liked) {
      await socialApi.unlikePost(post.id)
      post.is_liked = false
      post.like_count--
    } else {
      await socialApi.likePost(post.id)
      post.is_liked = true
      post.like_count++
    }
  } catch (error) {
    console.error('操作失败', error)
  }
}

const showComments = async (post) => {
  post.showComments = !post.showComments
  if (post.showComments && !post.comments) {
    try {
      const res = await socialApi.getComments(post.id)
      post.comments = res.data?.items || []
    } catch (error) {
      console.error('获取评论失败', error)
    }
  }
}

const submitComment = async (post) => {
  if (!post.commentText?.trim()) return
  try {
    await socialApi.addComment(post.id, { content: post.commentText })
    post.commentText = ''
    post.comment_count++
    const res = await socialApi.getComments(post.id)
    post.comments = res.data?.items || []
    ElMessage.success('评论成功')
  } catch (error) {
    console.error('评论失败', error)
  }
}

const toggleFollow = async (userId, post) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    if (post.is_following) {
      await unfollowUserApi(userId)
      post.is_following = false
    } else {
      await followUserApi(userId)
      post.is_following = true
    }
  } catch (error) {
    console.error('操作失败', error)
  }
}

const followUser = async (user) => {
  try {
    await userApi.followUser(user.id)
    ElMessage.success('关注成功')
    fetchSuggestedUsers()
  } catch (error) {
    console.error('关注失败', error)
  }
}

const sharePost = (post) => {
  ElMessage.success('链接已复制到剪贴板')
}

const previewImage = (urls, index) => {
  imagePreview.value = {
    visible: true,
    urls: urls.map(getFullImageUrl),
    index
  }
}

const searchTopic = (topic) => {
  ElMessage.success(`搜索话题: ${topic.name}`)
}

const goToProfile = () => {
  if (userStore.userInfo?.id) {
    router.push(`/profile/${userStore.userInfo.id}`)
  }
}

const goToUserProfile = (userId) => {
  router.push(`/profile/${userId}`)
}

onMounted(() => {
  fetchPosts()
  fetchSuggestedUsers()
})
</script>

<style scoped>
.social-feed-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.main-content {
  padding-top: 80px;
  padding-bottom: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 左侧栏 */
.left-sidebar {
  position: sticky;
  top: 80px;
}

.user-card {
  margin-bottom: 16px;
}

.user-brief {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.user-info h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
}

.user-info p {
  margin: 0;
  font-size: 13px;
  color: #909399;
}

.user-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 16px;
}

.stat-item {
  text-align: center;
  cursor: pointer;
}

.stat-item .num {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.stat-item .label {
  font-size: 12px;
  color: #909399;
}

.nav-card {
  margin-bottom: 16px;
}

.nav-menu {
  display: flex;
  flex-direction: column;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
  position: relative;
}

.nav-item:hover {
  background: #f5f7fa;
}

.nav-item.active {
  background: #ecf5ff;
  color: #409eff;
}

.nav-item .msg-badge {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
}

/* 中间内容 */
.feed-content {
  min-height: 600px;
}

.publish-card {
  margin-bottom: 16px;
}

.publish-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.publish-input {
  flex: 1;
  background: #f5f7fa;
  padding: 10px 16px;
  border-radius: 20px;
  cursor: text;
  color: #909399;
}

.publish-input:hover {
  background: #ebeef5;
}

.publish-actions {
  display: flex;
  justify-content: space-around;
  padding-top: 12px;
  margin-top: 12px;
  border-top: 1px solid #ebeef5;
}

.filter-tabs {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
}

.post-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.post-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.post-info {
  flex: 1;
}

.post-info h4 {
  margin: 0 0 4px 0;
  font-size: 15px;
  cursor: pointer;
}

.post-info h4:hover {
  color: #409eff;
}

.post-info p {
  margin: 0;
  font-size: 12px;
  color: #909399;
}

.post-content {
  margin-bottom: 12px;
}

.post-text {
  margin: 0 0 12px 0;
  line-height: 1.6;
  white-space: pre-wrap;
}

:deep(.topic-tag) {
  color: #409eff;
  cursor: pointer;
}

:deep(.mention-tag) {
  color: #67c23a;
  cursor: pointer;
}

.post-images {
  display: grid;
  gap: 4px;
  border-radius: 8px;
  overflow: hidden;
}

.img-item {
  cursor: pointer;
  overflow: hidden;
}

.img-item.single {
  grid-column: span 1;
}

.img-item.double {
  aspect-ratio: 1;
}

.img-item.triple {
  aspect-ratio: 1;
}

.img-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-images:has(.img-item:nth-child(1):last-child) {
  grid-template-columns: 1fr;
}

.post-images:has(.img-item:nth-child(2):last-child) {
  grid-template-columns: repeat(2, 1fr);
}

.post-images:has(.img-item:nth-child(3)) {
  grid-template-columns: repeat(3, 1fr);
}

.post-images:has(.img-item:nth-child(4)) {
  grid-template-columns: repeat(2, 1fr);
}

.post-poll {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 12px;
}

.poll-option {
  display: flex;
  justify-content: space-between;
  padding: 10px 12px;
  margin-bottom: 8px;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.poll-option:hover {
  background: #ecf5ff;
}

.poll-option .option-count {
  color: #909399;
  font-size: 13px;
}

.post-tags {
  margin-bottom: 12px;
}

.post-tags .el-tag {
  margin-right: 8px;
  cursor: pointer;
}

.post-footer {
  display: flex;
  justify-content: space-around;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: #606266;
  transition: all 0.3s;
}

.action-item:hover {
  color: #409eff;
}

.action-item.active {
  color: #f56c6c;
}

.comment-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}

.comment-list {
  margin-bottom: 12px;
  max-height: 300px;
  overflow-y: auto;
}

.comment-item {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.comment-content {
  flex: 1;
  background: #f5f7fa;
  padding: 10px 14px;
  border-radius: 12px;
}

.comment-content h5 {
  margin: 0 0 4px 0;
  font-size: 13px;
}

.comment-content p {
  margin: 0 0 4px 0;
  font-size: 14px;
}

.comment-time {
  font-size: 11px;
  color: #909399;
}

.load-more {
  text-align: center;
  padding: 20px 0;
}

/* 右侧栏 */
.right-sidebar {
  position: sticky;
  top: 80px;
}

.topic-card, .suggest-card {
  margin-bottom: 16px;
}

.topic-list {
  display: flex;
  flex-direction: column;
}

.topic-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 0;
  cursor: pointer;
  border-bottom: 1px solid #f0f2f5;
}

.topic-item:last-child {
  border-bottom: none;
}

.topic-rank {
  width: 20px;
  text-align: center;
  font-weight: bold;
  color: #909399;
}

.topic-rank.top {
  color: #f56c6c;
}

.topic-name {
  flex: 1;
  color: #303133;
}

.topic-name:hover {
  color: #409eff;
}

.topic-count {
  font-size: 12px;
  color: #909399;
}

.suggest-list {
  display: flex;
  flex-direction: column;
}

.suggest-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
}

.suggest-info {
  flex: 1;
}

.suggest-info h5 {
  margin: 0 0 2px 0;
  font-size: 14px;
  cursor: pointer;
}

.suggest-info h5:hover {
  color: #409eff;
}

.suggest-info p {
  margin: 0;
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .left-sidebar, .right-sidebar {
    display: none;
  }
}
</style>

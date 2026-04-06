<template>
  <div class="event-detail-page">
    <Navbar />
    
    <div class="container" style="padding-top: 80px;">
      <!-- 返回按钮 -->
      <div class="back-nav">
        <el-button link @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回活动列表
        </el-button>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-wrapper">
        <el-skeleton :rows="10" animated />
      </div>
      
      <template v-else-if="event">
        <div class="content-grid">
          <!-- 左侧：活动信息 -->
          <div class="left-content">
            <el-card class="event-card">
              <!-- 封面图 -->
              <div class="event-cover">
                <el-image 
                  :src="event.cover_image || defaultCover" 
                  fit="cover"
                  class="cover-img"
                >
                  <template #error>
                    <div class="cover-placeholder">
                      <el-icon :size="60"><Calendar /></el-icon>
                    </div>
                  </template>
                </el-image>
                
                <div class="cover-overlay">
                  <el-tag :type="statusType(event.status)" size="large" effect="dark">
                    {{ statusText(event.status) }}
                  </el-tag>
                </div>
              </div>
              
              <!-- 活动信息 -->
              <div class="event-info">
                <h1 class="event-title">{{ event.title }}</h1>
                
                <div class="creator-info">
                  <el-avatar :size="40" :src="event.creator?.avatar_url" />
                  <div class="creator-meta">
                    <span class="username">{{ event.creator?.username }}</span>
                    <span class="time">{{ formatTime(event.created_at) }} 发布</span>
                  </div>
                  
                  <!-- 管理操作 -->
                  <el-dropdown v-if="isCreator" @command="handleCommand">
                    <el-button link>
                      <el-icon><More /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="edit">编辑活动</el-dropdown-item>
                        <el-dropdown-item command="cancel" divided>取消活动</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
                
                <!-- 活动详情 -->
                <div class="info-section">
                  <div class="info-item">
                    <el-icon><Calendar /></el-icon>
                    <div class="info-content">
                      <label>活动时间</label>
                      <p>{{ formatDateTime(event.start_time) }}</p>
                      <p v-if="event.end_time" class="sub">至 {{ formatDateTime(event.end_time) }}</p>
                    </div>
                  </div>
                  
                  <div class="info-item">
                    <el-icon><Location /></el-icon>
                    <div class="info-content">
                      <label>活动地点</label>
                      <p>{{ event.location }}</p>
                    </div>
                  </div>
                  
                  <div class="info-item">
                    <el-icon><Wallet /></el-icon>
                    <div class="info-content">
                      <label>费用</label>
                      <p>{{ feeText(event.fee_type, event.fee_amount) }}</p>
                    </div>
                  </div>
                  
                  <div class="info-item">
                    <el-icon><User /></el-icon>
                    <div class="info-content">
                      <label>人数</label>
                      <p>
                        {{ event.current_participants }} 人已报名
                        <template v-if="event.max_participants">
                          / 限额 {{ event.max_participants }} 人
                        </template>
                      </p>
                    </div>
                  </div>
                </div>
                
                <!-- 活动描述 -->
                <div class="description-section">
                  <h3>活动详情</h3>
                  <p class="description-text">{{ event.description || '暂无详细描述' }}</p>
                </div>
              </div>
            </el-card>
            
            <!-- 签到区（活动进行中或已结束，且已报名） -->
            <el-card v-if="showCheckIn" class="checkin-card">
              <template #header>
                <div class="card-header">
                  <span>活动签到</span>
                </div>
              </template>
              
              <div v-if="!hasCheckedIn" class="checkin-section">
                <p class="checkin-tip">请在现场进行签到，确认您已参加活动</p>
                <el-button type="success" size="large" @click="handleCheckIn" :loading="checkInLoading">
                  <el-icon><Check /></el-icon>
                  立即签到
                </el-button>
              </div>
              
              <div v-else class="checked-in-section">
                <el-icon class="success-icon" :size="48" color="#67c23a"><CircleCheck /></el-icon>
                <p>您已完成签到</p>
                <p class="checkin-time">签到时间：{{ formatTime(checkInTime) }}</p>
              </div>
            </el-card>
            
            <!-- 评价区（活动结束后） -->
            <el-card v-if="showReviews" class="reviews-card">
              <template #header>
                <div class="card-header">
                  <span>活动评价</span>
                </div>
              </template>
              
              <!-- 待评价列表 -->
              <div v-if="pendingReviews.length > 0" class="pending-reviews">
                <p class="section-title">待评价参与者</p>
                <div v-for="user in pendingReviews" :key="user.id" class="review-item">
                  <el-avatar :size="40" :src="user.avatar_url" />
                  <span class="username">{{ user.username }}</span>
                  <el-rate v-model="reviewForm[user.id].rating" show-score />
                  <el-input
                    v-model="reviewForm[user.id].content"
                    placeholder="写下您的评价..."
                    size="small"
                    style="width: 200px"
                  />
                  <el-button type="primary" size="small" @click="submitReview(user.id)">
                    评价
                  </el-button>
                </div>
              </div>
              
              <!-- 已有评价 -->
              <div v-if="reviews.length > 0" class="reviews-list">
                <p class="section-title">已收到的评价</p>
                <div v-for="review in reviews" :key="review.id" class="review-item received">
                  <el-avatar :size="40" :src="review.reviewer?.avatar_url" />
                  <div class="review-content">
                    <div class="review-header">
                      <span class="username">{{ review.reviewer?.username }}</span>
                      <el-rate :model-value="review.rating" disabled show-score />
                    </div>
                    <p class="review-text">{{ review.content }}</p>
                  </div>
                </div>
              </div>
              
              <el-empty v-if="pendingReviews.length === 0 && reviews.length === 0" description="暂无评价" />
            </el-card>
            
            <!-- 评论区 -->
            <el-card class="comments-card">
              <template #header>
                <div class="card-header">
                  <span>活动讨论 ({{ comments.length }})</span>
                </div>
              </template>
              
              <!-- 评论输入 -->
              <div v-if="canComment" class="comment-input-section">
                <el-input
                  v-model="commentContent"
                  type="textarea"
                  :rows="3"
                  placeholder="发表评论..."
                  maxlength="500"
                  show-word-limit
                />
                <div class="comment-actions">
                  <el-button type="primary" @click="submitComment" :loading="commentLoading">
                    发表评论
                  </el-button>
                </div>
              </div>
              
              <el-alert
                v-else-if="event.status === 'ended'"
                title="活动已结束"
                type="info"
                :closable="false"
              />
              
              <!-- 评论列表 -->
              <div class="comments-list" v-loading="commentsLoading">
                <el-empty v-if="comments.length === 0" description="暂无评论" />
                
                <div
                  v-for="comment in comments"
                  :key="comment.id"
                  class="comment-item"
                >
                  <el-avatar :size="36" :src="comment.user?.avatar_url" />
                  <div class="comment-content">
                    <div class="comment-header">
                      <span class="username">{{ comment.user?.username }}</span>
                      <span class="time">{{ formatTime(comment.created_at) }}</span>
                      <el-button
                        v-if="canDeleteComment(comment)"
                        link
                        type="danger"
                        size="small"
                        @click="deleteComment(comment.id)"
                      >
                        删除
                      </el-button>
                    </div>
                    <p class="comment-text">{{ comment.content }}</p>
                  </div>
                </div>
              </div>
            </el-card>
          </div>
          
          <!-- 右侧：参与者 -->
          <div class="right-sidebar">
            <el-card class="participants-card">
              <template #header>
                <div class="card-header">
                  <span>参与者</span>
                  <span class="count">{{ participants.length }} 人</span>
                </div>
              </template>
              
              <div class="participants-list" v-loading="participantsLoading">
                <el-empty v-if="participants.length === 0" description="暂无参与者" />
                
                <div
                  v-for="p in participants"
                  :key="p.id"
                  class="participant-item"
                  @click="viewProfile(p.id)"
                >
                  <el-avatar :size="40" :src="p.avatar_url" />
                  <div class="participant-info">
                    <span class="name">{{ p.username }}</span>
                    <span v-if="p.id === event.creator_id" class="tag">发起人</span>
                  </div>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </template>
      
      <!-- 错误状态 -->
      <el-result
        v-else
        icon="error"
        title="活动不存在或已被删除"
      >
        <template #extra>
          <el-button type="primary" @click="goBack">返回列表</el-button>
        </template>
      </el-result>
    </div>
    
    <!-- 底部固定操作栏 -->
    <div v-if="event && !isCreator" class="bottom-bar">
      <div class="container">
        <div class="bar-content">
          <div class="bar-info">
            <span class="bar-title">{{ event.title }}</span>
            <span class="bar-meta">{{ event.current_participants }} 人已报名</span>
          </div>
          <el-button
            :type="joinButtonType"
            :disabled="!canJoin"
            size="large"
            @click="handleJoin"
            :loading="joinLoading"
          >
            {{ joinButtonText }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  ArrowLeft, Calendar, Location, User, Wallet, More, Check, CircleCheck 
} from '@element-plus/icons-vue'
import Navbar from '@/components/Navbar.vue'
import { socialApi } from '@/api/social'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const eventId = computed(() => route.params.id)
const isCreator = computed(() => event.value?.creator_id === userStore.userInfo?.id)

// 数据
const loading = ref(true)
const event = ref(null)
const participants = ref([])
const participantsLoading = ref(false)
const comments = ref([])
const commentsLoading = ref(false)
const commentContent = ref('')
const commentLoading = ref(false)
const joinLoading = ref(false)

// 签到相关
const hasCheckedIn = ref(false)
const checkInTime = ref(null)
const checkInLoading = ref(false)

// 评价相关
const reviews = ref([])
const pendingReviews = ref([])
const reviewForm = ref({})

// 默认封面
const defaultCover = 'https://placehold.co/800x400/667eea/ffffff?text=Activity'

// 状态映射
const statusMap = {
  open: '报名中',
  full: '已满员',
  ongoing: '进行中',
  ended: '已结束',
  cancelled: '已取消'
}

const statusType = (status) => {
  const map = { open: 'success', full: 'danger', ongoing: 'warning', ended: 'info', cancelled: 'info' }
  return map[status] || 'info'
}

const statusText = (status) => statusMap[status] || status

// 费用文本
const feeText = (type, amount) => {
  if (type === 'free') return '免费'
  if (type === 'aa') return 'AA制（现场结算）'
  if (type === 'fixed') return `固定费用 ¥${amount / 100}`
  return '未知'
}

// 是否可以报名
const canJoin = computed(() => {
  if (!userStore.isLoggedIn) return false
  return ['open'].includes(event.value?.status)
})

// 是否已报名
const hasJoined = computed(() => {
  return participants.value.some(p => p.id === userStore.userInfo?.id)
})

// 报名按钮
const joinButtonType = computed(() => {
  if (hasJoined.value) return 'success'
  if (event.value?.status === 'full') return 'info'
  return 'primary'
})

const joinButtonText = computed(() => {
  if (hasJoined.value) return '已报名'
  if (event.value?.status === 'full') return '已满员'
  if (event.value?.status === 'ended') return '已结束'
  if (event.value?.status === 'ongoing') return '进行中'
  return '立即报名'
})

// 是否可以评论
const canComment = computed(() => {
  return userStore.isLoggedIn && !['ended', 'cancelled'].includes(event.value?.status)
})

// 是否显示签到
const showCheckIn = computed(() => {
  return userStore.isLoggedIn && 
         hasJoined.value && 
         ['ongoing', 'ended'].includes(event.value?.status)
})

// 是否显示评价
const showReviews = computed(() => {
  return userStore.isLoggedIn && 
         event.value?.status === 'ended' && 
         hasJoined.value
})

// 获取活动详情
const fetchEvent = async () => {
  loading.value = true
  try {
    const res = await socialApi.getEvent(eventId.value)
    event.value = res.data
  } catch (err) {
    console.error('获取活动详情失败:', err)
    event.value = null
  } finally {
    loading.value = false
  }
}

// 获取参与者
const fetchParticipants = async () => {
  participantsLoading.value = true
  try {
    const res = await socialApi.getEventParticipants(eventId.value)
    participants.value = res.data.items || []
  } catch (err) {
    console.error('获取参与者失败:', err)
  } finally {
    participantsLoading.value = false
  }
}

// 获取评论
const fetchComments = async () => {
  commentsLoading.value = true
  try {
    const res = await socialApi.getEventComments(eventId.value)
    comments.value = res.data.items || []
  } catch (err) {
    console.error('获取评论失败:', err)
  } finally {
    commentsLoading.value = false
  }
}

// 发表评论
const submitComment = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  
  commentLoading.value = true
  try {
    await socialApi.createEventComment(eventId.value, {
      content: commentContent.value
    })
    ElMessage.success('评论成功')
    commentContent.value = ''
    fetchComments()
  } catch (err) {
    console.error('评论失败:', err)
    ElMessage.error('评论失败')
  } finally {
    commentLoading.value = false
  }
}

// 删除评论
const deleteComment = async (commentId) => {
  try {
    await ElMessageBox.confirm('确定删除此评论？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await socialApi.deleteEventComment(commentId)
    ElMessage.success('删除成功')
    fetchComments()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除失败:', err)
      ElMessage.error('删除失败')
    }
  }
}

// 是否可以删除评论
const canDeleteComment = (comment) => {
  return comment.user_id === userStore.userInfo?.id || isCreator.value
}

// 处理报名/退出
const handleJoin = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  if (hasJoined.value) {
    // 退出活动
    try {
      await ElMessageBox.confirm('确定退出此活动？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      
      joinLoading.value = true
      await socialApi.leaveEvent(eventId.value)
      ElMessage.success('已退出活动')
      fetchEvent()
      fetchParticipants()
    } catch (err) {
      if (err !== 'cancel') {
        console.error('退出失败:', err)
        ElMessage.error('退出失败')
      }
    } finally {
      joinLoading.value = false
    }
  } else {
    // 报名
    joinLoading.value = true
    try {
      await socialApi.joinEvent(eventId.value)
      ElMessage.success('报名成功')
      fetchEvent()
      fetchParticipants()
    } catch (err) {
      console.error('报名失败:', err)
      ElMessage.error(err.response?.data?.error || '报名失败')
    } finally {
      joinLoading.value = false
    }
  }
}

// 下拉菜单命令
const handleCommand = (command) => {
  if (command === 'edit') {
    router.push(`/social/events/${eventId.value}/edit`)
  } else if (command === 'cancel') {
    cancelEvent()
  }
}

// 取消活动
const cancelEvent = async () => {
  try {
    await ElMessageBox.confirm('确定取消此活动？此操作不可恢复', '警告', {
      confirmButtonText: '确定取消',
      cancelButtonText: '再想想',
      type: 'danger'
    })
    
    await socialApi.updateEvent(eventId.value, { status: 'cancelled' })
    ElMessage.success('活动已取消')
    fetchEvent()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('取消失败:', err)
      ElMessage.error('取消失败')
    }
  }
}

// 查看用户主页
const viewProfile = (userId) => {
  router.push(`/profile/${userId}`)
}

// 返回列表
const goBack = () => {
  router.push('/social/events')
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

const formatDateTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

onMounted(() => {
  fetchEvent()
  fetchParticipants()
  fetchComments()
  if (showCheckIn.value) {
    fetchCheckInStatus()
  }
  if (showReviews.value) {
    fetchReviews()
    fetchPendingReviews()
  }
})

// 获取签到状态
const fetchCheckInStatus = async () => {
  try {
    const res = await socialApi.getCheckInStatus(eventId.value)
    hasCheckedIn.value = res.data.checked_in
    checkInTime.value = res.data.check_in_time
  } catch (err) {
    console.error('获取签到状态失败:', err)
  }
}

// 签到
const handleCheckIn = async () => {
  checkInLoading.value = true
  try {
    await socialApi.checkInEvent(eventId.value, { method: 'manual' })
    ElMessage.success('签到成功')
    hasCheckedIn.value = true
    fetchCheckInStatus()
  } catch (err) {
    console.error('签到失败:', err)
    ElMessage.error(err.response?.data?.error || '签到失败')
  } finally {
    checkInLoading.value = false
  }
}

// 获取评价列表
const fetchReviews = async () => {
  try {
    const res = await socialApi.getEventReviews(eventId.value)
    reviews.value = res.data.items || []
  } catch (err) {
    console.error('获取评价失败:', err)
  }
}

// 获取待评价列表
const fetchPendingReviews = async () => {
  try {
    const res = await socialApi.getPendingReviews(eventId.value)
    pendingReviews.value = res.data.items || []
    // 初始化评价表单
    pendingReviews.value.forEach(user => {
      if (!reviewForm.value[user.id]) {
        reviewForm.value[user.id] = { rating: 5, content: '' }
      }
    })
  } catch (err) {
    console.error('获取待评价列表失败:', err)
  }
}

// 提交评价
const submitReview = async (userId) => {
  const form = reviewForm.value[userId]
  if (!form || !form.rating) {
    ElMessage.warning('请给出评分')
    return
  }
  
  try {
    await socialApi.createEventReview(eventId.value, {
      reviewee_id: userId,
      rating: form.rating,
      content: form.content
    })
    ElMessage.success('评价成功')
    fetchReviews()
    fetchPendingReviews()
  } catch (err) {
    console.error('评价失败:', err)
    ElMessage.error(err.response?.data?.error || '评价失败')
  }
}
</script>

<style scoped>
.event-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 80px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.back-nav {
  margin-bottom: 20px;
}

.loading-wrapper {
  padding: 40px;
  background: white;
  border-radius: 8px;
}

/* 两栏布局 */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 20px;
}

/* 左侧内容 */
.left-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 封面 */
.event-cover {
  position: relative;
  height: 300px;
  margin: -20px -20px 20px -20px;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
}

.cover-img {
  width: 100%;
  height: 100%;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.cover-overlay {
  position: absolute;
  top: 16px;
  left: 16px;
}

.event-title {
  margin: 0 0 16px 0;
  font-size: 24px;
  color: #333;
  line-height: 1.4;
}

/* 发起人信息 */
.creator-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

.creator-meta {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.creator-meta .username {
  font-weight: 500;
  color: #333;
}

.creator-meta .time {
  font-size: 13px;
  color: #999;
}

/* 信息项 */
.info-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.info-item .el-icon {
  font-size: 24px;
  color: #667eea;
}

.info-content {
  flex: 1;
}

.info-content label {
  display: block;
  font-size: 13px;
  color: #999;
  margin-bottom: 4px;
}

.info-content p {
  margin: 0;
  font-size: 15px;
  color: #333;
  font-weight: 500;
}

.info-content p.sub {
  font-size: 13px;
  color: #666;
  font-weight: normal;
  margin-top: 4px;
}

/* 活动描述 */
.description-section {
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.description-section h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
}

.description-text {
  margin: 0;
  font-size: 15px;
  line-height: 1.8;
  color: #444;
  white-space: pre-wrap;
}

/* 签到区 */
.checkin-card {
  margin-bottom: 20px;
}

.checkin-section {
  text-align: center;
  padding: 20px 0;
}

.checkin-tip {
  color: #666;
  margin-bottom: 16px;
}

.checked-in-section {
  text-align: center;
  padding: 20px 0;
}

.checked-in-section p {
  margin: 8px 0;
  color: #67c23a;
  font-weight: 500;
}

.checkin-time {
  font-size: 13px;
  color: #999 !important;
}

.success-icon {
  margin-bottom: 8px;
}

/* 评价区 */
.reviews-card {
  margin-bottom: 20px;
}

.pending-reviews,
.reviews-list {
  margin-bottom: 24px;
}

.section-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.review-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 12px;
}

.review-item .username {
  flex: 1;
  font-weight: 500;
}

.review-item.received {
  flex-direction: column;
  align-items: flex-start;
}

.review-content {
  flex: 1;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}

.review-text {
  margin: 0;
  font-size: 14px;
  color: #666;
}

/* 评论区 */
.comments-card {
  margin-bottom: 20px;
}

.card-header {
  font-weight: 500;
}

.card-header .count {
  margin-left: 8px;
  color: #999;
  font-weight: normal;
}

.comment-input-section {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.comment-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 6px;
}

.comment-header .username {
  font-weight: 500;
  color: #333;
}

.comment-header .time {
  font-size: 12px;
  color: #999;
}

.comment-text {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: #444;
}

/* 右侧边栏 */
.right-sidebar {
  position: sticky;
  top: 80px;
  height: fit-content;
}

.participants-card {
  max-height: 500px;
  overflow-y: auto;
}

.participants-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.participant-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.participant-item:hover {
  background: #f5f7fa;
}

.participant-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.participant-info .name {
  font-size: 14px;
  color: #333;
}

.participant-info .tag {
  font-size: 11px;
  padding: 2px 6px;
  background: #e6f2ff;
  color: #409eff;
  border-radius: 4px;
}

/* 底部固定栏 */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
  padding: 12px 0;
  z-index: 100;
}

.bar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bar-info {
  display: flex;
  flex-direction: column;
}

.bar-title {
  font-weight: 500;
  font-size: 15px;
  color: #333;
}

.bar-meta {
  font-size: 13px;
  color: #666;
}

/* 响应式 */
@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .right-sidebar {
    position: static;
  }
  
  .info-section {
    grid-template-columns: 1fr;
  }
  
  .event-cover {
    height: 200px;
  }
  
  .event-title {
    font-size: 20px;
  }
}
</style>
